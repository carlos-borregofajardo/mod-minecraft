package com.example.teleportportals.portal;

import com.example.teleportportals.TeleportPortalsMod;
import com.example.teleportportals.data.ColorBaseBlockData;
import com.example.teleportportals.data.PortalReturnData;
import com.mojang.logging.LogUtils;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.living.LivingDeathEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.listener.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/**
 * Gestiona el sistema de teletransporte tras la muerte: al morir el jugador
 * se genera un portal verde cerca del punto de muerte que, al reaparecer,
 * lo lleva a su base y le permite volver desde la base al portal.
 * <p>
 * La colocación del portal se aplaza un tick (cola {@link #pendingPortals})
 * para que una explosión en curso no destruya el portal recién colocado.
 */
@Mod.EventBusSubscriber(modid = TeleportPortalsMod.MODID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class DeathPortalHandler {
    private static final Logger LOGGER = LogUtils.getLogger();

    private DeathPortalHandler() {
        // Solo eventos estáticos; no se instancia.
    }

    // Posición del portal verde generado al morir, para teletransportar al jugador
    // a la base cuando reaparezca y permitirle volver desde la base al punto de muerte.
    private static final Map<UUID, BlockPos> deathPortalPositions = new HashMap<>();

    // Cola de portales que se van a colocar en el siguiente tick, para evitar que
    // una explosión en curso destruya el portal justo después de colocarlo.
    private static final List<PendingPortal> pendingPortals = new ArrayList<>();

    private record PendingPortal(UUID playerId, ServerLevel level, BlockPos deathPos) {}

    // Radio máximo (en bloques) donde se buscará un lugar seguro para el portal de muerte.
    private static final int PORTAL_SEARCH_RADIUS = 4;

    // Flags para level.setBlock: notifica a vecinos y envía el cambio a los clientes.
    private static final int SET_BLOCK_FLAGS = 3;

    // Bloques peligrosos donde no debe colocarse un portal de muerte.
    private static final Set<Block> DANGEROUS_BLOCKS = Set.of(
        Blocks.LAVA,
        Blocks.FIRE,
        Blocks.SOUL_FIRE,
        Blocks.CAMPFIRE,
        Blocks.SOUL_CAMPFIRE,
        Blocks.MAGMA_BLOCK,
        Blocks.CACTUS,
        Blocks.SWEET_BERRY_BUSH,
        Blocks.WITHER_ROSE
    );

    /**
     * Al morir un jugador, encola la colocación de un portal verde cerca
     * del punto de muerte. Se retrasa al siguiente tick para evitar que
     * una explosión en curso destruya el portal inmediatamente.
     */
    @SubscribeEvent
    public static void onDeath(LivingDeathEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;

        ServerLevel level = (ServerLevel) player.level();
        BlockPos deathPos = player.blockPosition();
        LOGGER.debug("[DeathTP] {} murió en {}", player.getName().getString(), deathPos);

        // Colocar un bloque de teletransporte (portal verde) en un espacio vacío
        // cercano al punto de muerte. Ese portal apuntará al bloque base que haya
        // colocado el jugador en ese momento.
        // Se aplaza al siguiente tick para que, si la muerte fue por una explosión,
        // la explosión termine de destruir bloques antes de colocar el portal.
        pendingPortals.add(new PendingPortal(player.getUUID(), level, deathPos));
    }

    /**
     * Al reaparecer un jugador, si existe un portal de muerte válido y una base,
     * lo teletransporta a la base y guarda el portal para poder volver desde la base.
     */
    @SubscribeEvent
    public static void onRespawn(PlayerEvent.PlayerRespawnEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) return;
        if (event.isEndConquered()) return; // No interferir con el regreso del End
        LOGGER.debug("[DeathTP] {} reapareció", player.getName().getString());

        BlockPos portalPos = deathPortalPositions.remove(player.getUUID());
        LOGGER.debug("[DeathTP] deathPortalPosition recuperada = {}", portalPos);
        if (portalPos == null) return;

        ServerLevel level = (ServerLevel) player.level();
        if (!level.isLoaded(portalPos)) {
            level.getChunkAt(portalPos);
        }
        if (!level.getBlockState(portalPos).is(PortalColor.GREEN.getPortalBlock().get())) {
            LOGGER.warn("[DeathTP] El portal de muerte en {} ya no existe; no se teletransporta a la base.", portalPos);
            player.sendSystemMessage(Component.translatable("message.teleport_portals.portal_destroyed"));
            return;
        }

        ColorBaseBlockData data = PortalColor.GREEN.getData(level);
        BlockPos basePos = data.getBasePos();
        LOGGER.debug("[DeathTP] basePos = {}", basePos);
        if (basePos == null || !level.getBlockState(basePos).is(PortalColor.GREEN.getBaseBlock().get())) {
            data.clear();
            player.sendSystemMessage(Component.translatable("message.teleport_portals.no_base_block"));
            return;
        }

        // Llevar al jugador a la base y registrar el portal para poder volver desde la base.
        Vec3 destination = TeleportHelper.centeredAbove(basePos);
        player.teleportTo(level, destination.x, destination.y, destination.z, Set.of(), 0f, 0f, false);
        PortalReturnData.get(level).setLastPortalPos(PortalColor.GREEN, player.getUUID(), portalPos);
        PortalBlock.clearCooldown(PortalColor.GREEN, player.getUUID());
        LOGGER.debug("[DeathTP] teletransportado a la base {}", basePos);
    }

    /**
     * Al desconectarse un jugador, elimina sus entradas en los mapas
     * volátiles del mod para que no crezcan indefinidamente.
     */
    @SubscribeEvent
    public static void onPlayerLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        UUID uuid = event.getEntity().getUUID();
        deathPortalPositions.remove(uuid);
        for (PortalColor color : PortalColor.values()) {
            color.clearCooldown(uuid);
        }
    }

    /**
     * Procesa la cola de portales pendientes al final de cada tick del servidor.
     * Se colocan en este momento para asegurar que cualquier explosión en curso
     * haya terminado antes de buscar un lugar seguro.
     */
    @SubscribeEvent
    public static void onServerTickPost(TickEvent.ServerTickEvent.Post event) {
        if (pendingPortals.isEmpty()) return;
        List<PendingPortal> toProcess = new ArrayList<>(pendingPortals);
        pendingPortals.clear();
        for (PendingPortal pending : toProcess) {
            placeDeathPortal(pending.level, pending.playerId, pending.deathPos);
        }
    }

    /**
     * Coloca el portal de muerte alrededor de deathPos.
     */
    private static void placeDeathPortal(ServerLevel level, UUID playerId, BlockPos deathPos) {
        BlockPos portalPos = findEmptySpaceNear(level, deathPos, PORTAL_SEARCH_RADIUS);
        LOGGER.debug("[DeathTP] portalPos candidato = {}", portalPos);
        if (portalPos != null) {
            boolean placed = level.setBlock(portalPos, PortalColor.GREEN.getPortalBlock().get().defaultBlockState(), SET_BLOCK_FLAGS);
            LOGGER.debug("[DeathTP] setBlock en {} -> {}", portalPos, placed);
            if (placed) {
                PortalBlock.clearCooldown(PortalColor.GREEN, playerId);
                PortalReturnData.get(level).clearLastPortalPos(PortalColor.GREEN, playerId);
                deathPortalPositions.put(playerId, portalPos.immutable());
                return;
            }
        }
        LOGGER.warn("[DeathTP] No se encontró un lugar seguro para el portal cerca de {}", deathPos);
        ServerPlayer player = level.getServer().getPlayerList().getPlayer(playerId);
        if (player != null) {
            player.sendSystemMessage(Component.translatable("message.teleport_portals.no_safe_portal_spot"));
        }
    }

    /**
     * Busca un bloque vacío seguro cerca de la posición dada para colocar un portal.
     * Evita el punto exacto de muerte (para no dejarlo sobre lava, fuego o el
     * epicentro de una explosión) y prioriza bloques de aire con suelo sólido debajo.
     * Devuelve null si no encuentra ningún lugar seguro.
     */
    private static BlockPos findEmptySpaceNear(ServerLevel level, BlockPos origin, int radius) {
        // Empezamos en r=1 para no colocar el portal exactamente donde murió el jugador.
        for (int r = 1; r <= radius; r++) {
            for (int dx = -r; dx <= r; dx++) {
                for (int dz = -r; dz <= r; dz++) {
                    if (Math.abs(dx) != r && Math.abs(dz) != r) continue; // borde del anillo
                    for (int dy = -1; dy <= 2; dy++) {
                        BlockPos candidate = origin.offset(dx, dy, dz);
                        if (isSafePortalSpot(level, candidate, true)) {
                            return candidate;
                        }
                    }
                }
            }
        }
        // Si no hay sitio con suelo sólido, aceptamos cualquier sitio seguro.
        for (int r = 1; r <= radius; r++) {
            for (int dx = -r; dx <= r; dx++) {
                for (int dz = -r; dz <= r; dz++) {
                    if (Math.abs(dx) != r && Math.abs(dz) != r) continue;
                    for (int dy = -1; dy <= 2; dy++) {
                        BlockPos candidate = origin.offset(dx, dy, dz);
                        if (isSafePortalSpot(level, candidate, false)) {
                            return candidate;
                        }
                    }
                }
            }
        }
        return null;
    }

    /**
     * Devuelve true si el bloque candidato es un lugar seguro para colocar el portal.
     */
    private static boolean isSafePortalSpot(ServerLevel level, BlockPos candidate, boolean requireSolidFloor) {
        BlockPos below = candidate.below();
        if (!level.isEmptyBlock(candidate)) return false;
        if (isDangerousBlock(level, candidate) || isDangerousBlock(level, below)) return false;

        if (requireSolidFloor) {
            BlockState belowState = level.getBlockState(below);
            if (level.isEmptyBlock(below) || !belowState.isCollisionShapeFullBlock(level, below) || isDangerousBlock(level, below)) {
                return false;
            }
        }
        return true;
    }

    /**
     * Devuelve true si el bloque en la posición dada puede dañar/destruir el portal
     * o impedir que el jugador lo use (lava, fuego, cactus, etc.).
     */
    private static boolean isDangerousBlock(ServerLevel level, BlockPos pos) {
        BlockState state = level.getBlockState(pos);
        if (DANGEROUS_BLOCKS.stream().anyMatch(state::is)) {
            return true;
        }
        // Cualquier fluido (agua, lava, etc.) se considera peligroso.
        return !state.getFluidState().isEmpty();
    }
}

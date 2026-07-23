package com.example.teleportportals.portal;

import com.example.teleportportals.Config;
import com.example.teleportportals.data.ColorBaseBlockData;
import com.example.teleportportals.data.PortalReturnData;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.InsideBlockEffectApplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

import java.util.UUID;

/**
 * Bloque portal genérico del sistema de teletransporte.
 * <p>
 * Cuando un jugador entra en contacto con él, lo teletransporta a la posición
 * almacenada en {@link ColorBaseBlockData} para el color correspondiente.
 * También guarda la última posición de portal usada en {@link PortalReturnData}
 * para permitir el viaje de vuelta desde el bloque base.
 */
public class PortalBlock extends Block {

    // Configuración de la animación de partículas del bloque en cliente.
    private static final int ANIMATION_PARTICLE_COUNT = 4;
    private static final double ANIMATION_PARTICLE_MAX_HEIGHT = 1.5;
    private static final double ANIMATION_PARTICLE_SPEED_Y = 0.2;

    private final PortalColor color;

    public PortalBlock(Properties properties, PortalColor color) {
        super(properties);
        this.color = color;
    }

    @Override
    public void entityInside(BlockState state, Level level, BlockPos pos, Entity entity, InsideBlockEffectApplier effectApplier, boolean bobbing) {
        if (level.isClientSide()) return;
        if (!(entity instanceof ServerPlayer player)) return;

        long now = level.getGameTime();
        Long last = color.getCooldownMap().get(player.getUUID());
        if (last != null && now - last < Config.portalCooldown) return;

        if (!(level instanceof ServerLevel serverLevel)) return;

        ColorBaseBlockData data = color.getData(serverLevel);
        BlockPos basePos = data.getBasePos();
        if (basePos == null) return; // No hay bloque base colocado

        // Si la base guardada ya no existe (fue destruida), limpiar los datos.
        if (!level.getBlockState(basePos).is(color.getBaseBlock().get())) {
            data.clear();
            return;
        }

        color.getCooldownMap().put(player.getUUID(), now);

        Vec3 destination = TeleportHelper.centeredAbove(basePos);

        PortalReturnData.get(serverLevel).setLastPortalPos(color, player.getUUID(), pos.immutable());

        PortalEffects.playTeleportEffects(serverLevel, color, destination.x, destination.y, destination.z);
        player.teleportTo(destination.x, destination.y, destination.z);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        for (int i = 0; i < ANIMATION_PARTICLE_COUNT; i++) {
            double dx = pos.getX() + random.nextDouble();
            double dy = pos.getY() + random.nextDouble() * ANIMATION_PARTICLE_MAX_HEIGHT;
            double dz = pos.getZ() + random.nextDouble();
            level.addParticle(color.getParticle(), dx, dy, dz, 0.0, ANIMATION_PARTICLE_SPEED_Y, 0.0);
        }
    }

    /**
     * Elimina el cooldown de teletransporte del jugador para el color indicado.
     */
    public static void clearCooldown(PortalColor color, UUID uuid) {
        color.clearCooldown(uuid);
    }
}

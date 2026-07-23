package com.example.teleportportals.portal;

import com.example.teleportportals.data.ColorBaseBlockData;
import com.example.teleportportals.data.PortalReturnData;

import com.mojang.logging.LogUtils;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import org.slf4j.Logger;

/**
 * Bloque base genérico del sistema de teletransporte.
 * <p>
 * Al colocarse registra su posición en {@link ColorBaseBlockData} para el color
 * correspondiente. Al romperse la borra. Hacer clic derecho sobre él devuelve al
 * jugador al último portal del mismo color guardado en {@link PortalReturnData}.
 */
public class TeleportBaseBlock extends Block {

    private static final Logger LOGGER = LogUtils.getLogger();

    private final PortalColor color;

    public TeleportBaseBlock(Properties properties, PortalColor color) {
        super(properties);
        this.color = color;
    }

    @Override
    protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean moved) {
        super.onPlace(state, level, pos, oldState, moved);
        if (!level.isClientSide() && level instanceof ServerLevel serverLevel) {
            color.getData(serverLevel).setBasePos(pos);
        }
    }

    @Override
    public BlockState playerWillDestroy(Level level, BlockPos pos, BlockState state, Player player) {
        if (!level.isClientSide() && level instanceof ServerLevel serverLevel) {
            ColorBaseBlockData data = color.getData(serverLevel);
            if (pos.equals(data.getBasePos())) {
                data.clear();
            }
        }
        return super.playerWillDestroy(level, pos, state, player);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hitResult) {
        if (level.isClientSide() || !(player instanceof ServerPlayer serverPlayer) || !(level instanceof ServerLevel serverLevel)) {
            return InteractionResult.SUCCESS;
        }

        BlockPos portalPos = PortalReturnData.get(serverLevel).getLastPortalPos(color, serverPlayer.getUUID());
        LOGGER.debug("[{}TP] {}BaseBlock click: portalPos guardado = {}", color.name(), color.getName(), portalPos);
        if (portalPos == null) {
            return InteractionResult.PASS;
        }

        // Asegurar que el chunk donde está el portal esté cargado antes de comprobarlo.
        // getChunkAt carga el chunk si es necesario, pero no lo mantiene forzosamente cargado.
        if (!serverLevel.isLoaded(portalPos)) {
            serverLevel.getChunkAt(portalPos);
        }

        boolean isPortal = serverLevel.getBlockState(portalPos).is(color.getPortalBlock().get());
        LOGGER.debug("[{}TP] {}BaseBlock click: bloque en {} es {}_portal? {}", color.name(), color.getName(), portalPos, color.getName(), isPortal);
        if (!isPortal) {
            PortalReturnData.get(serverLevel).clearLastPortalPos(color, serverPlayer.getUUID());
            serverPlayer.sendSystemMessage(Component.translatable("message.teleport_portals.return_portal_gone"));
            return InteractionResult.PASS;
        }

        serverLevel.removeBlock(portalPos, false);

        Vec3 destination = TeleportHelper.centeredAt(portalPos);

        PortalEffects.playTeleportEffects(serverLevel, color, destination.x, destination.y, destination.z);
        serverPlayer.teleportTo(destination.x, destination.y, destination.z);

        PortalReturnData.get(serverLevel).clearLastPortalPos(color, serverPlayer.getUUID());
        PortalBlock.clearCooldown(color, serverPlayer.getUUID());

        return InteractionResult.CONSUME;
    }
}

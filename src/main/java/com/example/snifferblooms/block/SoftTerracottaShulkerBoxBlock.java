package com.example.snifferblooms.block;

import com.example.snifferblooms.SnifferBloomsMod;
import com.example.snifferblooms.block.entity.SoftTerracottaShulkerBoxBlockEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.ShulkerBoxBlock;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityTicker;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.entity.ShulkerBoxBlockEntity;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.BlockState;
import org.jspecify.annotations.Nullable;

public class SoftTerracottaShulkerBoxBlock extends ShulkerBoxBlock {

    public SoftTerracottaShulkerBoxBlock(DyeColor color, BlockBehaviour.Properties properties) {
        super(color, properties);
    }

    @Override
    public BlockEntity newBlockEntity(BlockPos worldPosition, BlockState blockState) {
        return new SoftTerracottaShulkerBoxBlockEntity(this.getColor(), worldPosition, blockState);
    }

    @Override
    public <T extends BlockEntity> @Nullable BlockEntityTicker<T> getTicker(Level level, BlockState blockState, BlockEntityType<T> type) {
        return createTickerHelper(type, SnifferBloomsMod.SOFT_TERRACOTTA_SHULKER_BOX_ENTITY.get(), ShulkerBoxBlockEntity::tick);
    }
}
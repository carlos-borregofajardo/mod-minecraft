package com.example.snifferblooms.block.entity;

import com.example.snifferblooms.SnifferBloomsMod;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.entity.ShulkerBoxBlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public class SoftTerracottaShulkerBoxBlockEntity extends ShulkerBoxBlockEntity {

    public SoftTerracottaShulkerBoxBlockEntity(DyeColor color, BlockPos worldPosition, BlockState blockState) {
        super(color, worldPosition, blockState);
    }

    public SoftTerracottaShulkerBoxBlockEntity(BlockPos worldPosition, BlockState blockState) {
        super(worldPosition, blockState);
    }

    @Override
    public BlockEntityType<?> getType() {
        return SnifferBloomsMod.SOFT_TERRACOTTA_SHULKER_BOX_ENTITY.get();
    }

    @Override
    public Holder<BlockEntityType<?>> typeHolder() {
        return SnifferBloomsMod.SOFT_TERRACOTTA_SHULKER_BOX_ENTITY.get().builtInRegistryHolder();
    }
}
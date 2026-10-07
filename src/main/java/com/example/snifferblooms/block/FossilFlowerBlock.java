package com.example.snifferblooms.block;

import com.mojang.serialization.MapCodec;
import net.minecraft.world.level.block.VegetationBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;

public class FossilFlowerBlock extends VegetationBlock {

    public static final MapCodec<FossilFlowerBlock> CODEC = simpleCodec(FossilFlowerBlock::new);

    public FossilFlowerBlock(BlockBehaviour.Properties properties) {
        super(properties);
    }

    @Override
    protected MapCodec<? extends VegetationBlock> codec() {
        return CODEC;
    }
}
package com.example.snifferblooms.client.renderer;

import com.example.snifferblooms.SnifferBloomsMod;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Transformation;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.blockentity.ShulkerBoxRenderer;
import net.minecraft.client.renderer.blockentity.state.ShulkerBoxRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.model.sprite.SpriteId;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.core.Direction;
import net.minecraft.resources.Identifier;

public class SoftTerracottaShulkerBoxRenderer extends ShulkerBoxRenderer {

    private static final SpriteId SPRITE = Sheets.SHULKER_MAPPER.apply(
        Identifier.fromNamespaceAndPath(SnifferBloomsMod.MODID, "shulker_soft_terracotta")
    );

    public SoftTerracottaShulkerBoxRenderer(BlockEntityRendererProvider.Context context) {
        super(context);
    }

    @Override
    public void submit(ShulkerBoxRenderState state, PoseStack poseStack, SubmitNodeCollector submitNodeCollector, CameraRenderState camera) {
        poseStack.pushPose();
        poseStack.mulPose(modelTransform(state.direction));
        this.submit(poseStack, submitNodeCollector, state.lightCoords, OverlayTexture.NO_OVERLAY, state.progress, state.breakProgress, SPRITE, 0);
        poseStack.popPose();
    }
}
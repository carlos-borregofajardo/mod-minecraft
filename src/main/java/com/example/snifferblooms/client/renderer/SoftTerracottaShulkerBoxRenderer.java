package com.example.snifferblooms.client.renderer;

import com.example.snifferblooms.FossilColor;
import com.example.snifferblooms.SnifferBloomsMod;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.blockentity.ShulkerBoxRenderer;
import net.minecraft.client.renderer.blockentity.state.ShulkerBoxRenderState;
import net.minecraft.client.renderer.state.level.CameraRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.model.sprite.SpriteId;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.DyeColor;
import org.jspecify.annotations.Nullable;

import java.util.EnumMap;
import java.util.Map;

public class SoftTerracottaShulkerBoxRenderer extends ShulkerBoxRenderer {

    private static final Map<DyeColor, SpriteId> SPRITES = new EnumMap<>(DyeColor.class);

    static {
        for (FossilColor color : FossilColor.values()) {
            SPRITES.put(color.getVanilla(), Sheets.SHULKER_MAPPER.apply(
                Identifier.fromNamespaceAndPath(SnifferBloomsMod.MODID, "shulker_" + color.getId())
            ));
        }
    }

    public SoftTerracottaShulkerBoxRenderer(BlockEntityRendererProvider.Context context) {
        super(context);
    }

    @Override
    public void submit(ShulkerBoxRenderState state, PoseStack poseStack, SubmitNodeCollector submitNodeCollector, CameraRenderState camera) {
        SpriteId sprite = spriteFor(state.color);
        poseStack.pushPose();
        poseStack.mulPose(modelTransform(state.direction));
        this.submit(poseStack, submitNodeCollector, state.lightCoords, OverlayTexture.NO_OVERLAY, state.progress, state.breakProgress, sprite, 0);
        poseStack.popPose();
    }

    private static SpriteId spriteFor(@Nullable DyeColor color) {
        SpriteId sprite = color == null ? null : SPRITES.get(color);
        return sprite != null ? sprite : Sheets.DEFAULT_SHULKER_TEXTURE_LOCATION;
    }
}
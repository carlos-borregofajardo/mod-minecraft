package com.example.snifferblooms.item;

import net.minecraft.core.Holder;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.stats.Stats;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.entity.SignText;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.network.chat.TextColor;

import java.util.function.UnaryOperator;

// DyeItem that, besides the nearest vanilla DyeColor, stamps the exact fossil hex
// onto the sign text as a per-line Style color. SignBlockEntity.setMessages reuses
// each line's Style when the sign is edited again, so the color survives re-edits,
// just like a vanilla dye. The DyeColor is still stored for the glow path and as a
// sensible fallback if the Style is ever stripped.
public class FossilDyeItem extends DyeItem {
    private final int rgb;
    private final DyeColor vanilla;

    public FossilDyeItem(int rgb, DyeColor vanilla, Item.Properties properties) {
        super(properties);
        this.rgb = rgb;
        this.vanilla = vanilla;
    }

    @Override
    public boolean tryApplyToSign(Level level, SignBlockEntity sign, boolean front, ItemStack stack, Player player) {
        TextColor color = TextColor.fromRgb(this.rgb);
        UnaryOperator<SignText> operator = text -> {
            text = text.setColor(this.vanilla);
            for (int i = 0; i < SignText.LINES; i++) {
                Component message = text.getMessage(i, false);
                text = text.setMessage(i, message.copy().setStyle(message.getStyle().withColor(color)));
            }
            return text;
        };

        boolean applied = sign.updateText(operator, front);
        if (applied) {
            level.playSound(null, sign.getBlockPos(), SoundEvents.DYE_USE, SoundSource.BLOCKS, 1.0F, 1.0F);
            player.awardStat(Stats.ITEM_USED.get(stack.getItem()));
            if (level instanceof ServerLevel serverLevel) {
                serverLevel.gameEvent(GameEvent.BLOCK_CHANGE, sign.getBlockPos(), GameEvent.Context.of(player, sign.getBlockState()));
            }
        }
        return applied;
    }
}
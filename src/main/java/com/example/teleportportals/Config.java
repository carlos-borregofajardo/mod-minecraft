package com.example.teleportportals;

import net.minecraftforge.common.ForgeConfigSpec;
import net.minecraftforge.eventbus.api.listener.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.config.ModConfigEvent;

/**
 * Configuración del mod de portales y bases.
 */
@Mod.EventBusSubscriber(modid = TeleportPortalsMod.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class Config {
    private static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();

    private static final ForgeConfigSpec.IntValue PORTAL_COOLDOWN = BUILDER
        .comment("Cooldown in ticks between portal teleports per player")
        .defineInRange("portalCooldown", 60, 0, Integer.MAX_VALUE);

    static final ForgeConfigSpec SPEC = BUILDER.build();

    public static int portalCooldown;

    @SubscribeEvent
    static void onLoad(final ModConfigEvent event) {
        portalCooldown = PORTAL_COOLDOWN.get();
    }
}

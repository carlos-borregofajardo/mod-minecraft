package com.example.teleportportals;

import com.example.teleportportals.portal.PortalColor;
import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.config.ModConfig;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

/**
 * Punto de entrada del mod de portales y bases de teletransporte.
 * <p>
 * Registra los bloques portal/base de cada color, sus partículas tintadas y
 * la pestaña creativa propia.
 */
@Mod(TeleportPortalsMod.MODID)
public final class TeleportPortalsMod {
    public static final String MODID = "teleport_portals";

    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);
    public static final DeferredRegister<ParticleType<?>> PARTICLE_TYPES = DeferredRegister.create(ForgeRegistries.PARTICLE_TYPES, MODID);

    static {
        for (PortalColor color : PortalColor.values()) {
            color.registerParticle(PARTICLE_TYPES);
        }
        for (PortalColor color : PortalColor.values()) {
            color.registerBlocks(BLOCKS);
        }
        for (PortalColor color : PortalColor.values()) {
            color.registerItems(ITEMS);
        }
    }

    public static final RegistryObject<CreativeModeTab> PORTALS_TAB = CREATIVE_MODE_TABS.register("portals_tab", () -> CreativeModeTab.builder()
        .withTabsBefore(CreativeModeTabs.COMBAT)
        .icon(() -> PortalColor.GREEN.getPortalItem().get().getDefaultInstance())
        .displayItems((_, output) -> {
            for (PortalColor color : PortalColor.values()) {
                output.accept(color.getPortalItem().get());
                output.accept(color.getBaseItem().get());
            }
        }).build());

    public TeleportPortalsMod(FMLJavaModLoadingContext context) {
        var modBusGroup = context.getModBusGroup();
        BLOCKS.register(modBusGroup);
        ITEMS.register(modBusGroup);
        CREATIVE_MODE_TABS.register(modBusGroup);
        PARTICLE_TYPES.register(modBusGroup);

        BuildCreativeModeTabContentsEvent.BUS.addListener(TeleportPortalsMod::addCreative);
        context.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }

    private static void addCreative(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
            for (PortalColor color : PortalColor.values()) {
                event.accept(color.getBaseItem());
            }
        }
    }
}

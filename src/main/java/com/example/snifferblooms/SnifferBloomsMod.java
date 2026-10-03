package com.example.snifferblooms;

import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.Item;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;


@Mod(SnifferBloomsMod.MODID)
public final class SnifferBloomsMod {
    public static final String MODID = "sniffer_blooms";

    public static final DeferredRegister<Item> ITEMS =
        DeferredRegister.create(ForgeRegistries.ITEMS, MODID);

    public static final RegistryObject<Item> SOFT_TERRACOTTA_DYE =
        ITEMS.register("soft_terracotta_dye", () -> new DyeItem(
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_dye"))
                .component(DataComponents.DYE, DyeColor.ORANGE)
        ));

    public SnifferBloomsMod(FMLJavaModLoadingContext context) {
        ITEMS.register(context.getModBusGroup());
    }
}
package com.example.snifferblooms;

import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.Item;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.block.WoolCarpetBlock;

@Mod(SnifferBloomsMod.MODID)
public final class SnifferBloomsMod {
    public static final String MODID = "sniffer_blooms";

    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    
    //blocks
    public static final RegistryObject<Block> SOFT_TERRACOTTA_WOOL =
        BLOCKS.register("soft_terracotta_wool", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_wool"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.GUITAR)
                .strength(0.8F)
                .sound(SoundType.WOOL)
                .ignitedByLava()
    ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_CARPET =
        BLOCKS.register("soft_terracotta_carpet", () -> new WoolCarpetBlock(
            DyeColor.ORANGE,
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_carpet"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .strength(0.1F)
                .sound(SoundType.WOOL)
                .ignitedByLava()
    ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_TERRACOTTA =
        BLOCKS.register("soft_terracotta_terracotta", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_terracotta"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.25F, 4.2F)
    ));

    //items
    public static final RegistryObject<Item> SOFT_TERRACOTTA_DYE =
        ITEMS.register("soft_terracotta_dye", () -> new DyeItem(
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_dye"))
                .component(DataComponents.DYE, DyeColor.ORANGE)
    ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_WOOL_ITEM =
        ITEMS.register("soft_terracotta_wool", () -> new BlockItem(
            SOFT_TERRACOTTA_WOOL.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_wool"))
                .useBlockDescriptionPrefix()
    ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_CARPET_ITEM =
        ITEMS.register("soft_terracotta_carpet", () -> new BlockItem(
            SOFT_TERRACOTTA_CARPET.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_carpet"))
                .useBlockDescriptionPrefix()
    ));

     public static final RegistryObject<Item> SOFT_TERRACOTTA_TERRACOTTA_ITEM =
        ITEMS.register("soft_terracotta_terracotta", () -> new BlockItem(
            SOFT_TERRACOTTA_TERRACOTTA.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_terracotta"))
                .useBlockDescriptionPrefix()
    ));



    public SnifferBloomsMod(FMLJavaModLoadingContext context) {
        BLOCKS.register(context.getModBusGroup());
        ITEMS.register(context.getModBusGroup());
        BuildCreativeModeTabContentsEvent.BUS.addListener(this::addCreativeTabItems);
    }

      private void addCreativeTabItems(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(SOFT_TERRACOTTA_DYE);
        }
        if (event.getTabKey() == CreativeModeTabs.COLORED_BLOCKS) {
            event.accept(SOFT_TERRACOTTA_WOOL_ITEM);
            event.accept(SOFT_TERRACOTTA_CARPET_ITEM);
            event.accept(SOFT_TERRACOTTA_TERRACOTTA_ITEM);
        }
    }
}
package com.example.snifferblooms;

import com.example.snifferblooms.block.SoftTerracottaShulkerBoxBlock;
import com.example.snifferblooms.block.entity.SoftTerracottaShulkerBoxBlockEntity;
import com.example.snifferblooms.client.renderer.SoftTerracottaShulkerBoxRenderer;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.BundleItem;
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
import net.minecraft.world.item.equipment.Equippable;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.block.WoolCarpetBlock;
import net.minecraft.world.level.block.StainedGlassBlock;
import net.minecraft.world.level.block.StainedGlassPaneBlock;
import net.minecraft.world.level.block.BedBlock;
import net.minecraft.world.level.block.ConcretePowderBlock;
import net.minecraft.world.level.block.CandleBlock;
import net.minecraft.world.level.block.CandleCakeBlock;
import net.minecraft.world.level.block.GlazedTerracottaBlock;
import net.minecraft.world.level.block.ShulkerBoxBlock;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.entity.ShulkerBoxBlockEntity;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.fml.loading.FMLEnvironment;
import net.minecraftforge.client.event.EntityRenderersEvent;

@Mod(SnifferBloomsMod.MODID)
public final class SnifferBloomsMod {
    public static final String MODID = "sniffer_blooms";

    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITY_TYPES = DeferredRegister.create(ForgeRegistries.BLOCK_ENTITY_TYPES, MODID);

    // blocks
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

    public static final RegistryObject<Block> SOFT_TERRACOTTA_GLAZED_TERRACOTTA =
        BLOCKS.register("soft_terracotta_glazed_terracotta", () -> new GlazedTerracottaBlock(
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_glazed_terracotta"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.25F, 4.2F)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_STAINED_GLASS =
        BLOCKS.register("soft_terracotta_stained_glass", () -> new StainedGlassBlock(
            DyeColor.ORANGE,
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_stained_glass"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.HAT)
                .strength(0.3F)
                .sound(SoundType.GLASS)
                .noOcclusion()
                .isValidSpawn((state, level, pos, entityType) -> false)
                .isRedstoneConductor((state, level, pos) -> false)
                .isSuffocating((state, level, pos) -> false)
                .isViewBlocking((state, level, pos) -> false)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_STAINED_GLASS_PANE =
        BLOCKS.register("soft_terracotta_stained_glass_pane", () -> new StainedGlassPaneBlock(
            DyeColor.ORANGE,
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_stained_glass_pane"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.HAT)
                .strength(0.3F)
                .sound(SoundType.GLASS)
                .noOcclusion()
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_CONCRETE =
        BLOCKS.register("soft_terracotta_concrete", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_concrete"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.8F)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_CONCRETE_POWDER =
        BLOCKS.register("soft_terracotta_concrete_powder", () -> new ConcretePowderBlock(
            SOFT_TERRACOTTA_CONCRETE.get(),
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_concrete_powder"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .instrument(NoteBlockInstrument.SNARE)
                .strength(0.5F)
                .sound(SoundType.SAND)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_CANDLE =
        BLOCKS.register("soft_terracotta_candle", () -> new CandleBlock(
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_candle"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .noOcclusion()
                .strength(0.1F)
                .sound(SoundType.CANDLE)
                .lightLevel(CandleBlock.LIGHT_EMISSION)
                .pushReaction(PushReaction.DESTROY)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_CANDLE_CAKE =
        BLOCKS.register("soft_terracotta_candle_cake", () -> new CandleCakeBlock(
            SOFT_TERRACOTTA_CANDLE.get(),
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_candle_cake"))
                .forceSolidOn()
                .strength(0.5F)
                .sound(SoundType.WOOL)
                .pushReaction(PushReaction.DESTROY)
                .lightLevel(state -> state.getValue(CandleCakeBlock.LIT) ? 3 : 0)
        ));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_SHULKER_BOX =
        BLOCKS.register("soft_terracotta_shulker_box", () -> new SoftTerracottaShulkerBoxBlock(
            DyeColor.ORANGE,
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_shulker_box"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .forceSolidOn()
                .strength(2.0F)
                .dynamicShape()
                .noOcclusion()
                .isSuffocating((state, level, pos) -> level.getBlockEntity(pos) instanceof ShulkerBoxBlockEntity s ? s.isClosed() : true)
                .isViewBlocking((state, level, pos) -> level.getBlockEntity(pos) instanceof ShulkerBoxBlockEntity s ? s.isClosed() : true)
                .pushReaction(PushReaction.DESTROY)
        ));

    public static final RegistryObject<BlockEntityType<SoftTerracottaShulkerBoxBlockEntity>> SOFT_TERRACOTTA_SHULKER_BOX_ENTITY =
        BLOCK_ENTITY_TYPES.register("soft_terracotta_shulker_box",
            () -> new BlockEntityType<>(SoftTerracottaShulkerBoxBlockEntity::new, java.util.Set.of(SOFT_TERRACOTTA_SHULKER_BOX.get())));

    public static final RegistryObject<Block> SOFT_TERRACOTTA_BED =
        BLOCKS.register("soft_terracotta_bed", () -> new BedBlock(
            DyeColor.ORANGE,
            BlockBehaviour.Properties.of()
                .setId(BLOCKS.key("soft_terracotta_bed"))
                .mapColor(MapColor.TERRACOTTA_ORANGE)
                .strength(0.2F)
                .sound(SoundType.WOOD)
                .ignitedByLava()
                .noOcclusion()
        ));

    // items
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

    public static final RegistryObject<Item> SOFT_TERRACOTTA_GLAZED_TERRACOTTA_ITEM =
        ITEMS.register("soft_terracotta_glazed_terracotta", () -> new BlockItem(
            SOFT_TERRACOTTA_GLAZED_TERRACOTTA.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_glazed_terracotta"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_STAINED_GLASS_ITEM =
        ITEMS.register("soft_terracotta_stained_glass", () -> new BlockItem(
            SOFT_TERRACOTTA_STAINED_GLASS.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_stained_glass"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_STAINED_GLASS_PANE_ITEM =
        ITEMS.register("soft_terracotta_stained_glass_pane", () -> new BlockItem(
            SOFT_TERRACOTTA_STAINED_GLASS_PANE.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_stained_glass_pane"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_CONCRETE_ITEM =
        ITEMS.register("soft_terracotta_concrete", () -> new BlockItem(
            SOFT_TERRACOTTA_CONCRETE.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_concrete"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_CONCRETE_POWDER_ITEM =
        ITEMS.register("soft_terracotta_concrete_powder", () -> new BlockItem(
            SOFT_TERRACOTTA_CONCRETE_POWDER.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_concrete_powder"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_CANDLE_ITEM =
        ITEMS.register("soft_terracotta_candle", () -> new BlockItem(
            SOFT_TERRACOTTA_CANDLE.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_candle"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_SHULKER_BOX_ITEM =
        ITEMS.register("soft_terracotta_shulker_box", () -> new BlockItem(
            SOFT_TERRACOTTA_SHULKER_BOX.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_shulker_box"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_BED_ITEM =
        ITEMS.register("soft_terracotta_bed", () -> new BlockItem(
            SOFT_TERRACOTTA_BED.get(),
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_bed"))
                .useBlockDescriptionPrefix()
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_HARNESS =
        ITEMS.register("soft_terracotta_harness", () -> new Item(
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_harness"))
                .stacksTo(1)
                .component(net.minecraft.core.component.DataComponents.EQUIPPABLE, Equippable.harness(DyeColor.ORANGE))
        ));

    public static final RegistryObject<Item> SOFT_TERRACOTTA_BUNDLE =
        ITEMS.register("soft_terracotta_bundle", () -> new BundleItem(
            new Item.Properties()
                .setId(ITEMS.key("soft_terracotta_bundle"))
                .stacksTo(1)
                .component(DataComponents.BUNDLE_CONTENTS, net.minecraft.world.item.component.BundleContents.EMPTY)
        ));

    public SnifferBloomsMod(FMLJavaModLoadingContext context) {
        BLOCKS.register(context.getModBusGroup());
        ITEMS.register(context.getModBusGroup());
        BLOCK_ENTITY_TYPES.register(context.getModBusGroup());
        BuildCreativeModeTabContentsEvent.BUS.addListener(this::addCreativeTabItems);

        if (FMLEnvironment.dist == Dist.CLIENT) {
            EntityRenderersEvent.RegisterRenderers.BUS.addListener(event ->
                event.registerBlockEntityRenderer(
                    SOFT_TERRACOTTA_SHULKER_BOX_ENTITY.get(),
                    SoftTerracottaShulkerBoxRenderer::new
                )
            );
        }
    }

    private void addCreativeTabItems(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            event.accept(SOFT_TERRACOTTA_DYE);
        }
        if (event.getTabKey() == CreativeModeTabs.COLORED_BLOCKS) {
            event.accept(SOFT_TERRACOTTA_WOOL_ITEM);
            event.accept(SOFT_TERRACOTTA_CARPET_ITEM);
            event.accept(SOFT_TERRACOTTA_TERRACOTTA_ITEM);
            event.accept(SOFT_TERRACOTTA_GLAZED_TERRACOTTA_ITEM);
            event.accept(SOFT_TERRACOTTA_STAINED_GLASS_ITEM);
            event.accept(SOFT_TERRACOTTA_STAINED_GLASS_PANE_ITEM);
            event.accept(SOFT_TERRACOTTA_CONCRETE_ITEM);
            event.accept(SOFT_TERRACOTTA_CONCRETE_POWDER_ITEM);
            event.accept(SOFT_TERRACOTTA_CANDLE_ITEM);
            event.accept(SOFT_TERRACOTTA_SHULKER_BOX_ITEM);
            event.accept(SOFT_TERRACOTTA_BED_ITEM);
            event.accept(SOFT_TERRACOTTA_HARNESS);
            event.accept(SOFT_TERRACOTTA_BUNDLE);
        }
    }
}
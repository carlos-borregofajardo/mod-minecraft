package com.example.snifferblooms;

import com.example.snifferblooms.block.FossilFlowerBlock;
import com.example.snifferblooms.block.SoftTerracottaShulkerBoxBlock;
import com.example.snifferblooms.item.FossilDyeItem;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.BundleItem;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.component.BundleContents;
import net.minecraft.world.item.equipment.Equippable;
import net.minecraft.world.level.block.BedBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.CandleBlock;
import net.minecraft.world.level.block.CandleCakeBlock;
import net.minecraft.world.level.block.ConcretePowderBlock;
import net.minecraft.world.level.block.DoublePlantBlock;
import net.minecraft.world.level.block.FlowerPotBlock;
import net.minecraft.world.level.block.GlazedTerracottaBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StainedGlassBlock;
import net.minecraft.world.level.block.StainedGlassPaneBlock;
import net.minecraft.world.level.block.WoolCarpetBlock;
import net.minecraft.world.level.block.entity.ShulkerBoxBlockEntity;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

import java.util.HashSet;
import java.util.Set;

public enum FossilColor {
    SOFT_TERRACOTTA("soft_terracotta", 0xD98A62, DyeColor.ORANGE),
    FOSSIL_TURQUOISE("fossil_turquoise", 0x62B7AE, DyeColor.CYAN),
    ANCIENT_ROSE("ancient_rose", 0xD889A5, DyeColor.MAGENTA),
    FERN_GREEN("fern_green", 0x658F68, DyeColor.GREEN),
    POLLEN_YELLOW("pollen_yellow", 0xE5C968, DyeColor.YELLOW),
    LAVENDER("lavender", 0xA58FBE, DyeColor.PURPLE),
    MIST_BLUE("mist_blue", 0x8EC6D4, DyeColor.LIGHT_BLUE),
    STONE_GRAY("stone_gray", 0x858783, DyeColor.GRAY),
    ASH_GRAY("ash_gray", 0xB9B7A9, DyeColor.LIGHT_GRAY),
    CLAY_RED("clay_red", 0xB85F5A, DyeColor.RED),
    BARK_BROWN("bark_brown", 0x9A7255, DyeColor.BROWN),
    FOSSIL_BLUE("fossil_blue", 0x668EB8, DyeColor.BLUE),
    FOSSIL_IVORY("fossil_ivory", 0xE8E2D0, DyeColor.WHITE),
    SOFT_LIME("soft_lime", 0xA8C875, DyeColor.LIME),
    CORAL("coral", 0xE6A6B8, DyeColor.PINK),
    OBSIDIAN("obsidian", 0x3D3B3A, DyeColor.BLACK);

    // The 16 fossil colors do not all become both flowers: warm hues become the
    // torchflower, cool hues become the pitcher plant.
    public static final Set<String> TORCHFLOWER_COLORS = Set.of(
        "soft_terracotta", "ancient_rose", "pollen_yellow", "clay_red",
        "bark_brown", "fossil_ivory", "coral", "ash_gray");
    public static final Set<String> PITCHER_COLORS = Set.of(
        "fossil_turquoise", "fern_green", "lavender", "mist_blue",
        "stone_gray", "fossil_blue", "soft_lime", "obsidian");

    private final String id;
    private final int rgb;
    private final DyeColor vanilla;

    private RegistryObject<Block> wool;
    private RegistryObject<Block> carpet;
    private RegistryObject<Block> terracotta;
    private RegistryObject<Block> glazedTerracotta;
    private RegistryObject<Block> stainedGlass;
    private RegistryObject<Block> stainedGlassPane;
    private RegistryObject<Block> concrete;
    private RegistryObject<Block> concretePowder;
    private RegistryObject<Block> candle;
    private RegistryObject<Block> candleCake;
    private RegistryObject<Block> shulkerBox;
    private RegistryObject<Block> bed;
    private RegistryObject<Block> torchflower;
    private RegistryObject<Block> pottedTorchflower;
    private RegistryObject<Block> pitcherPlant;

    private RegistryObject<Item> dye;
    private RegistryObject<Item> woolItem;
    private RegistryObject<Item> carpetItem;
    private RegistryObject<Item> terracottaItem;
    private RegistryObject<Item> glazedTerracottaItem;
    private RegistryObject<Item> stainedGlassItem;
    private RegistryObject<Item> stainedGlassPaneItem;
    private RegistryObject<Item> concreteItem;
    private RegistryObject<Item> concretePowderItem;
    private RegistryObject<Item> candleItem;
    private RegistryObject<Item> shulkerBoxItem;
    private RegistryObject<Item> bedItem;
    private RegistryObject<Item> torchflowerItem;
    private RegistryObject<Item> pitcherPlantItem;
    private RegistryObject<Item> torchflowerSeeds;
    private RegistryObject<Item> pitcherSeeds;
    private RegistryObject<Item> harness;
    private RegistryObject<Item> bundle;

    FossilColor(String id, int rgb, DyeColor vanilla) {
        this.id = id;
        this.rgb = rgb;
        this.vanilla = vanilla;
    }

    public String getId() {
        return this.id;
    }

    public int getRgb() {
        return this.rgb;
    }

    public DyeColor getVanilla() {
        return this.vanilla;
    }

    public RegistryObject<Block> getWool() {
        return this.wool;
    }

    public RegistryObject<Block> getCarpet() {
        return this.carpet;
    }

    public RegistryObject<Block> getTerracotta() {
        return this.terracotta;
    }

    public RegistryObject<Block> getGlazedTerracotta() {
        return this.glazedTerracotta;
    }

    public RegistryObject<Block> getStainedGlass() {
        return this.stainedGlass;
    }

    public RegistryObject<Block> getStainedGlassPane() {
        return this.stainedGlassPane;
    }

    public RegistryObject<Block> getConcrete() {
        return this.concrete;
    }

    public RegistryObject<Block> getConcretePowder() {
        return this.concretePowder;
    }

    public RegistryObject<Block> getCandle() {
        return this.candle;
    }

    public RegistryObject<Block> getCandleCake() {
        return this.candleCake;
    }

    public RegistryObject<Block> getShulkerBox() {
        return this.shulkerBox;
    }

    public RegistryObject<Block> getBed() {
        return this.bed;
    }

    public RegistryObject<Block> getTorchflower() {
        return this.torchflower;
    }

    public RegistryObject<Block> getPottedTorchflower() {
        return this.pottedTorchflower;
    }

    public RegistryObject<Block> getPitcherPlant() {
        return this.pitcherPlant;
    }

    public RegistryObject<Item> getDye() {
        return this.dye;
    }

    public RegistryObject<Item> getWoolItem() {
        return this.woolItem;
    }

    public RegistryObject<Item> getCarpetItem() {
        return this.carpetItem;
    }

    public RegistryObject<Item> getTerracottaItem() {
        return this.terracottaItem;
    }

    public RegistryObject<Item> getGlazedTerracottaItem() {
        return this.glazedTerracottaItem;
    }

    public RegistryObject<Item> getStainedGlassItem() {
        return this.stainedGlassItem;
    }

    public RegistryObject<Item> getStainedGlassPaneItem() {
        return this.stainedGlassPaneItem;
    }

    public RegistryObject<Item> getConcreteItem() {
        return this.concreteItem;
    }

    public RegistryObject<Item> getConcretePowderItem() {
        return this.concretePowderItem;
    }

    public RegistryObject<Item> getCandleItem() {
        return this.candleItem;
    }

    public RegistryObject<Item> getShulkerBoxItem() {
        return this.shulkerBoxItem;
    }

    public RegistryObject<Item> getBedItem() {
        return this.bedItem;
    }

    public RegistryObject<Item> getTorchflowerItem() {
        return this.torchflowerItem;
    }

    public RegistryObject<Item> getPitcherPlantItem() {
        return this.pitcherPlantItem;
    }

    public RegistryObject<Item> getTorchflowerSeeds() {
        return this.torchflowerSeeds;
    }

    public RegistryObject<Item> getPitcherSeeds() {
        return this.pitcherSeeds;
    }

    public RegistryObject<Item> getHarness() {
        return this.harness;
    }

    public RegistryObject<Item> getBundle() {
        return this.bundle;
    }

    public static void registerBlocks(DeferredRegister<Block> blocks) {
        for (FossilColor color : values()) {
            color.registerBlocksSelf(blocks);
        }
    }

    private void registerBlocksSelf(DeferredRegister<Block> blocks) {
        this.wool = blocks.register(this.id + "_wool", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_wool"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.GUITAR)
                .strength(0.8F)
                .sound(SoundType.WOOL)
                .ignitedByLava()
        ));

        this.carpet = blocks.register(this.id + "_carpet", () -> new WoolCarpetBlock(
            this.vanilla,
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_carpet"))
                .mapColor(this.vanilla.getTerracottaColor())
                .strength(0.1F)
                .sound(SoundType.WOOL)
                .ignitedByLava()
        ));

        this.terracotta = blocks.register(this.id + "_terracotta", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_terracotta"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.25F, 4.2F)
        ));

        this.glazedTerracotta = blocks.register(this.id + "_glazed_terracotta", () -> new GlazedTerracottaBlock(
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_glazed_terracotta"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.25F, 4.2F)
        ));

        this.stainedGlass = blocks.register(this.id + "_stained_glass", () -> new StainedGlassBlock(
            this.vanilla,
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_stained_glass"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.HAT)
                .strength(0.3F)
                .sound(SoundType.GLASS)
                .noOcclusion()
                .isValidSpawn((state, level, pos, entityType) -> false)
                .isRedstoneConductor((state, level, pos) -> false)
                .isSuffocating((state, level, pos) -> false)
                .isViewBlocking((state, level, pos) -> false)
        ));

        this.stainedGlassPane = blocks.register(this.id + "_stained_glass_pane", () -> new StainedGlassPaneBlock(
            this.vanilla,
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_stained_glass_pane"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.HAT)
                .strength(0.3F)
                .sound(SoundType.GLASS)
                .noOcclusion()
        ));

        this.concrete = blocks.register(this.id + "_concrete", () -> new Block(
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_concrete"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.BASEDRUM)
                .requiresCorrectToolForDrops()
                .strength(1.8F)
        ));

        this.concretePowder = blocks.register(this.id + "_concrete_powder", () -> new ConcretePowderBlock(
            this.concrete.get(),
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_concrete_powder"))
                .mapColor(this.vanilla.getTerracottaColor())
                .instrument(NoteBlockInstrument.SNARE)
                .strength(0.5F)
                .sound(SoundType.SAND)
        ));

        this.candle = blocks.register(this.id + "_candle", () -> new CandleBlock(
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_candle"))
                .mapColor(this.vanilla.getTerracottaColor())
                .noOcclusion()
                .strength(0.1F)
                .sound(SoundType.CANDLE)
                .lightLevel(CandleBlock.LIGHT_EMISSION)
                .pushReaction(PushReaction.DESTROY)
        ));

        this.candleCake = blocks.register(this.id + "_candle_cake", () -> new CandleCakeBlock(
            this.candle.get(),
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_candle_cake"))
                .forceSolidOn()
                .strength(0.5F)
                .sound(SoundType.WOOL)
                .pushReaction(PushReaction.DESTROY)
                .lightLevel(state -> state.getValue(CandleCakeBlock.LIT) ? 3 : 0)
        ));

        this.shulkerBox = blocks.register(this.id + "_shulker_box", () -> new SoftTerracottaShulkerBoxBlock(
            this.vanilla,
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_shulker_box"))
                .mapColor(this.vanilla.getTerracottaColor())
                .forceSolidOn()
                .strength(2.0F)
                .dynamicShape()
                .noOcclusion()
                .isSuffocating((state, level, pos) -> level.getBlockEntity(pos) instanceof ShulkerBoxBlockEntity s ? s.isClosed() : true)
                .isViewBlocking((state, level, pos) -> level.getBlockEntity(pos) instanceof ShulkerBoxBlockEntity s ? s.isClosed() : true)
                .pushReaction(PushReaction.DESTROY)
        ));

        this.bed = blocks.register(this.id + "_bed", () -> new BedBlock(
            this.vanilla,
            BlockBehaviour.Properties.of()
                .setId(blocks.key(this.id + "_bed"))
                .mapColor(this.vanilla.getTerracottaColor())
                .strength(0.2F)
                .sound(SoundType.WOOD)
                .ignitedByLava()
                .noOcclusion()
        ));

        if (TORCHFLOWER_COLORS.contains(this.id)) {
            this.torchflower = blocks.register(this.id + "_torchflower", () -> new FossilFlowerBlock(
                BlockBehaviour.Properties.of()
                    .setId(blocks.key(this.id + "_torchflower"))
                    .mapColor(MapColor.PLANT)
                    .noCollision()
                    .instabreak()
                    .sound(SoundType.GRASS)
                    .offsetType(BlockBehaviour.OffsetType.XZ)
                    .pushReaction(PushReaction.DESTROY)
            ));
            this.pottedTorchflower = blocks.register("potted_" + this.id + "_torchflower", () -> new FlowerPotBlock(
                this.torchflower.get(),
                BlockBehaviour.Properties.of()
                    .setId(blocks.key("potted_" + this.id + "_torchflower"))
                    .mapColor(MapColor.PLANT)
                    .instabreak()
                    .noCollision()
                    .pushReaction(PushReaction.DESTROY)
            ));
        }
        if (PITCHER_COLORS.contains(this.id)) {
            this.pitcherPlant = blocks.register(this.id + "_pitcher_plant", () -> new DoublePlantBlock(
                BlockBehaviour.Properties.of()
                    .setId(blocks.key(this.id + "_pitcher_plant"))
                    .mapColor(MapColor.PLANT)
                    .instabreak()
                    .noCollision()
                    .sound(SoundType.GRASS)
                    .pushReaction(PushReaction.DESTROY)
            ));
        }
    }

    public static void registerItems(DeferredRegister<Item> items) {
        for (FossilColor color : values()) {
            color.registerItemsSelf(items);
        }
    }

    private void registerItemsSelf(DeferredRegister<Item> items) {
        this.dye = items.register(this.id + "_dye", () -> new FossilDyeItem(
            this.rgb,
            this.vanilla,
            new Item.Properties()
                .setId(items.key(this.id + "_dye"))
                .component(DataComponents.DYE, this.vanilla)
        ));

        this.woolItem = this.registerBlockItem(items, this.id + "_wool", this.wool);
        this.carpetItem = this.registerBlockItem(items, this.id + "_carpet", this.carpet);
        this.terracottaItem = this.registerBlockItem(items, this.id + "_terracotta", this.terracotta);
        this.glazedTerracottaItem = this.registerBlockItem(items, this.id + "_glazed_terracotta", this.glazedTerracotta);
        this.stainedGlassItem = this.registerBlockItem(items, this.id + "_stained_glass", this.stainedGlass);
        this.stainedGlassPaneItem = this.registerBlockItem(items, this.id + "_stained_glass_pane", this.stainedGlassPane);
        this.concreteItem = this.registerBlockItem(items, this.id + "_concrete", this.concrete);
        this.concretePowderItem = this.registerBlockItem(items, this.id + "_concrete_powder", this.concretePowder);
        this.candleItem = this.registerBlockItem(items, this.id + "_candle", this.candle);
        this.shulkerBoxItem = this.registerBlockItem(items, this.id + "_shulker_box", this.shulkerBox);
        this.bedItem = this.registerBlockItem(items, this.id + "_bed", this.bed);

        if (TORCHFLOWER_COLORS.contains(this.id)) {
            this.torchflowerSeeds = items.register(this.id + "_torchflower_seeds", () -> new BlockItem(
                this.torchflower.get(),
                new Item.Properties()
                    .setId(items.key(this.id + "_torchflower_seeds"))
            ));
            this.torchflowerItem = this.registerBlockItem(items, this.id + "_torchflower", this.torchflower);
        }
        if (PITCHER_COLORS.contains(this.id)) {
            this.pitcherSeeds = items.register(this.id + "_pitcher_seeds", () -> new BlockItem(
                this.pitcherPlant.get(),
                new Item.Properties()
                    .setId(items.key(this.id + "_pitcher_seeds"))
            ));
            this.pitcherPlantItem = this.registerBlockItem(items, this.id + "_pitcher_plant", this.pitcherPlant);
        }

        this.harness = items.register(this.id + "_harness", () -> new Item(
            new Item.Properties()
                .setId(items.key(this.id + "_harness"))
                .stacksTo(1)
                .component(DataComponents.EQUIPPABLE, Equippable.harness(this.vanilla))
        ));

        this.bundle = items.register(this.id + "_bundle", () -> new BundleItem(
            new Item.Properties()
                .setId(items.key(this.id + "_bundle"))
                .stacksTo(1)
                .component(DataComponents.BUNDLE_CONTENTS, BundleContents.EMPTY)
        ));
    }

    private RegistryObject<Item> registerBlockItem(DeferredRegister<Item> items, String name, RegistryObject<Block> block) {
        return items.register(name, () -> new BlockItem(
            block.get(),
            new Item.Properties()
                .setId(items.key(name))
                .useBlockDescriptionPrefix()
        ));
    }

    public static Set<Block> shulkerBoxBlocks() {
        Set<Block> blocks = new HashSet<>();
        for (FossilColor color : values()) {
            blocks.add(color.shulkerBox.get());
        }
        return blocks;
    }

    /**
     * Both the flower and its seed are BlockItems of the same block, so copying
     * (creative pick-block) returns whatever {@link Item#BY_BLOCK} maps last.
     * Force the flower to win so copying a plant gives the plant, not the seed.
     */
    public static void mapFlowerItemsToBlocks() {
        for (FossilColor color : values()) {
            if (color.torchflower != null && color.torchflowerItem != null) {
                Item.BY_BLOCK.put(color.torchflower.get(), color.torchflowerItem.get());
            }
            if (color.pitcherPlant != null && color.pitcherPlantItem != null) {
                Item.BY_BLOCK.put(color.pitcherPlant.get(), color.pitcherPlantItem.get());
            }
        }
    }
}
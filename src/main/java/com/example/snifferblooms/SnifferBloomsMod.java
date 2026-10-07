package com.example.snifferblooms;

import com.example.snifferblooms.block.entity.SoftTerracottaShulkerBoxBlockEntity;
import com.example.snifferblooms.client.renderer.SoftTerracottaShulkerBoxRenderer;
import com.example.snifferblooms.item.FossilDyeItem;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.network.chat.TextColor;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.item.DyeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.entity.SignBlockEntity;
import net.minecraft.world.level.block.entity.SignText;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.fml.LogicalSide;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.loading.FMLEnvironment;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

import java.util.HashSet;
import java.util.Set;

@Mod(SnifferBloomsMod.MODID)
public final class SnifferBloomsMod {
    public static final String MODID = "sniffer_blooms";

    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITY_TYPES = DeferredRegister.create(ForgeRegistries.BLOCK_ENTITY_TYPES, MODID);

    public static final RegistryObject<BlockEntityType<SoftTerracottaShulkerBoxBlockEntity>> SOFT_TERRACOTTA_SHULKER_BOX_ENTITY;

    private static final Set<Integer> FOSSIL_SIGN_RGB = new HashSet<>();

    static {
        for (FossilColor color : FossilColor.values()) {
            FOSSIL_SIGN_RGB.add(color.getRgb());
        }
        FossilColor.registerBlocks(BLOCKS);
        SOFT_TERRACOTTA_SHULKER_BOX_ENTITY = BLOCK_ENTITY_TYPES.register("soft_terracotta_shulker_box",
            () -> new BlockEntityType<>(SoftTerracottaShulkerBoxBlockEntity::new, FossilColor.shulkerBoxBlocks()));
        FossilColor.registerItems(ITEMS);
    }

    public SnifferBloomsMod(FMLJavaModLoadingContext context) {
        BLOCKS.register(context.getModBusGroup());
        ITEMS.register(context.getModBusGroup());
        BLOCK_ENTITY_TYPES.register(context.getModBusGroup());
        BuildCreativeModeTabContentsEvent.BUS.addListener(this::addCreativeTabItems);
        PlayerInteractEvent.RightClickBlock.BUS.addListener(this::onRightClickBlock);

        if (FMLEnvironment.dist == Dist.CLIENT) {
            EntityRenderersEvent.RegisterRenderers.BUS.addListener(event ->
                event.registerBlockEntityRenderer(
                    SOFT_TERRACOTTA_SHULKER_BOX_ENTITY.get(),
                    SoftTerracottaShulkerBoxRenderer::new
                )
            );
        }
    }

    private void onRightClickBlock(PlayerInteractEvent.RightClickBlock event) {
        if (event.getSide() != LogicalSide.SERVER) {
            return;
        }
        Level level = event.getLevel();
        ItemStack stack = event.getItemStack();
        if (!(stack.getItem() instanceof DyeItem) || stack.getItem() instanceof FossilDyeItem) {
            return;
        }
        if (stack.get(DataComponents.DYE) == null) {
            return;
        }
        if (!(level.getBlockEntity(event.getPos()) instanceof SignBlockEntity sign)) {
            return;
        }
        boolean front = sign.isFacingFrontText(event.getEntity());
        sign.updateText(text -> {
            SignText result = text;
            for (int i = 0; i < SignText.LINES; i++) {
                Component message = result.getMessage(i, false);
                Style style = message.getStyle();
                TextColor color = style.getColor();
                if (color != null && FOSSIL_SIGN_RGB.contains(color.getValue())) {
                    result = result.setMessage(i, message.copy().setStyle(style.withColor((TextColor) null)));
                }
            }
            return result;
        }, front);
    }

    private void addCreativeTabItems(BuildCreativeModeTabContentsEvent event) {
        FossilColor.mapFlowerItemsToBlocks();
        if (event.getTabKey() == CreativeModeTabs.INGREDIENTS) {
            for (FossilColor color : FossilColor.values()) {
                event.accept(color.getDye());
            }
        }
        if (event.getTabKey() == CreativeModeTabs.NATURAL_BLOCKS) {
            for (FossilColor color : FossilColor.values()) {
                if (color.getTorchflowerItem() != null) {
                    event.accept(color.getTorchflowerItem());
                }
                if (color.getPitcherPlantItem() != null) {
                    event.accept(color.getPitcherPlantItem());
                }
                if (color.getTorchflowerSeeds() != null) {
                    event.accept(color.getTorchflowerSeeds());
                }
                if (color.getPitcherSeeds() != null) {
                    event.accept(color.getPitcherSeeds());
                }
            }
        }
        if (event.getTabKey() == CreativeModeTabs.COLORED_BLOCKS) {
            for (FossilColor color : FossilColor.values()) {
                event.accept(color.getWoolItem());
                event.accept(color.getCarpetItem());
                event.accept(color.getTerracottaItem());
                event.accept(color.getGlazedTerracottaItem());
                event.accept(color.getStainedGlassItem());
                event.accept(color.getStainedGlassPaneItem());
                event.accept(color.getConcreteItem());
                event.accept(color.getConcretePowderItem());
                event.accept(color.getCandleItem());
                event.accept(color.getShulkerBoxItem());
                event.accept(color.getBedItem());
            }
        }
        if (event.getTabKey() == CreativeModeTabs.TOOLS_AND_UTILITIES) {
            ItemStack bundleAnchor = Items.DYED_BUNDLE.pick(DyeColor.BLACK).getDefaultInstance();
            ItemStack harnessAnchor = Items.HARNESS.pick(DyeColor.BLACK).getDefaultInstance();
            FossilColor[] colors = FossilColor.values();
            for (int i = colors.length - 1; i >= 0; i--) {
                FossilColor color = colors[i];
                event.getEntries().putAfter(bundleAnchor, new ItemStack(color.getBundle().get()),
                    CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS);
                event.getEntries().putAfter(harnessAnchor, new ItemStack(color.getHarness().get()),
                    CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS);
            }
        }
    }
}
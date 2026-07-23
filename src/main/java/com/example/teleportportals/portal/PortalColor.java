package com.example.teleportportals.portal;

import com.example.teleportportals.data.ColorBaseBlockData;

import net.minecraft.core.particles.ParticleType;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.minecraft.world.level.saveddata.SavedDataType;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

import net.minecraft.server.level.ServerLevel;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.WeakHashMap;

/**
 * Enum centralizado que define cada color del sistema de teletransporte.
 * <p>
 * Agrupa la configuración común de cada portal/base (nombre, color del mapa,
 * partícula asociada, referencias a bloques e ítems, datos persistentes y
 * cooldown por jugador) para evitar la duplicación de clases por color.
 */
public enum PortalColor {
    // El verde usa la partícula vanilla happy_villager (sin tinte); su RGB no se usa.
    GREEN("green", MapColor.EMERALD, 0.0F, 0.0F, 0.0F),
    BLUE("blue", MapColor.LAPIS, 0.3F, 0.55F, 1.0F),
    YELLOW("yellow", MapColor.COLOR_YELLOW, 1.0F, 0.9F, 0.2F),
    RED("red", MapColor.COLOR_RED, 1.0F, 0.15F, 0.15F),
    LIGHT_GRAY("light_gray", MapColor.COLOR_LIGHT_GRAY, 0.75F, 0.75F, 0.75F),
    BLACK("black", MapColor.COLOR_BLACK, 0.1F, 0.1F, 0.1F);

    private final String name;
    private final MapColor mapColor;
    private final float particleRed;
    private final float particleGreen;
    private final float particleBlue;

    private RegistryObject<SimpleParticleType> particle;
    private RegistryObject<Block> portalBlock;
    private RegistryObject<Block> baseBlock;
    private RegistryObject<Item> portalItem;
    private RegistryObject<Item> baseItem;
    private SavedDataType<ColorBaseBlockData> dataType;

    private final Map<UUID, Long> cooldownMap = new HashMap<>();

    // Índice por nombre ("green", "blue", ...) para deserializar datos guardados.
    private static final Map<String, PortalColor> BY_NAME = new HashMap<>();

    static {
        for (PortalColor color : values()) {
            BY_NAME.put(color.getName(), color);
        }
    }

    /**
     * @return el color con el nombre dado, o {@code null} si no existe.
     */
    public static PortalColor byName(String name) {
        return BY_NAME.get(name);
    }

    // Cache del SavedData por nivel para no repetir el computeIfAbsent del
    // DataStorage en cada consulta (p. ej. cada tick dentro de un portal).
    // Claves débiles: si el nivel se descarga, la entrada se libera sola.
    private final Map<ServerLevel, ColorBaseBlockData> dataCache = new WeakHashMap<>();

    PortalColor(String name, MapColor mapColor, float particleRed, float particleGreen, float particleBlue) {
        this.name = name;
        this.mapColor = mapColor;
        this.particleRed = particleRed;
        this.particleGreen = particleGreen;
        this.particleBlue = particleBlue;
    }

    public String getName() {
        return name;
    }

    public MapColor getMapColor() {
        return mapColor;
    }

    public float getParticleRed() {
        return particleRed;
    }

    public float getParticleGreen() {
        return particleGreen;
    }

    public float getParticleBlue() {
        return particleBlue;
    }

    public SavedDataType<ColorBaseBlockData> getDataType() {
        return dataType;
    }

    public RegistryObject<Block> getPortalBlock() {
        return portalBlock;
    }

    public RegistryObject<Block> getBaseBlock() {
        return baseBlock;
    }

    public RegistryObject<Item> getPortalItem() {
        return portalItem;
    }

    public RegistryObject<Item> getBaseItem() {
        return baseItem;
    }

    /**
     * @return la partícula asociada al color. El verde reutiliza la partícula
     *         vanilla {@code happy_villager}; el resto usa su propia partícula registrada.
     */
    public SimpleParticleType getParticle() {
        return this == GREEN ? ParticleTypes.HAPPY_VILLAGER : particle.get();
    }

    /**
     * Obtiene los datos de base de este color para el nivel dado, cacheando la
     * instancia (los {@link net.minecraft.world.level.saveddata.SavedData SavedData}
     * son singletons por nivel) para evitar la búsqueda en el DataStorage en cada llamada.
     */
    public ColorBaseBlockData getData(ServerLevel level) {
        return dataCache.computeIfAbsent(level, l -> ColorBaseBlockData.get(l, this));
    }

    public Map<UUID, Long> getCooldownMap() {
        return cooldownMap;
    }

    public void clearCooldown(UUID uuid) {
        cooldownMap.remove(uuid);
    }

    /**
     * Registra la partícula custom del color (excepto verde, que usa la vanilla).
     */
    public void registerParticle(DeferredRegister<ParticleType<?>> register) {
        if (this != GREEN) {
            this.particle = register.register(name + "_villager", () -> new SimpleParticleType(false));
        }
    }

    /**
     * Registra el bloque portal y el bloque base de este color.
     */
    public void registerBlocks(DeferredRegister<Block> blockRegister) {
        this.dataType = ColorBaseBlockData.typeFor(this);

        this.portalBlock = blockRegister.register(name + "_portal",
            () -> new PortalBlock(BlockBehaviour.Properties.of()
                .setId(blockRegister.key(name + "_portal"))
                .mapColor(mapColor)
                .noCollision()
                .noOcclusion()
                .strength(1.0F, 3600000.0F)
                .sound(SoundType.GLASS)
                .noLootTable()
                .pushReaction(PushReaction.BLOCK),
                this
            )
        );

        this.baseBlock = blockRegister.register(name + "_base",
            () -> new TeleportBaseBlock(BlockBehaviour.Properties.of()
                .setId(blockRegister.key(name + "_base"))
                .mapColor(MapColor.METAL)
                .strength(3.0F)
                .sound(SoundType.METAL),
                this
            )
        );
    }

    /**
     * Registra los ítems asociados al bloque portal y al bloque base de este color.
     * Debe llamarse después de {@link #registerBlocks(DeferredRegister)}.
     */
    public void registerItems(DeferredRegister<Item> itemRegister) {
        this.portalItem = itemRegister.register(name + "_portal",
            () -> new BlockItem(portalBlock.get(), new Item.Properties().setId(itemRegister.key(name + "_portal")))
        );
        this.baseItem = itemRegister.register(name + "_base",
            () -> new BlockItem(baseBlock.get(), new Item.Properties().setId(itemRegister.key(name + "_base")))
        );
    }
}

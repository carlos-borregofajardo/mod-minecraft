package com.example.teleportportals.data;

import com.example.teleportportals.TeleportPortalsMod;
import com.example.teleportportals.portal.PortalColor;

import com.mojang.serialization.Codec;
import com.mojang.serialization.DataResult;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.level.saveddata.SavedDataType;

import java.util.EnumMap;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Datos persistentes por mundo que almacenan la última posición de portal
 * usada por cada jugador, para cada color del sistema de teletransporte.
 * <p>
 * Los mapas se indexan por {@link PortalColor}, por lo que añadir un color al
 * enum no requiere tocar esta clase. En disco se serializan planos
 * ({@code {green: {...}, blue: {...}}}), igual que con el formato anterior.
 */
public class PortalReturnData extends SavedData {
    // Codec para UUID como String, necesario porque las claves de un mapa
    // serializado en NBT deben ser cadenas de texto.
    private static final Codec<UUID> UUID_STRING_CODEC = Codec.STRING.xmap(UUID::fromString, UUID::toString);
    private static final Codec<Map<UUID, BlockPos>> PLAYER_PORTAL_MAP_CODEC = Codec.unboundedMap(UUID_STRING_CODEC, BlockPos.CODEC);

    // Codec de PortalColor a partir de su nombre ("green", "blue", ...).
    private static final Codec<PortalColor> COLOR_CODEC = Codec.STRING.flatXmap(
        name -> {
            PortalColor color = PortalColor.byName(name);
            return color != null
                ? DataResult.success(color)
                : DataResult.error(() -> "Unknown portal color: " + name);
        },
        color -> DataResult.success(color.getName())
    );

    public static final Codec<PortalReturnData> CODEC = Codec.unboundedMap(COLOR_CODEC, PLAYER_PORTAL_MAP_CODEC)
        .xmap(PortalReturnData::new, PortalReturnData::nonEmptyPortals);

    public static final SavedDataType<PortalReturnData> TYPE = new SavedDataType<>(
        Identifier.fromNamespaceAndPath(TeleportPortalsMod.MODID, "portal_return_data"),
        PortalReturnData::new,
        CODEC,
        null
    );

    private final EnumMap<PortalColor, Map<UUID, BlockPos>> portals;

    public PortalReturnData() {
        this.portals = new EnumMap<>(PortalColor.class);
    }

    private PortalReturnData(Map<PortalColor, Map<UUID, BlockPos>> portals) {
        this.portals = new EnumMap<>(PortalColor.class);
        // El mapa deserializado por el codec puede ser inmutable; copiamos
        // cada sub-mapa a un HashMap para que setLastPortalPos funcione.
        portals.forEach((color, map) -> this.portals.put(color, new HashMap<>(map)));
    }

    private Map<UUID, BlockPos> getMap(PortalColor color) {
        return portals.computeIfAbsent(color, _ -> new HashMap<>());
    }

    /**
     * @return solo las entradas con datos, para no escribir mapas vacíos en el NBT.
     */
    private Map<PortalColor, Map<UUID, BlockPos>> nonEmptyPortals() {
        Map<PortalColor, Map<UUID, BlockPos>> result = new EnumMap<>(PortalColor.class);
        portals.forEach((color, map) -> {
            if (!map.isEmpty()) {
                result.put(color, new HashMap<>(map));
            }
        });
        return result;
    }

    /**
     * @return la última posición de portal del color indicado usada por el jugador,
     *         o {@code null} si no hay ninguna guardada.
     */
    public BlockPos getLastPortalPos(PortalColor color, UUID uuid) {
        return getMap(color).get(uuid);
    }

    /**
     * Guarda la última posición de portal del color indicado para el jugador
     * y marca los datos como sucios para que se guarden en disco.
     */
    public void setLastPortalPos(PortalColor color, UUID uuid, BlockPos pos) {
        getMap(color).put(uuid, pos.immutable());
        this.setDirty();
    }

    /**
     * Borra la última posición de portal del color indicado para el jugador.
     */
    public void clearLastPortalPos(PortalColor color, UUID uuid) {
        if (getMap(color).remove(uuid) != null) {
            this.setDirty();
        }
    }

    /**
     * Obtiene (o crea) la instancia de datos persistente para el mundo dado.
     */
    public static PortalReturnData get(ServerLevel level) {
        return level.getDataStorage().computeIfAbsent(TYPE);
    }
}

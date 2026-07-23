package com.example.teleportportals.data;

import com.example.teleportportals.TeleportPortalsMod;
import com.example.teleportportals.portal.PortalColor;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.level.saveddata.SavedDataType;

import java.util.Optional;

/**
 * Datos persistentes por mundo que almacenan la posición del bloque base de un
 * color concreto del sistema de teletransporte.
 * <p>
 * Sustituye a las clases individuales {@code GreenBaseBlockData},
 * {@code BlueBaseBlockData}, etc., unificando la lógica y parametrizando el
 * identificador de guardado mediante {@link PortalColor}.
 */
public class ColorBaseBlockData extends SavedData {

    private static Codec<ColorBaseBlockData> codecFor(PortalColor color) {
        return RecordCodecBuilder.create(instance ->
            instance.group(
                BlockPos.CODEC.optionalFieldOf("base").forGetter(d -> Optional.ofNullable(d.basePos))
            ).apply(instance, opt -> new ColorBaseBlockData(color, opt.orElse(null)))
        );
    }

    /**
     * Crea el {@link SavedDataType} asociado al color indicado.
     */
    public static SavedDataType<ColorBaseBlockData> typeFor(PortalColor color) {
        return new SavedDataType<>(
            Identifier.fromNamespaceAndPath(TeleportPortalsMod.MODID, color.getName() + "_base_block"),
            ColorBaseBlockData::new,
            codecFor(color),
            null
        );
    }

    private final PortalColor color;
    private BlockPos basePos;

    private ColorBaseBlockData() {
        this(null, null);
    }

    private ColorBaseBlockData(PortalColor color, BlockPos pos) {
        this.color = color;
        this.basePos = pos;
    }

    /**
     * @return la posición de la base activa, o {@code null} si no hay ninguna.
     */
    public BlockPos getBasePos() {
        return basePos;
    }

    /**
     * Establece la posición de la base y marca los datos como sucios para que se guarden.
     */
    public void setBasePos(BlockPos pos) {
        this.basePos = pos;
        this.setDirty();
    }

    /**
     * Elimina la base guardada y marca los datos como sucios.
     */
    public void clear() {
        this.basePos = null;
        this.setDirty();
    }

    /**
     * Obtiene (o crea) la instancia de datos persistente para el mundo y color dados.
     */
    public static ColorBaseBlockData get(ServerLevel level, PortalColor color) {
        return level.getDataStorage().computeIfAbsent(color.getDataType());
    }
}

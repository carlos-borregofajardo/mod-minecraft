package com.example.teleportportals.portal;

import net.minecraft.core.BlockPos;
import net.minecraft.world.phys.Vec3;

/**
 * Helper para calcular posiciones de teletransporte de forma consistente.
 * <p>
 * Centraliza los offsets comunes (centrar al jugador en X/Z y situarlo
 * verticalmente) para evitar duplicar valores mágicos en varias clases.
 */
public final class TeleportHelper {
    private TeleportHelper() {
        // Clase de utilidad; no se instancia.
    }

    // Offset para centrar al jugador en el bloque destino.
    private static final double CENTER_OFFSET = 0.5;

    /**
     * Devuelve la posición centrada en X/Z sobre el bloque dado,
     * manteniendo la coordenada Y del bloque.
     * <p>
     * Útil para teletransportar de vuelta al portal exacto donde se encontraba el jugador.
     */
    public static Vec3 centeredAt(BlockPos pos) {
        return new Vec3(pos.getX() + CENTER_OFFSET, pos.getY(), pos.getZ() + CENTER_OFFSET);
    }

    /**
     * Devuelve la posición centrada en X/Z y situada justo encima del bloque dado.
     * <p>
     * Útil para teletransportar al jugador encima de un bloque base o portal destino.
     */
    public static Vec3 centeredAbove(BlockPos pos) {
        return new Vec3(pos.getX() + CENTER_OFFSET, pos.getY() + 1.0, pos.getZ() + CENTER_OFFSET);
    }
}

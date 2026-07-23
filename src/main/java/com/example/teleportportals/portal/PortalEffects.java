package com.example.teleportportals.portal;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;

/**
 * Efectos audiovisuales compartidos del sistema de teletransporte:
 * sonido de activación de portal y ráfaga de partículas del color dado.
 * <p>
 * Centraliza las constantes que antes estaban duplicadas en {@link PortalBlock}
 * y {@link TeleportBaseBlock}.
 */
public final class PortalEffects {
    private PortalEffects() {
        // Clase de utilidad; no se instancia.
    }

    private static final int PARTICLE_COUNT = 20;
    private static final double PARTICLE_SPREAD_XZ = 0.5;
    private static final double PARTICLE_SPREAD_Y = 1.0;
    private static final double PARTICLE_SPEED = 0.1;

    private static final float SOUND_VOLUME = 1.0F;
    private static final float SOUND_PITCH = 1.0F;

    /**
     * Reproduce el sonido de teletransporte y una ráfaga de partículas del
     * color indicado un bloque por encima de la posición dada.
     */
    public static void playTeleportEffects(ServerLevel level, PortalColor color, double x, double y, double z) {
        level.playSound(null, x, y, z, SoundEvents.PORTAL_TRIGGER, SoundSource.BLOCKS, SOUND_VOLUME, SOUND_PITCH);
        level.sendParticles(
            color.getParticle(),
            x, y + 1, z,
            PARTICLE_COUNT,
            PARTICLE_SPREAD_XZ, PARTICLE_SPREAD_Y, PARTICLE_SPREAD_XZ,
            PARTICLE_SPEED
        );
    }
}

package com.example.teleportportals.client;

import com.example.teleportportals.TeleportPortalsMod;
import com.example.teleportportals.portal.PortalColor;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RegisterParticleProvidersEvent;
import net.minecraftforge.eventbus.api.listener.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

/**
 * Registros de cliente del mod de portales y bases.
 * Solo se carga en el lado cliente ({@code value = Dist.CLIENT}).
 */
@Mod.EventBusSubscriber(modid = TeleportPortalsMod.MODID, value = Dist.CLIENT)
public final class ClientModEvents {
    private ClientModEvents() {
        // Solo eventos estáticos; no se instancia.
    }

    @SubscribeEvent
    public static void registerParticleProviders(RegisterParticleProvidersEvent event) {
        // El verde usa la partícula vanilla happy_villager; el resto, la partícula tintada del color.
        for (PortalColor color : PortalColor.values()) {
            if (color == PortalColor.GREEN) continue;
            event.registerSpriteSet(color.getParticle(), sprites -> new ColoredVillagerParticle.Provider(
                sprites, color.getParticleRed(), color.getParticleGreen(), color.getParticleBlue()
            ));
        }
    }
}

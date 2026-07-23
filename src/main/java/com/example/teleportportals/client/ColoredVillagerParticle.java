package com.example.teleportportals.client;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.SingleQuadParticle;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.util.RandomSource;

/**
 * Partícula tintada con la misma forma que la partícula happy_villager.
 * Usa el sprite "glint" de vanilla y un comportamiento flotante similar al
 * de las partículas de felicidad de los aldeanos.
 * <p>
 * Unifica las antiguas clases por color ({@code BlueVillagerParticle},
 * {@code RedVillagerParticle}, etc.): el tinte se pasa al {@link Provider}.
 */
public class ColoredVillagerParticle extends SingleQuadParticle {

    protected ColoredVillagerParticle(ClientLevel level, double x, double y, double z,
                                      double dx, double dy, double dz,
                                      TextureAtlasSprite sprite, RandomSource random,
                                      float red, float green, float blue) {
        super(level, x, y, z, dx, dy, dz, sprite);
        this.lifetime = 20 + random.nextInt(20);
        this.gravity = 0.0F;
        this.friction = 0.99F; // igual que happy_villager, movimiento muy lento
        this.setSize(0.02F, 0.02F);
        this.setColor(red, green, blue);
    }

    @Override
    public Layer getLayer() {
        return Layer.OPAQUE;
    }

    @Override
    public void move(double dx, double dy, double dz) {
        this.setBoundingBox(this.getBoundingBox().move(dx, dy, dz));
        this.setLocationFromBoundingbox();
    }

    @Override
    public void tick() {
        this.xo = this.x;
        this.yo = this.y;
        this.zo = this.z;

        if (this.lifetime-- <= 0) {
            this.remove();
            return;
        }

        this.move(this.xd, this.yd, this.zd);
        this.xd *= 0.99D;
        this.yd *= 0.99D;
        this.zd *= 0.99D;
    }

    public static class Provider implements ParticleProvider<SimpleParticleType> {
        private final SpriteSet sprites;
        private final float red;
        private final float green;
        private final float blue;

        public Provider(SpriteSet sprites, float red, float green, float blue) {
            this.sprites = sprites;
            this.red = red;
            this.green = green;
            this.blue = blue;
        }

        @Override
        public Particle createParticle(SimpleParticleType type, ClientLevel level, double x, double y, double z,
                                       double dx, double dy, double dz, RandomSource random) {
            return new ColoredVillagerParticle(level, x, y, z, dx, dy, dz, sprites.get(random), random, red, green, blue);
        }
    }
}

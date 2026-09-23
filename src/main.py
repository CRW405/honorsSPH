import numpy as np
import scipy as sp
import asyncio
import platform
from pyray import *
from typing import *

screen_width:int = 500
screen_height:int = 500
g:float = 9.81
p_size:int = 10

class Particle:
    def __init__(self, position, density, velocity, pressure, color=BLUE):
        self.position = position
        self.density = density
        self.velocity = velocity
        self.pressure = pressure
        self.color = color

global p_texture, p_source, p_origin

def create_particle_texture()->None:
    global p_texture, p_source, p_origin
    p_image = gen_image_color(1,1, WHITE)
    p_texture = load_texture_from_image(p_image)
    unload_image(p_image)
    p_source = Rectangle(0,0,1,1)
    p_origin = Vector2(0.5,0.5)

def draw_particle(particle: Particle)->None:
    draw_texture_pro(p_texture,
                     p_source,
                     Rectangle(particle.position[0] - p_size/2,
                               particle.position[1] - p_size/2,
                               p_size,
                               p_size),
                     p_origin,
                     0.0,
                     particle.color)

# Placeholder !!!!
def apply_forces(particle: Particle, dt: float)->None:
    # Apply gravity
    particle.velocity[1] += g * dt

    # Update position based on velocity
    particle.position += particle.velocity * dt

    # bounds checking
    if particle.position[1] > screen_height - p_size/2:
        particle.position[1] = screen_height - p_size/2
    if particle.position[1] < p_size/2:
        particle.position[1] = p_size/2
    if particle.position[0] > screen_width - p_size/2:
        particle.position[0] = screen_width - p_size/2


async def main():
    # setup and init
    init_window(screen_width, screen_height,"Honors SPH Fluid Sim")
    fps:int = 60
    set_target_fps(fps)
    create_particle_texture()

    test:Particle = Particle(np.array([screen_width/2, screen_height/2]),
                             1.0,
                             np.array([50.0, -25.0]),
                             1.0) # example particle

    # main loop
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)

        # this is where we do real work
        draw_text("Hello World", 200, 200, 20, BLACK)
        apply_forces(test, 1/fps)
        draw_particle(test)

        end_drawing()
        await asyncio.sleep(0)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())

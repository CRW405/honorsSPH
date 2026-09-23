import numpy as np
import scipy as sp
import asyncio
import platform
from pyray import *
from typing import *

screen_width: int = 500
screen_height: int = 500
g: float = 9.81
p_size: int = 10

p_texture: Texture2D
p_source: Rectangle
p_origin: Vector2

class Particles:
    positions: np.ndarray
    velocities: np.ndarray
    densities: np.ndarray
    pressures: np.ndarray

    def __init__(self) -> None:
        self.positions = np.empty((0, 2))
        self.velocities = np.empty((0, 2))
        self.densities = np.empty(0)
        self.pressures = np.empty(0)

    def add(self, position: np.ndarray, density: float, velocity: np.ndarray, pressure: float) -> None:
        self.positions = np.append(self.positions, position)
        self.velocities = np.append(self.velocities, velocity)
        self.densities = np.append(self.densities, density)
        self.pressures = np.append(self.pressures, pressure)

    def create_random_particles(self, amount: int) -> None:
        self.positions = np.random.rand(amount, 2) * np.array([screen_width, screen_height])
        self.velocities = np.zeros((amount, 2))
        self.densities = np.zeros(amount)
        self.pressures = np.zeros(amount)

    def render(self) -> None:
        for i in range(len(self.positions)):
            draw_texture_pro(p_texture,
                             p_source,
                             Rectangle(self.positions[i][0] - p_size / 2,
                                       self.positions[i][1] - p_size / 2,
                                       p_size,
                                       p_size),
                             p_origin,
                             0.0,
                             WHITE)


def create_particle_texture() -> None:
    global p_texture, p_source, p_origin
    p_image: Image = gen_image_color(1, 1, WHITE)
    p_texture = load_texture_from_image(p_image)
    unload_image(p_image)
    p_source = Rectangle(0, 0, 1, 1)
    p_origin = Vector2(0.5, 0.5)

# def draw_particle(particle: Particle) -> None:
#     draw_texture_pro(p_texture,
#                      p_source,
#                      Rectangle(particle.position[0] - p_size / 2,
#                                particle.position[1] - p_size / 2,
#                                p_size,
#                                p_size),
#                      p_origin,
#                      0.0,
#                      particle.color)

target_fps: int = 60
speedup:float = 1.0 # I didnt wanna wait to see my results
random_partcle_amount: int = 10000

async def main() -> None:
    # setup and init
    init_window(screen_width, screen_height, "Honors SPH Fluid Sim")
    set_window_size(screen_width, screen_height)
    set_target_fps(target_fps)

    create_particle_texture()

    particles = Particles()
    particles.create_random_particles(random_partcle_amount)

    # main loop
    while not window_should_close():
        dt: float = get_frame_time() * speedup
        begin_drawing()
        clear_background(WHITE)

        # this is where we do real work
        draw_text("Hello World", 200, 200, 20, BLACK)
        particles.render()

        draw_text(f"FPS: {get_fps()}", 10, 10, 20, BLACK)
        end_drawing()
        await asyncio.sleep(0)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())

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

def create_particle_texture() -> None:
    global p_texture, p_source, p_origin
    p_image: Image = gen_image_color(1, 1, WHITE)
    p_texture = load_texture_from_image(p_image)
    unload_image(p_image)
    p_source = Rectangle(0, 0, 1, 1)
    p_origin = Vector2(0.5, 0.5)

class Particles:
    positions: np.ndarray
    velocities: np.ndarray
    densities: np.ndarray
    pressures: np.ndarray
    color: Color

    def __init__(self, color:Color=BLUE) -> None:
        self.positions = np.empty((0, 2))
        self.velocities = np.empty((0, 2))
        self.densities = np.empty(0)
        self.pressures = np.empty(0)
        self.color = color

    def add(self, position: np.ndarray, velocity: np.ndarray, density: float, pressure: float) -> None:
        self.positions = np.vstack([self.positions, position])
        self.velocities = np.vstack([self.velocities, velocity])
        self.densities = np.append(self.densities, density)
        self.pressures = np.append(self.pressures, pressure)

    def create_random_particles(self, amount: int) -> None:
        self.positions = np.random.rand(amount, 2) * np.array([screen_width, screen_height])
        self.velocities = np.random.rand(amount, 2) * 50 - 25
        self.densities = np.zeros(amount)
        self.pressures = np.zeros(amount)

    # Placeholder !!! Poor Performnace
    def render_textures(self) -> None:
        for i in range(len(self.positions)):
            draw_texture_pro(p_texture,
                             p_source,
                             Rectangle(self.positions[i][0] - p_size / 2,
                                       self.positions[i][1] - p_size / 2,
                                       p_size,
                                       p_size),
                             p_origin,
                             0.0,
                             self.color)

    # Placeholder !!!
    def update(self, dt: float) -> None:
        self.velocities[:, 1] += g * dt

        self.positions += self.velocities * dt

        # floor collision
        floor = self.positions[:, 1] > screen_height - p_size / 2
        self.positions[floor, 1] = screen_height - p_size / 2
        self.velocities[floor, 1] *= -0.5  # bounce

        # ceiling collision
        ceiling = self.positions[:, 1] < p_size / 2
        self.positions[ceiling, 1] = p_size / 2
        self.velocities[ceiling, 1] *= -0.5

        # right wall collision
        right = self.positions[:, 0] > screen_width - p_size / 2
        self.positions[right, 0] = screen_width - p_size / 2
        self.velocities[right, 0] *= -0.5

        # left wall collision
        left = self.positions[:, 0] < p_size / 2
        self.positions[left, 0] = p_size / 2
        self.velocities[left, 0] *= -0.5

def spawn(particle_system: Particles, position: np.ndarray, velocity: np.ndarray, density: float, pressure: float) -> None:
    particle_system.add(position, velocity, density, pressure)

target_fps: int = 60
speedup:float = 1.0
random_partcle_amount: int = 1000

async def main() -> None:
    # setup and init
    init_window(screen_width, screen_height, "Honors SPH Fluid Sim")
    set_window_size(screen_width, screen_height)
    set_target_fps(target_fps)

    create_particle_texture()

    particles = Particles(color=BLUE)
    particles.create_random_particles(random_partcle_amount)

    single = Particles(color=RED)
    single.add(np.array([[screen_width / 2, screen_height / 2]]),
               np.array([10.0, 10.0]),
               1.0,
               1.0)

    placeable = Particles(color=GREEN)

    # main loop
    while not window_should_close():
        dt: float = get_frame_time() * speedup
        begin_drawing()
        clear_background(WHITE)

        # this is where we do real work
        draw_text("Hello World", 200, 200, 20, BLACK)
        particles.update(dt)
        particles.render_textures()
        single.update(dt)
        single.render_textures()

        if is_mouse_button_down(MOUSE_BUTTON_LEFT):
            mouse_pos = np.array([get_mouse_x(), get_mouse_y()])
            spawn(placeable, mouse_pos, np.array([0.0, 0.0]), 1.0, 1.0)
        placeable.update(dt)
        placeable.render_textures()

        p_count = len(particles.positions) + len(single.positions) + len(placeable.positions)
        draw_text(f"Particle Count: {p_count}", 10, 30, 20, BLACK)

        draw_text(f"FPS: {get_fps()}", 10, 10, 20, BLACK)
        end_drawing()
        await asyncio.sleep(0)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())

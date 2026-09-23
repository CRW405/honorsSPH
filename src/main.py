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

class Particle:
    def __init__(self, position: np.ndarray, density: float,
                 velocity: np.ndarray, pressure: float,
                 color: Color = BLUE) -> None:
        self.position: np.ndarray = position
        self.density: float = density
        self.velocity: np.ndarray = velocity
        self.pressure: float = pressure
        self.color: Color = color

def create_particle_texture() -> None:
    global p_texture, p_source, p_origin
    p_image: Image = gen_image_color(1, 1, WHITE)
    p_texture = load_texture_from_image(p_image)
    unload_image(p_image)
    p_source = Rectangle(0, 0, 1, 1)
    p_origin = Vector2(0.5, 0.5)

def draw_particle(particle: Particle) -> None:
    draw_texture_pro(p_texture,
                     p_source,
                     Rectangle(particle.position[0] - p_size / 2,
                               particle.position[1] - p_size / 2,
                               p_size,
                               p_size),
                     p_origin,
                     0.0,
                     particle.color)

# Placeholder !!!!
def apply_forces(particle: Particle, dt: float) -> None:
    particle.velocity[1] += g * dt

    particle.position += particle.velocity * dt

    if particle.position[1] > screen_height - p_size / 2:
        particle.position[1] = screen_height - p_size / 2
        particle.velocity[1] *= -0.5  # bounce

    if particle.position[1] < p_size / 2:
        particle.position[1] = p_size / 2
        particle.velocity[1] *= -0.5

    if particle.position[0] > screen_width - p_size / 2:
        particle.position[0] = screen_width - p_size / 2
        particle.velocity[0] *= -0.5

    if particle.position[0] < p_size / 2:
        particle.position[0] = p_size / 2
        particle.velocity[0] *= -0.5

def create_random_particles(num_particles: int) -> List[Particle]:
    particles: List[Particle] = []
    for _ in range(num_particles):
        position: np.ndarray = np.array([np.random.uniform(0, screen_width),
                                         np.random.uniform(0, screen_height)])
        density: float = 1.0
        velocity: np.ndarray = np.array([np.random.uniform(-50, 50),
                                         np.random.uniform(-50, 50)])
        pressure: float = 1.0
        color: Color = RED
        particles.append(Particle(position, density, velocity, pressure, color))
    return particles

target_fps: int = 60
speedup:float = 1.0 # I didnt wanna wait to see my results
random_partcle_amount: int = 10000

async def main() -> None:
    # setup and init
    init_window(screen_width, screen_height, "Honors SPH Fluid Sim")
    set_window_size(screen_width, screen_height)
    set_target_fps(target_fps)
    create_particle_texture()

    # some particle tests
    test: Particle = Particle(np.array([screen_width / 2, screen_height / 2]),
                              1.0,
                              np.array([50.0, -25.0]),
                              1.0)  # example particle
    test_many: List[Particle] = create_random_particles(random_partcle_amount)  # example many particles

    # main loop
    while not window_should_close():
        dt: float = get_frame_time() * speedup
        begin_drawing()
        clear_background(WHITE)

        # this is where we do real work
        draw_text("Hello World", 200, 200, 20, BLACK)
        [apply_forces(p, dt) for p in test_many]
        [draw_particle(p) for p in test_many]
        apply_forces(test, dt)
        draw_particle(test)

        draw_text(f"FPS: {get_fps()}", 10, 10, 20, BLACK)
        end_drawing()
        await asyncio.sleep(0)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())

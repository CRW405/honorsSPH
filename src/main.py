import numpy as np
import scipy as sp
import asyncio
import platform
from pyray import *
from typing import *

screen_width: int = 500
screen_height: int = 500

# Fluid behavior will change based off density, fluidity, and velocity
# g: float = (2 * screen_height) / 0.8**2
g: float = 9.81 * 10
p_size: int = 10

p_texture: Texture2D
p_source: Rectangle
p_origin: Vector2

# If we want, we can find an actual image but I didt wanna do that so I created one dynamically
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
    color: Color # We can turn this into some sort of index -> color map later on if we want per particle colors

    # initialize empty arrays for position, velocity, density, pressure, and color
    def __init__(self, color:Color=BLUE) -> None:
        self.positions = np.empty((0, 2))
        self.velocities = np.empty((0, 2))
        self.densities = np.empty(0)
        self.pressures = np.empty(0)
        self.pressure_forces = np.empty((0, 2))
        self.color = color

    def add(self, position: np.ndarray, velocity: np.ndarray, density: float, pressure: float) -> None:
        self.positions = np.vstack([self.positions, position])
        self.velocities = np.vstack([self.velocities, velocity])
        self.densities = np.append(self.densities, density)
        self.pressures = np.append(self.pressures, pressure)

    def remove(self, index: int) -> None:
        self.positions = np.delete(self.positions, index, axis=0)
        self.velocities = np.delete(self.velocities, index, axis=0)
        self.densities = np.delete(self.densities, index)
        self.pressures = np.delete(self.pressures, index)

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

    # Density calculations made here
    def density(self, smoothing_radius: float, mass: float = 1.0) -> None:
            # deal with empty particle system 
            if len(self.positions) == 0:
                self.densities = np.empty(0)
                return

            self.densities = np.zeros(len(self.positions))

            # build spatial tree using all current positons of the particles
            tree = sp.spatial.cKDTree(self.positions)

            # find neighbors for every particle 
            for i in range(len(self.positions)):
                neighbors = tree.query_ball_point(self.positions[i], smoothing_radius)

                # calculate distance (r) between particle (i) and each neighbor
                density_sum = 0.0
                for neighbor_idx in neighbors:
                    neighbor_pos = self.positions[neighbor_idx]
                    # gets distance (r) from the position index and its neighbor position 
                    r = np.linalg.norm(self.positions[i] - neighbor_pos)

                    # condition linear smoothing kernel weight 
                    if r < smoothing_radius:
                        weight = 1.0 - (r / smoothing_radius)
                        density_sum += mass * weight

                self.densities[i] = density_sum
                
            # test to see if density has been implemented
            # print(f"Sample Densities: {self.densities[:5]}")

    '''
    p = k * (rho_{i} - rho{0}) 
    where k is the stiffness constant / imcompressable the fluid is 
    rho_{i} = self.densities
    rho_{0} = inital density
    '''
    def pressure(self, rho_initial: float = 30.0, k: float = 200.0):
        self.pressures = k * (self.densities - rho_initial)
        # clamp negative pressure to 0 since fluids don't pull 
        self.pressures = np.maximum(self.pressures, 0.0)
        return 

    def pressure_force(self, smoothing_radius):
        # deal with empty particle system 
        if len(self.positions) == 0:
            self.densities = np.empty((0, 2))
            return

        self.pressure_forces = np.zeros((len(self.positions), 2))

        # build spatial tree using all current positons of the particles
        tree = sp.spatial.cKDTree(self.positions)

        for particle_idx in range(len(self.positions)):
            neighbors = tree.query_ball_point(self.positions[particle_idx], smoothing_radius)

            # calculate neighbors 
            pressure_sum = np.zeros(2)
            for neighbor_idx in neighbors:
                neighbor_pos = self.positions[neighbor_idx]

                # setup for neighbor particles and the pressure it'll between each other
                pressure_i = self.pressures[particle_idx]
                pressure_j = self.pressures[neighbor_idx]

                r_ij = neighbor_pos - self.positions[particle_idx]
                r = np.linalg.norm(neighbor_pos - self.positions[particle_idx])

                if r > 0:
                    push_particle = r_ij / r 
                    pressure_sum += ((pressure_i + pressure_j) * (1.0 - r / smoothing_radius)) * push_particle

            self.pressure_forces[particle_idx] = pressure_sum


    # Placeholder !!!
    def update(self, dt: float) -> None:
        if len(self.positions) == 0:
            return
        # calculate density function first thing every frame
        self.density(smoothing_radius = 20.0)

        # calculate pressure using density
        self.pressure()

        # calculate forces from particles' neighbors
        self.pressure_force(smoothing_radius = 20.0)

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

        accelerations = np.zeros_like(self.velocities)
        accelerations[:, 1] = g

        safe_densities = np.maximum(self.densities, 1.0)
        accelerations += self.pressure_forces / safe_densities[:, np.newaxis]
        
        # update velocities using acceleration
        self.velocities += accelerations * dt

        # update positions using velocity
        self.positions += self.velocities * dt



def spawn(particle_system: Particles, position: np.ndarray, velocity: np.ndarray, density: float, pressure: float) -> None:
    particle_system.add(position, velocity, density, pressure)

target_fps: int = 60
speedup:float = 1.0

async def main() -> None:
    # setup and init
    init_window(screen_width, screen_height, "Honors SPH Fluid Sim")
    set_window_size(screen_width, screen_height)
    set_target_fps(target_fps)

    create_particle_texture()

    # In the final version, we will obviously only have one particle system, this is for testing
    random_partcle_amount: int = 1000
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
        draw_text("", 200, 200, 20, BLACK)
        particles.update(dt)
        particles.render_textures()
        single.update(dt)
        single.render_textures()

        if is_mouse_button_down(MOUSE_BUTTON_LEFT):
            mouse_pos = np.array([get_mouse_x(), get_mouse_y()])
            spawn(placeable, mouse_pos, np.array([0.0, 0.0]), 1.0, 1.0)
        placeable.update(dt)
        placeable.render_textures()

        # Technically a performance hit, we should create a global variable and update on actual add and remove but this is python so we hate performace
        p_count = len(particles.positions) + len(single.positions) + len(placeable.positions)
        draw_text(f"Particle Count: {p_count}", 10, 30, 20, BLACK)

        draw_text(f"FPS: {get_fps()}", 10, 10, 20, BLACK)
        end_drawing()
        await asyncio.sleep(0)
    close_window()

if __name__ == "__main__":
    asyncio.run(main())

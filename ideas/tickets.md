# Potential Git Issue Tickets

**Due Date: Week of Decemeber 7, 2026** 

This is what I had in mine for potential tasks that we will have throughout the next 2-3 months in order to complete this project. **Everything listed under each month needs to be completed before we move on the next month.**


## September
1. Research: 
    * Density, fluidity, and pressure
    * How 2D fluid sims work
    * Learn how to use `raylib` in Python 
    * *Bonus:* look into how `scipy.spatial.cKDTree` function works

2. Create/brainstorm features and tasks for this project
    * Create SMART tasks so that each these features are attainable within a short amount of time
    * More tickets completed = more dopamine + motivation to complete more tickets (hopefully)

3. Convert said features / tasks into Git issue tickets 

4. Set up basic coding environment
    * Create folders for assets, class attributes, etc. 

> *Note: Step 1 is independent and 2-4 will be done together in a meeting*

## October

> **Goal:** \
    1. Set up window to display particles and give them basic functionality \
    2. Particles fall downwards and stay in the `raylib` window / stop on the floor

1. Setup window for displaying everything
    * Create `main.py`

2. Create the rectangle container that holds all the particles so that they don't fall off the screen
    * **Done** when container is visible on screen  

3. Create `particle` class 
    * *Requirements:* position, velocity, radius, and color of particle 
    * **Done** when you can manually add 1 particle and see it at a fixed spot 

4. Implement `gravity`
    * Particles accelerate downward each frame

5. `spawn` function that places N amount of particles in container 
    * distance between each of them
    * **Done** when 20-50 particles fall without overlapping each other

6. `collision` function that closes off the floor of the container
    * **Done** when particles stop at the container floor 

7. Research `scipy.spatial.cKDTree` function and create a test script 
    * prints neighbor counrs for a small hardcoded set of points
    * **Done** when test script matches neighbor amount



## November

>**Goal** \
    1. Particles behave like liquid  
    (Spread and settling, not stacking like) \
    2. Mouse spawning works 

1. Create `smoothing_kernal` function 
    * takes in distance and returns weight
    * **Done** when you're able to plot / print its output and confirm that it's 0 at distance `h` and largest at distance 0 

2. Connect `cKDTree` test script from Oct.7 into actual particle system
    * used to find real neighbors for each particle
    * **Dones** when you can print the IDs of all its neightbors for the chosen particle

3. Implement `density_calc` per particle using the kernal and neighbors
    * **Done** when hand calculations for small amount of particles matches with program calculation output

4. Implement `pressure` 
    * push from high to low pressure
    * **Done** when a single tight clamp of particles visibly spreads apart after spawning

5. Combine `gravity` (Oct.4) + `pressure` (Nov.4) + `collision` (Oct.6) 
    * **Done** when particles poured into container and spread across the floor like fluid

6. Adjust kernal radius `h`, pressure stiffness constant, and timestep size until the pool from Nov.7 is stable 
    * **Done** when there are no glitches (jittering / explosions) 

7. **Mouse Interactivity** 
    * allow user to click/drag to spawn particles at the cursor 
    * **Done** when clicking anywhere inside the container adds particles that fall into the fluid

8. **UI** 
    * Add basic on-screen controls for user 
        * sliders to adjust density, fluidity, etc
    * **Done** when adjusting it visibly changes fluid behavior in real time


> *Note: HackOKC can potentially slow us down the first week*


## Decemeber 

> **Goal:**  
    Get ready for ***DEMO DAY!!!***

1. Debug + catch up on anything missed 
2. Create presentation on concept before demoing app
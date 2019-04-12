# Boid-Simulation

This is my recreation of Boids, the artificial life emulator by Craig Reynolds. The idea is to explore emergent behaviours stemming from a simple set of rules. 

## The Rules

- Separation: steer to avoid local boids
- Alignment: steer towards the average aim of local boids
- Cohesion: steer to move towards the average position of local boids

## My additions

- Obstacles: boids avoid all objects, not just other boids
- Species: species form their own flocks, which interact and avoid one another
- Predators: special boids that hunt and kill other boids

My goal was to add new features without adding too much complexity, and for the most part, I think I succeeded. The behaviours we see are emergent, and honestly, it's pretty fun to just watch them go. 
# Boid-Simulation

This is a fun exploration of emergent behaviors from a very simple ruleset, inspired by some very peculiar behavior in my Ants project. The rules of Boids are as follows: 

1. Separation - avoid crowding local boids
2. Alignment - aim towards the average direction of local boids
3. Cohesion - move towards the center of local boids

Once this working model is complete, I have plans to add some more logic to the boids, such as avoiding all objects (not just local boids), as well as interacting with boids of a different flock (species). The intent here is to expand the rules to make more sense without adding unreasonable complexity, as the goal is for behaviours to *emerge*, not to be *programmed*. 

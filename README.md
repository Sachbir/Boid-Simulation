# Boid-Simulation

This is my recreation of Boids, the artificial life emulator by Craig Reynolds. The idea is to explore emergent behaviours stemming from a simple set of rules. 

Boids follow 3 basic rules: 

- Separation: steer to avoid local boids
- Alignment: steer towards the average aim of local boids
- Cohesion: steer to move towards the average position of local boids

As of now, I've completed the simulation as it was originally outlined, and even expanded on it. I've added obstacle avoidance, and different species that interact with one another, all without significantly altering the simplicity of the system. 

The only other thing I'd like to add is a predator-prey dynamic. I think it'd be interesting to see how the flocks would react in response. I'm thinking I could give predators a speed advantage but prey a turning advantage, which may give them a fighting chance. 
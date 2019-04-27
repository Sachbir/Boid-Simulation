class Chunk:

    def __init__(self):

        self.boids = []
        self.predators = []
        self.entities = []

    def add_boid(self, boid):
        self.boids.append(boid)

    def add_predator(self, predator):
        self.predators.append(predator)

    def add_entity(self, entity):
        self.entities.append(entity)

    def get_entities(self, entity_type):

        if entity_type == "boids":
            return self.boids
        elif entity_type == "predators":
            return self.predators
        elif entity_type == "entities":
            return self.entities

        raise ValueError(entity_type + " is not a valid entity type")

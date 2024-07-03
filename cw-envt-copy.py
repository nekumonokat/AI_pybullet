# USED FOR MIDTERM
import numpy as np
import math, random, time
import pybullet as p
import pybullet_data
import creature, genome

p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

def make_mountain(num_rocks = 100, max_size = 0.25, arena_size = 10, mountain_height = 5):
    def gaussian(x, y, sigma = arena_size/4):
        """Return the height of the mountain at position (x, y) using a Gaussian function."""
        return mountain_height * math.exp(-((x**2 + y**2) / (2 * sigma**2)))

    for _ in range(num_rocks):
        x = random.uniform(-1 * arena_size/2, arena_size/2)
        y = random.uniform(-1 * arena_size/2, arena_size/2)
        z = gaussian(x, y)  # Height determined by the Gaussian function

        # Adjust the size of the rocks based on height. Higher rocks (closer to the peak) will be smaller.
        size_factor = 1 - (z / mountain_height)
        size = random.uniform(0.1, max_size) * size_factor

        orientation = p.getQuaternionFromEuler([random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)])
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents = [size, size, size])
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents = [size, size, size], rgbaColor = [0.5, 0.5, 0.5, 1])
        rock_body = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = rock_shape, baseVisualShapeIndex = rock_visual, basePosition = [x, y, z], baseOrientation = orientation)

def make_rocks(num_rocks = 100, max_size = 0.25, arena_size = 10):
    for _ in range(num_rocks):
        x = random.uniform(-1 * arena_size/2, arena_size/2)
        y = random.uniform(-1 * arena_size/2, arena_size/2)
        z = 0.5  # Adjust based on your needs
        size = random.uniform(0.1,max_size)
        orientation = p.getQuaternionFromEuler([random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14)])
        rock_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents = [size, size, size])
        rock_visual = p.createVisualShape(p.GEOM_BOX, halfExtents = [size, size, size], rgbaColor = [0.5, 0.5, 0.5, 1])
        rock_body = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = rock_shape, baseVisualShapeIndex = rock_visual, basePosition = [x, y, z], baseOrientation = orientation)

def make_arena(arena_size = 10, wall_height = 1):
    wall_thickness = 0.5
    floor_collision_shape = p.createCollisionShape(shapeType = p.GEOM_BOX, halfExtents = [arena_size/2, arena_size/2, wall_thickness])
    floor_visual_shape = p.createVisualShape(shapeType = p.GEOM_BOX, halfExtents = [arena_size/2, arena_size/2, wall_thickness], rgbaColor = [1, 1, 0, 1])
    floor_body = p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = floor_collision_shape, baseVisualShapeIndex = floor_visual_shape, basePosition = [0, 0, -wall_thickness])

    wall_collision_shape = p.createCollisionShape(shapeType = p.GEOM_BOX, halfExtents = [arena_size/2, wall_thickness/2, wall_height/2])
    wall_visual_shape = p.createVisualShape(shapeType = p.GEOM_BOX, halfExtents = [arena_size/2, wall_thickness/2, wall_height/2], rgbaColor = [0.7, 0.7, 0.7, 1])  # Gray walls

    # Create four walls
    p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = wall_collision_shape, baseVisualShapeIndex = wall_visual_shape, basePosition = [0, arena_size/2, wall_height/2])
    p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = wall_collision_shape, baseVisualShapeIndex = wall_visual_shape, basePosition = [0, -arena_size/2, wall_height/2])

    wall_collision_shape = p.createCollisionShape(shapeType = p.GEOM_BOX, halfExtents = [wall_thickness/2, arena_size/2, wall_height/2])
    wall_visual_shape = p.createVisualShape(shapeType = p.GEOM_BOX, halfExtents = [wall_thickness/2, arena_size/2, wall_height/2], rgbaColor = [0.7, 0.7, 0.7, 1])  # Gray walls

    p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = wall_collision_shape, baseVisualShapeIndex = wall_visual_shape, basePosition = [arena_size/2, 0, wall_height/2])
    p.createMultiBody(baseMass = 0, baseCollisionShapeIndex = wall_collision_shape, baseVisualShapeIndex = wall_visual_shape, basePosition = [-arena_size/2, 0, wall_height/2])

p.setGravity(0, 0, -10)

arena_size = 20
make_arena(arena_size = arena_size)
#make_rocks(arena_size = arena_size)

mountain_position = (0, 0, -1)  # Adjust as needed
mountain_orientation = p.getQuaternionFromEuler((0, 0, 0))
p.setAdditionalSearchPath('shapes/')

# mountain = p.loadURDF("mountain.urdf", mountain_position, mountain_orientation, useFixedBase = 1)
# mountain = p.loadURDF("mountain_with_cubes.urdf", mountain_position, mountain_orientation, useFixedBase = 1)
mountain = p.loadURDF("gaussian_pyramid.urdf", mountain_position, mountain_orientation, useFixedBase = 1)

# HYPERPARAMETER TUNING: (same as test_ga)
gene_count = 10
render = 25
scale = 0.1

c = creature.Creature(gene_count = gene_count)
dna = genome.Genome.from_csv(str(render) + "_elite.csv")
c.set_dna(dna)

# save it to XML
with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

# load it into the sim
cid = p.loadURDF('test.urdf', (10, 0, 5))
c.update_position([0, 0, 0])
m_pos, m_orn = p.getBasePositionAndOrientation(mountain)
p.resetDebugVisualizerCamera(15, 20, 200, m_pos)

target_pos = np.array([0.5, 0, 4])
# # creating visual box to find the position of mountain
# target_box_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents = [0.1, 0.1, 0.1])
# target_box = p.createMultiBody(target_box_shape, target_box_shape, basePosition = target_pos)

p.setRealTimeSimulation(1)

# keeps simulation running
while True:
    for jid in range(p.getNumJoints(cid)):
        m = c.get_motors()[jid]
        # controlling each motor
        p.setJointMotorControl2(cid, jid,
                                controlMode = p.VELOCITY_CONTROL, 
                                targetVelocity = m.get_output(), force = 5)
        
    # checking that youre getting distance travelled
    pos, orn = p.getBasePositionAndOrientation(cid)
    c.update_position(pos)
    # dist = c.get_distance_travelled()
    # print(dist)

    # calculate the direction to the target
    direction = target_pos - np.array(pos)
    dist_to_target = np.linalg.norm(direction)
    print("distance to target:", dist_to_target)
    # normalising direction vector
    direction_norm = direction / dist_to_target
    # applying force towards the target
    force = direction_norm * scale
    p.applyExternalForce(cid, linkIndex = -1, forceObj = force, posObj = pos, flags = p.WORLD_FRAME)

    p.stepSimulation()
    time.sleep(0.1)
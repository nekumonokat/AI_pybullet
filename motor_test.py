# NOT UNIT TESTING
import pybullet as p
import time
import creature

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching = 0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0, 0, -10) # x, z, y

c = creature.Creature(gene_count = 5)
with open("test.urdf", "w") as f:
    c.get_expanded_links()
    f.write(c.to_xml())

cid = p.loadURDF("test.urdf")
p.setRealTimeSimulation(1)
p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1])
c.update_position([0, 0, 0])

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
    print(c.get_distance_travelled())

    p.stepSimulation()
    time.sleep(0.1)
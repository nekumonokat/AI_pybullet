import pybullet as p
import time
import creature

p.connect(p.DIRECT)
p.setPhysicsEngineParameter(enableFileCaching = 0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
p.setGravity(0, 0, -10) # x, z, y
p.setRealTimeSimulation(1)

# generating random creature
cr = creature.Creature(gene_count = 4)
# save to XML
with open("test.urdf", "w") as f:
    f.write(cr.to_xml())
# load into the simulation
cid = p.loadURDF("test.urdf")
p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1])
cr.update_position([0, 0, 0])

frame_counter = 0
total_frames = 2400 # at 240Hz, that's 10 seconds

for frame in range(total_frames):
    p.stepSimulation()

    if frame % 24 == 0:
        for jid in range(p.getNumJoints(cid)):
            m = cr.get_motors()[jid]
            p.setJointMotorControl2(cid, jid,
                                    controlMode = p.VELOCITY_CONTROL,
                                    targetVelocity = m.get_output())
        
        pos, orn = p.getBasePositionAndOrientation(cid)
        cr.update_position(pos)
        print(cr.get_distance_travelled())
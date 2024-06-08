import pybullet as p
import time

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching = 0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)
c = p.loadURDF("test.urdf")
p.resetBasePositionAndOrientation(c, [0, 0, 5], [0, 0, 0, 1])

p.setGravity(0, 0, -10) # x, z, y
p.setRealTimeSimulation(1)

# keeps simulation running
while True:
    p.stepSimulation()
    time.sleep(1/240)
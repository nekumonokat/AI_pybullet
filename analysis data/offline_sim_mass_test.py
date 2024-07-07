# USED FOR MIDTERM
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

gene_count = 8
masses = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
summary_file = "mass_test_summary.txt"

with open(summary_file, "w") as sumf:
    for run in range(10):
        for mass in masses:
            try:
                cr = creature.Creature(gene_count, 0.5, 0.7, mass)

                # save to XML
                with open("test.urdf", "w") as f:
                    f.write(cr.to_xml())

                # load into the simulation
                cid = p.loadURDF("test.urdf")
                p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1])
                cr.update_position([0, 0, 0])

                frame_counter = 0
                total_frames = 2400 # at 240Hz, that's 10 seconds
                avg_dist = 0
                count = 0

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
                        avg_dist += cr.get_distance_travelled()
                        count += 1

                sumf.write(f"run: {run+1} mass: {mass} average_dist: {avg_dist/count}\n")
                print(f"run: {run+1} mass: {mass} average_dist: {avg_dist/count}")
            
            except:
                pass

            sumf.write("")
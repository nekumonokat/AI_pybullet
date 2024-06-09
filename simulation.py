import pybullet as p

class Simulation():
    def __init__(self):
        self.physicsClientId = p.connect(p.DIRECT)

    def run_creature(self, cr, iterations = 2400):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId = pid)
        p.setGravity(0, 0, -10, physicsClientId = pid)

        xml_file = "temp.urdf"
        xml_str = cr.to_xml()

        with open(xml_file, "w") as f:
            f.write(xml_str)

        cid = p.loadURDF(xml_file, physicsClientId = pid)

        # stepping through simulation
        for step in range(iterations):
            p.stepSimulation(physicsClientId = pid)
            if step % 24 == 0:
                self.update_motors(cid, cr)
            
            # updating the position
            pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId = pid)
            cr.update_position(pos)

    def update_motors(self, cid, cr):
        """
        cid is the id in the physics engine
        cr is a creature object
        """

        # get iterate through each joint and controlling the motors
        for jid in range(p.getNumJoints(cid,physicsClientId = self.physicsClientId)):
            m = cr.get_motors()[jid]
            p.setJointMotorControl2(cid, jid,
                                    controlMode = p.VELOCITY_CONTROL,
                                    targetVelocity = m.get_output(), force = 5,
                                    physicsClientId = self.physicsClientId)
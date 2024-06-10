import pybullet as p
from multiprocessing import Pool

class Simulation():
    def __init__(self, sim_id = 0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr, iterations = 2400):
        # highly recursive creatures crash pybullet
        try:
            pid = self.physicsClientId
            p.resetSimulation(physicsClientId = pid)
            p.setGravity(0, 0, -10, physicsClientId = pid)
            p.setPhysicsEngineParameter(enableFileCaching = 0, physicsClientId = pid)

            floor_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId = pid)
            floor = p.createMultiBody(floor_shape, floor_shape, physicsClientId = pid)

            xml_file = "temp" + str(self.sim_id) + ".urdf"
            xml_str = cr.to_xml()

            with open(xml_file, "w") as f:
                f.write(xml_str)

            cid = p.loadURDF(xml_file, physicsClientId = pid)
            p.resetBasePositionAndOrientation(cid, [0, 0, 2.5], [0, 0, 0, 1], physicsClientId = pid)

            # stepping through simulation
            for step in range(iterations):
                p.stepSimulation(physicsClientId = pid)
                if step % 24 == 0:
                    self.update_motors(cid, cr)
                
                # updating the position
                pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId = pid)
                cr.update_position(pos)
        except:
            print("sim failed cr links:", len(cr.get_expanded_links()))

    def update_motors(self, cid, cr):
        """
        cid is the id in the physics engine
        cr is a creature object
        """

        # get iterate through each joint and controlling the motors
        for jid in range(p.getNumJoints(cid, physicsClientId = self.physicsClientId)):

            m = cr.get_motors()[jid]
            p.setJointMotorControl2(cid, jid,
                                    controlMode = p.VELOCITY_CONTROL,
                                    targetVelocity = m.get_output(), force = 5,
                                    physicsClientId = self.physicsClientId)
            
    def eval_population(self, pop, iterations):
        for cr in pop.creatures:
            self.run_creature(cr, 2400)

# doesn't work on windows
class ThreadedSim():
    def __init__(self, pool_size):
        self.sims = [Simulation(i) for i in range(pool_size)]

    @staticmethod
    def static_run_creature(sim, cr, iterations):
        sim.run_creature(cr, iterations)
        return cr
    
    def eval_population(self, pop, iterations):
        pool_args = [] # stores sets of sets of arguments
        start_idx = 0 # allows for double iteration
        pool_size = len(self.sims)

        while start_idx < len(pop.creatures):
            this_pool_args = []
            for i in range(start_idx, start_idx + pool_size):
                if i == len(pop.creatures): # the end
                    break

                # works out sim_idx
                sim_idx = 1 % len(self.sims)
                print("eval_pop: c idx", start_idx, ", sim_idx", sim_idx)

                this_pool_args.append([
                    self.sims[sim_idx],
                    pop.creatures[i],
                    iterations
                ])
            
            pool_args.append(this_pool_args)
            start_idx += pool_size

        new_creatures = []
        for pool_argset in pool_args:
            with Pool(pool_size) as p:
                # works on a copy of the creatures
                creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
                # print("Got", len(creatures), "from starmap type of 0 is", type(creatures))
                new_creatures.extend(creatures)
        for cr in new_creatures:
            print(cr.get_distance_travelled())
        pop.creatures = new_creatures
import unittest
import simulation
import creature
import os
import population

class TestSimulation(unittest.TestCase):
    def testSimulationExists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)

    def testSimID(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.physicsClientId)

    def testRun(self):
        sim = simulation.Simulation()
        # cr = creature.Creature(gene_count = 3)
        self.assertIsNotNone(sim.run_creature)

    # ensures creature is written to disc
    def testRunXML(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        self.assertTrue(os.path.exists("temp.urdf"))

    # checking that creature position has changed
    def testPosChanged(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        # print(cr.start_position, cr.last_position)
        self.assertNotEqual(cr.start_position, cr.last_position)

    def testDistChanged(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        dist = cr.get_distance_travelled()
        print("distance travelled:", dist)
        self.assertGreater(dist, 0)

    def testPop(self):
        pop = population.Population(pop_size = 10, gene_count = 4)
        sim = simulation.Simulation()

        for cr in pop.creatures:
            sim.run_creature(cr)

        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

unittest.main()
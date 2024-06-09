import unittest
import simulation
import creature
import os

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

unittest.main()
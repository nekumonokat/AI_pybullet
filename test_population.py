import unittest
import population

class TestPopulation(unittest.TestCase):
    def testPopulationExists(self):
        pop = population.Population(pop_size = 10, gene_count = 4)
        self.assertIsNotNone(pop)

    def testPopHasIndivs(self):
        pop = population.Population(pop_size = 10, gene_count = 4)
        self.assertEqual(len(pop.creatures), 10)

unittest.main()
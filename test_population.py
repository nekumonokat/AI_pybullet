import unittest
import population

class TestPopulation(unittest.TestCase):
    def testPopulationExists(self):
        pop = population.Population(pop_size = 10, gene_count = 4)
        self.assertIsNotNone(pop)

    def testPopHasIndivs(self):
        pop = population.Population(pop_size = 10, gene_count = 4)
        self.assertEqual(len(pop.creatures), 10)

    def testFitmap(self):
        fits = [2.5, 1.2, 3.4]
        want = [2.5, 3.7, 7.1]
        fitmap = population.Population.get_fitness_map(fits)
        self.assertEqual(fitmap, want)

    def testSelectParent(self):
        fits = [2.5, 1.2, 3.4]
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertLess(pid, 3)

    def testSelectParent2(self):
        fits = [0, 1000, 0.1] # highly likely to be idx 1
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertEqual(pid, 1)

unittest.main()
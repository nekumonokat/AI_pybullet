import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np

class TestGA(unittest.TestCase):
    def testGA(self):
        pop = poplib.Population(pop_size = 10, gene_count = 3)
        sim = simlib.Simulation()

        for generation in range(10):
            sim.eval_population(pop, 2400)
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            fitmap = poplib.Population.get_fitness_map(fits)
            print("gen:", generation, "max:", np.max(fits), "mean:", np.mean(fits))
            
            # keeping the fittest creature (elitism)
            fmax = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == fmax:
                    elite = cr
                    break
            
            new_gen = []
            for cid in range(len(pop.creatures)):
                p1_idx = poplib.Population.select_parent(fitmap)
                p2_idx = poplib.Population.select_parent(fitmap)

                # conducting crossover
                dna = genlib.Genome.crossover(pop.creatures[p1_idx].dna,
                                            pop.creatures[p2_idx].dna)
                
                # conducting mutations
                dna = genlib.Genome.point_mutate(dna, 0.1, 0.25)
                dna = genlib.Genome.grow_mutate(dna, 0.25)
                dna = genlib.Genome.shrink_mutate(dna, 0.25)

                # creating the creature and appending into new generation
                cr = crlib.Creature(1)
                cr.set_dna(dna)
                new_gen.append(cr)
            
            new_gen[0] = elite
            csv_filename = str(generation) + "_elite.csv"
            genlib.Genome.to_csv(elite.dna, csv_filename)
            # replacing current population with new generation
            pop.creatures = new_gen

unittest.main()
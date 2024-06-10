import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as genlib
import numpy as np
import csv

class TestGA(unittest.TestCase):
    def testGA(self):

        # HYPERPARAMETER TUNING:
        pop_size = 200
        gene_count = 3
        gen_count = 10

        pop = poplib.Population(pop_size = pop_size, gene_count = gene_count)
        sim = simlib.Simulation()
        summary_file = "summary.csv"
        mid_gen_count = gen_count // 2

        with open(summary_file, "w", newline = "") as f:
            for generation in range(gen_count):
                sim.eval_population(pop, 2400)
                fits = [cr.get_distance_travelled() for cr in pop.creatures]
                fitmap = poplib.Population.get_fitness_map(fits)

                print("gen:", generation, "max:", np.max(fits), "mean:", np.mean(fits))
                fmax = np.max(fits)
                fmean = np.mean(fits)
                f.write(f"gen: {generation} max: {fmax} mean: {fmean}")
                
                # keeping the fittest creature (elitism)
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
                    cr = crlib.Creature(gene_count = gene_count)
                    cr.set_dna(dna)
                    new_gen.append(cr)
                
                new_gen[0] = elite
                # replacing current population with new generation
                pop.creatures = new_gen

                if generation in [0, mid_gen_count, gen_count-1]:
                    genlib.Genome.to_csv(elite.dna, str(generation) + "_elite.csv")

unittest.main()
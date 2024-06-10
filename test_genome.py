# contains tests for the Genome class
import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation
import os

class TestGenome(unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))
   
    def testRandomGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    # adding parameter
    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def testRandomGeneIsNumpyArray(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        dna = genome.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(dna)
    
    def testGeneSpecExists(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)
    
    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec["link-length"])

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec["link-length"]["idx"])
    
    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["idx"]], 0)

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-recurrence", gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def testFlatLinks(self):
        links = [
            genome.URDFLink(name = "A", parent_name = "None", recur = 1),
            genome.URDFLink(name = "B", parent_name = "A", recur = 1),
            genome.URDFLink(name = "C", parent_name = "B", recur = 2),
            genome.URDFLink(name = "D", parent_name = "C", recur = 1)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks(self):
        links = [
            genome.URDFLink(name = "A", parent_name = "None", recur = 1),
            genome.URDFLink(name = "B", parent_name = "A", recur = 1),
            genome.URDFLink(name = "C", parent_name = "B", recur = 2),
            genome.URDFLink(name = "D", parent_name = "C", recur = 1)
        ]

        exp_links = [links[0]] # adding root link
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links)
        # print([l.name+" parent is "+str(l.parent_name) for l in exp_links])
        self.assertEqual(len(exp_links), 6)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links), 3)

    # ensuring links have unique names
    def testGetLinksUniqueNames(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        
        for l in links:
            names = [link.name for link in links if link.name == l.name]
            self.assertEqual(len(names), 1)

    def testLinkToXML(self):
        link = genome.URDFLink(name = "A", parent_name = "None", recur = 1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_link_xml(adom)
        self.assertIsNotNone(xml_str)

    def testJointToXML(self):
        link = genome.URDFLink(name = "A", parent_name = "None", recur = 1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_joint_xml(adom)
        self.assertIsNotNone(xml_str)

    def testCrossover(self):
        g1 = np.array([[1,2,3], [4,5,6], [7,8,9]])
        g2 = np.array([[10,11,12], [13,14,15], [16,17,18]])
        g3 = genome.Genome.crossover(g1, g2)
        # print(g3)
        self.assertEqual(len(g3), len(g1))

    def testPointMutation(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        # print(g1, "(before)")
        # (rate of 1 used to confirm mutation works)
        g2 = genome.Genome.point_mutate(g1, rate = 1, amount = 0.25)
        # print(g2, "(after)")

    def testShrinkMutation(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        # print(g1, "(before)")
        # (rate of 1 used to confirm mutation works)
        g2 = genome.Genome.shrink_mutate(g1, rate = 1)
        # print(g2, "(after)")
        self.assertNotEqual(len(g1), len(g2))

    def testGrowMutation(self):
        g1 = np.array([[1.0,2.0,3.0], [4.0,5.0,6.0], [7.0,8.0,9.0]])
        # print(g1, "(before)")
        # (rate of 1 used to confirm mutation works)
        g2 = genome.Genome.grow_mutate(g1, rate = 1)
        # print(g2, "(after)")
        self.assertGreater(len(g2), len(g1))

    def testToCSV(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, "test.csv")
        self.assertTrue(os.path.exists("test.csv"))

    def testToCSVContents(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, "test.csv")
        expect = "1,2,3,\n"

        with open("test.csv") as f:
            csv_str = f.read()

        self.assertEqual(csv_str, expect)

    def testToCSVContents(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, "test.csv")
        expect = "1,2,3,\n4,5,6,\n"

        with open("test.csv") as f:
            csv_str = f.read()

        self.assertEqual(csv_str, expect)

    def testFromCSV(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, "test.csv")
        g2 = genome.Genome.from_csv("test.csv")
        self.assertTrue(np.array_equal(g1, g2))


unittest.main()
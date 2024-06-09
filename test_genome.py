# contains tests for the Genome class
import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation

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

unittest.main()
import genome
from xml.dom.minidom import getDOMImplementation

class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)

    def get_flat_links(self):
        genome_dicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
        self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links
    
    def get_expanded_links(self):
        # if its not generated, it'll generate
        self.get_flat_links()
        exp_links = [self.flat_links[0]]
        genome.Genome.expandLinks(  self.flat_links[0],
                                    self.flat_links[0].name,
                                    self.flat_links,
                                    exp_links  )
        
        # generating and storing into creature so its not static
        self.exp_links = exp_links
        return self.exp_links
    
    def to_xml(self):
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")

        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_xml(adom))

        first = True # skips the root node
        for link in self.exp_links:
            if first:
                first = False
                continue
            robot_tag.appendChild(link.to_joint_xml(adom))

        robot_tag.setAttribute("name", "creature")
        return robot_tag.toprettyxml()
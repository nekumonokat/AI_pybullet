# USED FOR MIDTERM
import numpy as np
import copy

class Genome():
    @staticmethod # just sits there
    # HYPERPARAMETER TUNING: TESTING VALUES
    def get_random_gene(length, l_len = 0.1, l_rad = 0.1):
        gene = np.array([np.random.random() for i in range(length)])
        gene[1] = l_len
        gene[2] = l_rad
        return gene
    
    @staticmethod
    def get_random_genome(gene_length, gene_count, l_len = 0.1, l_rad = 0.1):
        genome = [Genome.get_random_gene(gene_length, l_len, l_rad) for i in range(gene_count)]
        return genome
    
    @staticmethod
    def get_gene_spec():
        gene_spec = {
            "link-shape": {"scale": 1},
            "link-length": {"scale": 1},
            "link-radius": {"scale": 1},
            "link-recurrence": {"scale": 4},
            "link-mass": {"scale": 1},
            "joint-type": {"scale": 1},
            "joint-parent": {"scale": 1},
            "joint-axis-xyz": {"scale": 1},
            "joint-origin-rpy-1": {"scale": np.pi * 2},
            "joint-origin-rpy-2": {"scale": np.pi * 2},
            "joint-origin-rpy-3": {"scale": np.pi * 2},
            "joint-origin-xyz-1": {"scale": 1},
            "joint-origin-xyz-2": {"scale": 1},
            "joint-origin-xyz-3": {"scale": 1},
            "control-waveform": {"scale": 1},
            "control-amp": {"scale": 0.25},
            "control-freq": {"scale": 1}
        }

        idx = 0
        for key in gene_spec.keys():
            gene_spec[key]["idx"] = idx
            idx += 1

        return gene_spec
    
    @staticmethod
    def get_gene_dict(gene, spec):
        gene_dict = {}

        for key in spec:
            idx = spec[key]["idx"]
            scale = spec[key]["scale"]
            gene_dict[key] = gene[idx] * scale
        
        return gene_dict
    
    @staticmethod
    def get_genome_dicts(dna, spec):
        genome_dicts = []
        for gene in dna:
            genome_dicts.append(Genome.get_gene_dict(gene, spec))
        return genome_dicts
    
    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, exp_links):
        # taking the links where the link parent is the parent_link's name
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        sibling_idx = 1

        for c in children:
            for r in range(int(c.recur)):
                sibling_idx += 1
                c_copy = copy.copy(c)
                c_copy.parent_name = uniq_parent_name
                uniq_name = c_copy.name + str(len(exp_links))
                c_copy.name = uniq_name
                # ensures that there is a proper index to rotate the links
                c_copy.sibling_idx = sibling_idx
                exp_links.append(c_copy)
                assert c.parent_name != c.name, "Genome::expandLinks: link joined to itself: " + c.name + " joins " + c.parent_name 
                Genome.expandLinks(c, uniq_name, flat_links, exp_links)
    
    @staticmethod
    def genome_to_links(genome_dicts):
        # first iteration only has 1 link, 1 parent, but it can't link to itself
        links = []
        link_idx = 0
        parent_names = [str(link_idx)] # making it available as a parent

        for gdict in genome_dicts:
            # converting the dictionary into a link
            link_name = str(link_idx)
            # finding parent index and link recurrence from gdict
            parent_idx = gdict["joint-parent"] * len(parent_names)
            # ISSUE: range exceeded - solved by modulo
            parent_name = parent_names[int(parent_idx) % len(parent_names)]
            recur = gdict["link-recurrence"]

            # setting recurrence to > 0
            link = URDFLink(name = link_name, parent_name = parent_name, recur = recur+1,
                            link_length = gdict["link-length"],
                            link_radius = gdict["link-radius"],
                            link_mass = gdict["link-mass"],
                            joint_type = gdict["joint-type"],
                            joint_axis_xyz = gdict["joint-axis-xyz"],
                            joint_origin_rpy_1 = gdict["joint-origin-rpy-1"],
                            joint_origin_rpy_2 = gdict["joint-origin-rpy-2"],
                            joint_origin_rpy_3 = gdict["joint-origin-rpy-3"],
                            joint_origin_xyz_1 = gdict["joint-origin-xyz-1"],
                            joint_origin_xyz_2 = gdict["joint-origin-xyz-2"],
                            joint_origin_xyz_3 = gdict["joint-origin-xyz-3"],
                            control_waveform = gdict["control-waveform"],
                            control_amp = gdict["control-amp"],
                            control_freq = gdict["control-freq"])
            
            links.append(link)
            if link_idx != 0: # so it doesn't re-add first link
                parent_names.append(link_name)
            link_idx += 1
        
        # ensuring root link links to nothing
        links[0].parent_name = "None"
        return links
    
    @staticmethod
    def crossover(g1, g2):
        """
        g1 and g2 are raw dna data - lists of lists of floats
        """

        xo = np.random.randint(len(g1))

        if xo == 0:
            return g2
        if xo == len(g1) - 1:
            return g1
        if xo > len(g2):
            xo = len(g2) - 1

        g3 = np.concatenate((g1[:xo], g2[xo:]))
        return g3
    
    @staticmethod
    def point_mutate(dna, rate, amount):
        """
        rate: per gene how likely it is to mutate
        amount: how much it's gonna mutated by
        """
        
        for gene in dna:
            if np.random.rand() < rate:
                idx = np.random.randint(len(gene))
                # scales [-0.5 to 0.5] by the amount
                r = np.random.rand() - 0.5 * amount
                gene[idx] = gene[idx] + r
        
        return dna

    @staticmethod
    def shrink_mutate(dna, rate):
        if len(dna) == 1:
            return dna
        
        if np.random.rand() < rate:
            idx = np.random.randint(len(dna))
            dna = np.delete(dna, idx, 0)
        return dna
    
    @staticmethod
    def grow_mutate(dna, rate):
        if np.random.rand() < rate:
            new_gene = Genome.get_random_gene(len(dna[0]))
            dna = np.append(dna, [new_gene], axis = 0)
        return dna
    
    @staticmethod
    def to_csv(dna, csv_file):
        csv_str = ""

        for gene in dna:
            for value in gene:
                csv_str += str(value) + ","
            csv_str += "\n"

        with open(csv_file, "w") as f:
            f.write(csv_str)

    @staticmethod
    def from_csv(csv_file):
        csv_str = ""

        with open(csv_file) as f:
            csv_str = f.read()
        
        dna = []
        lines = csv_str.split("\n")
        for line in lines:
            vals = line.split(",")
            gene = [float(v) for v in vals if v != ""]
            if len(gene) > 0:
                dna.append(gene)

        return dna
    
class URDFLink():
    def __init__( self, name, parent_name, recur,
                #  pre-defined to prevent errors
                 link_length = 0.1, link_radius = 0.1, link_mass = 0.1,
                 joint_type = 0.1, joint_axis_xyz = 0.1,
                 joint_origin_rpy_1 = 0.1,
                 joint_origin_rpy_2 = 0.1,
                 joint_origin_rpy_3 = 0.1,
                 joint_origin_xyz_1 = 0.1,
                 joint_origin_xyz_2 = 0.1,
                 joint_origin_xyz_3 = 0.1,
                 control_waveform = 0.1, control_amp = 0.1, control_freq = 0.1 ):
        
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        # HYPERPARAMETER TUNING: LOCKING VALUES
        self.link_length = 0.5
        self.link_radius = 0.7
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq
        # to resolve geometry issue
        self.sibling_idx = 1

    def to_link_xml(self, adom):
        link_tag = adom.createElement("link")
        link_tag.setAttribute("name", self.name)
        vis_tag = adom.createElement("visual")
        geom_tag = adom.createElement("geometry")
        cyl_tag = adom.createElement("cylinder")
        cyl_tag.setAttribute("length", str(self.link_length))
        cyl_tag.setAttribute("radius", str(self.link_radius))

        geom_tag.appendChild(cyl_tag)
        vis_tag.appendChild(geom_tag)

        col_tag = adom.createElement("collision")
        c_geom_tag = adom.createElement("geometry")
        c_cyl_tag = adom.createElement("cylinder")
        c_cyl_tag.setAttribute("length", str(self.link_length))
        c_cyl_tag.setAttribute("radius", str(self.link_radius))
        
        c_geom_tag.appendChild(c_cyl_tag)
        col_tag.appendChild(c_geom_tag)

        inertial_tag = adom.createElement("inertial")
        mass_tag = adom.createElement("mass")
        # setting mass to pi * r^2 * height
        mass = np.pi * (self.link_radius * self.link_radius * self.link_length)
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = adom.createElement("inertia")
        inertia_tag.setAttribute("ixx", "0.03")
        inertia_tag.setAttribute("iyy", "0.03")
        inertia_tag.setAttribute("izz", "0.03")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyz", "0")

        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)
        link_tag.appendChild(vis_tag)
        link_tag.appendChild(col_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag
    
    def to_joint_xml(self, adom):
        joint_tag = adom.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)

        if self.joint_type >= 0.5:
            joint_tag.setAttribute("type", "revolute")
        else:
            joint_tag.setAttribute("type", "fixed")

        parent_tag = adom.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = adom.createElement("child")
        child_tag.setAttribute("link", self.name)
        axis_tag = adom.createElement("axis")
        
        if self.joint_axis_xyz <= 0.33:
            axis_tag.setAttribute("xyz", "1 0 0")
        elif self.joint_axis_xyz > 0.33 and self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        else:
            axis_tag.setAttribute("xyz", "0 0 1")
        
        limit_tag = adom.createElement("limit")
        # effort upper lower velocity
        limit_tag.setAttribute("effort", "1")
        limit_tag.setAttribute("lower", "0")
        limit_tag.setAttribute("upper", "1")
        limit_tag.setAttribute("velocity", "1")

        origin_tag = adom.createElement("origin")
        xyz = str(self.joint_origin_xyz_1) + " " + str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        origin_tag.setAttribute("xyz", xyz)

        # calculating angle of link based on sibling idx
        rpy1 = self.joint_origin_rpy_1 * self.sibling_idx
        rpy = str(rpy1) + " " + str(self.joint_origin_rpy_2) + " " + str(self.joint_origin_rpy_3)
        origin_tag.setAttribute("rpy", rpy)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(origin_tag)

        return joint_tag
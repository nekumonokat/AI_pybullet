import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum # makes code more readable
import numpy as np

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor:
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
            self.motor_type = MotorType.SINE

        self.amp = control_amp
        self.freq = control_freq
        self.phase = 0

    # generating periodic waveform to setup speed
    def get_output(self):
        self.phase = (self.phase + self.freq) % (np.pi * 2) # wraps back

        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1

        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)

        return output

class Creature:
    def __init__(self, gene_count, l_len = 0.1, l_rad = 0.1):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count, l_len, l_rad)
        self.flat_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def set_dna(self, dna):
        self.dna = dna
        self.flat_links = None
        self.motors = None
        self.get_flat_links()
        self.get_expanded_links()
        self.start_position = None
        self.last_position = None
        self.dist = 0

    def get_flat_links(self):
        if self.flat_links == None:
            genome_dicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
            self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links
    
    def get_expanded_links(self):
        exp_links = [self.flat_links[0]]
        genome.Genome.expandLinks(  self.flat_links[0],
                                    self.flat_links[0].name,
                                    self.flat_links,
                                    exp_links  )
        
        # generating and storing into creature so its not static
        self.exp_links = exp_links
        return self.exp_links
    
    def to_xml(self):
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
        return '<?xml version = "1.0"?>' + "\n" + robot_tag.toprettyxml()
    
    # motors should be 1 less than links
    def get_motors(self):
        if self.motors == None:
            motors = []

            for i in range(1, len(self.exp_links)):
                l = self.exp_links[i]
                m = Motor(l.control_waveform, l.control_amp, l.control_freq)
                motors.append(m)

            self.motors = motors
        return self.motors
    
    def update_position(self, pos):
        if self.start_position == None:
            self.start_position = pos
        else:
            self.last_position = pos

    def get_distance_travelled(self):
        if self.start_position is None or self.last_position is None:
            return 0
        
        pos1 = np.array(self.start_position)
        pos2 = np.array(self.last_position)
        return np.linalg.norm(pos1 - pos2)

        # return self.dist
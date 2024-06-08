import unittest
import creature
import pybullet as p

class CreatureTest(unittest.TestCase):
    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count = 4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testCreatureGetExpLinks(self):
        c = creature.Creature(gene_count = 4)
        links = c.get_flat_links()
        exp_links = c.get_expanded_links()

        # # used to debug issue of links and exp_links not syncing
        # for l in links:
        #     print("l.name:", l.name, "l.parent_name:", l.parent_name, "l.recur:", int(l.recur))
        # for e in exp_links:
        #     print("e.name:", e.name, "e.parent_name:", e.parent_name)

        self.assertGreaterEqual(len(exp_links), len(links))

    def testCreatureToXML(self):
        c = creature.Creature(gene_count = 4)
        xml_str = c.to_xml()

        # writes as a new URDF file
        with open("test.urdf", "w") as f:
            f.write('<?xml version = "1.0"?>' + "\n" + xml_str)

        # self.assertIsNotNone(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF("test.urdf")
        self.assertIsNotNone(cid)

unittest.main()
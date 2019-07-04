from ways import get_from_svg, write_graph, read_graph, find_paths
from unittest import TestCase, main


class TestGraphReading(TestCase):

    def setUp(self):
        self.svg_path = '../../Data/3этаж.svg'
        self.save_path = 'graph.bin'

    def test_get_graph(self):
        graph = get_from_svg(self.svg_path)
        self.assertEqual(len(graph.edges), len(graph.nodes) - 1)

    def test_read_graph(self):
        graph = get_from_svg(self.svg_path)
        write_graph(graph, self.save_path)
        new_graph = read_graph(self.save_path)
        assert new_graph == graph

    def test_find_path(self):
        graph = get_from_svg(self.svg_path)
        for list in find_paths(graph, graph.index_by_id('enter_g303'), graph.index_by_id('enter_v316')):
            for node in list:
                print(node.id)

    def test_find_path_with_view(self):
        graph = get_from_svg(self.svg_path)
        lines = []
        f = open(self.svg_path)
        for line in f.readlines():
            lines.append(line)
        f.close()
        nodes_code = ''
        for list in find_paths(graph, graph.index_by_id('enter_g303'), graph.index_by_id('enter_v316')):
            for node in list:
                nodes_code += '<circle\nstyle=\"display:inline;fill:#3333cc;fill-opacity:1;stroke:none;stroke-width:0' \
                              '.1\"\nr=\"0.4\"\ncy=\"' + str(node.point.y) + \
                              '\"\ncx=\"' + str(node.point.x) + '\"\nid=\"' + str(node.id) + '\" />\n'
        lines.insert(len(lines)-2, nodes_code)
        f = open('path_nodes.svg', 'w')
        for line in lines:
            f.write(line)
        f.close()


if __name__ == '__main__':
    main()

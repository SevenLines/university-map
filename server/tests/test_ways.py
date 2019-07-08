from ways import get_from_svg, write_graph, read_graph, find_paths, get_full_graph
from unittest import skip
import tests


class TestGraphReading(tests.TestCaseBase):

    def setUp(self):
        super(TestGraphReading, self).setUp()
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
        for nodes in find_paths(graph, 'enter_g303', 'enter_v316'):
            for node in nodes:
                print(node.id)

    def test_find_path_with_view(self):
        graph = get_from_svg(self.svg_path)
        lines = []
        f = open(self.svg_path)
        for line in f.readlines():
            lines.append(line)
        f.close()
        nodes_code = ''
        for nodes in find_paths(graph, 'enter_g303', 'enter_v316'):
            for node in nodes:
                nodes_code += '<circle\nstyle=\"display:inline;fill:#3333cc;fill-opacity:1;stroke:none;stroke-width:0' \
                              '.1\"\nr=\"0.4\"\ncy=\"' + str(node.point.y) + \
                              '\"\ncx=\"' + str(node.point.x) + '\"\nid=\"' + node.id + '\" />\n'
        lines.insert(len(lines) - 2, nodes_code)
        f = open('path_nodes.svg', 'w')
        for line in lines:
            f.write(line)
        f.close()

    # Найдёт 2 пути
    def test_find_path_between_floors(self):
        graph = get_full_graph(['../../Data/2этаж.svg', '../../Data/3этаж.svg'])
        paths = find_paths(graph, 'enter_v225', 'enter_v316')
        for nodes in paths:
            print('начало')
            for node in nodes:
                print(node.id)
            print('конец\n')

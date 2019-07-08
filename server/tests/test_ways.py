from ways import Graph, get_from_svg, write_graph, read_graph, find_paths, get_full_graph
from unittest import TestCase, main, skip

svg_files = ['../../Data/0этаж.svg', '../../Data/1этаж.svg', '../../Data/2этаж.svg', '../../Data/3этаж.svg']


class TestGraphReading(TestCase):
    def setUp(self):
        self.graph = [Graph([], []) for _ in range(4)]
        self.graph[2] = get_from_svg(svg_files[2])
        self.graph[3] = get_from_svg(svg_files[3])

    # Третий этаж читается из svg
    def test_get_third_floor(self):
        # assert len(graph[3].nodes) > 300
        # assert len(graph[3].edges) > 300
        print(len(self.graph[3].nodes))

    # Второй этаж читается из svg
    def test_get_second_floor(self):
        # assert len(graph[2].nodes) > 300
        # assert len(graph[2].edges) > 300
        print(len(self.graph[2].nodes))

    # Граф сохраняется и загружается
    def test_save_graph(self):
        save = 'graph.bin'
        write_graph(self.graph[3], save)
        new_graph = read_graph(save)
        self.assertEqual(new_graph, self.graph[3])

    # Поиск пути на третьем этаже
    def test_find_path3(self):
        for node in find_paths(self.graph[3], 'enter_g303', 'enter_v316'):
            print(node.id)

    # Поиск пути на втором этаже
    def test_find_path2(self):
        for node in find_paths(self.graph[2], 'enter_g203', 'enter_v216'):
            print(node.id)

    # Отрисовка пути в svg
    def test_find_path_with_view(self):
        lines = []
        f = open(svg_files[3])
        for line in f.readlines():
            lines.append(line)
        f.close()
        nodes_code = ''
        for node in find_paths(self.graph[3], 'enter_g303', 'enter_v316'):
            nodes_code += '<circle\nstyle=\"display:inline;fill:#3333cc;fill-opacity:1;stroke:none;stroke-width:0' \
                              '.1\"\nr=\"0.4\"\ncy=\"' + str(node.y) + \
                              '\"\ncx=\"' + str(node.x) + '\"\nid=\"' + node.id + '\" />\n'
        lines.insert(len(lines) - 2, nodes_code)
        f = open('path_nodes.svg', 'w')
        for line in lines:
            f.write(line)
        f.close()

    # Найдёт 2 пути
    def test_find_path_between_floors(self):
        full_graph = get_full_graph(svg_files)
        path = find_paths(full_graph, 'enter_v216', 'enter_v316')
        print('начало')
        for node in path:
            print(node.id)
        print('конец\n')


if __name__ == '__main__':
    main()

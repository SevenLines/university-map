import tests
from networkx import Graph
from ways import get_from_svg, get_full_graph, write_graph, read_graph, find_path, set_weight, get_node_by_id, get_weight


class TestGraphReading(tests.TestCaseBase):
    svg_files = ['../../Data/0этаж.svg', '../../Data/1этаж.svg', '../../Data/2этаж.svg', '../../Data/3этаж.svg']
    bin_files = ['0floor.bin', '1floor.bin', '2floor.bin', '3floor.bin']
    full_file = 'full.bin'

    @classmethod
    def setUpClass(cls):
        for i in range(4):
            write_graph(get_from_svg(cls.svg_files[i], i), cls.bin_files[i])
        write_graph(get_full_graph(cls.svg_files, [0, 1, 2, 3]), cls.full_file)

    def setUp(self):
        super(TestGraphReading, self).setUp()
        self.G = [Graph() for _ in range(4)]
        self.G[2] = read_graph(self.bin_files[2])
        self.G[3] = read_graph(self.bin_files[3])

    # Третий этаж читается из svg
    def test_get_third_floor(self):
        self.assertTrue(len(self.G[3].nodes) > 300)
        self.assertTrue(len(self.G[3].edges) > 300)

    # Второй этаж читается из svg
    def test_get_second_floor(self):
        self.assertTrue(len(self.G[2].nodes) > 300)
        self.assertTrue(len(self.G[2].edges) > 300)

    # Граф сохраняется и загружается
    def test_save_graph(self):
        save = 'graph.bin'
        write_graph(self.G[3], save)
        read_graph(save)

    # Поиск пути на третьем этаже
    def test_find_path3(self):
        print('\nначало')
        for node in find_path(self.G[3], 'enter_g303', 'enter_v316'):
            print(node.id)
        print('конец\n')

    # Поиск пути на втором этаже
    def test_find_path2(self):
        print('\nначало')
        for node in find_path(self.G[2], 'enter_g203', 'enter_v216'):
            print(node.id)
        print('конец\n')

    # Отрисовка пути в svg
    def test_find_path_with_view(self):
        lines = []
        f = open(self.svg_files[3])
        for line in f.readlines():
            lines.append(line)
        f.close()
        nodes_code = ''
        for node in find_path(self.G[3], 'enter_g303', 'enter_v316'):
            nodes_code += '<circle\nstyle=\"display:inline;fill:#3333cc;fill-opacity:1;stroke:none;stroke-width:0' \
                              '.1\"\nr=\"0.4\"\ncy=\"' + str(node.y) + \
                              '\"\ncx=\"' + str(node.x) + '\"\nid=\"' + node.id + '\" />\n'
        lines.insert(len(lines) - 2, nodes_code)
        f = open('path_nodes.svg', 'w')
        for line in lines:
            f.write(line)
        f.close()

    # Поиск пути между этажами
    def test_find_path_between_floors(self):
        full_graph = read_graph(self.full_file)
        path = find_path(full_graph, 'enter_v216', 'enter_v316')
        print('\nначало')
        for node in path:
            print(node.id)
        print('конец\n')

    # Изменение веса ребра
    def test_set_weight(self):
        for n in self.G[2].neighbors(get_node_by_id(self.G[2], 'enter_g203')):
            first_neighbor = n
            break
        old_weight = get_weight(self.G[2], 'enter_g203', first_neighbor.id)
        set_weight(self.G[2], 'enter_g203', first_neighbor.id, old_weight + 125)
        new_weight = get_weight(self.G[2], 'enter_g203', first_neighbor.id)
        self.assertEqual(new_weight, old_weight + 125)

    # Поиск пути в правом крыле 3-его этажа
    def test_find_path_3_right(self):
        print('\nначало')
        for node in find_path(self.G[3], 'enter_d304', 'enter_i303'):
            print(node.id)
        print('конец\n')
        print('\nначало')
        for node in find_path(self.G[3], 'enter_j318', 'enter_j300'):
            print(node.id)
        print('конец\n')

    # Поиск пути в правом крыле 2-ого этажа
    def test_find_path_2_right(self):
        print('\nначало')
        for node in find_path(self.G[2], 'enter_d200', 'enter_j219'):
            print(node.id)
        print('конец\n')

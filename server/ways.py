from xml.dom.minidom import parseString
import pickle
import math
import networkx as nx
from networkx import Graph


class Point(object):
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


class Node(object):
    def __init__(self, id: str, point: Point, floor: int):
        self.__id = str(id)
        self.__point = point
        self.__floor = floor

    def __eq__(self, other):
        return self.point == other.point and self.id == other.id

    def __hash__(self):
        return hash(self.id + str(self.x) + str(self.y) + str(self.floor))

    @property
    def point(self):
        return self.__point

    @property
    def x(self):
        return self.__point.x

    @property
    def y(self):
        return self.__point.y

    @property
    def floor(self):
        return self.__floor

    @property
    def id(self):
        return self.__id


def get_from_svg(path: str, floor: int) -> Graph:
    G = Graph()

    try:
        file = open(path)
        svg = parseString(file.read())
        file.close()
    except FileNotFoundError as _:
        return G

    ways_layer = None
    for g in svg.getElementsByTagName('g'):
        if g.getAttribute('id') == 'ways_layer':
            ways_layer = g
            break

    if ways_layer is None:
        return G

    nodes: [Node] = get_vertex(ways_layer, floor)

    for path in ways_layer.getElementsByTagName('path'):
        d = path.getAttribute('d')
        points = d.split(" ")
        x1 = float(points[1].split(",")[0])
        y1 = float(points[1].split(",")[1])

        if points[0] == 'M':
            if len(points) == 3:
                x2 = float(points[2].split(",")[0])
                y2 = float(points[2].split(",")[1])
            else:
                if points[2] == 'V':
                    x2 = x1
                    y2 = float(points[3])
                elif points[2] == 'H':
                    x2 = float(points[3])
                    y2 = y1

        elif points[0] == 'm':
            if len(points) == 3:
                x2 = x1 + float(points[2].split(",")[0])
                y2 = y1 + float(points[2].split(",")[1])
            else:
                if points[2] == 'v':
                    x2 = x1
                    y2 = y1 + float(points[3])
                elif points[2] == 'h':
                    x2 = x1 + float(points[3])
                    y2 = y1

        first_point = Point(x1, y1)
        second_point = Point(x2, y2)
        first = Node(str(first_point), first_point, floor)
        second = Node(str(second_point), second_point, floor)

        found = False
        for node in nodes:
            if is_near(node.point, first.point):
                first = node
                found = True
                break
        if not found:
            nodes.append(first)

        found = False
        for node in nodes:
            if is_near(node.point, second.point):
                second = node
                found = True
                break
        if not found:
            nodes.append(second)

        G.add_node(first, label=first.id)
        G.add_node(second, label=second.id)
        G.add_edge(first, second, weight=distance(first.point, second.point))

    return G


def get_vertex(scope, floor: int) -> [Node]:
    vertex = []
    for circle in scope.getElementsByTagName('circle'):
        x = circle.getAttribute('cx')
        y = circle.getAttribute('cy')
        id = circle.getAttribute('id')
        vertex.append(Node(id, Point(x, y), floor))
    return vertex


def is_near(first: Point, second: Point):
    z = distance(first, second)
    if math.sqrt(z) < 0.5:
        return True
    else:
        return False


def distance(first: Point, second: Point):
    return (first.x - second.x) ** 2 + (first.y - second.y) ** 2


def read_graph(path: str) -> Graph:
    file = open(path, 'rb')
    graph = pickle.load(file)
    file.close()
    return graph


def write_graph(graph: Graph, path: str):
    file = open(path, 'wb')
    pickle.dump(graph, file)
    file.close()


def get_full_graph(paths: [str], floors: [int]) -> Graph:
    """
    Возвращает объединённый из svg файлов граф. Этажи соединены лестницами.
    Порядок номеров этажей должен совпадать с порядком этажей в svg файлах.

    :param paths: Список svg файлов
    :param floors: Список номеров этажей.
    :return:
    """
    G = Graph()
    for i in range(len(paths)):
        G = nx.union(G, get_from_svg(paths[i], floors[i]))
    for letter in ['a', 'b', 'v', 'g', 'd', 'e', 'j']:
        for floor in floors:
            first = get_node_by_id(G, 'stairs_' + letter + '_' + str(floor) + '_start')
            second = get_node_by_id(G, 'stairs_' + letter + '_' + str(floor + 1) + '_start')
            if first is not None and second is not None:
                G.add_edge(first, second)
            first = get_node_by_id(G, 'stairs_' + letter + '_' + str(floor) + '_end')
            second = get_node_by_id(G, 'stairs_' + letter + '_' + str(floor + 1) + '_end')
            if first is not None and second is not None:
                G.add_edge(first, second)
    return G


def get_node_by_id(G: Graph, id: str) -> Node:
    for node in G.nodes:
        if node.id == id:
            return node


def find_path(G: Graph, start_id: str, end_id: str) -> [Node]:
    """
    Находит кратчайший путь между двумя узлами графа.

    :param G: Граф
    :param start_id: id начального узла
    :param end_id:  id конечного узла
    :return: Список узлов, через которые проходит путь.
    """
    start = get_node_by_id(G, start_id)
    end = get_node_by_id(G, end_id)
    if start is None or end is None:
        return None
    return nx.bidirectional_shortest_path(G, start, end)


def set_weight(G: Graph, first_id: str, second_id: str, weight):
    G[get_node_by_id(G, first_id)][get_node_by_id(G, second_id)]['weight'] = weight


def get_weight(G: Graph, first_id: str, second_id: str):
    return G[get_node_by_id(G, first_id)][get_node_by_id(G, second_id)]['weight']

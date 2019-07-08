from xml.dom.minidom import parseString
import pickle
import math


class Point(object):
    def __init__(self, x, y):
        self.__x__ = float(x)
        self.__y__ = float(y)

    def __eq__(self, other):
        return self.__x__ == other.__x__ and self.__y__ == other.__y__

    def x(self):
        return self.__x__

    def y(self):
        return self.__y__


class Node(object):
    def __init__(self, id: str, point: Point):
        self.id = str(id)
        self.__point__ = point

    def __eq__(self, other):
        return self.__point__ == other.__point__ and self.id == other.id

    def x(self):
        return self.__point__.x()

    def y(self):
        return self.__point__.y()


class Edge(object):
    def __init__(self, first: Node, second: Node):
        self.first = first
        self.second = second

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second


class Graph(object):
    def __init__(self, nodes: [Node], edges: [Edge]):
        self.nodes: [Node] = nodes
        self.edges: [Edge] = edges

    def __eq__(self, other):
        if len(self.nodes) != len(other.nodes):
            return False
        if len(self.edges) != len(other.edges):
            return False
        for i in range(len(self.nodes)):
            if self.nodes[i] != other.nodes[i]:
                return False
        for i in range(len(self.edges)):
            if self.edges[i] != other.edges[i]:
                return False
        return True

    def index_of_node(self, node: Node):
        for i in range(len(self.nodes)):
            if self.nodes[i] == node:
                return i

    def index_by_id(self, id: str):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == id:
                return i

    def node_by_id(self, id: str) -> Node:
        for node in self.nodes:
            if node.id == id:
                return node

    def rel_list(self):
        rel_list = [[]]
        for i in range(len(self.nodes)):
            if i > 0:
                rel_list.append([])
            for j in range(len(self.edges)):
                if self.nodes[i] == self.edges[j].first:
                    rel_list[i].append(self.index_of_node(self.edges[j].second))
                elif self.nodes[i] == self.edges[j].second:
                    rel_list[i].append(self.index_of_node(self.edges[j].first))
        return rel_list

    def join(self, graph):
        nodes = self.nodes.copy()
        edges = self.edges.copy()
        for edge in graph.edges:
            edges.append(edge)
        for node in graph.nodes:
            nodes.append(node)
        return Graph(nodes, edges)

    def add_edge(self, first_id: str, second_id: str):
        first = self.node_by_id(first_id)
        second = self.node_by_id(second_id)
        if first is not None and second is not None:
            edge = Edge(first, second)
            self.edges.append(edge)
            # print("Ребро:", first_id, '->', second_id)


def get_from_svg(path: str) -> Graph:
    try:
        file = open(path)
        svg = parseString(file.read())
        file.close()
    except FileNotFoundError as _:
        return Graph([], [])

    global ways_layer
    for g in svg.getElementsByTagName('g'):
        if g.getAttribute('id') == 'ways_layer':
            ways_layer = g
            break

    if ways_layer is None:
        return Graph([], [])

    edges: [Edge] = []
    nodes: [Node] = get_vertex(ways_layer)

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
        first = Node(str(first_point), first_point)
        second = Node(str(second_point), second_point)

        found = False
        for node in nodes:
            if is_near(node.__point__, first.__point__):
                first = node
                found = True
                break
        if not found:
            nodes.append(first)

        found = False
        for node in nodes:
            if is_near(node.__point__, second.__point__):
                second = node
                found = True
                break
        if not found:
            nodes.append(second)

        edges.append(Edge(first, second))

    return Graph(nodes, edges)


def get_vertex(scope) -> [Node]:
    vertex = []
    for circle in scope.getElementsByTagName('circle'):
        x = circle.getAttribute('cx')
        y = circle.getAttribute('cy')
        id = circle.getAttribute('id')
        vertex.append(Node(id, Point(x, y)))
    return vertex


def is_near(first: Point, second: Point):
    z = (first.x() - second.x()) ** 2 + (first.y() - second.y()) ** 2
    if math.sqrt(z) < 0.5:
        return True
    else:
        return False


def read_graph(path: str) -> Graph:
    file = open(path, 'rb')
    graph = pickle.load(file)
    file.close()
    return graph


def write_graph(graph: Graph, path: str):
    file = open(path, 'wb')
    pickle.dump(graph, file)
    file.close()


def get_full_graph(paths: [str]):
    graph = Graph([], [])
    for path in paths:
        graph = graph.join(get_from_svg(path))
    for letter in ['a', 'b', 'v', 'g', 'd', 'e', 'j']:
        for floor in range(3):
            graph.add_edge('stairs_' + letter + '_' + str(floor) + '_start',
                           'stairs_' + letter + '_' + str(floor + 1) + '_start')
            graph.add_edge('stairs_' + letter + '_' + str(floor) + '_end',
                           'stairs_' + letter + '_' + str(floor + 1) + '_end')
    return graph


def find_paths(graph: Graph, start_id, end_id) -> [Node]:
    start = graph.index_by_id(start_id)
    end = graph.index_by_id(end_id)
    rel_list = graph.rel_list()
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in set(rel_list[vertex]) - set(path):
            if next == end:
                path += [next]
                paths = []
                for i in path:
                    paths.append(graph.nodes[i])
                return paths
            else:
                stack.append((next, path + [next]))

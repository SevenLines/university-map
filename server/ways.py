from xml.dom.minidom import parseString
import math


class Point(object):
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


class Node(object):
    id = ''
    point = None

    def __init__(self, id, point):
        self.id = id
        self.point = point


class Edge(object):
    first = None
    second = None

    def __init__(self, first, second):
        self.first = first
        self.second = second


class Graph(object):
    nodes = []
    edges = []

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges


# Возвращает граф из .svg по адресу 'path'
def get_graph(path):
    file = open(path)
    svg = parseString(file.read())
    file.close()
    nodes = []
    edges = []
    auto_id = 0

    for g in svg.getElementsByTagName('g'):
        if g.getAttribute('id') == 'ways_layer':
            ways_layer = g
            break

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

        first = Node(auto_id, Point(x1, y1))
        auto_id += 1
        second = Node(auto_id, Point(x2, y2))
        auto_id += 1
        nodes.append(first)
        nodes.append(second)
        edges.append(Edge(first, second))

    graph = Graph(nodes, edges)

    vertex = get_vertex(ways_layer)

    for node in graph.nodes:
        for v in vertex:
            if is_near(node.point, v.point):
                node.id = v.id
                break

    return graph


def get_vertex(scope) -> [Node]:
    vertex = []
    for circle in scope.getElementsByTagName('circle'):
        x = circle.getAttribute('cx')
        y = circle.getAttribute('cy')
        id = circle.getAttribute('id')
        vertex.append(Node(id, Point(x, y)))
    return vertex


def is_near(first, second):
    z = (first.x - second.x)**2 + (first.y - second.y)**2
    if math.sqrt(z) < 1:  # какая погрешность?
        return True
    else:
        return False

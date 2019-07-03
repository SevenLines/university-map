from ways import get_graph
from unittest import TestCase, main


class TestGraphReading(TestCase):
    def test_get_graph(self):
        graph = get_graph("../../Data/3этаж.svg")
        self.assertTrue(len(graph.nodes) > 100)
        self.assertTrue(len(graph.edges) > 100)


if __name__ == '__main__':
    main()

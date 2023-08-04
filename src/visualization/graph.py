class Node:

    def __init__(self, uri: str):
        self.uri: str = uri

    def get_uri(self) -> str:
        return self.uri


class Predicate:

    def __init__(self, uri: str):
        self.uri: str = uri

    def get_uri(self) -> str:
        return self.uri


class Graph:

    def __init__(self):
        self.nodes: list[Node] = []
        self.edges: list[tuple[Node, Predicate, Node]] = []

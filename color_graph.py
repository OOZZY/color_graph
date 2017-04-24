#!/usr/bin/env python3

import sys

def string_array_to_int_array(string_array):
    int_array = []
    for string in string_array:
        int_array.append(int(string))
    return int_array

def parse_text(text):
    text = text.strip() # remove surrounding whitespace
    text = text.strip("()") # remove surrounding parens
    text_splits = text.split("(")

    for i in range(0, len(text_splits)):
        text_splits[i] = text_splits[i].strip()
        text_splits[i] = text_splits[i].strip("()")

    item = text_splits[0]
    item_splits = string_array_to_int_array(item.split())
    num_vertexes = item_splits[0]
    num_colors = item_splits[1]

    graph = {}
    for i in range(1, len(text_splits)):
        item = text_splits[i]
        item_splits = string_array_to_int_array(item.split())
        vertex = item_splits[0]
        connected_vertexes = set(item_splits[1:])
        graph[vertex] = connected_vertexes

    return num_vertexes, num_colors, graph

def vertexes(assignment):
    return set(assignment.keys())

class Problem(object):
    def __init__(self, num_vertexes, num_colors, graph):
        self.num_vertexes = num_vertexes
        self.num_colors = num_colors
        self.graph = graph

    def vertexes(self):
        return set(self.graph.keys())

    def assignment_is_complete(self, assignment):
        return self.vertexes() == vertexes(assignment)

    def unassigned_vertexes(self, assignment):
        return self.vertexes() - vertexes(assignment)

    def colors(self):
        return range(num_colors)

    def assignment_is_consistent(self, assignment):
        for vertex in vertexes(assignment):
            connected_vertexes = self.graph[vertex]
            for connected_vertex in connected_vertexes:
                if connected_vertex in vertexes(assignment):
                    if assignment[vertex] == assignment[connected_vertex]:
                        return False

        return True

def recursive_backtracking_search(assignment, problem):
    if problem.assignment_is_complete(assignment):
        return assignment

    unassigned_vertexes = problem.unassigned_vertexes(assignment)
    vertex = min(unassigned_vertexes)

    for color in problem.colors():
        assignment[vertex] = color
        if problem.assignment_is_consistent(assignment):
            result = recursive_backtracking_search(assignment, problem)
            if result == None:
                del assignment[vertex]
            else:
                return result

    return None


def backtracking_search(problem):
    return recursive_backtracking_search({}, problem)

text = sys.stdin.read()
num_vertexes, num_colors, graph = parse_text(text)
problem = Problem(num_vertexes, num_colors, graph)
solution = backtracking_search(problem)

print("num_vertexes:", problem.num_vertexes)
print("num_colors:", problem.num_colors)
print("graph:", problem.graph)
print("solution:", solution)

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
        adjacent_vertexes = set(item_splits[1:])
        graph[vertex] = adjacent_vertexes

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
        assert vertexes(assignment).issubset(self.vertexes())

        return self.vertexes() == vertexes(assignment)

    def unassigned_vertexes(self, assignment):
        assert vertexes(assignment).issubset(self.vertexes())

        return self.vertexes() - vertexes(assignment)

    def colors(self):
        return set(range(num_colors))

    def assignment_is_consistent(self, assignment):
        assert vertexes(assignment).issubset(self.vertexes())

        for vertex in vertexes(assignment):
            adjacent_vertexes = self.graph[vertex]
            for adjacent_vertex in adjacent_vertexes:
                if adjacent_vertex in vertexes(assignment):
                    if assignment[vertex] == assignment[adjacent_vertex]:
                        return False

        return True

    def choose_unassigned_vertex_without_heuristic(self, assignment):
        assert vertexes(assignment).issubset(self.vertexes())

        unassigned_vertexes = self.unassigned_vertexes(assignment)
        return next(iter(unassigned_vertexes))

    def remaining_colors(self, assignment, vertex):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex in unassigned_vertexes

        used_colors = set()
        adjacent_vertexes = self.graph[vertex]
        for adjacent_vertex in adjacent_vertexes:
            if adjacent_vertex in vertexes(assignment):
                used_colors.add(assignment[adjacent_vertex])

        return self.colors() - used_colors

    def num_remaining_colors(self, assignment, vertex):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex in unassigned_vertexes

        return len(self.remaining_colors(assignment, vertex))

    # Returns the number of constraints where vertex is involved with an
    # unassigned vertex.
    def num_vertex_constraints(self, assignment, vertex):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex in unassigned_vertexes

        adjacent_vertexes = self.graph[vertex]
        unassigned_adjacent_vertexes = adjacent_vertexes - vertexes(assignment)
        return len(unassigned_adjacent_vertexes)

    def vertexes_with_minimum_remaining_colors(self, assignment, vertex_set):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex_set.issubset(unassigned_vertexes)

        first = next(iter(vertex_set))
        minimum_remaining_colors = self.num_remaining_colors(assignment, first)
        vertexes_to_return = set([first])

        for vertex in vertex_set:
            num_remaining_colors = self.num_remaining_colors(assignment, vertex)

            if num_remaining_colors < minimum_remaining_colors:
                minimum_remaining_colors = num_remaining_colors
                vertexes_to_return = set([vertex])
            elif num_remaining_colors == minimum_remaining_colors:
                vertexes_to_return.add(vertex)

        return vertexes_to_return

    def vertexes_with_maximum_vertex_constraints(self, assignment, vertex_set):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex_set.issubset(unassigned_vertexes)

        first = next(iter(vertex_set))
        maximum_vertex_constraints = self.num_vertex_constraints(assignment, first)
        vertexes_to_return = set([first])

        for vertex in vertex_set:
            num_vertex_constraints = self.num_vertex_constraints(assignment, vertex)

            if num_vertex_constraints > maximum_vertex_constraints:
                maximum_vertex_constraints = num_vertex_constraints
                vertexes_to_return = set([vertex])
            elif num_vertex_constraints == maximum_vertex_constraints:
                vertexes_to_return.add(vertex)

        return vertexes_to_return

    def choose_unassigned_vertex_with_heuristic(self, assignment):
        assert vertexes(assignment).issubset(self.vertexes())

        unassigned_vertexes = self.unassigned_vertexes(assignment)
        unassigned_vertexes = self.vertexes_with_minimum_remaining_colors(
            assignment, unassigned_vertexes)
        unassigned_vertexes = self.vertexes_with_maximum_vertex_constraints(
            assignment, unassigned_vertexes)
        return next(iter(unassigned_vertexes))

    # Returns the total number of assignments that would be ruled out if
    # vertex=color was added to assignment.
    def num_color_constraints(self, assignment, vertex, color):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex in unassigned_vertexes
        assert color in self.remaining_colors(assignment, vertex)

        adjacent_vertexes = self.graph[vertex]
        unassigned_adjacent_vertexes = adjacent_vertexes - vertexes(assignment)

        # Create new assignment that includes vertex=color
        new_assignment = dict(assignment)
        new_assignment[vertex] = color
        num_constraints = 0

        for adjacent_vertex in unassigned_adjacent_vertexes:
            num_remaining_colors = self.num_remaining_colors(assignment, adjacent_vertex)
            new_num_remaining_colors = self.num_remaining_colors(new_assignment, adjacent_vertex)
            num_constraints += num_remaining_colors - new_num_remaining_colors

        return num_constraints

    def colors_with_minimum_color_constraints(self, assignment, vertex):
        assert vertexes(assignment).issubset(self.vertexes())
        unassigned_vertexes = self.unassigned_vertexes(assignment)
        assert vertex in unassigned_vertexes

        remaining_colors = self.remaining_colors(assignment, vertex)

        if not remaining_colors:
            return set()

        first = next(iter(remaining_colors))
        minimum_color_constraints = self.num_color_constraints(assignment, vertex, first)
        colors_to_return = set([first])

        for color in remaining_colors:
            num_color_constraints = self.num_color_constraints(assignment, vertex, color)

            if num_color_constraints < minimum_color_constraints:
                minimum_color_constraints = num_color_constraints
                colors_to_return = set([color])
            elif num_color_constraints == minimum_color_constraints:
                colors_to_return.add(color)

        return colors_to_return

    def recursive_backtracking_search(self, assignment):
        if self.assignment_is_complete(assignment):
            return assignment

        # vertex = self.choose_unassigned_vertex_without_heuristic(assignment)
        vertex = self.choose_unassigned_vertex_with_heuristic(assignment)

        # colors = self.colors()
        # colors = self.remaining_colors(assignment, vertex)
        colors = self.colors_with_minimum_color_constraints(assignment, vertex)

        print("chosen vertex:", vertex)
        print("chosen colors:", colors)

        for color in colors:
            print(vertex, "=", color)
            assignment[vertex] = color
            if self.assignment_is_consistent(assignment):
                result = self.recursive_backtracking_search(assignment)
                if result == None:
                    del assignment[vertex]
                else:
                    return result

        return None

    def backtracking_search(self):
        return self.recursive_backtracking_search({})

text = sys.stdin.read()
num_vertexes, num_colors, graph = parse_text(text)
problem = Problem(num_vertexes, num_colors, graph)
solution = problem.backtracking_search()

print("num_vertexes:", problem.num_vertexes)
print("num_colors:", problem.num_colors)
print("graph:", problem.graph)
print("solution:", solution)

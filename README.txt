The program is written in Python 3 and so it requires Python 3 to run.

Run program:
$ ./color_graph.py < <path-to-text-file>

The program takes input from stdin so you can use shell redirection to pass a text file to the program. The program assumes that the input text is in the format specified in the assignment.

The program outputs the problem as well as the solution. The solution is a set of assignments. Colors are represented by integers from 0 to num_colors-1.

The following are two example runs of the program:

$ ./color_graph.py < Asst2.data.txt
num_vertexes: 10
num_colors: 4
problem.graph:
1 : {2, 3, 4, 6, 7, 10}
2 : {1, 3, 4, 5, 6}
3 : {1, 2}
4 : {1, 2}
5 : {2, 6}
6 : {8, 1, 2, 5, 7}
7 : {8, 1, 10, 6, 9}
8 : {9, 6, 7}
9 : {8, 10, 7}
10 : {1, 9, 7}
solution:
1 = 0
2 = 1
3 = 2
4 = 2
5 = 0
6 = 2
7 = 1
8 = 0
9 = 2
10 = 3

$ ./color_graph.py < Asst2.data.3colors.txt
num_vertexes: 10
num_colors: 3
problem.graph:
1 : {2, 3, 4, 6, 7, 10}
2 : {1, 3, 4, 5, 6}
3 : {1, 2}
4 : {1, 2}
5 : {2, 6}
6 : {8, 1, 2, 5, 7}
7 : {8, 1, 10, 6, 9}
8 : {9, 6, 7}
9 : {8, 10, 7}
10 : {1, 9, 7}
solution:
No solution.

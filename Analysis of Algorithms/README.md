<a name="br1"></a> 

Assignment: NP-Completeness and Heuristic Algorithms

*Note: You will discuss Question 1 as part of the Group Assignment. (Check this*

*week’s Group Assignment on Canvas for details).*

**1. NP-Completeness:** Consider the Travelling Salesperson (TSP) problem that was covered in

the exploration.

Problem: Given a graph G with V vertices and E edges, determine if the graph has a TSP

solution with a cost of at most k.

Prove that the above stated problem is NP-Complete.

**2. Implement Heuristic Algorithm:**

a. Below matrix represents the distance of 5 cities from each other. Represent it in the

form of a graph

|   | A  | B  | C  | D  | E  |
|---|----|----|----|----|----|
| A | 0  | 2  | 3  | 20 | 1  |
| B | 2  | 0  | 15 | 2  | 20 |
| C | 3  | 15 | 0  | 20 | 13 |
| D | 20 | 2  | 20 | 0  | 9  |
| E | 1  | 20 | 13 | 9  | 0  |

b. Apply Nearest-neighbor heuristic to this matrix and find the approximate solution

for this matrix if it were for TSP problem.

c. What is the approximation ratio of your approximate solution?

d. Implement the nearest neighbor heuristic for TSP problem. Consider the first node

as the starting point. The input Graph is provided in the form of a 2-D matrix. Name

your function **solve\_tsp(G)**. Name your file **TSP.py**. You can assume the graph to be

fully connected.

Sample input

G: [[0,1,3,7], [1,0,2,3],[3,2,0,1], [7,3,1,0]]

Output: 11


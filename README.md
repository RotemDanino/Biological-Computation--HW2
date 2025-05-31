# Biological-Computation-HW2
Biological Computation- HW2
---

## Question 1

### Sections a, b

For sections **a** and **b**, the relevant function is:

Q1_a_b();
This function calls another function:
connected_sub_graphs(n);
The parameter n represents the number of vertices.
The function connected_sub_graphs returns a text file named Q1_output_n.txt, where n is the number of vertices.

Inside Q1_a_b, the function is called for n = 1, 2, 3, 4.

### Sections c, d
For sections c and d, the relevant function is:
Q1_c_d(int X);
The parameter X represents the time limit in hours.

The function generates an output file named Q1_cd_output.txt, which contains the maximum value of n for which the number of motifs can be computed within X hours.
It also prints to the console the computation time for each n, until the time limit is reached.

## Question 2
The relevant function for Question 2 is:
Q2();
This function receives as input a text file (with .txt extension) located in the directory from which the code is executed.
Currently, the function is called from main with the input file Q2_input.txt.
It generates an output text file named Q2_output_n.txt, where n is the number of vertices found in the input file.

How to Run
To run the code:
All function calls are made from the main function.

Currently, the following calls are active in main:

Q1_a_b()

Q2()

The call to Q1_c_d() is currently hidden (commented out) due to its long runtime.

Notes
All input and output files in this repository are the results of running the given inputs from the assignment.

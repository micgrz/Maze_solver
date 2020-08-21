# Maze solver
<h3>The external modules used in this program are:</h3>

- numpy==1.19.1
- matplotlib==3.3.0
- opencv-python==4.3.0.36

They can be found in *requirements.txt* file and should be installed before running the program. 


<h3>The program itself can be run from IDE or directly from the terminal.</h3>


<h4>Running the program from the terminal:</h4>

First of all, the user should navigate to the project's directory. Next the following command should be run:

*python3 maze_solver.py maze_solver maze_01.png*

Where *maze_01.png* is the name of the maze image that will be processed by the program.



<h4>Running the program from IDE:</h4>

The user will be asked about the name of the file (image of the maze):

*"Enter the image of maze name: "*


<h4>Then, both processes (running from IDE and terminal) look the same. They are as follows:</h4>

The user will be asked whether he/she would like to enter the coordinates of the start and finish points. 

*"Do you want to input the start and finish point coordinates?[Y/N]. Answer: "*

If yes (Y), the user will be asked following questions:

*"Enter start point x coordinate: "*

*"Enter start point y coordinate: "*

*"Enter finish point x coordinate: "*

*"Enter finish point y coordinate: "*

The input values are pixels and should be numerical.

If no (N), the program will be run with default values of start and finish points, the ones that makes processing of 4 attached mazes images possible. In case of these mazes, the start point is in top left corner (6 pixels, 4 pixels) and the finish is in the bottom right corner (image_width - 6 pixels, image_height - 4 pixels).

The program will find the solution, show it on the screen with comparison to the not solved maze, and save the plot to the file with following name: 

*solution_to_the_maze_01.png*

Where *maze_01.png* is the name of the processed file.

The file will be saved to the project's directory.

The file maze_01.png was generated via http://www.mazegenerator.net.

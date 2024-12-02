###### README FILE ######
My project is Rubik's cube

Term Project for CMU 15-112 Fundamentals of Programming (Fall 2024)
Completed: December 3, 2024

About the project:
  This project is mainly the rubiks cube solver. It uses CFOP method to solve the cube, with using Dijkstra algorithm to solve each stage of CFOP. It also has the timer mode for the practice with real cube.


It consists of 3 python files:
 1. main.py (drawing, mouse and keys events, onStep)
 2. functions.py (main functions of the project)
 3. Classes.py (classes for the project)


How to run the project:
 - run the main.py file

Customization:
  you can custom some settings in the main.py file
  In the onAppStartSettings function, you can change:
	1. number of moves of the scramble that will be generated
	2. number of time limit for each solving stage (in seconds)

Mode:
  There are 2 modes within this project:
	1. The main mode (getting the solutions)
	2. The timer mode (for practice with the actual physical cube)
  You can change the mode at the "Timer Mode" button at the right bottom of the screen

Notes:
  Finding the solution can take long time, So I set the time limit for each solving stage.
  You can change the time limit as mentioned above
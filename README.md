# Heat Equation Solver

This heat equation solver website allows the user to draw an initial heat distribution using a drawing tool and watch the heat disperse according to the heat equation. 

Access the website [here](https://lucaspavlicek.github.io/heat_equation_solver/).

## Purpose
My website showcases a past class project of mine and also has the potential to serve as an educational tool. The user can play around and see how heat disperses in their own custom scenarios, and has easy access to my own written explanation and the actual code. While there are more polished websites serving a similar purpose, this website can focus specifically on numerical methods for the heat equation. The large-sized pixels and discrete temperature values are perfect for someone learning about finite difference methods. There is plenty of room for future improvements and expansions; in fact, the heatequationsolver.py file already has code for two alternative heat equation solvers.

## How it works
### Specifications
The solver approximates 2D heat diffusion on a square according to the partial differential equation:

$$\frac{\partial U}{\partial t} = \alpha (\frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2})$$

We won't derive an analytical solution to the equation; it would not be practical to find an analytical solution to whatever whacky initial condition a user draws. Instead, we will focus on numerical approximations to the heat equation. The website uses a finite difference method, so the problem is broken down into a 64 by 64 grid. We assume Dirichlet boundary conditions, meaning that the boundary of the square is fixed at a certain temperature. In this case, the border is held at a temperature of zero. Imagine there is another ring of pixels around the canvas, and each of these pixels is held constant at temperature zero. To keep things simple, the diffusion constant, $\alpha$, the grid spacing, typically denoted $\Delta x$, and the time discretization spacing, $\Delta t$, are all set to one. Lastly, the solver approximates three hundred frames of heat flow.

### The Locally One-Dimensional (LOD) Method
The method is a clever way to utilize a 1D finite difference method to solve the heat equation in 2D. As the name might imply, we treat things one-dimensionally, one at a time, relying on a 1D finite difference approximation. This text won't go into detail about the 1D methods and instead focuses on extending the 1D methods into 2D. I used 1D Crank-Nicolson, but any 1D finite difference method should do the trick. For more information on the 1D Crank-Nicolson method, see the heat diffusion section on the [Wikipedia page](https://en.wikipedia.org/wiki/Crank%E2%80%93Nicolson_method). There is plenty of useful information available on the popular Crank-Nicolson method, as well as other methods online.

The Locally One-Dimensional method is quite simple. It essentially uses a 1D solver to simulate heat flow from left to right, and then up and down, and continues to alternate. It is a recursive method. In one iteration:
- We approximate a small iteration of heat flow going as if the grid were a bunch of one-dimensional horizontal rods that are completely insulated from each other. For each row in the grid, we simulate one iteration of a 1D heat equation solver.
- After we have simulated heat flow from left to right, we do the same thing going up and down—so we split the grid into columns insulated from each other, and simulate 1D heat flow going up and down.

The LOD method is not the most accurate method for 2D problems. Its strengths are its simplicity and computational efficiency. Each 1D iteration of Crank-Nicolson on a rod involves solving one tridiagonal system ($\mathcal{O} (n) $) where $n$ is the length of the rod. Each iteration of LOD utilizes Crank-Nicolson $2n$ times, for $n$ rows and then also $n$ columns. This gives one iteration of LOD a computational complexity of $\mathcal{O} (n^2) $. Not bad!

This specific implementation utilizes the Scipy function scipy.linalg.solve_banded() to efficiently

## Notes about the code
### Overview
The website relies on an HTML file to organize website elements, a CSS file for formatting, and a JavaScript file for interactability. That's all pretty standard, but there is also a Python script. That is because Python is better suited for numerical calculation, and it is my most proficient programming language. The website relies on the brilliant tool PyScript to run Python in the browser and allow communication between JavaScript and Python. When the user clicks the run button, the following happens:
- JavaScript saves the drawing canvas data into a variable.
- Python imports the variable from JavaScript and decodes its data into a Numpy array of temperatures, to be used as the initial condition.
- Python solves 300 iterations of heat diffusion.
- Python converts the results from a 3D array to a list of lists of lists and "shows" JavaScript.
- JavaScript receives the results and displays them in an interactive player.


...



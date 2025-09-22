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
- We approximate a small iteration of heat flow as if the grid were a bunch of one-dimensional horizontal rods that are completely insulated from each other. For each row in the grid, we simulate one iteration of a 1D heat equation solver.
- After we have simulated heat flow from left to right, we do the same thing going up and down—so we split the grid into columns insulated from each other, and simulate 1D heat flow going up and down.

The LOD method is not the most accurate method for 2D problems. Its strengths are its simplicity and computational efficiency. Each 1D iteration of Crank-Nicolson on a rod involves solving one tridiagonal system ($\mathcal{O} (n) $) where $n$ is the length of the rod. Each iteration of LOD utilizes Crank-Nicolson $2n$ times, for $n$ rows and then also $n$ columns. This gives one iteration of LOD a computational complexity of $\mathcal{O} (n^2) $. Not bad!

My implementation uses a for loop to loop through the rows and then the columns of the grid, and applies an iteration of 1D Crank-Nicolson by solving a linear system. It utilizes the Scipy function scipy.linalg.solve_banded(), which efficiently solves the tridiagonal system.

### How JavaScript and Python work together
The website relies on an HTML file to organize website elements, a CSS file for formatting, and a JavaScript file for interactability. That's all pretty standard, but there is also a Python script. That is because Python is better suited for numerical calculation, and it is my most proficient programming language. The website relies on the brilliant tool PyScript to run Python in the browser and allow communication between JavaScript and Python. When the user clicks the run button, the following happens:
- Python calls a JavaScript function that returns the drawing canvas as a variable.
- Python decodes the canvas data into a Numpy array of temperatures, to be used as the initial condition.
- Python solves 300 iterations of heat diffusion.
- Python converts the results from a 3D array to a list of lists of lists and "shows" JavaScript.
- JavaScript receives the results and displays them in an interactive player.
All of the other interactive parts of the website are handled by JavaScript.

### About the colorbar
Temperatures from 0 to 99 are assigned to colors and vice versa, with a conversion table, colortable.csv. While attempting to match the three-dimensional sRGB colors (the standard color space used by computers) to a 1D temperature value, I stumbled down a rabbit hole of colorimetry, and wanted to make my own color mapping instead of copying one. I ended up with a bit of a compromise. Here's how it was done.

It first seemed like a good idea to just use a portion of the visible color spectrum, since those colors are indexed by only one parameter, wavelength. This can't work because sRGB only covers a subset of all visible colors, and there are some colors along the visible spectrum that can't be generated by a computer monitor. Instead, the full color spectrum can be generated by three "imaginary" primary colors, called CIE X, Y, and Z. The colors visible to humans are a subset of the colors within the "span" (I'm using span loosely) of X, Y, and Z. Furthermore, sRGB colors are a further subset of colors visible to humans. The graph below illustrates this. Notice the visible colors fit within a large outer triangle formed by X, Y, and Z at (1, 0), (0, 1), and (0, 0) respectively. Also notice that the sRGB colors fit within the visible colors.

![color spaces](https://i.sstatic.net/KQ2GK.jpg)

The graph is a projection of the 3D color spaces into 2D. Remember that some of the colors shown aren't accurate, because of course a computer monitor cannot actually display all of the visible colors. I found this [Medium article](https://medium.com/hipster-color-science/a-beginners-guide-to-colorimetry-401f1830b65a) helpful. There is a lot more to it, but the point is that every spectral color (meaning the single wavelength colors of the visible color spectrum) can be generated by X, Y, and Z. I downloaded a table (ciexyz31_1.csv) of this relationship from [here](http://www.cvrl.org/), and used the linear transformation found [here](https://www.cs.rit.edu/~ncs/color/t_convert.html#RGB%20to%20XYZ%20&%20XYZ%20to%20RGB) to roughly convert to sRGB. Of course, some of the colors were lost. You might notice that there is a disproportionate amount of green in the color bar I used, for example. I also added a constant to all of the sRGB values, and cut off the ends of the visible color spectrum to get my final result. The Python code and input file I used to do this can be found in the 

## Future plans and ideas
- Add an ADI and 2D Crank-Nicolson solver and an option to pick which solver to use.
- Add an undo button for the drawer.
- Add a "how it works" and "about" tab to the website.

## Contact
I can be reached at [lucas.pavlicek@gmail.com](lucas.pavlicek@gmail.com)



...



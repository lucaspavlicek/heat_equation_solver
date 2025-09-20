# Heat Equation Solver

This heat equation solver website allows the user to draw an initial heat distribution using a drawing tool and watch the heat disperse according to the heat equation. 

link to website

## Purpose
My website showcases a past class project of mine and also has the potential to serve as an educational tool. The user can play around and see how heat disperses in their own custom scenarios, and has easy access to my own written explanation and the actual code. While there are more polished websites serving a similar purpose, this website can focus specifically on numerical methods for the heat equation. The large-sized pixels and discrete temperature values are perfect for someone learning about finite difference methods. There is plenty of room for future improvements and expansions; in fact, the heatequationsolver.py file already has code for two alternative heat equation solvers.

## How it works
### The specific problem
The solver approximates 2D heat diffusion on a square according to the partial differential equation:
```math
\frac{\partial U}{\partial t} = \alpha \(\frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2}\)
```
We assume Dirchelet boundary conditions, meaning that the boundary of the square is fixed at a certain temperature. In this case, the border is held at a temperature of zero. I divided the square into a 64 by 64 grid, and you can draw your own initial heat distribution. The solver simulates 200 iterations in time. I also kept everything unit-less to be nice and simple, and set the diffusion constant to 1. One final note, The boundary on my grid doesn't appear to be actually zero. Just imagine there was another ring of tiles all set to zero around the perimeter. My code acts as if there is.



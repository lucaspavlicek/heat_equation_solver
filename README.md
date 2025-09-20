# Heat Equation Solver

This heat equation solver website allows the user to draw an initial heat distribution using a drawing tool and watch the heat disperse according to the heat equation. 

link to website

## Purpose
My website showcases a past class project of mine and also has the potential to serve as an educational tool. The user can play around and see how heat disperses in their own custom scenarios, and has easy access to my own written explanation and the actual code. While there are more polished websites serving a similar purpose, this website can focus specifically on numerical methods for the heat equation. The large-sized pixels and discrete temperature values are perfect for someone learning about finite difference methods. There is plenty of room for future improvements and expansions; in fact, the heatequationsolver.py file already has code for two alternative heat equation solvers.

## How it works
### Specifications
The solver approximates 2D heat diffusion on a square according to the partial differential equation:

$$\frac{\partial U}{\partial t} = \alpha \big(\frac{\partial^2 U}{\partial x^2} + \frac{\partial^2 U}{\partial y^2}\big)$$

We won't derive an analytical solution to the equation; it would not be practical to find an analytical solution to whatever whacky intial condition that a user draws. Instead we will focus on numerical approximations to the heat equation. The website uses a finite difference method, so the problem is broken down into a 64 by 64 grid. We assume Dirichlet boundary conditions, meaning that the boundary of the square is fixed at a certain temperature. In this case, the border is held at a temperature of zero. Imagine there is another ring of pixels around the canvas, and each of these pixels is held constant at temperature zero. To keep things simple, the diffusion constant, $\alpha$, the grid spacing, typically denoted $\Delta x$, and the time discretization spacing, $\Delta t$, are all set to one. Lastly, the solver approximates three hundred frames of heat flow.

...



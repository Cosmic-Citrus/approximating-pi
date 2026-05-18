# Repo:    approximating-pi/mandelbrot_method


## Description


Consider a complex number $z = x + iy$ such that $f(z) = z^2 + c$ for some constant $c$. If we consider recursive map to get roots $z_{n+1} = z_n^2 + c$ where $z_0 = 1$, then there are a subset of values that constrain $z_{n+1}$ from escaping beyond a cut-off (usually $2$) to infinity. At particular points, the number of iterations can be used to approximate $\pi$. Using $c=-\frac{3}{4} + (\frac{1}{10})^n$ gives the approximation $\pi \approx (\frac{1}{10})^n \cdot number\space iterations$ to $n$ digits of precision.

![mandelbrot-zoom-into-chaos](/mandelbrot_method/output/mandelbrot_set_v2.gif)

![mandelbrot-zoom-into-abyss](/mandelbrot_method/output/mandelbrot_set-wConstant_v1.gif)



Sources:
- [youtube](https://www.youtube.com/watch?v=d0vY0CKYhPY)


## Getting Started

### Dependencies

- Python 3.9.6
- numpy == 1.26.4
- matplotlib == 3.9.4

### Executing program

- Download this repository to your local computer
  
- Modify `path_to_save_directory` in `example.py` and run
  

## Version History

- 0.1
  - Initial Release

## To-Do

- Animate trajectory of roots in Mandelbrot Set

## License

This project is licensed under the Apache License - see the LICENSE file for details.

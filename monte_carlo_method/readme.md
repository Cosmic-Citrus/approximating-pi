# Repo:    approximating-pi/monte_carlo_method


## Description


Suppose a circle of radius $r$ is inscribed inside of a square of side-length $l$. This means $2r = l$. The ratio of the areas of the circle to the square is given by $\frac{\pi r^2}{l^2} = \frac{\pi r^2}{(2r)^2} = \frac{\pi}{4}$. Using a uniform random distribution of $N$ points, the number of points inside the circle (given by $N_{circle}$) can be compared to the total number of points inside the square $N$ such that $\pi \approx 4 \cdot \frac{N_{circle}}{N_{square}}$.



![monte-carlo-tutorial](/monte_carlo_method/output/approximation_method.gif)

![monte-carlo-ensemble-accuracy](/monte_carlo_method/output/ensemble_approximation_accuracy.png)


Sources:
- [arxiv](https://arxiv.org/ftp/arxiv/papers/1909/1909.13212.pdf)
- [wikipedia](https://en.wikipedia.org/wiki/Approximations_of_pi#/media/File:Pi_monte_carlo_en.gif)


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

- Vary random seed of Monte Carlo Estimator
- Add number of trial runs to legend

## License

This project is licensed under the Apache License - see the LICENSE file for details.

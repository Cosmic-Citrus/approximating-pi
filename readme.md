# Repo:    approximating-pi

The purpose of this code is to find interesting (and sometimes unconventional) methods to approximate the value of pi ($\pi$) to high accuracy and precision.

## Description

The ratio of the circumference of a circle to its diameter is given by the constant $\pi=3.1415926536...$; this value can be approximated by a variety of methods, a few of which are implemented here.

### Mandelbrot Set

The Mandelbrot set can be computed using the equation

$z_{n+1} = z_{n}^2 + c$

where

$c = -\frac{3}{4} + i\epsilon$

$\epsilon = \left(\frac{1}{10}\right)^{n}$ 

$i \equiv \sqrt{-1}$

$n \equiv$ `number_digits`  

Starting at $z_{0}=0$, the loop terminates when $|z_{n} \geq 2|$, allowing one to obtain an estimate $\pi \approx n \epsilon$.  

#### Input

    `number_digits = 5`

#### Output

    `value_estimate = 3.1416000000`

    `relative_error_as_percentage = 0.0002338435`

#### References

* [video](https://www.youtube.com/watch?v=d0vY0CKYhPY) by Numberphile

### 1-D Collisions

An elastic collision conserves momentum and conserves energy. In terms of momentum, this means that

$m_{1}v_{1, i} + m_{2}v_{2, i} = m_{1}v_{1, f} + m_{2}v_{2, f}$

$\implies p_{1, i} + p_{2, i} = p_{1, f} + p_{2, f}$

where

$m$ is mass

$v$ is velocity

$p$ is momentum

$i$ and $f$ denote sub-scripts "initial" and "final", respectively

Suppose a block of mass $m_{1}$ is placed onto a frictionless surface and is initially not moving ($v_{1} = 0$). A wall is placed to the left of $m_{1}$, and a block of mass $m_{2}$ is placed to right of $m_{1}$; $m_{2}$ is initially moving to the left - towards $m_{1}$ - with velocity $v_{2}$ ($v_{2} < 0$).  If the mass ratio $\frac{m_{2}}{m_{1}} = 100^{n}$ (where $n \in \mathbb{Z}^{+}$), then $n$ is the total number of collisions - this includes collisions between $m_{1}$ with $m_{2}$ and collisions between $m_{1}$ with the wall; furthermore, the precision of the estimated value will be proportional to $n$. For simplicity, set $m_{1} = 1$. The loop terminates at the last collision.

#### Input

    `number_digits = 5`

#### Output

    `value_estimate = 3.1415000000`

    `relative_error_as_percentage = 0.0029492554`

#### References

* [video](https://www.youtube.com/watch?v=HEfHFsfGXjs) by 3Blue1Brown

### Monte Carlo Method

Suppose there is a circle of radius $r$ inscribed inside of a square of side-length $l$ (such that $l = 2r$). For simplicity, set $r=1$. 

The area of the square is given by

$A_{square} = l^{2}$

The area of the circle is given by

$A_{circle} = \pi r^{2}$

It follows that the ratio of the inner circle to the outer square is given by

$\frac{A_{circle}}{A_{square}} = \frac{\pi r^{2}}{l^{2}} = \frac{\pi}{4}$

Now suppose that $N$ points (where $N >> 1$) are uniformally distributed at pseudo-random within the bounds of this square, and $M$ points (where $M < N$) are counted inside the circle.

$\implies \frac{\pi}{4} \approx \frac{M}{N}$

$\implies \pi \approx \frac{4M}{N}$

One can create an ensemble by repeating this procedure over $k$ trial runs to collect statistics (such as mean and median) of the estimated value; the accuracy of the estimation should increase as $k \rightarrow \infty$.

#### Input

    `random_seed = 0`

    `number_points_total = 5000`

    `number_trials = 100`

    `radius = 1`

#### Output

    `value_estimate = 3.1416800000`

    `relative_error_as_percentage = 0.0027803226`

#### References

* [animation](https://commons.wikimedia.org/wiki/File:Pi_monte_carlo_all.gif) and accompanying Wikipedia [article](https://en.wikipedia.org/wiki/Monte_Carlo_method)

## Getting Started

### Dependencies

* Python 3.9.6
* numpy == 1.26.4

### Executing program

* Download this repository to your local computer

* Run any of the following to see that these methods actually work
  
  * `src/estimator_by_1-D_collisions.py`
  
  * `src/estimator_by_mandelbrot.py`
  
  * `src/estimator_by_monte_carlo.py`

## Version History

* 0.1
  * Initial Release

## To-Do

* add Archimedes method

* add 2-D collisions method

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

# Repo:    approximating-pi

The purpose of this code is to find interesting (and sometimes unconventional) methods to approximate the value of pi ($\pi$) to high accuracy and precision.

## Description

The ratio of the circumference of a circle to its diameter is given by the constant $\pi=3.1415926536...$; this value can be approximated by a variety of methods, including (but not limited) to:

* Mandelbrot set
  
  * The Mandelbrot set can be computed  by
        $z_{n+1} = z_{n}^2 + c$
    
        where 
    
            $c = -\frac{3}{4} + i\epsilon$
    
            $\epsilon = (\frac{1}{10})^{n}$
    
            $i \equiv \sqrt{-1}$
    
            $n \equiv$ `number_digits`
  
  * The loop terminates when $|z| \geq 2$ to obtain the estimate as 
            $\pi \approx n\epsilon$
  
  * `number_digits=5` $\implies$ `value_estimate=3.1416000000`, `relative_error_as_percentage=0.0002338435`
  
  * More information about this method can be found in [this video by Numberphile](https://www.youtube.com/watch?v=d0vY0CKYhPY)

* One-dimensional collisions
  
  * An elastic collision conserves momentum and conserves energy; in terms of momentum, this means
        $m_{1}v_{1, i} + m_{2}v_{2, i} = m_{1}v_{1, i} + m_{2}v_{2, i} \implies p_{1, i} + p_{2, i} = p_{1, f} + p_{2, f}$
        where
            subscripts $1$ and $2$ denote the object of mass $m$ and velocity $v$
            subscripts $i$ and $f$ denote the initial and final velocity $v$
            $p \equiv m v$          
  
  * Suppose that there is a block of mass $m_{1}$ that is initally not moving ($v_{1} = 0$) such that to the left of $m_{1}$ is a wall and to the right of $m_{1}$ is a block of mass $m_{2}$ moving towards the left ($v_{2} < 0$)
  
  * If  $\frac{m_{2}}{m_{1}} = 100^{n}$ where $n \in \mathbb{Z}^{+}$ (set of positive integers), then $n$ is equal to the number of collisions (between masses $m_{1}$ and $m_{2}$, and between masses $m_{1}$ or $m_{2}$ with the wall), which in turn is proportional to `number_digits` ; to keep it simple, set $m_{1} \equiv 1$
  
  * The loop terminates at the last collision
  
  * `number_digits=5`$\implies$`value_estimate=3.1415000000`,` relative_error_as_percentage=0.0029492554`
  
  * More information about this method can be found in [this video by 3Blue1Brown](https://www.youtube.com/watch?v=HEfHFsfGXjs)

* Monte-Carlo method
  
  * Place a circle of radius $r$ inscribed inside of a square of side-length $l$ (such that the diameter $2r$ of the circle is equal to the side-length of the square), and then drop $N$ uniformally distributed points at pseudo-random  within the bounds of the square and count $M$ points inside the circle
  * To keep it simple, set $r=1$ $\implies$ $l=2$; the ratio of the area of the circle to the area of the square is given by
        $\frac{\pi r^2}{l^2} = \frac{\pi}{4} \approx \frac{M}{N} \implies \pi \approx \frac{4M}{N}$
  * One can create an ensemble by repeating this procedure $k$ times to collect statistics (such as mean and median) of the estimated value; the accuracy of the estimation should increase as $k \rightarrow \infty$ 
  * `random_seed=0`, `number_points_total=5000`, `number_trials=100`, `r=1` $\implies$ `value_estimate=3.1416800000`, `relative_error_as_percentage=0.0027803226`. 

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
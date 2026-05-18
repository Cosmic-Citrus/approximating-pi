# Repo:    approximating-pi/elastic_collisions_1D_method


## Description


Consider a $1-$D system of two masses $m_1 = 1$ kg and $\frac{m_2}{m_1} = 10^{n-1}$ such that where $v_1 = 0 \frac{m}{s}$, $v_2 < 0 \frac{m}{s}$, and collisions are perfectely elastic. The momentum of the $i-$th mass is given by $p_i = m_i \cdot v_i$. Elastic collisions allow for conservation of momentum - given by $p_1 + p_2 \equiv k_1$ where $k_1$ is constant - and conservation of energy - given by $\frac{p_1^2}{2m_1} + \frac{p_2^2}{2m_2} = k_2$ where $k_2$ is constant. The number of collisions will then be an under-approximation of $\pi \approx \lfloor \frac{number \space collisions}{10^{n-1}} \rfloor$ up to $n$ digits of precision. The phase-space $p_2$ vs $p_1$ traces out an ellipse, but one can transform this ellipse into a circle by using the scaling $p_1^\prime = \sqrt{m_1} v_1$ and $p_2^\prime = \sqrt{m_2} v_2$, for which the total energy $E^\prime = \frac{(p_1^\prime)^2}{2m_1} + \frac{(p_2^\prime)^2}{2m_2} = 2r$ where $E^\prime$ is constant.

![elastic-collidions-kinematics](/elastic_collisions_1D_method/output/velocity_vs_time_v1.png)

![elastic-collisions-phase-space](/elastic_collisions_1D_method/output/phase_space_v1.gif)


Sources:
- [youtube](https://www.youtube.com/watch?v=HEfHFsfGXjs)
- [arxiv](https://arxiv.org/pdf/1901.06260.pdf)
- [3B1B](https://www.3blue1brown.com/lessons/clacks-solution)


## Getting Started

### Dependencies

- Python 3.9.6
- numpy == 1.26.4
- matplotlib == 3.9.4

### Executing program

- Download this repository to your local computer
  
- Modify `path_to_save_directory` in the `example.py` and run
  

## Version History

- 0.1
  - Initial Release

## To-Do

- Add 2-D Elastic Collisions Method
- Explore 1-D Elastic Collisions Method in base$-12$ and base$-24$

## License

This project is licensed under the Apache License - see the LICENSE file for details.

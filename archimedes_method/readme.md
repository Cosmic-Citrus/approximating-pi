# Repo:    approximating-pi/archimedes_method


## Description


Archimedes used regular $N-$sided polygons to estimate the minimum and maximum perimeters that bound the circumference of a circle. For each $N$, a polygon is inscribed inside the circle (corresponding to lower bound) and another polygon is placed on the outside of the circle (corresponding to upper bound). Each of the starting hexagons have $6$ congruent equilateral triangles. From the center of the circle, the angle bisector for each of these triangles will split each of these triangles into $2$ congruent half-triangles, such that the polygon of sides $2N$ can be inferred.


![srchimedes-tutorial](/archimedes_method/output/approximation_method.gif)

![archimedes-accuracy](/archimedes_method/output/approximation_accuracy.png)


Sources:
- [blog](https://mathscholar.org/2019/02/simple-proofs-archimedes-calculation-of-pi/)
- [blog](https://www.craig-wood.com/nick/articles/pi-archimedes/)
- [github](https://github.com/umcconnell/archimedes-pi)


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

- Update animation to better include outer polygon

## License

This project is licensed under the Apache License - see the LICENSE file for details.

# neurofinder-python

[![Travis](https://img.shields.io/travis/codeneuro/neurofinder-python.svg?style=flat-square)]()

> helper python module for neuron finding algorithms

This repository contains a module and a CLI for working with neuron finding algorithm results. It is used by the [neurofinder](https://github.com/codeneuro/neurofinder) benchmarking challenge to compare ground truth results to results from submitted algorithms.

You can use it to compare ground truth against algorithm results and load result files in standard formats, either as a command line tool, or as a module inside a python project.

## install

Install using pip

```
pip install neurofinder
```

## use as a command line tool

To evaluate a pair of results, just pass two `JSON` files as arguments

```
neurofinder evaluate a.json b.json
```

We assume the results are in the following format for spatial regions:

```
[
  {"coordinates": [[x, y], ...]}, 
  {"coordinates": [[x, y], ...]}, 
  ...
]
```

You can also pass `JSON` strings. Usually the first file will be ground truth and the second will be the result of an algorithm.

## use as a module

You can also use this module inside a Python project, for example

```python
from neurofinder import load, match

a = load('a.json')
b = load('b.json')
match(a, b)
```

## methods

This module supports both Python 2.7 and 3.4, and provides the following methods.

#### `neurofinder.load(file)`

Load regions from either a `JSON` or `MAT` file.

#### `neurofinder.match(a, b, threshold=inf)`

Match regions from `a` to `b` based on distances between their centers. Returns a list of indicies specifying, for each region in `a`, what the index of the matching region in `b` is. If `threshold` is less than `inf`, will not allow matches that exceed this distance.

#### `neurofinder.centers(a, b, threshold=inf)`

Compare centers between two sets of regions `a` and `b`. Returns two metrics, the `recall` and `precision`, which are defined as the total number of matching regions, according to the given distance `threshold`, dividing by the number of regions in `a`, or `b`, respectively.

#### `neurofinder.shapes(a, b, threshold=inf)`

Compare shapes between regions in `a` and `b` after first finding matches. For each pair of matched regions, the `overlap` and `exactness` are computed as the number of intersecting pixels divided by the number of pixels in the first, or second, region, respectively.

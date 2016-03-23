# neurofinder-python

[![Travis](https://img.shields.io/travis/codeneuro/neurofinder-python.svg?style=flat-square)]()

> helper python module for neuron finding algorithms

This repository contains a module and a CLI for working with neuron finding algorithm results. It is used by the [neurofinder](https://github.com/codeneuro/neurofinder) benchmarking challenge to compare ground truth results to results from submitted algorithms.

The included functions compute statistics on the similarities between two sets of binary spatial masks. You can use it to compare ground truth against algorithm results and load result files in standard formats, either as a command line tool, or as a module inside a python project (supports Python 2.7 and 3.4).

If you have any questions about these metrics or want to suggest others, please open an issue or submit a pull request!

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

And get this output

```
{"recall": 0.75, "exactness": 0.8333, "combined": 0.8571, "overlap": 0.85, "precision": 1.0}
```

We assume the inputs are in the following format for spatial regions:

```
[
  {"coordinates": [[x, y], ...]}, 
  {"coordinates": [[x, y], ...]}, 
  ...
]
```

See the files `a.json` and `b.json` in this repository as examples. Usually the first file will be ground truth and the second will be the result of an algorithm. You can also pass `JSON` strings. 

## use as a module

You can also use this module inside a Python project, for example

```python
from neurofinder import load, match

a = load('a.json')
b = load('b.json')
match(a, b)
```

## methods

#### `neurofinder.load(file)`

Load regions from a `JSON` file.

#### `neurofinder.match(a, b, threshold=inf)`

Match regions from `a` to `b` based on distances between their centers. Returns a list of indicies specifying, for each region in `a`, what the index of the matching region in `b` is. If `threshold` is less than `inf`, will not allow matches that exceed this distance.

#### `neurofinder.centers(a, b, threshold=inf)`

Compare centers between two sets of regions `a` and `b`. Returns two metrics, the `recall` and `precision`, which are defined as the total number of matching regions, according to the given distance `threshold`, dividing by the number of regions in `a`, or `b`, respectively.

#### `neurofinder.shapes(a, b, threshold=inf)`

Compare shapes between regions in `a` and `b` after first finding matches. For each pair of matched regions, the `overlap` and `exactness` are computed as the number of intersecting pixels divided by the number of pixels in the first, or second, region, respectively.

## metrics

Five asymmetric metrics are computed when comparing two sets of regions, all based on standard concepts from [information retrieval](https://en.wikipedia.org/wiki/Information_retrieval). Because the metrics are asymmetric, **it matters which set of regions is first or second**; by convention, we typically compare ground truth to estimated.

The first two metrics are based entirely on the central location of each region, ignoring the particular spatial structure. First, a greedy matching procedure is used to find, for each region in the first set, a unique match in the second set. Then the following metrics are computed:

- `precision` fraction of matched regions divided by the number of regions in the first set
- `recall` fraction of matched regions divided by the number of regions in the second set

A high `precision` means that most of the target regions in the first set were found in the second. A high `recall` means that few regions in the second set were identified that did not have matches in the first set.

The third metric `score` is simply a combination of the first two, using the equation 

```python
score = 2 * (recall * precision) / (recall + precision)
```

The final two metrics are based on the exact match of spatial regions. First the same matching procedure as above is used to find region pairs, then for every pair, two measures are computed

- `overlap` fraction of intersecting pixels divided by the number of pixels in the first region
- `exactness` fraction of intersecting pixels divided by the number of pixels in the second region

These are then averaged over pairs to obtain final scores.


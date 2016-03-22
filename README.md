# neurofinder-python

> python module for testing neuron finding algorithms.

This repository contains a module and a CLI for working with neuron finding algorithms. It is used by the [neurofinder](https://github.com/neurofinder) benchmarking challenge to compare ground truth results to results from submitted algorithms.

## install

Install using pip

```
pip install neurofinder
```

## use as a command line tool

To evaluate a pair of results, just pass two `JSON` files as arguments

```
neurofinder evaluate neurons1.json neurons2.json
```

You can also pass `MAT` files as one or both arguments

```
neurofinder evaluate neurons1.mat neurons2.mat
```

## use as a python module

Import the module and pass it two dictionaries

```
import neurofinder

results = neurofinder.evaluate(neurons1, neurons2)
```
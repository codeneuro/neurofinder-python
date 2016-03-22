# neurofinder-python

Python module for testing neuron finding algorithms.

## install

Install using pip

```
pip install neurofinder
```

## use as a command line tool

To evaluate a pair of results, just pass them as arguments

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

results = neurofinder.evaulator(neurons1, neurons2)
```
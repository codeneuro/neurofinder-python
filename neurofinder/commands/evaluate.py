import os
import json
import click
from .. import load, centers, shapes

@click.argument('file1', nargs=1, metavar='<file1>', required=True)
@click.argument('file2', nargs=1, metavar='<file2>', required=True)
@click.command('evaluate', short_help='compare results of two algorithms', options_metavar='<options>')
def evaluate(file1, file2):
    a = load(file1)
    b = load(file2)
    precision, recall = centers(a, b)
    overlap, exactness = shapes(a, b)
    combined = 2 * (recall * precision) / (recall + precision)
    
    result = {'combined': combined, 'overlap': overlap, 'precision': precision, 'recall': recall, 'exactness': exactness}
    print json.dumps(result)
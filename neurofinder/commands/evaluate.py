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
    
    result = {'combined': round(combined, 4), 'overlap': round(overlap, 4), 'precision': round(precision, 4), 'recall': round(recall, 4), 'exactness': round(exactness, 4)}
    print json.dumps(result)
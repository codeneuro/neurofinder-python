import os
import json
import click
from .. import load, centers, shapes

@click.argument('files', nargs=2, metavar='<files>', required=True)
@click.option('--threshold', default=5, help='threshold distance')
@click.command('evaluate', short_help='compare results of two algorithms', options_metavar='<options>')
def evaluate(files, threshold):
    a = load(files[0])
    b = load(files[1])

    recall, precision = centers(a, b, threshold=threshold)
    inclusion, exclusion = shapes(a, b, threshold=threshold)

    if recall == 0 and precision == 0:
      combined = 0
    else:
      combined = 2 * (recall * precision) / (recall + precision)
    
    result = {'combined': round(combined, 4), 'inclusion': round(inclusion, 4), 'precision': round(precision, 4), 'recall': round(recall, 4), 'exclusion': round(exclusion, 4)}
    print(json.dumps(result))
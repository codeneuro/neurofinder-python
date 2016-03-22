import os
import click

@click.command('evaluate', short_help='compare results of two algorithms', options_metavar='<options>')
def evaluate():
    print('evaluating algorithms')

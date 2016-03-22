import click

settings = dict(help_option_names=['-h', '--help'])
from .commands import evaluate

@click.group(options_metavar='', subcommand_metavar='<command>', context_settings=settings)
def cli():
    """
    Hi! This is a command line tool for comparing neuron finding algorithms.
    """
    print 'hi'

cli.add_command(evaluate)
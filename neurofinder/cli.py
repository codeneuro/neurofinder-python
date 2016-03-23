import click

settings = dict(help_option_names=['-h', '--help'])
from .commands import evaluate

@click.group(options_metavar='', subcommand_metavar='<command>', context_settings=settings)
def cli():
    """
    Hi! This is a tool for working with neuron finding algorithm results.

    Check out the list of commands to see what you can do.
    """

cli.add_command(evaluate)
#!/usr/bin/env python
import click
from .bulmaCsskrt import BulmaCsskrt
from .bootstrapCsskrt import BootstrapCsskrt


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--framework', '-f', default='bulma',
              type=click.Choice(['bulma', 'bootstrap']),
              help='Name of the framework. De')
@click.option('--pretty-print', '-p', is_flag=True)
def freshify(filename, framework, pretty_print):
    csskrter = None

    if framework == 'bootstrap':
        csskrter = BootstrapCsskrt(filename)
    elif framework == 'bulma':
        csskrter = BulmaCsskrt(filename)

    csskrter.freshify()
    csskrter.output(pretty_print)
    print()
    print("~~~ Done! ~~~~")


if __name__ == '__main__':
    freshify()


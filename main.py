import click
from bulmaCsskrt import BulmaCsskrt


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--framework', default='bulma', help='Name of the framework')
def freshify(filename, framework):
    csskrter = None

    if framework == 'bootstrap':
        raise NotImplementedError
    elif framework == 'bulma':
        csskrter = BulmaCsskrt(filename)

        csskrter.freshify()


if __name__ == '__main__':
    freshify()



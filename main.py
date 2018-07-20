import click
from bulmaCsskrrt import BulmaCsskrrt

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--framework', default='bulma', help='Name of the framework')
def freshify(filename, framework):
    csskrrter = None


    if framework == 'bootstrap':
        raise NotImplementedError
    elif framework == 'bulma':
        csskrrter = BulmaCsskrrt(filename)

    csskrrter.freshify()


if __name__ == '__main__':
    freshify()
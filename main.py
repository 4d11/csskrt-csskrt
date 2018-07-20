import click
from bulmaCsskrrt import BulmaCsskrrt

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--framework', default='bulma', help='Name of the framework')
def freshify(filename, framework):
    csskrrter = None
    f = open(filename)  # should be able to handle dirs (for later) todo
    f_data = f.read()

    if framework == 'bootstrap':
        raise NotImplementedError
    elif framework == 'bulma':
        csskrrter = BulmaCsskrrt(f_data)

    csskrrter.freshify()


if __name__ == '__main__':
    freshify()
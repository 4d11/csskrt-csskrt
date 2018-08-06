import click
from bulmaCsskrt import BulmaCsskrt
from bootstrapCsskrt import BootstrapCsskrt


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--framework', default='bulma', help='Name of the framework')
def freshify(filename, framework):
    csskrter = None

    if framework == 'bootstrap':
        csskrter = BootstrapCsskrt(filename)
    elif framework == 'bulma':
        csskrter = BulmaCsskrt(filename)
    else:
        raise Exception("Invalid framework")

    csskrter.freshify()
    print("Done!")


if __name__ == '__main__':
    freshify()



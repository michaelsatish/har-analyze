import click
import os
from click.exceptions import ClickException

from .dashboard import read_har_json, plot_har


@click.command()
@click.argument('path', type=click.Path(exists=True))
def plot(path):
    """
    Plot HTTP Archive format Timings
    :param path: Path containing HAR specs in json files
    """
    data = []
    har_files = [file for file in os.listdir(path) if file.endswith('.json')]

    if not har_files:
        raise ClickException('No Json file to process in given path')

    click.echo('***** Processing har files *****')
    for har_file in har_files:
        data.append(read_har_json(os.path.join(path, har_file), har_file))

    plot_har(data)


if __name__ == '__main__':
    plot()

import json
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from click.exceptions import ClickException

logger = logging.getLogger(__name__)


def calculate_timing(timings: dict) -> int:
    """
    Entry Time Calculation

    entry.time == entry.timings.blocked + entry.timings.dns +
    entry.timings.connect + entry.timings.send + entry.timings.wait +
    entry.timings.receive;
    """
    if not isinstance(timings, dict):
        raise ClickException('The Timings Object should be of type dict')

    total_time = 0
    for timing, time in timings.items():
        if timing == 'ssl':
            # Time required for SSL/TLS negotiation.
            # If this field is defined then the time is also included in the connect field
            continue

        if timing == 'comment':
            # A comment provided by the user or the application
            continue

        if time == -1:
            # -1 if the timing does not apply to the current request
            continue

        total_time += time

    return total_time


def read_har_json(har_file_path: str, har_filename: str) -> list:
    """
    Collect data from Har Json files
    Information collected:
    type_: request content type
    request: request method 'GET'...
    status: status code '200'...
    time: entry.time
    """
    entries = []

    with open(har_file_path) as f:
        data = json.load(f)

    try:
        for entry in data['log']['entries']:
            har_file = har_filename
            type_ = entry['response']['content']['mimeType']
            request = entry['request']['method']
            status = entry['response']['status']
            time = calculate_timing(entry['timings'])

            entries.append({
                'Har': har_file,
                'Request Content Type': type_,
                'Request Method': request,
                'Response Status': status,
                'Time': time
            })

        return entries

    except KeyError as err:
        logger.error('Error occured while processing har json files %s' % err, exc_info=True)
        ClickException('Missing Key {key} in file {filename}'.format(key=err, filename=har_filename))


def plot_har(entries: list):
    """
    Plot HTTP Archive format Timings
    """
    try:
        df = pd.DataFrame.from_records([x for y in entries for x in y])
        df = df.replace(r'^\s*$', np.nan, regex=True)
        plot_df = df.groupby('Har')[['Time']].sum()

        plot_df.plot(kind='bar', title='Time in Milliseconds')
        plt.show()

    except Exception as err:
        logger.error('Error occured while ploting data %s' % err, exc_info=True)
        ClickException('Error occured while ploting data %s' % err)

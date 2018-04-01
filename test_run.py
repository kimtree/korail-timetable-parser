import pprint
from ktp.parser import KorailTimeTableParser

parser = KorailTimeTableParser('')
parser.parse()

import csv
with open('trains.csv', 'w', newline='') as csvfile:
    trains = parser.get_trains()

    for train in trains:
        stops = train.get_stops()

        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [train.get_idx(),
             train.get_name(),
             stops[0].station_idx,
             stops[-1].station_idx,
             train.get_remarks()])

    print('DONE')

with open('stops.csv', 'w', newline='') as csvfile:
    trains = parser.get_trains()
    i = 1
    for train in trains:
        stops = train.get_stops()

        for stop in stops:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [i,
                 stop.line_name,
                 train.get_idx(),
                 stop.station_idx,
                 stop.time])
            i += 1

    print('DONE')


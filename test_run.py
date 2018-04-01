import pprint
from ktp.parser import KorailTimeTableParser

parser = KorailTimeTableParser('')
parser.parse()

trains = parser.get_trains()
for train in trains:
    pprint.pprint([train.get_idx(), train.get_name(), train.get_remarks()])
    pprint.pprint(train.get_stops())


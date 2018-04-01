import collections

# 정차역 형식
Stop = collections.namedtuple('Stop', ['station_idx', 'name', 'time'])


class Train(object):
    def __init__(self, idx, name):
        # 열차 번호
        self.idx = idx
        # 열차 종류
        self.name = name
        # 정차역 리스트
        self.stops = []
        # 비고 사항
        self.remarks = None

    def add_stops(self, stop):
        self.stops.append(stop)

    def set_remarks(self, remarks):
        self.remarks = remarks

    def get_last_stop(self):
        return self.stops[-1]

    def get_stops(self):
        return self.stops

    def get_idx(self):
        return self.idx

    def get_name(self):
        return self.name

    def get_remarks(self):
        return self.remarks

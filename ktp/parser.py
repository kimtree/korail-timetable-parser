import xlrd

from ktp.train import Train, Stop

# 열차 정보 인덱스
IDX_COL_TRAIN = (4, 42)

# 첫번쨰 정차역부터 마지막 정차역까지 컬럼의 인덱스
IDX_COL_STATIONS = (10, 51)

# 비고정보 인덱스
IDX_COL_REMAKRS = 52

# 열차정보 인덱스 (열차종별, 열차번호)
IDX_COL_TRAIN_INFO = (8, 9)

# 종착역 인덱스
IDX_COL_LAST_STATION = (53, 56)


class KorailTimeTableParser(object):
    def __init__(self, excel_filename):
        self.excel_filename = excel_filename
        self.trains = []

    def parse(self):
        with xlrd.open_workbook(self.excel_filename) as workbook:
            sheet = workbook.sheets()[2]
            print(sheet.name)

            station_name = sheet.col_slice(1, IDX_COL_STATIONS[0] - 1, IDX_COL_STATIONS[1] + 1)
            station = sheet.col_slice(2, IDX_COL_STATIONS[0] - 1, IDX_COL_STATIONS[1] + 1)

            # 열차별 loop
            for col in range(IDX_COL_TRAIN[0] - 1, IDX_COL_TRAIN[1] + 1):
                # 기본 정보
                train_info = sheet.col_slice(col, IDX_COL_TRAIN_INFO[0] - 1,
                                             IDX_COL_TRAIN_INFO[1] + 1)
                train = Train(int(train_info[1].value), train_info[0].value)

                # 정차역 정보
                stops = sheet.col_slice(col, IDX_COL_STATIONS[0] - 1, IDX_COL_STATIONS[1] + 1)
                for idx, stop in enumerate(stops):
                    if stop.value and stop.ctype == xlrd.XL_CELL_DATE:
                        time = xlrd.xldate_as_datetime(stop.value, workbook.datemode)
                        train.add_stops(
                            Stop(int(station[idx].value),
                                 station_name[idx].value,
                                 time.strftime('%H:%M')
                             )
                        )

                # 비고 정보
                remarks = sheet.col_slice(col, IDX_COL_REMAKRS - 1, IDX_COL_REMAKRS + 1)
                train.set_remarks(remarks[0].value)

                # 종착역 정보
                last_station = sheet.col_slice(col, IDX_COL_LAST_STATION[0] - 1, IDX_COL_LAST_STATION[1] + 1)
                last_station_name = last_station[0]
                last_station_time = xlrd.xldate_as_datetime(last_station[3].value, workbook.datemode)

                if train.get_last_stop().name != last_station_name.value:
                    train.add_stops(
                        Stop(999,
                             last_station_name.value,
                             last_station_time.strftime('%H:%M')
                             )
                    )

                self.trains.append(train)

    def get_trains(self):
        return self.trains

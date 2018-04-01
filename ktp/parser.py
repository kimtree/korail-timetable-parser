import xlrd

from ktp.train import Train, Stop
from ktp.parse_position import fixed_positions, positions


class KorailTimeTableParser(object):
    def __init__(self, excel_filename):
        self.excel_filename = excel_filename
        self.trains = []

    def append_train(self, train):
        for prev_train in self.trains:
            if prev_train.idx == train.idx:
                return

        self.trains.append(train)

    def parse(self):
        with xlrd.open_workbook(self.excel_filename) as workbook:
            for line_num in range(fixed_positions['IDX_EXCEL_SHEET_NUM'][0] - 1,
                                  fixed_positions['IDX_EXCEL_SHEET_NUM'][1]):
                sheet = workbook.sheets()[line_num]
                line_num -= 1

                line_name = sheet.cell_value(0, 1)
                print(sheet.cell_value(0, 1))

                # 좌측 정차역 정보 목록
                station_name = sheet.col_slice(1,
                                               positions['IDX_COL_STOPS'][line_num][0] - 1,
                                               positions['IDX_COL_STOPS'][line_num][1] + 1)
                station = sheet.col_slice(2,
                                          positions['IDX_COL_STOPS'][line_num][0] - 1,
                                          positions['IDX_COL_STOPS'][line_num][1] + 1)

                # 열차별 loop
                for col in range(positions['IDX_COL_TRAIN'][line_num][0] - 1,
                                 positions['IDX_COL_TRAIN'][line_num][1] + 1):
                    # 기본 정보
                    train_info = sheet.col_slice(col,
                                                 fixed_positions['IDX_COL_TRAIN_INFO'][0] - 1,
                                                 fixed_positions['IDX_COL_TRAIN_INFO'][1] + 1)
                    train = Train(int(train_info[1].value), train_info[0].value)

                    # 시발역 정보
                    start_station = sheet.col_slice(col,
                                                    fixed_positions['IDX_COL_START_STATION'][0] - 1,
                                                    fixed_positions['IDX_COL_START_STATION'][1] + 1)
                    start_station_name = start_station[0]
                    start_station_time = xlrd.xldate_as_datetime(start_station[3].value,
                                                                 workbook.datemode)

                    train.add_stops(
                        Stop(999,
                             start_station_name.value,
                             start_station_time.strftime('%H:%M'),
                             line_name
                             )
                    )

                    # 정차역 정보
                    stops = sheet.col_slice(col,
                                            positions['IDX_COL_STOPS'][line_num][0] - 1,
                                            positions['IDX_COL_STOPS'][line_num][1] + 1)
                    for idx, stop in enumerate(stops):
                        if stop.value and stop.ctype == xlrd.XL_CELL_DATE:
                            time = xlrd.xldate_as_datetime(stop.value, workbook.datemode)
                            train.add_stops(
                                Stop(int(station[idx].value),
                                     station_name[idx].value,
                                     time.strftime('%H:%M'),
                                     line_name
                                 )
                            )

                    # 비고 정보
                    remarks = sheet.cell_value(positions['IDX_COL_STOPS'][line_num][1], col)
                    train.set_remarks(remarks)

                    # 종착역 정보
                    last_station = sheet.col_slice(col,
                                                   positions['IDX_COL_STOPS'][line_num][1] + 1,
                                                   positions['IDX_COL_STOPS'][line_num][1] + 5)
                    last_station_name = last_station[0]
                    last_station_time = xlrd.xldate_as_datetime(last_station[3].value, workbook.datemode)

                    train.add_stops(
                        Stop(999,
                             last_station_name.value,
                             last_station_time.strftime('%H:%M'),
                             line_name
                             )
                    )

                    self.append_train(train)

    def get_trains(self):
        return self.trains

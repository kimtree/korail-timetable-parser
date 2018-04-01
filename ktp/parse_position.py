"""
각 키별 노선 순서
0 - 경부선 하행
1 - 경부선 상행
2 - 장항선 하행
3 - 장항선 상행
4 - 호남선 하행
5 - 호남선 상행
6 - 전라선 하행
7 - 전라선 상행

IDX_COL_TRAIN                      열차별 인덱스 (예: D~AQ 컬럼을 숫자로 표시)

IDX_COL_START_STATION              시발역 인덱스
IDX_COL_TRAIN_INFO                 열차정보 인덱스 (열차종별, 열차번호)
IDX_COL_STOPS                      첫번쨰 정차역부터 마지막 정차역까지 컬럼의 인덱스
"""
fixed_positions = {
    'IDX_EXCEL_SHEET_NUM': (2, 9),
    'IDX_COL_START_STATION': (4, 7),
    'IDX_COL_TRAIN_INFO': (8, 9),
}

positions = {
    'IDX_COL_TRAIN': [(4, 42), (4, 42), (4, 18), (4, 18), (4, 22), (4, 22), (4, 16), (4, 16)],
    'IDX_COL_STOPS': [(10, 52), (10, 51), (10, 33), (10, 33), (10, 43), (10, 45), (10, 38), (10, 38)],
}

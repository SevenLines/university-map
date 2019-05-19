from datetime import datetime


def get_date_week_even(dt: datetime):
    """
    Возвращает 0 если неделя нечетная, и 1 если неделя четная
    """
    if dt.month >= 9:
        september_1st = datetime(dt.year, 9, 1)
    else:
        september_1st = datetime(dt.year - 1, 9, 1)

    wk = dt.isocalendar()[1]
    september_1st_week = september_1st.isocalendar()[1]
    if dt.year == september_1st.year:
        return (wk - september_1st_week) % 2
    else:
        return (52 - september_1st_week + wk) % 2
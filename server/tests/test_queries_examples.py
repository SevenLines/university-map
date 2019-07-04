import tests
from sqlalchemy import func
from models.raspnagr import Auditory, Raspis, RaspisZaoch, Raspnagr, Kontkurs, Discipline


class TestQueriesExamples(tests.TestCaseBase):
    def test_list_all_auds(self):
        """
        Выводит 10 самых больших аудиторий
        Подсмотреть поля у модели можно кликнув на Auditory с Ctrl

        получиться такой запрос:
        SELECT TOP 10 auditories.id_60 AS auditories_id_60,
            auditories.obozn AS auditories_obozn,
            auditories.korp AS auditories_korp,
            auditories.maxstud AS auditories_maxstud,
            auditories.specoborud AS auditories_specoborud
        FROM auditories
        ORDER BY auditories.maxstud DESC

        """
        auditories = Auditory.query.order_by(Auditory.maxstud.desc()).limit(10)
        print("\nquery:")
        print(auditories)
        print("Аудитории:")
        for aud in auditories:
            print(aud.title, aud.maxstud)

    def test_get_specific_auditory(self):
        """
        Возвращает аудиторию по идентификатору
        """
        aud = Auditory.query.get(908)
        print(aud.title)

    def test_filter_raspis_by_aud1(self):
        """
        Выведет данные по занятиями в аудитории с id 908
        список полей занятия можно подсмотреть кликнув с Ctrl на Raspis
        """
        schedule = Raspis.query \
            .filter(Raspis.aud_id == 908) \
            .order_by(Raspis.everyweek, Raspis.day, Raspis.para)

        print("\nquery")
        print(schedule)  # выводит запроса

        for item in schedule:
            print(item.everyweek, item.day, item.para)

    def test_filter_raspis_by_aud_and_day(self):
        """
        Выведет данные по занятиями в аудитории с id 908 в понедельник
        список полей занятия можно подсмотреть кликнув с Ctrl на Raspis
        """
        schedule = Raspis.query \
            .filter(Raspis.aud_id == 908) \
            .filter(Raspis.day == 5) \
            .order_by(Raspis.everyweek, Raspis.day, Raspis.para)

        for item in schedule:
            print(item.everyweek, item.day, item.para)

    def test_filter_raspis_by_multiple_auds_with_specific_columns(self):
        """
        Выведет данные по занятиями в аудитории с id 908 и 907 в понедельник
        список полей занятия можно подсмотреть кликнув с Ctrl на Raspis

        Получится такой запрос:

        SELECT rtrim(auditories.obozn) AS auditory,
            raspnagr.id_51 AS raspnagr_id,
            raspis.day AS raspis_day,
            raspis.para AS raspis_para,
            rtrim(kontkurs.obozn) AS kont_title,
            rtrim(vacpred.pred) AS discipline
        FROM raspis
            LEFT OUTER JOIN auditories ON auditories.id_60 = raspis.aud
            LEFT OUTER JOIN raspnagr ON raspnagr.id_51 = raspis.raspnagr
            LEFT OUTER JOIN kontkurs ON kontkurs.id_1 = raspnagr.kont
            LEFT OUTER JOIN vacpred ON vacpred.id_15 = raspnagr.pred
        WHERE raspis.aud IN (908, 907)
        ORDER BY auditories.obozn, raspis.everyweek, raspis.day, raspis.para
        """
        schedule = Raspis.query \
            .filter(Raspis.aud_id.in_([908, 907])) \
            .outerjoin(Auditory, Auditory.id == Raspis.aud_id) \
            .outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id) \
            .outerjoin(Kontkurs, Kontkurs.id == Raspnagr.kontkurs_id) \
            .outerjoin(Discipline, Discipline.id == Raspnagr.pred_id) \
            .with_entities(
                func.rtrim(Auditory.title).label("auditory"),
                Raspnagr.id.label("raspnagr_id"),
                Raspis.day,
                Raspis.para,
                func.rtrim(Kontkurs.title).label("kont_title"),
                func.rtrim(Discipline.title).label("discipline"),
            ) \
            .order_by(Auditory.title, Raspis.everyweek, Raspis.day, Raspis.para)

        print(schedule)

        for item in schedule:
            print(f"Аудитория {item.auditory} День: {item.day} Пара: "
                  f"{item.para} конитнгент: {item.kont_title} дисциплина: {item.discipline}")

    def test_group_by_para(self):
        """
        считаем сколько занятий приходится на каждую пару
        получается такой запрос

        SELECT raspis.para AS raspis_para, count(*) AS items_count
        FROM raspis
        GROUP BY raspis.para
        """
        result = Raspis.query.with_entities(
            Raspis.para,
            func.count("*").label("items_count")
        ).group_by(Raspis.para)

        # преобразовываем в словарик, где ключ это номер пары, а значение -- количество занятий
        ouput_dict = {
            i.para: i.items_count for i in result
        }

        for para, value in ouput_dict.items():
            print(f"В {para} пару {value} занятий")

        # или если нас интересует конкретная пара то так
        print(f"В {2} пару {ouput_dict[2]} занятий")

    def test_audience_percentage_day_for_pair(self):
        aud = Auditory.query.get(908)
        res = Raspis.query.filter(Raspis.aud_id == 908) \
            .with_entities(
            Raspis.para, func.count("*").label("items_count")). \
            group_by(Raspis.para)

        output_dict = {
            i.para: round(i.items_count / 12 * 100, 2) for i in res
        }

        for para, value in output_dict.items():
            print(f"В аудитории {aud.title.strip()} в {para} пару "
                  f"аудитория загружена на {value}%")

    def test_audience_percentage_day_for_day(self):
        aud = Auditory.query.get(908)
        schedule = Raspis.query \
            .filter(Raspis.aud_id == 908) \
            .with_entities(
                Raspis.day,
                func.count("*").label("pair_count")) \
            .group_by(Raspis.day) \
            .order_by(Raspis.day)

        print(aud)
        for item in schedule:
            print(f"В {item.day} день - {item.pair_count} пар. "
                  f"Аудитория загружена на {round(item.pair_count / 8 * 100, 2)}%")

#   def test_audience_percentage_day_for_day_and_extramural(self):

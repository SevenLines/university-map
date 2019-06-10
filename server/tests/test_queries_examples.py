from tests import TestCaseBase
from models.raspnagr import Auditory, Raspis

class TestQueriesExamples(TestCaseBase):
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

    def test_filter_raspis_by_aud(self):
        """
        Выведет данные по занятиями в аудитории с id 908
        список полей занятия можно подсмотреть кликнув с Ctrl на Raspis
        """
        schedule = Raspis.query.filter(
            Raspis.aud_id == 908,
        ).order_by(Raspis.everyweek, Raspis.day, Raspis.para)

        print("\nquery")
        print(schedule)  # выводи запроса

        for item in schedule:
            print(item.everyweek, item.day, item.para)
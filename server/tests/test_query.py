import tests
from sqlalchemy import func
from models.raspnagr import Auditory, Raspis, Raspnagr, Teacher


class TestQuery(tests.TestCaseBase):

        def test_filter_by_teacher_and_day(self):
            """
            SELECT para, a.obozn as aud
            FROM raspis r
            LEFT JOIN auditories a ON r.aud = a.id_60
            LEFT JOIN raspnagr rn ON rn.id_51 = r.raspnagr
            LEFT JOIN prepods p ON rn.prep = p.id_61
            WHERE preps is not NULL AND preps = 'Бахвалова З.А.' AND (day-1)%7+1 = 2
            ORDER BY para
            """
            schedule = Raspis.query \
                .filter(Teacher.name is not None) \
                .filter(func.rtrim(Teacher.name) == "Бахвалова З.А.") \
                .filter((Raspis.day - 1) % 7 + 1 == 1) \
                .outerjoin(Auditory, Auditory.id == Raspis.aud_id) \
                .outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id) \
                .outerjoin(Teacher, Raspnagr.prep_id == Teacher.id) \
                .with_entities(
                Raspis.para,
                func.rtrim(Auditory.title).label("auditory")
            ) \
                .order_by(Raspis.para)
            print(schedule)

            for item in schedule:
                print(f"Пара: {item.para}  Аудитория: {item.auditory}")

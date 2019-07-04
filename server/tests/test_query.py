import tests
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce
from models.raspnagr import Auditory, Raspis, Raspnagr, Teacher, Kontgrp, Kontkurs, Potoklist


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

        def test_filter_by_group_and_day(self):
            """
            SELECT para, a.obozn as aud,coalesce(pl.konts, kg.obozn, kk.obozn)as kont
            FROM raspis r
            LEFT JOIN auditories a ON r.aud = a.id_60
            LEFT JOIN raspnagr rn ON rn.id_51 = r.raspnagr
            LEFT JOIN kontgrp kg ON kg.id_7 = rn.kontid
            LEFT JOIN kontkurs kk ON kk.id_1 = rn.kont
            LEFT JOIN potoklist pl ON pl.op = rn.op
            WHERE (day-1)%7+1 = 1 AND kg.kont = 22979
            ORDER BY para
            """
            schedule = Raspis.query \
                .filter((Raspis.day -1)%7 ==1)\
                .filter(Kontgrp.kont_id == 22979)\
                .outerjoin(Auditory, Raspis.aud_id == Auditory.id)\
                .outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id)\
                .outerjoin(Kontgrp, Kontgrp.id == Raspnagr.kontgrp_id) \
                .outerjoin(Kontkurs, Kontkurs.id == Raspnagr.kontkurs_id) \
                .outerjoin(Potoklist, Potoklist.op == Raspnagr.op)\
                .with_entities(
                Raspis.para,
                func.rtrim(Auditory.title).label("auditory"),
                coalesce(Potoklist.title, Kontgrp.title, Kontkurs.title).label("group")
                ) \
                .order_by(Raspis.para)

            print(schedule)

            for item in schedule:
                 print(f"Пара: {item.para} Аудитория: {item.auditory} Группа: {item.group}")
from datetime import datetime
from itertools import groupby

from flask import request
from flask_restplus import Resource, Namespace
from sqlalchemy import or_, and_, func
from wtforms import Form, DateField

from server.helpers import get_date_week_even
from server.models.raspnagr import Auditory, Raspis, Raspnagr, Teacher, Discipline, Kontkurs, Kontgrp, Kontlist, \
    Potoklist, Normtime, RaspisZaoch

api = Namespace("auditories")


@api.route('/list')
class AuditoriesList(Resource):
    def get(self):
        auditories = Auditory.query.order_by(Auditory.title)

        result = {a.id: {
            "id": a.id,
            "title": a.title.strip(),
            "key": Auditory.get_key(a.title),
        } for a in auditories}

        return result


@api.route("/day-occupation")
class AuditoriesDayOccupation(Resource):
    class InnerForm(Form):
        date = DateField(format="%d.%m.%Y")

    def add_joins(self, query):
        query = query \
            .outerjoin(Teacher, Teacher.id == Raspnagr.prep_id) \
            .outerjoin(Discipline, Discipline.id == Raspnagr.pred_id) \
            .outerjoin(Kontkurs, Kontkurs.id == Raspnagr.kontkurs_id) \
            .outerjoin(Kontgrp, Kontgrp.id == Raspnagr.kontgrp_id) \
            .outerjoin(Potoklist, Potoklist.op == Raspnagr.op) \
            .outerjoin(Normtime, Normtime.id == Raspnagr.nt)
        return query

    def common_entites(self):
        return [
            func.rtrim(Teacher.full_name).label("teacher"),
            func.rtrim(Discipline.title).label("discipline"),
            func.rtrim(func.coalesce(Potoklist.title, Kontgrp.title, Kontkurs.title)).label("kont"),
            Normtime.id.label("nt"),
        ]

    def get_data(self, date: datetime):
        week_even = get_date_week_even(date)
        day = date.weekday() + 1
        week_day = day + 7 if week_even == 1 else day

        raspis = self.add_joins(Raspis.query.filter(
            or_(
                and_(Raspis.everyweek == 2,  Raspis.day == day),
                and_(Raspis.everyweek == 1,  Raspis.day == week_day),
            )
        ).outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id)) \
            .filter(Raspis.aud_id.isnot(None)) \
            .with_entities(
            Raspis.aud_id.label("aud_id"),
            Raspis.para,
            Raspis.kol_par,
            *self.common_entites()
        ).order_by(Raspis.aud_id, Raspis.para)

        occupation = {
            aud_id: {
                i.para: {
                    'teacher': i.teacher,
                    'discipline': i.discipline,
                    'kont': i.kont,
                    'nt': i.nt,
                }
                for i in items
            } for aud_id, items in groupby(raspis, lambda x: x.aud_id)
        }

        raspis_zaoch = self.add_joins(RaspisZaoch.query.filter(
            RaspisZaoch.dt == date
        ).outerjoin(Raspnagr, Raspnagr.id == RaspisZaoch.raspnagr_id)) \
            .with_entities(
            RaspisZaoch.aud.label("aud1_id"),
            RaspisZaoch.aud2.label("aud2_id"),
            RaspisZaoch.para,
            RaspisZaoch.hours,
            *self.common_entites()
        )

        for item in raspis_zaoch:
            occupation_item = occupation.setdefault(item.aud1_id, {})
            for para in range(item.hours // 2):
                para_key = para + item.para
                para_item = occupation_item.setdefault(para_key, {})
                if not para_item:
                    occupation_item[para_key] = {
                        'teacher': item.teacher,
                        'discipline': item.discipline,
                        'kont': item.kont,
                        'nt': item.nt,
                    }

                if item.aud2_id:
                    occupation_item = occupation.setdefault(item.aud2_id, {})
                    para_item = occupation_item.setdefault(para_key, {})
                    if not para_item:
                        occupation_item[para_key] = {
                            'teacher': item.teacher,
                            'discipline': item.discipline,
                            'kont': item.kont,
                            'nt': item.nt,
                        }

        return occupation

    def get(self):
        form = self.InnerForm(request.args)
        if form.validate():
            return self.get_data(form.data['date'])

        return form.errors

from datetime import datetime
from itertools import groupby

from flask import request
from flask_restplus import Resource, Namespace
from sqlalchemy import or_, and_, func
from wtforms import Form, DateField

from server.helpers import get_date_week_even
from server.models.raspnagr import Auditory, Raspis

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

    def get_data(self, date: datetime):
        week_even = get_date_week_even(date)
        day = date.weekday() + 1
        week_day = day + 7 if week_even == 1 else day

        raspis = Raspis.query.filter(
            or_(
                and_(Raspis.everyweek == 2,  Raspis.day == day),
                and_(Raspis.everyweek == 1,  Raspis.day == week_day),
            )
        ).outerjoin(
            Auditory, Auditory.id == Raspis.aud_id
        ).filter(
            Auditory.id.isnot(None)
        ).with_entities(
            Auditory.id.label("aud_id"),
            func.rtrim(Auditory.title).label("aud_title"),
            Raspis.para,
            Raspis.kol_par
        ).order_by(Auditory.id, Raspis.para)

        return {
            aud_id: {
                i.para: i
                for i in items
            } for aud_id, items in groupby(raspis, lambda x: x.aud_id)
        }

    def get(self):
        form = self.InnerForm(request.args)
        if form.validate():
            return self.get_data(form.data['date'])

        return form.errors

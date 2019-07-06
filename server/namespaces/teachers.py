from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import func
from wtforms import Form, IntegerField

from models.raspnagr import Teacher, Raspis, Raspnagr, Discipline, Kontkurs, Kontgrp, Potoklist, Normtime, Auditory
from ways import find_paths, get_full_graph

api = Namespace("teachers")

@api.route('/way_view_teachers')
class TeacherWayView(Resource):
    def get(self):
        teachers = Raspis.query \
            .filter(Teacher.name is not None) \
            .filter(Teacher.id == request.args.get('id'))\
            .filter((Raspis.day - 1) % 7 + 1 == request.args.get('day')) \
            .outerjoin(Auditory, Auditory.id == Raspis.aud_id) \
            .outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id) \
            .outerjoin(Teacher, Raspnagr.prep_id == Teacher.id) \
            .with_entities(
            Raspis.para,
            Raspis.day,
            Teacher.id,
            Auditory.id.label("auditory_id"),
            func.rtrim(Auditory.title).label("auditory")
        ) \
            .order_by(Raspis.para)

        result = [
            {
                'id': t.id,
                'day': t.day,
                'para': t.para,
                'auditory_id': t.auditory_id,
                'auditory': t.auditory.strip()
            } for t in teachers
        ]

        return result

    def get_path_teacher(self):
        schedule = TeacherWayView.get(self)
        graph = get_full_graph(['../../Data/2этаж.svg', '../../Data/3этаж.svg'])
        paths = find_paths(graph, 'enter_v316', 'enter_v225')
        for nodes in paths:
            for node in nodes:
                print(node.id)




@api.route('/list')
class TeachersList(Resource):
    def get(self):
        teachers = Teacher.query.order_by(Teacher.full_name)

        result = [
            {
                'id': t.id,
                'name': t.name.strip(),
                'full_name': t.full_name.strip(),
            } for t in teachers
        ]

        return result


@api.route('/occupation')
class TeacherOccupation(Resource):
    class InnerForm(Form):
        id = IntegerField()

    def add_joins(self, query):
        query = query \
            .outerjoin(Teacher, Teacher.id == Raspnagr.prep_id) \
            .outerjoin(Discipline, Discipline.id == Raspnagr.pred_id) \
            .outerjoin(Kontkurs, Kontkurs.id == Raspnagr.kontkurs_id) \
            .outerjoin(Kontgrp, Kontgrp.id == Raspnagr.kontgrp_id) \
            .outerjoin(Potoklist, Potoklist.op == Raspnagr.op) \
            .outerjoin(Normtime, Normtime.id == Raspnagr.nt)
        return query

    def get_data(self, id, *args, **kwargs):
        raspis = self.add_joins(Raspis.query.outerjoin(
            Raspnagr, Raspnagr.id == Raspis.raspnagr_id
        )).filter(
            Raspnagr.prep_id == id
        ).with_entities(
            Raspis.para,
            Raspis.everyweek,
            Raspis.day,
            Raspis.aud_id
        )

        result = []
        for item in raspis:
            result.append({
                'para': item.para,
                'everyweek': item.everyweek,
                'day': item.day,
                'aud_id': item.aud_id,
            })

        return result

    def get(self):
        form = self.InnerForm(request.args)
        if form.validate():
            return self.get_data(form.data['id'])

        return form.errors

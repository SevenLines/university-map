from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

from models.raspnagr import Raspis, Raspnagr, Kontkurs, Kontgrp, Potoklist, Auditory
from ways import get_full_graph, find_paths

api = Namespace("groups")

@api.route('/way_view_groups')
class GroupWayView(Resource):
    def get_data(self):
        groups = Raspis.query \
                .filter(Kontgrp.kont_id == request.args.get('kont_id')) \
                .filter((Raspis.day - 1) % 7 + 1 == request.args.get('day')) \
                .outerjoin(Auditory, Auditory.id == Raspis.aud_id) \
                .outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id) \
                .outerjoin(Kontgrp, Kontgrp.id == Raspnagr.kontgrp_id) \
                .outerjoin(Kontkurs, Kontkurs.id == Raspnagr.kontkurs_id) \
                .outerjoin(Potoklist, Potoklist.op == Raspnagr.op) \
                .with_entities(
                Kontgrp.kont_id,
                Raspis.day,
                Raspis.para,
                Auditory.id.label("auditory_id"),
                func.rtrim(Auditory.title).label("auditory"),
                func.rtrim(coalesce(Potoklist.title, Kontgrp.title, Kontkurs.title)).label("group")
            ) \
                .order_by(Raspis.para)

        result = [
            {
                'kont_id': t.kont_id,
                'day': t.day,
                'para': t.para,
                'auditory_id': t.auditory_id,
                'auditory': t.auditory,
                'group': t.group.strip()
            } for t in groups
        ]

        return result

    def get(self):
        schedule = self.get_data()
        graph = get_full_graph([ '../../Data/2этаж.svg', '../../Data/3этаж.svg'])
        point_list = []
        for i in range(len(schedule)):
            paths = find_paths(graph, Auditory.get_new_aud_title('Г-303'), Auditory.get_new_aud_title('В-316'))
            for node in paths:
                point_list.append({
                    'x': node.x(),
                    'y': node.y()
                })

        return point_list


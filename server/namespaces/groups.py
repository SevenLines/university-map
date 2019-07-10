from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

from models.raspnagr import Raspis, Raspnagr, Kontkurs, Kontgrp, Potoklist, Auditory
from ways import get_full_graph, find_path


def pave_the_way_between_auds(aud_list):
    svg_files = ['../../Data/0этаж.svg', '../../Data/1этаж.svg', '../../Data/2этаж.svg', '../../Data/3этаж.svg']
    graph = get_full_graph(svg_files, [0, 1, 2, 3])
    point_list = []
    point_sub_list = []
    for i in range(len(aud_list) - 1):
        if (aud_list[i] != aud_list[i + 1]):
            paths = find_path(graph, Auditory.get_new_aud_title(aud_list[i]),
                               Auditory.get_new_aud_title(aud_list[i + 1]))
            for node in paths:
                point_sub_list.append({
                    'x': node.x,
                    'y': node.y,
                    'level': node.floor
                })
            point_sub_list[0]['aud'] = aud_list[i]
            point_sub_list[-1]['aud'] = aud_list[i + 1]
            point_list += point_sub_list
    return point_list

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
        aud_list = []
        for i in range(len(schedule)):
            aud_list.append(schedule[i]['auditory'])
        return pave_the_way_between_auds(aud_list)


@api.route('/flow_view')
class FlowView(Resource):
    def get(self):
        query = Raspis.query \
                .filter(Raspis.day == request.args.get('day')) \
                .filter((Raspis.para == 3) | (Raspis.para == 4)) \
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

        # transitions = {}
        # for item in query:
        #     if item.id is not transitions:
        #         transitions[item.id] = []
        #         transitions[item.id].append(item.auditory_id)
        #
        # return transitions








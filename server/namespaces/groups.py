from flask import request
from flask_restplus import Namespace, Resource
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

from models.raspnagr import Raspis, Raspnagr, Kontkurs, Kontgrp, Potoklist, Auditory
from ways import get_full_graph, find_path


def get_path(aud_list):
    svg_files = ['../../Data/0этаж.svg', '../../Data/1этаж.svg', '../../Data/2этаж.svg', '../../Data/3этаж.svg']
    graph = get_full_graph(svg_files, [0, 1, 2, 3])
    paths=[]
    occupation = {}
    for
    for i in range(len(aud_list) - 1):
        if (aud_list[i] != aud_list[i + 1]):
            path = find_path(graph, Auditory.get_new_aud_title(aud_list[i]),
                              Auditory.get_new_aud_title(aud_list[i + 1]))


            for path in paths:
                for node in paths:
                    key = f"{node.x}{node.y}{node.floor}"
                    if key not in occupation:
                        occupation[key] = {
                            'x': node.x,
                            'y': node.y,
                            'level': node.floor,
                            'counter': 0
                        }
                    occupation[key]['counter'] += 1

    return occupation


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
    def get_list(self):
        query = Raspis.query \
            .filter(Raspis.day == 1) \
            .filter((Raspis.para == 3) | (Raspis.para == 4)) \
            .filter(Kontgrp.kont_id is not None) \
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
            func.rtrim(Auditory.title).label("auditory")
        ) \
            .order_by(Raspis.para, Kontgrp.kont_id)

        transitions = {}
        transitions_list = []
        for item in query:
            if item.kont_id not in transitions:
                transitions[item.kont_id] = []
            transitions[item.kont_id].append(item.auditory)

        for kont_id, auditories in transitions.items():
            if (len(auditories) != 2):
                continue
            transitions_list.append({
                'kont_id': kont_id,
                'auditories': auditories
            })

        return (transitions_list)

    def get(self):
        transitions_list = self.get_list()
        transitions = [['Г-303', 'Г-203'], ['Г-203', 'Г-303'], ['Г-305', 'Г-306']]
        # points = []
        density = 0
        # for i in range(len(transitions)):
        #     points.append(pave_the_way_between_auds(transitions[i]))

        # for i in range(len(transitions_list)):
        #    points.append (transitions_list[i]['auditories'])
        occupation_map = []
        occupation_map.append(get_path(transitions))
        return occupation_map

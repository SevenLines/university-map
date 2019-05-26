# coding=utf-8
from flask import g
from sqlalchemy import func, case, PrimaryKeyConstraint
from sqlalchemy.orm.util import aliased
from sqlalchemy.sql.expression import or_, and_

from server.base import db
from server.consts import LETTER_MAPPING_TABLE


class Kontkurs(db.Model):
    id = db.Column('id_1', db.Integer, primary_key=True)
    title = db.Column("obozn")
    shup = db.Column(db.Integer)
    spclntion = db.Column(db.Integer)
    kurs = db.Column(db.Integer)
    fil = db.Column(db.Integer)
    fac_id = db.Column("fac", db.Integer, db.ForeignKey('vacfac.id_5'))
    aobozn_id = db.Column("aobozn", db.Integer, db.ForeignKey('vacaobozn.id_6'))
    stud = db.Column(db.Integer)
    groups = db.Column(db.Integer)
    pgroups = db.Column(db.Integer)
    smenao = db.Column(db.Integer)
    smenav = db.Column(db.Integer)
    groupkey = db.Column(db.Integer)
    undoworksps = db.Column(db.String(250))
    anothernumstudsps = db.Column(db.String(250))
    newnumstud = db.Column(db.SmallInteger)
    ntcgraph = db.Column(db.SmallInteger)
    syear = db.Column(db.Integer)

    groupslist = db.relationship('Kontgrp', backref='kontkurs', lazy='joined')
    kontlist = db.relationship('Kontlist', backref='kontkurs', lazy='select')
    raspnagr = db.relationship("Raspnagr", backref=db.backref('kontkurs', lazy='select'))

    def __str__(self, *args, **kwargs):
        return "<Kontkurs: {}>".format(self.title.strip())

    def __repr__(self):
        return str(self)

    def get_title(self):
        return self.title.replace("(И,О)", "")


class Obozn(db.Model):
    __tablename__ = "vacaobozn"
    id = db.Column('id_6', db.Integer, primary_key=True)
    title = db.Column("aobozn", db.String(50))

    kontkurs = db.relationship("Kontkurs", backref=db.backref("aobozn", lazy="joined"))


class Kontgrp(db.Model):
    id = db.Column('id_7', db.Integer, primary_key=True)
    kont_id = db.Column("kont", db.Integer, db.ForeignKey('kontkurs.id_1'))
    title = db.Column("obozn", db.String(20))
    ngroup = db.Column(db.Integer)
    students = db.Column(db.Integer)
    parent_id = db.Column("parent", db.Integer, db.ForeignKey('kontgrp.id_7'))
    depth = db.Column(db.Integer)
    budzh = db.Column(db.Integer)
    spclntion = db.Column(db.Integer)

    op = db.relationship("Kontgrplist", backref=db.backref("kontgrp", lazy="joined"), lazy='joined')
    raspnagr = db.relationship("Raspnagr", backref=db.backref('kontgrp', lazy='joined'))
    children = db.relationship("Kontgrp", backref=db.backref('parent', remote_side=[id], lazy="joined"))

    def __str__(self, *args, **kwargs):
        return "<Kontgrp: {}>".format(self.title.strip())

    def __repr__(self):
        return str(self)

    def get_title(self):
        return self.title.replace("(И,О)", "")
        # if self.parent_id:
        #     return "{}-{}-{}-{}".format(
        #         self.kontkurs.kurs,
        #         self.kontkurs.aobozn.title,
        #         self.parent.ngroup,
        #         self.ngroup,
        #     )
        # else:
        #     return "{}-{}-{}".format(
        #         self.kontkurs.kurs,
        #         self.kontkurs.aobozn.title,
        #         self.ngroup,
        #     )


class Kontlist(db.Model):
    id = db.Column('id_9', db.Integer, primary_key=True)
    op = db.Column(db.Integer, db.ForeignKey('raspnagr.op'))
    kontkurs_id = db.Column("kont", db.Integer, db.ForeignKey('kontkurs.id_1'))


class Kontgrplist(db.Model):
    id = db.Column('id_', db.Integer, primary_key=True)
    op = db.Column(db.Integer, db.ForeignKey('raspnagr.op'))
    kontgrp_id = db.Column("kontid", db.Integer, db.ForeignKey('kontgrp.id_7'))


class Potoklist(db.Model):
    id = db.Column('id_8', db.Integer, primary_key=True)
    op = db.Column('op', db.Integer)
    semestr = db.Column("semestr", db.Integer)
    title = db.Column('konts', db.String(220))


class Raspnagr(db.Model):
    id = db.Column('id_51', db.Integer, primary_key=True)
    kontkurs_id = db.Column("kont", db.Integer, db.ForeignKey('kontkurs.id_1'))
    kontgrp_id = db.Column("kontid", db.Integer, db.ForeignKey('kontgrp.id_7'))
    op = db.Column("op", db.Integer)
    nt = db.Column(db.Integer, db.ForeignKey("normtime.id_40"))
    sem = db.Column(db.Integer)
    pred_id = db.Column("pred", db.Integer, db.ForeignKey("vacpred.id_15"))
    kaf_id = db.Column("kaf", db.Integer, db.ForeignKey("vackaf.id_17"))
    fobuch = db.Column(db.SmallInteger)
    afobuch = db.Column(db.SmallInteger)
    nagrid = db.Column(db.Integer)
    h = db.Column(db.Float)
    hy = db.Column(db.Integer)
    dbeg = db.Column(db.Date)
    days = db.Column(db.Integer)
    prep_id = db.Column("prep", db.Integer, db.ForeignKey('prepods.id_61'))
    aud_id = db.Column("aud", db.Integer, db.ForeignKey('auditories.id_60'))
    nagrtype = db.Column(db.SmallInteger)
    nagrprop = db.Column(db.Integer)
    nagr_h = db.Column(db.Float)
    stud = db.Column(db.Integer)
    editstud = db.Column(db.Integer)
    rnprep = db.Column(db.Integer)
    # hy1 = db.Column(db.Integer)
    # hy2 = db.Column(db.Integer)
    syear = db.Column(db.Integer)

    raspis = db.relationship('Raspis', backref=db.backref('raspnagr', lazy='joined'), lazy='dynamic')
    raspis_zaoch = db.relationship('RaspisZaoch', backref=db.backref('raspnagr', lazy='joined'), lazy='dynamic')
    kontlist = db.relationship('Kontlist', backref='raspnagr', lazy='subquery')
    kontgrplist = db.relationship('Kontgrplist', backref='raspnagr', lazy='subquery')

    @classmethod
    def get_for_kontgrp(self, kontgrp):
        raspnagrs = Raspnagr.query.filter(
            or_(Raspnagr.kontgrp_id == kontgrp.id, Raspnagr.kontkurs_id == kontgrp.kont_id)
        )
        return raspnagrs

    @classmethod
    def get_for_kontkurs_id(self, kontkurs_id, sem=1, subgroup_number=0):
        Kontgrp2 = aliased(Kontgrp)
        KontgrpCommon = aliased(Kontgrp)
        KontgrpParent = aliased(Kontgrp)

        if not isinstance(kontkurs_id, list):
            kontkurs_id = [kontkurs_id, ]

        if int(subgroup_number):
            filter_ = and_(or_(
                Raspnagr.kontkurs_id.in_(kontkurs_id),
                Kontlist.kontkurs_id.in_(kontkurs_id),
                KontgrpCommon.kont_id.in_(kontkurs_id),
            ), or_(
                KontgrpCommon.id == None,
                and_(KontgrpParent.id == None, KontgrpCommon.ngroup == subgroup_number),
                KontgrpParent.ngroup == subgroup_number
            ), )
        else:
            filter_ = or_(
                Raspnagr.kontkurs_id.in_(kontkurs_id),
                KontgrpCommon.kont_id.in_(kontkurs_id),
                Kontlist.kontkurs_id.in_(kontkurs_id),
            )

        raspnagrs = Raspnagr.query.filter(
            Raspnagr.id.in_(Raspnagr.query \
                            .outerjoin(Kontgrp, Raspnagr.kontgrp_id == Kontgrp.id) \
                            .outerjoin(Kontgrplist, Kontgrplist.op == Raspnagr.op) \
                            .outerjoin(Kontlist, Kontlist.op == Raspnagr.op) \
                            .outerjoin(Kontgrp2, Kontgrp2.id == Kontgrplist.kontgrp_id) \
                            .outerjoin(KontgrpCommon, func.coalesce(Kontgrp2.id, Kontgrp.id) == KontgrpCommon.id) \
                            .outerjoin(KontgrpParent, KontgrpCommon.parent_id == KontgrpParent.id) \
                            .filter(filter_).filter(Raspnagr.sem == sem).with_entities(Raspnagr.id)))
        return raspnagrs


class Korpus(db.Model):
    __tablename__ = "vackorp"
    id = db.Column('id_67', db.Integer, primary_key=True)
    title = db.Column("korp", db.String(10))
    auditories = db.relationship('Auditory', backref='korp', lazy='dynamic')

    def __str__(self, *args, **kwargs):
        return "<Korpus: {}>".format(self.title.strip())

    def __repr__(self):
        return str(self)


class Auditory(db.Model):
    __tablename__ = "auditories"

    id = db.Column('id_60', db.Integer, primary_key=True)
    title = db.Column("obozn", db.String(20))
    korp_id = db.Column("korp", db.Integer, db.ForeignKey('vackorp.id_67'))
    maxstud = db.Column(db.SmallInteger)
    specoborud = db.Column(db.SmallInteger)

    def __str__(self, *args, **kwargs):
        return "<Auditory: {}>".format(self.title.strip())

    def __repr__(self):
        return str(self)

    @staticmethod
    def get_key(title: str):
        title = title.strip().lower().replace("_вт", "").replace("-", "").replace(".", "")
        title = title.translate(LETTER_MAPPING_TABLE)
        return title

    raspnagr = db.relationship('Raspnagr', backref=db.backref('auditory', lazy='joined'), lazy='dynamic')
    raspis = db.relationship('Raspis', backref=db.backref('auditory', lazy='joined'), lazy='dynamic')
    # raspis_zaoch = db.relationship('RaspisZaoch',  backref=db.backref('auditory', lazy='joined'), lazy='dynamic')


class Audlist(db.Model):
    __tablename__ = 'audlist'

    auds = db.Column('auds', db.Integer, primary_key=True)
    aud = db.Column('aud', db.Integer)


class Discipline(db.Model):
    __tablename__ = "vacpred"
    id = db.Column('id_15', db.Integer, primary_key=True)
    title = db.Column("pred", db.String(250))
    titles = db.Column("preds", db.String(250))

    raspnagr = db.relationship('Raspnagr', backref=db.backref('discipline', lazy='joined'), lazy='dynamic')


class Teacher(db.Model):
    __tablename__ = "prepods"
    id = db.Column('id_61', db.Integer, primary_key=True)
    full_name = db.Column('prep', db.String(100))
    name = db.Column('preps', db.String(50))

    raspnagr = db.relationship('Raspnagr', backref=db.backref('teacher', lazy='joined'), lazy='dynamic')


class TeacherForNagruzka(db.Model):
    __tablename__ = "rnprepods"
    id = db.Column("id_68", db.Integer, primary_key=True)
    prep = db.Column("prep", db.Integer)
    kaf = db.Column("kaf", db.Integer)


class TeacherList(db.Model):
    __tablename__ = "preplist"
    preps = db.Column("preps", db.Integer, primary_key=True)
    prep = db.Column("prep", db.Integer)


class Faculty(db.Model):
    __tablename__ = "vacfac"
    id = db.Column('id_5', db.Integer, primary_key=True)
    title = db.Column("fac", db.String(65))

    kontkurs = db.relationship('Kontkurs', backref=db.backref('faculty', lazy='joined'), lazy='dynamic')


class Chair(db.Model):
    __tablename__ = "vackaf"
    id = db.Column('id_17', db.Integer, primary_key=True)
    title = db.Column("kaf", db.String(100))
    short_title = db.Column("sokr", db.String(10))

    raspnagr = db.relationship('Raspnagr', backref=db.backref('chair', lazy='joined'), lazy='dynamic')


class Normtime(db.Model):
    id = db.Column('id_40', db.Integer, primary_key=True)
    vacnt = db.Column(db.Integer)
    title = db.Column("repvrnt", db.String(50))
    vrnt = db.Column(db.String(250))
    dopinfo = db.Column(db.String(250))


class Raspis(db.Model):
    id = db.Column('id_55', db.Integer, primary_key=True)
    raspnagr_id = db.Column("raspnagr", db.Integer, db.ForeignKey('raspnagr.id_51'))
    everyweek = db.Column(db.SmallInteger)
    day = db.Column(db.SmallInteger)
    para = db.Column(db.SmallInteger)
    kol_par = db.Column(db.SmallInteger)
    aud_id = db.Column("aud", db.Integer, db.ForeignKey('auditories.id_60'))
    n_zan = db.Column(db.Integer)  # диспетчер, который занятие ставил
    num_zant = db.Column(db.Integer)
    insdate = db.Column(db.DateTime)

    @classmethod
    def _get_table(cls, rows, group_by_lesson=False, key_template=None, *args, **kwargs):
        schedule = {
            para: {
                day: {
                    'everyweek': [],
                    'odd': [],
                    'even': [],
                } for day in [1, 2, 3, 4, 5, 6]
            } for para in [0, 1, 2, 3, 4, 5, 6, 7, 8]
        }

        if key_template is None:
            key_template = "{discipline_id}_{nt}"

        for lesson in rows.order_by(Raspis.day, Raspis.para):
            setattr(lesson, 'groups', [])

            if lesson.raspnagr.kontgrp:
                lesson.groups = [lesson.raspnagr.kontgrp, ]
                lesson.faculty = lesson.raspnagr.kontgrp.kontkurs.faculty
            elif lesson.raspnagr.kontkurs:
                lesson.groups = [lesson.raspnagr.kontkurs, ]
                lesson.faculty = lesson.raspnagr.kontkurs.faculty
            elif lesson.raspnagr.kontgrplist:
                lesson.groups = [i.kontgrp for i in lesson.raspnagr.kontgrplist]
                lesson.faculty = lesson.groups[0].kontkurs.faculty
            elif lesson.raspnagr.kontlist:
                lesson.groups = [i.kontkurs for i in lesson.raspnagr.kontlist]
                lesson.faculty = lesson.groups[0].faculty

            if lesson.everyweek == 1:
                if lesson.day > 7:
                    week = 'even'
                else:
                    week = 'odd'
            else:
                week = 'everyweek'

            schedule[lesson.para][(lesson.day - 1) % 7 + 1][week].append(lesson)
            schedule[lesson.para][(lesson.day - 1) % 7 + 1][week].sort(key=lambda l: l.groups[0].title)
            lesson.kurs_list = {getattr(i, 'kurs') if hasattr(i, 'kurs') else i.kontkurs.kurs for i in lesson.groups}

        if group_by_lesson:
            for para, days in schedule.items():
                for day, weeks in days.items():
                    for week, lessons in weeks.items():
                        weeks[week] = {}
                        for lesson in lessons:
                            for kont in lesson.groups:
                                kont.kurs = kont.kontkurs.kurs if hasattr(kont, 'kontkurs') else kont.kurs
                                key = key_template.format(**{
                                    'discipline_id': lesson.raspnagr.discipline.id,
                                    'nt': lesson.raspnagr.nt,
                                    'fac_id': lesson.faculty.id,
                                    'kurs': kont.kurs
                                })
                                weeks[week].setdefault(key, [])
                                weeks[week][key].append(lesson)
                        for key, dlessons in weeks[week].items():
                            weeks[week][key] = dlessons[0] if dlessons else None
                            for lesson in dlessons[1:]:
                                weeks[week][key].groups += lesson.groups
                            weeks[week][key].groups.sort(key=lambda l: l.title)
                        weeks[week] = list(weeks[week].values())

        for para, days in schedule.items():
            for day, weeks in days.items():
                for week, raspis in weeks.items():
                    for r in raspis:
                        r.groups = sorted(list(set(r.groups)), key=lambda x: x.title)

        return schedule

    @classmethod
    def get_for_chair(cls, chair, *args, **kwargs):
        raspis = Raspis.query.outerjoin(Raspnagr, Raspnagr.id == Raspis.raspnagr_id).filter(
            Raspnagr.kaf_id == chair.id,
            Raspnagr.sem == g.settings.semester
        )

        return cls._get_table(raspis, *args, **kwargs)

    @classmethod
    def get_for_kontgrp(cls, kontgrp, *args, **kwargs):
        raspis = Raspis.query.filter(
            or_(
                Raspis.raspnagr.has(and_(
                    Raspnagr.kontgrp_id == 0,
                    Raspnagr.kontkurs_id == kontgrp.kont_id
                )),
                Raspis.raspnagr.has(kontgrp_id=kontgrp.id),
                Raspis.raspnagr.has(and_(
                    Raspnagr.kontgrp.has(kont_id=kontgrp.kont_id),
                    Raspnagr.kontgrp.has(or_(
                        and_(
                            Kontgrp.depth < kontgrp.depth,
                            or_(
                                Kontgrp.id == kontgrp.parent_id,
                                Kontgrp.children.any(id=kontgrp.parent_id),
                            ),
                        ),
                        and_(
                            Kontgrp.depth > kontgrp.depth,
                            Kontgrp.parent_id == kontgrp.id,
                        )
                    )),
                )),
                Raspis.raspnagr.has(Raspnagr.kontlist.any(kontkurs_id=kontgrp.kont_id)),
                Raspis.raspnagr.has(Raspnagr.kontgrplist.any(kontgrp_id=kontgrp.id)),
            )
        )

        return cls._get_table(raspis, *args, **kwargs)

    @classmethod
    def get_for_kontkurs(cls, kontkurs, subgroup_number, *args, **kwargs):
        # Kontgrp2 = aliased(Kontgrp)
        #
        Kontkurs2 = aliased(Kontkurs)
        Kontgrp2 = aliased(Kontgrp)
        KontgrpCommon = aliased(Kontgrp)
        KontgrpParent = aliased(Kontgrp)

        if int(subgroup_number):
            filter_ = and_(or_(
                Raspnagr.kontkurs_id == kontkurs.id,
                Kontlist.kontkurs_id == kontkurs.id,
                KontgrpCommon.kont_id == kontkurs.id,
            ), or_(
                KontgrpCommon.id == None,
                and_(KontgrpParent.id == None, KontgrpCommon.ngroup == subgroup_number),
                KontgrpParent.ngroup == subgroup_number
            ), )
        else:
            filter_ = or_(
                Raspnagr.kontkurs_id == kontkurs.id,
                KontgrpCommon.kont_id == kontkurs.id,
                Kontkurs2.id == kontkurs.id,
            )

        raspis = Raspis.query \
            .join(Raspnagr) \
            .outerjoin(Kontgrp, Raspnagr.kontgrp_id == Kontgrp.id) \
            .outerjoin(Kontgrplist, Kontgrplist.op == Raspnagr.op) \
            .outerjoin(Kontlist, Kontlist.op == Raspnagr.op) \
            .outerjoin(Kontkurs2, Kontkurs2.id == Kontlist.kontkurs_id) \
            .outerjoin(Kontgrp2, Kontgrp2.id == Kontgrplist.kontgrp_id) \
            .outerjoin(KontgrpCommon, func.coalesce(Kontgrp2.id, Kontgrp.id) == KontgrpCommon.id) \
            .outerjoin(KontgrpParent, KontgrpCommon.parent_id == KontgrpParent.id) \
            .filter(filter_)

        return cls._get_table(raspis, *args, **kwargs)

    @classmethod
    def get_for_auditory(cls, auditory, *args, **kwargs):
        raspis = Raspis.query.filter(
            Raspis.aud_id == auditory.id
        )

        return cls._get_table(raspis, *args, **kwargs)

    @classmethod
    def get_for_teacher(cls, teacher, *args, **kwargs):
        raspis = Raspis.query.filter(
            or_(
                Raspis.raspnagr.has(prep_id=teacher.id),
            )
        )

        return cls._get_table(raspis, *args, **kwargs)

    @classmethod
    def get_for_discipline(cls, discipline, *args, **kwargs):
        raspis = Raspis.query.filter(
            or_(
                Raspis.raspnagr.has(pred_id=discipline.id),
            )
        )

        return cls._get_table(raspis, *args, **kwargs)


class RaspisZaoch(db.Model):
    TYPES = {
        1: 'exam',
        2: 'kurs',
    }

    id = db.Column('id', db.Integer, primary_key=True)
    para = db.Column("para", db.SmallInteger)
    dt = db.Column('dt', db.DateTime)
    date_created = db.Column('date_created', db.DateTime)
    hours = db.Column("hours", db.SmallInteger)
    aud = db.Column("aud", db.Integer, db.ForeignKey('auditories.id_60'))
    aud2 = db.Column("aud2", db.Integer, db.ForeignKey('auditories.id_60'))
    teacher_id = db.Column("teacher", db.Integer, db.ForeignKey('prepods.id_61'))
    kont_id = db.Column("kont", db.Integer, db.ForeignKey('kontkurs.id_1'))
    kontgrp_id = db.Column("kontgrp", db.Integer, db.ForeignKey('kontgrp.id_7'))
    op_id = db.Column("op", db.Integer, db.ForeignKey('potoklist.id_8'))
    raspnagr_id = db.Column("raspnagr", db.Integer, db.ForeignKey('raspnagr.id_51'))
    type = db.Column('type', db.SmallInteger)

    @classmethod
    def get_for_kontkurs_id(cls, kontkurs_id, sem, subgroup_numbers=None):
        if subgroup_numbers is None:
            subgroup_numbers = []

        subgroup_numbers_ids = []
            # numbers = item.split('-')
            # subgroup_numbers_ids.append(numbers[0], numbers[1] if len(numbers) > 0 else None)

        Kontgrp2 = aliased(Kontgrp)
        KontgrpCommon = aliased(Kontgrp)
        KontgrpParent = aliased(Kontgrp)
        KontgrpChild = aliased(Kontgrp)

        if len(subgroup_numbers) and subgroup_numbers[0] != '0':
            conditions_common = []
            conditions_parent = []
            for item in subgroup_numbers:
                c = item.split('-')
                if len(c) > 1:
                    conditions_common.append(and_(KontgrpCommon.ngroup==c[0], KontgrpChild.ngroup==c[1]))
                    conditions_parent.append(and_(KontgrpParent.ngroup==c[0], KontgrpCommon.ngroup==c[1]))
                else:
                    conditions_common.append(KontgrpCommon.ngroup == c[0])
                    conditions_parent.append(KontgrpParent.ngroup == c[0])

            filter_ = and_(or_(
                Raspnagr.kontkurs_id == kontkurs_id,
                Kontlist.kontkurs_id == kontkurs_id,
                KontgrpCommon.kont_id == kontkurs_id,
            ), or_(
                KontgrpCommon.id == None,
                and_(KontgrpParent.id == None, or_(*conditions_common)),
                or_(*conditions_parent)
            ))
        else:
            filter_ = func.coalesce(Kontlist.kontkurs_id, KontgrpCommon.kont_id, Raspnagr.kontkurs_id) == kontkurs_id

        zaoch = RaspisZaoch.query.with_entities(RaspisZaoch.id) \
            .outerjoin(Raspnagr, Raspnagr.id == RaspisZaoch.raspnagr_id) \
            .outerjoin(Kontlist, Kontlist.op == Raspnagr.op) \
            .outerjoin(Kontgrplist, Kontgrplist.op == Raspnagr.op) \
            .outerjoin(Kontgrp, Kontgrp.id == Kontgrplist.kontgrp_id) \
            .outerjoin(Kontgrp2, Raspnagr.kontgrp_id == Kontgrp2.id) \
            .outerjoin(KontgrpCommon, func.coalesce(Kontgrp.id, Kontgrp2.id) == KontgrpCommon.id) \
            .outerjoin(KontgrpParent, KontgrpCommon.parent_id == KontgrpParent.id) \
            .outerjoin(KontgrpChild, KontgrpChild.parent_id == KontgrpCommon.id) \
            .filter(filter_) \
            .filter(Raspnagr.sem == sem)

        result = RaspisZaoch.query.filter(
            RaspisZaoch.id.in_(zaoch)
        )

        return result

    @classmethod
    def query_with_konts(self):
        return RaspisZaoch.query.outerjoin(Kontkurs, Kontkurs.id == RaspisZaoch.kont_id) \
            .outerjoin(Kontgrp, Kontgrp.id == RaspisZaoch.kontgrp_id) \
            .outerjoin(Potoklist, Potoklist.op == RaspisZaoch.op_id)

    @classmethod
    def get_common_data(self):
        Auditory2 = aliased(Auditory)

        return RaspisZaoch.query \
            .outerjoin(Raspnagr, Raspnagr.id == RaspisZaoch.raspnagr_id) \
            .outerjoin(Auditory, RaspisZaoch.aud == Auditory.id) \
            .outerjoin(Auditory2, RaspisZaoch.aud2 == Auditory2.id) \
            .outerjoin(Teacher, Teacher.id == Raspnagr.prep_id) \
            .outerjoin(Discipline) \
            .outerjoin(Normtime) \
            .outerjoin(Kontgrp, Raspnagr.kontgrp_id == Kontgrp.id) \
            .outerjoin(Kontkurs, Raspnagr.kontkurs_id == Kontkurs.id) \
            .outerjoin(Potoklist, Raspnagr.op == Potoklist.op) \
            .order_by(RaspisZaoch.dt,
                      RaspisZaoch.para) \
            .with_entities(
            RaspisZaoch.id,
            RaspisZaoch.raspnagr_id,
            RaspisZaoch.dt,
            RaspisZaoch.para,
            RaspisZaoch.aud,
            RaspisZaoch.aud2,
            RaspisZaoch.kont_id,
            RaspisZaoch.kontgrp_id,
            RaspisZaoch.op_id,
            RaspisZaoch.type,
            RaspisZaoch.hours,
            Auditory.maxstud,
            Auditory2.maxstud.label('maxstud2'),
            Raspnagr.prep_id,
            Raspnagr.stud,
            Raspnagr.nt,
            func.rtrim(Normtime.title).label('normtime'),
            func.rtrim(Teacher.name).label("teacher"),
            func.rtrim(Auditory.title).label("auditory"),
            func.rtrim(Auditory2.title).label("auditory2"),
            func.rtrim(Discipline.title).label("discipline"),
            func.coalesce(Potoklist.title, Kontgrp.title, Kontkurs.title).label('konts')
        )

    @classmethod
    def get_common_data_format(cls, item):
        return {
            'id': item.raspnagr_id,
            'raspis_id': item.id,
            'dt': "{:%Y-%m-%d}".format(item.dt),
            'para': item.para,
            'aud': item.aud,
            'aud2': item.aud2,
            'hours': item.hours,
            'maxstud': item.maxstud,
            'maxstud2': item.maxstud2,
            'auditory': item.auditory,
            'auditory2': item.auditory2,
            'type': item.type,
        }


class Classifier(db.Model):
    id = db.Column('id_', db.Integer, primary_key=True)
    class_id = db.Column("class_id", db.SmallInteger)
    title = db.Column("val_", db.String(50))


class WishAudd(db.Model):
    __tablename__ = "wishaudd"

    id = db.Column('id_62', db.Integer, primary_key=True)
    aud = db.Column("aud", db.Integer, db.ForeignKey('auditories.id_60'))
    dayofweek = db.Column("dayofweek", db.SmallInteger)
    everyweek = db.Column("everyweek", db.SmallInteger)
    wishview = db.Column("wishview", db.SmallInteger)
    parasps = db.Column(db.String(20))


class WishAuddPara(db.Model):
    __tablename__ = "wishauddpara"

    wish = db.Column("wish", db.Integer, db.ForeignKey('wishaudd.id_62'), primary_key=True)
    para = db.Column("para", db.SmallInteger)

    wish_instance = db.relationship('WishAudd', backref=db.backref('pairs', lazy='joined'))


class WishKontd(db.Model):
    __tablename__ = 'wishkontd'

    id = db.Column("id_69", db.Integer, primary_key=True)
    kont = db.Column(db.Integer)
    kontid = db.Column(db.Integer)
    dayofweek = db.Column("dayofweek", db.SmallInteger)
    everyweek = db.Column("everyweek", db.SmallInteger)
    wishview = db.Column("wishview", db.SmallInteger)
    parasps = db.Column(db.String(20))


class WishKontdPara(db.Model):
    __tablename__ = "wishkontdpara"
    __table_args__ = (
        PrimaryKeyConstraint('wish', 'para'),
    )

    wish = db.Column("wish", db.Integer)
    para = db.Column("para", db.SmallInteger)


class AudActions(db.Model):
    __tablename__ = "aud_actions"

    id = db.Column('id', db.Integer, primary_key=True)
    aud = db.Column("aud_id", db.Integer, db.ForeignKey('auditories.id_60'))
    aud_to = db.Column("aud_to_id", db.Integer, db.ForeignKey('auditories.id_60'))
    kont = db.Column(db.Integer)
    action = db.Column(db.SmallInteger)
    comment = db.Column(db.String(100))
    prep_id = db.Column(db.Integer, db.ForeignKey('prepods.id_61'))
    date = db.Column(db.DateTime)
    para = db.Column(db.SmallInteger)
    para_count = db.Column(db.SmallInteger)


class Disp(db.Model):
    __tablename__ = "vacdisp"

    id = db.Column("id_75", db.Integer, primary_key=True)
    title = db.Column("disp", db.String(50))


class OwnRes(db.Model):
    __tablename__ = "ownres"

    id = db.Column("id_71", db.Integer, primary_key=True)
    objid = db.Column("objid", db.Integer)
    owner = db.Column("ownerid", db.Integer, db.ForeignKey("vacdisp.id_75"))


class Zansps(db.Model):
    __tablename__ = "zansps"

    id = db.Column("id_54", db.Integer, primary_key=True)
    zants = db.Column(db.Integer, db.ForeignKey("zanlist.zants"))
    prop1 = db.Column(db.SmallInteger, default=0)
    prop2 = db.Column(db.SmallInteger, default=0)
    prop3 = db.Column(db.SmallInteger, default=0)
    prop4 = db.Column(db.SmallInteger, default=0)
    prop5 = db.Column(db.SmallInteger, default=0)
    prop6 = db.Column(db.SmallInteger, default=0)
    prop7 = db.Column(db.SmallInteger, default=0)
    prop8 = db.Column(db.SmallInteger, default=0)
    prop9 = db.Column(db.SmallInteger, default=0)
    prop10 = db.Column(db.SmallInteger, default=0)
    prop11 = db.Column(db.SmallInteger, default=0)
    prop12 = db.Column(db.SmallInteger, default=0)
    prop13 = db.Column(db.SmallInteger, default=0)
    prop14 = db.Column(db.SmallInteger, default=0)
    prop15 = db.Column(db.SmallInteger, default=0)
    prop16 = db.Column(db.SmallInteger, default=0)
    prop17 = db.Column(db.SmallInteger, default=0)
    prop18 = db.Column(db.SmallInteger, default=0)
    prop19 = db.Column(db.SmallInteger, default=0)


class Zanlist(db.Model):
    __tablename__ = "zanlist"
    # __mapper_args__ = {
    #     'primary_key': ['zanlist.zants', 'zanlist.zan']
    # }

    zants = db.Column(db.Integer, db.ForeignKey("zansps.id_54"), primary_key=True)
    raspnagr_id = db.Column("zan", db.Integer, db.ForeignKey("raspnagr.id_51"))
"""
Copyright 2012 Jan Demter <jan@demter.de>

This file is part of LODStatsWWW.

LODStats is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LODStats is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LODStats.  If not, see <http://www.gnu.org/licenses/>.
"""
"""The application's model objects"""
from datetime import datetime
from rdfstats.model.meta import Session, Base
from sqlalchemy import schema, types, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects import postgresql

from formalchemy import FieldSet
from formalchemy import validators

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

def now():
    return datetime.now()

class _BaseMixin(object):
    """
    A helper mixin class to set properties on object creation.

    Also provides a convenient default __repr__() function, but be aware that
    also relationships are printed, which might result in loading the relation
    objects from the database
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "<%s(%s)>" % (self.__class__.__name__,
            ', '.join('%s=%r' % (k, self.__dict__[k])
                      for k in sorted(self.__dict__)
                      if '_' != k[0]
                      #if '_sa_' != k[:4] and '_backref_' != k[:9]
                      )
            )

class RDFDoc(Base, _BaseMixin):
    __tablename__ ='rdfdoc'

    id = schema.Column(types.Integer, schema.Sequence('rdfdoc_sq_id', optional=True), primary_key=True)
    uri = schema.Column(types.Text())
    name = schema.Column(types.Unicode(255)) # (as in ckan)
    format = schema.Column(types.Unicode(255)) # nt, rdf, n3, nquads, turtle
    last_updated = schema.Column(types.DateTime())
    worked_on = schema.Column(types.Boolean, default=False)
    stats = relationship("StatResult", backref="rdfdoc", primaryjoin="RDFDoc.id==StatResult.rdfdoc_id")
    current_stats_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id',
                        use_alter=True, name='fk_rdfdoc_current_stats_id'))
    file_last_modified = schema.Column(types.DateTime())
    in_datahub = schema.Column(types.Boolean)
    ckan_catalog = schema.Column(types.Text(), schema.ForeignKey('ckan_catalog.name', 
                        use_alter=True, name='rdfdoc_ckan_catalog_fkey'))
    active = schema.Column(types.Boolean, default=True)

    def reset_current_stats_and_worker(self):
        if self.current_stats is not None:
            self.current_stats.prep_delete()
            Session.commit()
            Session.delete(self.current_stats)
            Session.commit()
        if self.worker is not None:
            Session.delete(self.worker)
        self.last_updated=None
        self.file_last_modified=None
        self.worked_on=False
        Session.commit()

class WorkerProc(Base, _BaseMixin):
    __tablename__ = 'worker_proc'

    id = schema.Column(types.Integer, schema.Sequence('worker_proc_sq_id', optional=True), primary_key=True)
    pid = schema.Column(types.Integer())
    rdfdoc_id = schema.Column(types.Integer(), schema.ForeignKey('rdfdoc.id'), nullable=False)
    rdfdoc = relationship("RDFDoc", backref=backref("worker", uselist=False))
    started = schema.Column(types.DateTime(), default=now())

# rdf_class_stat_table = Table('rdf_class_stat_result', Base.metadata,
#             schema.Column('stat_result_id', types.Integer, schema.ForeignKey('stat_result.id')),
#             schema.Column('rdf_class_id', types.Integer, schema.ForeignKey('rdf_class.id')))
class RDFClassStat(Base, _BaseMixin):
    __tablename__ = 'rdf_class_stat_result'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    rdf_class_id = schema.Column(types.Integer(), schema.ForeignKey('rdf_class.id'), primary_key=True)
    count = schema.Column(types.BigInteger())
    rdf_class = relationship("RDFClass", backref="stat_result_assocs")
    stat_result = relationship("StatResult", backref="rdf_class_assocs")

from StatResult import StatResult

class RDFClass(Base, _BaseMixin):
    __tablename__ = 'rdf_class'
    id = schema.Column(types.Integer, schema.Sequence('rdf_class_sq_id', optional=True), primary_key=True)
    name = schema.Column(types.Text())
    uri = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(rdf_class=s))

class RDFVocabStat(Base, _BaseMixin):
    __tablename__ = 'rdf_vocab_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="vocab_assocs")
    vocab_id = schema.Column(types.Integer(), schema.ForeignKey('vocab.id'), primary_key=True)
    vocab = relationship("Vocab", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class Vocab(Base, _BaseMixin):
    __tablename__ = 'vocab'
    id = schema.Column(types.Integer, schema.Sequence('vocab_sq_id', optional=True), primary_key=True)
    uri = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(vocab=s))

class RDFPropertyStat(Base, _BaseMixin):
    __tablename__ = 'rdf_property_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="rdf_property_assocs")
    rdf_property_id = schema.Column(types.Integer(), schema.ForeignKey('rdf_property.id'), primary_key=True)
    rdf_property = relationship("RDFProperty", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class RDFProperty(Base, _BaseMixin):
    __tablename__ = 'rdf_property'
    id = schema.Column(types.Integer, schema.Sequence('rdf_property_sq_id', optional=True), primary_key=True)
    uri = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(rdf_property=s))

class DefinedClassStat(Base, _BaseMixin):
    __tablename__ = 'defined_class_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="defined_class_assocs")
    defined_class_id = schema.Column(types.Integer(), schema.ForeignKey('defined_class.id'), primary_key=True)
    defined_class = relationship("DefinedClass", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class DefinedClass(Base, _BaseMixin):
    __tablename__ = 'defined_class'
    id = schema.Column(types.Integer, schema.Sequence('defined_class_sq_id', optional=True), primary_key=True)
    uri = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(defined_class=s))

class RDFDatatypeStat(Base, _BaseMixin):
    __tablename__ = 'rdf_datatype_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="rdf_datatype_assocs")
    rdf_datatype_id = schema.Column(types.Integer(), schema.ForeignKey('rdf_datatype.id'), primary_key=True)
    rdf_datatype = relationship("RDFDatatype", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class RDFDatatype(Base, _BaseMixin):
    __tablename__ = 'rdf_datatype'
    id = schema.Column(types.Integer, schema.Sequence('rdf_datatype_sq_id', optional=True), primary_key=True)
    uri = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(rdf_datatype=s))

class LanguageStat(Base, _BaseMixin):
    __tablename__ = 'language_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="language_assocs")
    language_id = schema.Column(types.Integer(), schema.ForeignKey('language.id'), primary_key=True)
    language = relationship("Language", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class Language(Base, _BaseMixin):
    __tablename__ = 'language'
    id = schema.Column(types.Integer, schema.Sequence('language_sq_id', optional=True), primary_key=True)
    code = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(language=s))

class LinkStat(Base, _BaseMixin):
    __tablename__ = 'link_stat'
    stat_result_id = schema.Column(types.Integer(), schema.ForeignKey('stat_result.id'), primary_key=True)
    stat_result = relationship("StatResult", backref="link_assocs")
    link_id = schema.Column(types.Integer(), schema.ForeignKey('link.id'), primary_key=True)
    link = relationship("Link", backref="stat_result_assocs")
    count = schema.Column(types.BigInteger())

class Link(Base, _BaseMixin):
    __tablename__ = 'link'
    id = schema.Column(types.Integer, schema.Sequence('link_sq_id', optional=True), primary_key=True)
    code = schema.Column(types.Text())
    s_ns = schema.Column(types.Text())
    o_ns = schema.Column(types.Text())
    stat_result = association_proxy('stat_result_assocs', 'stat_result', creator=lambda s: StatResult(link=s))

class PropertyLabeled(Base, _BaseMixin):
    __tablename__ = 'rdf_property_label'
    id = schema.Column(types.Integer, schema.Sequence('rdf_property_label_id_seq', optional=True), primary_key=True)
    label_en = schema.Column(types.Text())
    uri = schema.Column(types.Text())
    count = schema.Column(types.Integer)
    rdf_property_id = schema.Column(types.Integer)
    label_en_index_col = schema.Column(postgresql.TSVECTOR)

class CkanCatalog(Base, _BaseMixin):
    __tablename__ = 'ckan_catalog'
    name = schema.Column(types.Text(), primary_key=True)
    api_url = schema.Column(types.Text())

# formalchemy
RDFDoc_fa = FieldSet(RDFDoc)
RDFDoc_fa.configure(options=[RDFDoc_fa.uri.label('URI of the dataset')])
RDFDoc_fa.configure(options=[RDFDoc_fa.uri.validate(validators.required)])

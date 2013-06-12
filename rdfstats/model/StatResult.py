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
from rdfstats.model.meta import Session, Base
from rdfstats.model import _BaseMixin

from sqlalchemy import schema, types, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

class StatResult(Base, _BaseMixin):
    __tablename__ = 'stat_result'
    
    id = schema.Column(types.Integer, schema.Sequence('stat_result_sq_id', optional=True), primary_key=True)
    void = schema.Column(types.Text())
    triples = schema.Column(types.BigInteger())
    last_updated = schema.Column(types.DateTime())
    triples_done = schema.Column(types.BigInteger())
    has_errors = schema.Column(types.Boolean)
    errors = schema.Column(types.Text())
    warnings = schema.Column(types.BigInteger())
    last_warning = schema.Column(types.Text())
    worked_on = schema.Column(types.Boolean, default=False)
    bytes = schema.Column(types.BigInteger())
    bytes_download = schema.Column(types.BigInteger())
    content_length = schema.Column(types.BigInteger())
    entities = schema.Column(types.BigInteger())
    literals = schema.Column(types.BigInteger())
    blanks = schema.Column(types.BigInteger())
    blanks_as_object = schema.Column(types.BigInteger())
    blanks_as_subject = schema.Column(types.BigInteger())
    subclasses = schema.Column(types.BigInteger())
    typed_subjects = schema.Column(types.BigInteger())
    labeled_subjects = schema.Column(types.BigInteger())
    class_hierarchy_depth = schema.Column(types.BigInteger())
    property_hierarchy_depth = schema.Column(types.BigInteger())
    properties_per_entity = schema.Column(types.Float())
    string_length_typed = schema.Column(types.Float())
    string_length_untyped = schema.Column(types.Float())
    links = schema.Column(types.BigInteger())
    rdfdoc_id = schema.Column(types.Integer(), schema.ForeignKey('rdfdoc.id'), nullable=False)
    current_of = relationship("RDFDoc", backref="current_stats", uselist=False,
        primaryjoin="RDFDoc.current_stats_id==StatResult.id", post_update=True)
    classes = association_proxy('rdf_class_assocs', 'rdf_class', creator=lambda s: RDFClass(stat_result=s))
    vocabs = association_proxy('vocab_assocs', 'vocab', creator=lambda s: Vocab(stat_result=s))
    properties = association_proxy('rdf_property_assocs', 'rdf_property', creator=lambda s: RDFProperty(stat_result=s))
    defined_classes = association_proxy('defined_class_assocs', 'defined_class', creator=lambda s: DefinedClass(stat_result=s))
    rdf_datatypes = association_proxy('rdf_datatype_assocs', 'rdf_datatype', creator=lambda s: RDFDatatype(stat_result=s))
    languages = association_proxy('language_assocs', 'language', creator=lambda s: Language(stat_result=s))
    links_all = association_proxy('link_assocs', 'link', creator=lambda s: Link(stat_result=s))
    
    def prep_delete(self):
        for c in self.rdf_class_assocs:
            Session.delete(c)
        for v in self.vocab_assocs:
            Session.delete(v)
        for p in self.rdf_property_assocs:
            Session.delete(p)
        for dc in self.defined_class_assocs:
            Session.delete(dc)
        for rd in self.rdf_datatype_assocs:
            Session.delete(rd)
        for l in self.language_assocs:
            Session.delete(l)
        for li in self.link_assocs:
            Session.delete(li)
    
    def json_dict(self):
        json_dict = {}
        json_dict['triples'] = self.triples
        json_dict['last_updated'] = unicode(self.last_updated)
        json_dict['has_errors'] = self.has_errors
        json_dict['errors'] = self.errors
        json_dict['warnings'] = self.warnings
        json_dict['last_warning'] = self.last_warning
        json_dict['bytes'] = self.bytes
        json_dict['entities'] = self.entities
        json_dict['literals'] = self.literals
        json_dict['blanks'] = self.blanks
        json_dict['blanks_as_object'] = self.blanks_as_object
        json_dict['blanks_as_subject'] = self.blanks_as_subject
        json_dict['subclasses'] = self.subclasses
        json_dict['typed_subjects'] = self.typed_subjects
        json_dict['labeled_subjects'] = self.labeled_subjects
        json_dict['class_hierarchy_depth'] = self.class_hierarchy_depth
        json_dict['property_hierarchy_depth'] = self.property_hierarchy_depth
        json_dict['properties_per_entity'] = self.properties_per_entity
        json_dict['string_length_typed'] = self.string_length_typed
        json_dict['string_length_untyped'] = self.string_length_untyped
        json_dict['links'] = self.links
        return json_dict

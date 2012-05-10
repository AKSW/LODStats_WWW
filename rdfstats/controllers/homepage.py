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
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.cache import beaker_cache

from rdfstats.lib.base import BaseController, render, Session
from sqlalchemy import func, and_, or_, desc

from rdfstats import model

log = logging.getLogger(__name__)

class HomepageController(BaseController):

    def home(self):
        c.rdfdocs = Session.query(model.RDFDoc).order_by(model.RDFDoc.worked_on.desc(), model.RDFDoc.name, model.RDFDoc.last_updated.desc(), ).all()
        c.rdfdoc_count = len(c.rdfdocs)
        c.workers = Session.query(model.WorkerProc).order_by(model.WorkerProc.started.desc()).all()
        c.no_of_rdfdocs_with_triples = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.StatResult.triples > 0).count()
        c.sparql_packages = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format == "sparql").count()
        c.dump_packages = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format != "sparql").count()
        c.error_packages_dump = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.errors != None,
                    model.RDFDoc.format != 'sparql',
                    model.RDFDoc.format != None
                )).count()
        c.error_packages_sparql = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.errors != None,
                    model.RDFDoc.format == 'sparql',
                    model.RDFDoc.format != None
                )).count()
        c.problem_packages = c.error_packages_sparql + c.error_packages_dump
        c.touched_packages = c.no_of_rdfdocs_with_triples+c.problem_packages
        c.triples_dump = Session.query(func.sum(model.StatResult.triples)).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format != "sparql").scalar()
        c.triples_sparql = Session.query(func.sum(model.StatResult.triples)).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format == "sparql").scalar()
        if c.triples_dump is None:
            c.triples_dump = 0
        if c.triples_sparql is None:
            c.triples_sparql = 0
        # most recent successful updates
        c.recent_updates = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.last_updated!=None,
                    model.StatResult.errors==None,
                    model.RDFDoc.last_updated!=None,
                )
                ).order_by(desc(model.RDFDoc.last_updated))[:5]
        # most recent updates with errors
        c.recent_updates_errors = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.last_updated!=None,
                    model.StatResult.errors!=None,
                    model.RDFDoc.last_updated!=None,
                )
                ).order_by(desc(model.RDFDoc.last_updated))[:5]
        return render('/home.html')
    
    @beaker_cache(expire=86400)
    def stats(self):
        c.rdfdocs = Session.query(model.RDFDoc).order_by(model.RDFDoc.worked_on.desc(), model.RDFDoc.name, model.RDFDoc.last_updated.desc(), ).all()
        c.rdfdoc_count = len(c.rdfdocs)
        c.workers = Session.query(model.WorkerProc).order_by(model.WorkerProc.started.desc()).all()
        c.no_of_rdfdocs_with_triples = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.StatResult.triples > 0).count()
        c.sparql_packages = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format == "sparql").count()
        c.dump_packages = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format != "sparql").count()
        c.error_packages_dump = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.errors != None,
                    model.RDFDoc.format != 'sparql',
                    model.RDFDoc.format != None
                )).count()
        c.error_packages_sparql = Session.query(model.RDFDoc).join(model.RDFDoc.current_stats).filter(
                and_(
                    model.StatResult.errors != None,
                    model.RDFDoc.format == 'sparql',
                    model.RDFDoc.format != None
                )).count()
        c.problem_packages = c.error_packages_sparql + c.error_packages_dump
        c.touched_packages = c.no_of_rdfdocs_with_triples+c.problem_packages
        c.triples_dump = Session.query(func.sum(model.StatResult.triples)).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format != "sparql").scalar()
        c.triples_sparql = Session.query(func.sum(model.StatResult.triples)).join(model.RDFDoc.current_stats).filter(model.RDFDoc.format == "sparql").scalar()
        if c.triples_dump is None:
            c.triples_dump = 0
        if c.triples_sparql is None:
            c.triples_sparql = 0
        vocabs = Session.query(model.Vocab).join(model.RDFVocabStat).join(model.StatResult).filter(
                model.StatResult.current_of!=None).all()
        c.vocabs = len(vocabs)
        rdf_classes = Session.query(model.RDFClass).join(model.RDFClassStat).join(model.StatResult).filter(
                model.StatResult.current_of!=None).all()
        c.rdf_classes = len(rdf_classes)
        c.properties = Session.query(model.RDFProperty).join(model.RDFPropertyStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).count()
        #c.properties = len(properties)
        c.datatypes = Session.query(model.RDFDatatype).join(model.RDFDatatypeStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).count()
        c.link_count = Session.query(model.Link).join(model.LinkStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).count()
        c.languages = Session.query(func.count(model.Language.id)).join(model.LanguageStat).join(model.StatResult).filter(
            model.StatResult.current_of!=None).scalar()
        # most common vocab
        stmt="SELECT count(rdf_vocab_stat.count) AS counter, vocab.uri AS uri, vocab.id AS id FROM rdf_vocab_stat,stat_result,rdfdoc,vocab \
            WHERE rdf_vocab_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and vocab.id=rdf_vocab_stat.vocab_id GROUP BY vocab.uri, vocab.id ORDER BY counter DESC LIMIT 5"
        c.v_usage = Session.query('uri', 'id', 'counter').from_statement(stmt).all()
        # most common classes
        stmt="SELECT count(rdf_class_stat_result.count) AS counter,rdf_class.uri, rdf_class.id FROM \
            rdf_class_stat_result,stat_result,rdfdoc,rdf_class WHERE \
            rdf_class_stat_result.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_class.id=rdf_class_stat_result.rdf_class_id GROUP BY rdf_class.uri, rdf_class.id ORDER BY counter DESC LIMIT 5"
        c.c_usage = Session.query('uri', 'id', 'counter').from_statement(stmt).all()
        # most common properties
        stmt="SELECT count(rdf_property_stat.count) AS counter,rdf_property.uri, rdf_property.id FROM \
            rdf_property_stat,stat_result,rdfdoc,rdf_property WHERE \
            rdf_property_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_property.id=rdf_property_stat.rdf_property_id GROUP BY rdf_property.uri, rdf_property.id ORDER BY counter DESC LIMIT 5"
        c.p_usage = Session.query('uri', 'id', 'counter').from_statement(stmt).all()
        # most common datatypes
        stmt="SELECT count(rdf_datatype_stat.count) AS counter,rdf_datatype.uri, rdf_datatype.id FROM \
            rdf_datatype_stat,stat_result,rdfdoc,rdf_datatype WHERE \
            rdf_datatype_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_datatype.id=rdf_datatype_stat.rdf_datatype_id GROUP BY rdf_datatype.uri, rdf_datatype.id ORDER BY counter DESC LIMIT 5"
        c.t_usage = Session.query('uri', 'id', 'counter').from_statement(stmt).all()
        # most common languages
        stmt="SELECT count(language_stat.count) AS counter,language.code, language.id FROM \
            language_stat,stat_result,rdfdoc,language WHERE \
            language_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and language.id=language_stat.language_id GROUP BY language.code, language.id ORDER BY counter DESC LIMIT 5"
        c.l_usage = Session.query('code', 'id', 'counter').from_statement(stmt).all()
        # most common linksets
        stmt="SELECT count(link_stat.count) AS counter,link.code, link.id FROM \
            link_stat,stat_result,rdfdoc,link WHERE \
            link_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and link.id=link_stat.link_id GROUP BY link.code, link.id ORDER BY counter DESC LIMIT 5"
        c.link_usage = Session.query('code', 'id', 'counter').from_statement(stmt).all()
        # absolute Summen
        # most commons vocab absolut
        stmt="SELECT sum(rdf_vocab_stat.count) AS sum, vocab.uri AS uri, vocab.id FROM rdf_vocab_stat,stat_result,rdfdoc,vocab \
            WHERE rdf_vocab_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and vocab.id=rdf_vocab_stat.vocab_id GROUP BY vocab.uri, vocab.id ORDER BY sum DESC LIMIT 5"
        c.v_sum = Session.query('uri', 'id', 'sum').from_statement(stmt).all()
        # most common classes absolut
        stmt="SELECT sum(rdf_class_stat_result.count) AS sum,rdf_class.uri, rdf_class.id FROM \
            rdf_class_stat_result,stat_result,rdfdoc,rdf_class WHERE \
            rdf_class_stat_result.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_class.id=rdf_class_stat_result.rdf_class_id GROUP BY rdf_class.uri, rdf_class.id ORDER BY sum DESC LIMIT 5"
        c.c_sum = Session.query('uri', 'id', 'sum').from_statement(stmt).all()
        # most common properties
        stmt="SELECT sum(rdf_property_stat.count) AS sum,rdf_property.uri, rdf_property.id FROM \
            rdf_property_stat,stat_result,rdfdoc,rdf_property WHERE \
            rdf_property_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_property.id=rdf_property_stat.rdf_property_id GROUP BY rdf_property.uri, rdf_property.id ORDER BY sum DESC LIMIT 5"
        c.p_sum = Session.query('uri', 'id', 'sum').from_statement(stmt).all()
        # most common datatypes
        stmt="SELECT sum(rdf_datatype_stat.count) AS sum,rdf_datatype.uri, rdf_datatype.id FROM \
            rdf_datatype_stat,stat_result,rdfdoc,rdf_datatype WHERE \
            rdf_datatype_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_datatype.id=rdf_datatype_stat.rdf_datatype_id GROUP BY rdf_datatype.uri, rdf_datatype.id ORDER BY sum DESC LIMIT 5"
        c.t_sum = Session.query('uri', 'id', 'sum').from_statement(stmt).all()
        # most common languages
        stmt="SELECT sum(language_stat.count) AS sum,language.code, language.id FROM \
            language_stat,stat_result,rdfdoc,language WHERE \
            language_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and language.id=language_stat.language_id GROUP BY language.code, language.id ORDER BY sum DESC LIMIT 5"
        c.l_sum = Session.query('code', 'id', 'sum').from_statement(stmt).all()
        stmt="SELECT sum(link_stat.count) AS sum,link.code, link.id FROM \
            link_stat,stat_result,rdfdoc,link WHERE \
            link_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and link.id=link_stat.link_id GROUP BY link.code, link.id ORDER BY sum DESC LIMIT 5"
        c.link_sum = Session.query('code', 'id', 'sum').from_statement(stmt).all()
        # basics
        # entities
        stmt="SELECT avg(stat_result.entities) AS avg, min(stat_result.entities) AS min, max(stat_result.entities) AS max, median(stat_result.entities) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.entities = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # literals
        stmt="SELECT avg(stat_result.literals) AS avg, min(stat_result.literals) AS min, max(stat_result.literals) AS max, median(stat_result.literals) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.literals = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # blanks
        stmt="SELECT avg(stat_result.blanks) AS avg, min(stat_result.blanks) AS min, max(stat_result.blanks) AS max, median(stat_result.blanks) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.blanks = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # blanks as subject
        stmt="SELECT avg(stat_result.blanks_as_subject) AS avg, min(stat_result.blanks_as_subject) AS min, max(stat_result.blanks_as_subject) AS max, median(stat_result.blanks_as_subject) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.blanks_as_subject = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # blanks as object
        stmt="SELECT avg(stat_result.blanks_as_object) AS avg, min(stat_result.blanks_as_object) AS min, max(stat_result.blanks_as_object) AS max, median(stat_result.blanks_as_object) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.blanks_as_object = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # subclasses
        stmt="SELECT avg(stat_result.subclasses) AS avg, min(stat_result.subclasses) AS min, max(stat_result.subclasses) AS max, median(stat_result.subclasses) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.subclasses = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # typed subjects
        stmt="SELECT avg(stat_result.typed_subjects) AS avg, min(stat_result.typed_subjects) AS min, max(stat_result.typed_subjects) AS max, median(stat_result.typed_subjects) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.typed_subjects = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # labeled subjects
        stmt="SELECT avg(stat_result.labeled_subjects) AS avg, min(stat_result.labeled_subjects) AS min, max(stat_result.labeled_subjects) AS max, median(stat_result.labeled_subjects) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.labeled_subjects = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # properties_per_entity
        stmt="SELECT avg(stat_result.properties_per_entity) AS avg, min(stat_result.properties_per_entity) AS min, max(stat_result.properties_per_entity) AS max, median(stat_result.properties_per_entity) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.properties_per_entity = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # string_length_typed
        stmt="SELECT avg(stat_result.string_length_typed) AS avg, min(stat_result.string_length_typed) AS min, max(stat_result.string_length_typed) AS max, median(stat_result.string_length_typed) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.string_length_typed = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # string length untyped
        stmt="SELECT avg(stat_result.string_length_untyped) AS avg, min(stat_result.string_length_untyped) AS min, max(stat_result.string_length_untyped) AS max, median(stat_result.string_length_untyped) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.string_length_untyped = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # class hierarchy
        stmt="SELECT avg(stat_result.class_hierarchy_depth) AS avg, min(stat_result.class_hierarchy_depth) AS min, max(stat_result.class_hierarchy_depth) AS max, median(stat_result.class_hierarchy_depth) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.class_hierarchy_depth = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # property hierarchy
        stmt="SELECT avg(stat_result.property_hierarchy_depth) AS avg, min(stat_result.property_hierarchy_depth) AS min, max(stat_result.property_hierarchy_depth) AS max, median(stat_result.property_hierarchy_depth) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.property_hierarchy_depth = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # links
        stmt="SELECT avg(stat_result.links) AS avg, min(stat_result.links) AS min, max(stat_result.links) AS max, median(stat_result.links) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL"
        c.links = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # triples
        stmt="SELECT avg(stat_result.triples) AS avg, min(stat_result.triples) AS min, max(stat_result.triples) AS max, median(stat_result.triples) AS median FROM \
            stat_result,rdfdoc WHERE \
            rdfdoc.current_stats_id=stat_result.id and stat_result.entities is not NULL and rdfdoc.format!='sparql'"
        c.triples = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # # langs per dataset
        # stmt = "SELECT avg(count), min(count), max(count), median(count) FROM \
        #     (SELECT count(language_stat.count) as count,rdfdoc.id AS rdfd FROM \
        #     language_stat,stat_result,rdfdoc,language WHERE \
        #     language_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
        #     and language.id=language_stat.language_id and stat_result.entities is not NULL GROUP BY rdfdoc.id) as counter"
        # c.dataset_lang = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # vocabs per dataset
        stmt = "SELECT avg(count), min(count), max(count), median(count) FROM \
            (SELECT count(rdf_vocab_stat.count) as count,rdfdoc.id AS rdfd FROM \
            rdf_vocab_stat,stat_result,rdfdoc,vocab WHERE \
            rdf_vocab_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and vocab.id=rdf_vocab_stat.vocab_id and stat_result.entities is not NULL GROUP BY rdfdoc.id) as counter"
        c.dataset_vocab = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # classes per dataset
        stmt = "SELECT avg(count), min(count), max(count), median(count) FROM \
            (SELECT count(rdf_class_stat_result.count) as count,rdfdoc.id AS rdfd FROM \
            rdf_class_stat_result,stat_result,rdfdoc,rdf_class WHERE \
            rdf_class_stat_result.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_class.id=rdf_class_stat_result.rdf_class_id and stat_result.entities is not NULL GROUP BY rdfdoc.id) as counter"
        c.dataset_classes = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        # properties per dataset
        stmt = "SELECT avg(count), min(count), max(count), median(count) FROM \
            (SELECT count(rdf_property_stat.count) as count,rdfdoc.id AS rdfd FROM \
            rdf_property_stat,stat_result,rdfdoc,rdf_property WHERE \
            rdf_property_stat.stat_result_id=stat_result.id and rdfdoc.current_stats_id=stat_result.id \
            and rdf_property.id=rdf_property_stat.rdf_property_id and stat_result.entities is not NULL GROUP BY rdfdoc.id) as counter"
        c.dataset_props = Session.query('avg', 'min', 'max', 'median').from_statement(stmt).one()
        return render('/rdfdoc/stats.html')

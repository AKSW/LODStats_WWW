"""Setup the rdfstats application"""
import logging

import pylons.test

from rdfstats.config.environment import load_environment
from rdfstats.model.meta import Session, Base

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup rdfstats here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)
    
    # Create aggregate functions for median
    dp_median_sql = """CREATE OR REPLACE FUNCTION _final_median(double precision[])
       RETURNS double precision AS
    $$
       SELECT AVG(val)
       FROM (
         SELECT val
         FROM unnest($1) val
         ORDER BY 1
         LIMIT  2 - MOD(array_upper($1, 1), 2)
         OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
       ) sub;
    $$
    LANGUAGE 'sql' IMMUTABLE;

    CREATE AGGREGATE median(double precision) (
      SFUNC=array_append,
      STYPE=double precision[],
      FINALFUNC=_final_median,
      INITCOND='{}'
    );"""
    Session.bind.engine.execute(dp_median_sql)

    median_sql = """CREATE OR REPLACE FUNCTION _final_median(numeric[])
       RETURNS numeric AS
    $$
       SELECT AVG(val)
       FROM (
         SELECT val
         FROM unnest($1) val
         ORDER BY 1
         LIMIT  2 - MOD(array_upper($1, 1), 2)
         OFFSET CEIL(array_upper($1, 1) / 2.0) - 1
       ) sub;
    $$
    LANGUAGE 'sql' IMMUTABLE;

    CREATE AGGREGATE median(numeric) (
      SFUNC=array_append,
      STYPE=numeric[],
      FINALFUNC=_final_median,
      INITCOND='{}'
    );"""
    Session.bind.engine.execute(median_sql)

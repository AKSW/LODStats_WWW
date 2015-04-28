//Query for the rdf_class table
select stat_result.id, rdf_class.uri, rdf_class_stat_result.count from stat_result JOIN rdf_class_stat_result ON rdf_class_stat_result.stat_result_id=stat_result.id JOIN rdf_class ON rdf_class.id=rdf_class_stat_result.rdf_class_id limit 5;

//Query for rdf_datatype table
select stat_result.id, rdf_datatype.uri, rdf_datatype_stat.count from stat_result JOIN rdf_datatype_stat ON rdf_datatype_stat.stat_result_id=stat_result.id JOIN rdf_datatype ON rdf_datatype.id=rdf_datatype_stat.rdf_datatype_id limit 5;

//Query for rdf_property table
select stat_result.id, rdf_property.uri, rdf_property_stat.count from stat_result JOIN rdf_property_stat ON rdf_property_stat.stat_result_id=stat_result.id JOIN rdf_property ON rdf_property.id=rdf_property_stat.rdf_property_id limit 5;

//Query for defined_class table
select stat_result.id, defined_class.uri, defined_class_stat.count from stat_result JOIN defined_class_stat ON defined_class_stat.stat_result_id=stat_result.id JOIN defined_class ON defined_class.id=defined_class_stat.defined_class_id limit 5;

//Query for language table
select stat_result.id, language.code, language_stat.count from stat_result JOIN language_stat ON language_stat.stat_result_id=stat_result.id JOIN language ON language.id=language_stat.language_id limit 5;

//Query for link table
select stat_result.id, link.code, link_stat.count from stat_result JOIN link_stat ON link_stat.stat_result_id=stat_result.id JOIN link ON link.id=link_stat.link_id limit 5;

//Query for vocab table
select stat_result.id, vocab.uri, rdf_vocab_stat.count from stat_result JOIN rdf_vocab_stat ON rdf_vocab_stat.stat_result_id=stat_result.id JOIN vocab ON vocab.id=rdf_vocab_stat.vocab_id limit 5;

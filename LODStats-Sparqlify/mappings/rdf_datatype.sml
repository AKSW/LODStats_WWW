Prefix fn: <http://aksw.org/sparqlify/>
Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
Prefix owl: <http://www.w3.org/2002/07/owl#>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
Prefix ls: <http://lodstats.aksw.org/>
Prefix ls-rdfdocs: <http://lodstats.aksw.org/rdfdocs/>
Prefix ls-statresult: <http://lodstats.aksw.org/stat_result/>
Prefix ls-ontology: <http://lodstats.aksw.org/ontology/ldso.owl#>
Prefix dcterms: <http://purl.org/dc/terms/>
Prefix void: <http://rdfs.org/ns/void#>
Prefix rdf-formats: <http://www.w3.org/ns/formats/>
Prefix dcat: <http://www.w3.org/ns/dcat#>

Create View RdfDatatype As
  Construct {
    ?statresultUri ls-ontology:datatypePartition ?blank .
    ?blank ls-ontology:datatype ?datatype .
    ?blank void:triples ?triples .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?datatype = uri(?uri)
    ?triples = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT rdf_datatype_stat.stat_result_id, 
           concat(rdf_datatype_stat.stat_result_id,
           rdf_datatype_stat.rdf_datatype_id, 'datatype') AS compoundkey,
           rdf_datatype.uri, 
           rdf_datatype_stat.count 
    FROM stat_result 
    JOIN rdf_datatype_stat 
      ON rdf_datatype_stat.stat_result_id=stat_result.id 
    JOIN rdf_datatype 
      ON rdf_datatype.id=rdf_datatype_stat.rdf_datatype_id 
  ]] 



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

Create View RdfProperty As
  Construct {
    ?statresultUri void:propertyPartition ?blank .
    ?blank void:property ?property .
    ?blank void:triples ?triples .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?property = uri(?uri)
    ?triples = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT rdf_property_stat.stat_result_id, 
           concat(rdf_property_stat.stat_result_id,
           rdf_property_stat.rdf_property_id, 'property') AS compoundkey,
           rdf_property.uri, 
           rdf_property_stat.count 
    FROM stat_result 
    JOIN rdf_property_stat 
      ON rdf_property_stat.stat_result_id=stat_result.id 
    JOIN rdf_property 
      ON rdf_property_stat.rdf_property_id=rdf_property.id
  ]] 

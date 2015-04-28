Prefix fn: <http://aksw.org/sparqlify/>
Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
Prefix owl: <http://www.w3.org/2002/07/owl#>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
Prefix ls: <http://lodstats.aksw.org/>
Prefix ls-rdfdocs: <http://lodstats.aksw.org/rdfdocs/>
Prefix ls-statresult: <http://lodstats.aksw.org/stat_result/>
Prefix ls-ontology: <http://lodstats.aksw.org/ontology/>
Prefix dcterms: <http://purl.org/dc/terms/>
Prefix void: <http://rdfs.org/ns/void#>
Prefix rdf-formats: <http://www.w3.org/ns/formats/>
Prefix dcat: <http://www.w3.org/ns/dcat#>

Create View RdfClass As
  Construct {
    ?statresultUri void:classPartition ?blank .
    ?blank void:class ?class .
    ?blank void:entities ?entities .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?class = uri(?uri)
    ?entities = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT rdf_class_stat_result.stat_result_id, 
           concat(rdf_class_stat_result.stat_result_id,
           rdf_class_stat_result.rdf_class_id, 'class') AS compoundkey,
           rdf_class.uri, 
           rdf_class_stat_result.count 
    FROM stat_result 
    JOIN rdf_class_stat_result 
      ON rdf_class_stat_result.stat_result_id=stat_result.id 
    JOIN rdf_class 
      ON rdf_class.id=rdf_class_stat_result.rdf_class_id 
  ]] 



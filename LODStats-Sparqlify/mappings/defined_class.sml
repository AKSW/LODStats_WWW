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

Create View RdfDefinedClass As
  Construct {
    ?statresultUri void:classPartition ?blank .
    ?blank void:class ?definedClass .
    ?blank void:entities ?entities .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?definedClass = uri(?uri)
    ?entities = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT defined_class_stat.stat_result_id, 
           concat(defined_class_stat.stat_result_id,
           defined_class_stat.defined_class_id, 'definedClass') AS compoundkey,
           defined_class.uri, 
           defined_class_stat.count 
    FROM stat_result 
    JOIN defined_class_stat 
      ON defined_class_stat.stat_result_id=stat_result.id 
    JOIN defined_class 
      ON defined_class_stat.defined_class_id=defined_class.id
  ]] 

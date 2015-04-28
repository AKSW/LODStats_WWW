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

Create View Language As
  Construct {
    ?statresultUri ls-ontology:languagePartition ?blank .
    ?blank ls-ontology:language ?language .
    ?blank void:triples ?triples .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?language = TypedLiteral(?code, xsd:string)
    ?triples = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT language_stat.stat_result_id, 
           concat(language_stat.stat_result_id,
           language_stat.language_id, 'language') AS compoundkey,
           language.code, 
           language_stat.count 
    FROM stat_result 
    JOIN language_stat 
      ON language_stat.stat_result_id=stat_result.id 
    JOIN language 
      ON language_stat.language_id=language.id
  ]] 

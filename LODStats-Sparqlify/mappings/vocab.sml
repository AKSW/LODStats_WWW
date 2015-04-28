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

Create View Vocab As
  Construct {
    ?statresultUri ls-ontology:vocabularyPartition ?blank .
    ?blank ls-ontology:vocabulary ?vocabulary .
    ?blank void:triples ?triples .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?stat_result_id)
    ?vocabulary = uri(?uri)
    ?triples = TypedLiteral(?count, xsd:int)
    ?blank = bNode(?compoundkey)

  From
  [[SELECT rdf_vocab_stat.stat_result_id, 
           concat(rdf_vocab_stat.stat_result_id,
           rdf_vocab_stat.vocab_id, 'vocabulary') AS compoundkey,
           vocab.uri, 
           rdf_vocab_stat.count 
    FROM stat_result 
    JOIN rdf_vocab_stat 
      ON rdf_vocab_stat.stat_result_id=stat_result.id 
    JOIN vocab 
      ON rdf_vocab_stat.vocab_id=vocab.id
  ]] 

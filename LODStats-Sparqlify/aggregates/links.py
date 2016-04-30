from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://localhost:8890/sparql")

getDatasetsTriplesQuery="""
PREFIX ldso: <http://lodstats.aksw.org/ontology/ldso.owl#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX void: <http://rdfs.org/ns/void#>

select ?dataset ?links where {
  ?statResult a ldso:StatResult.
  ?statResult dc:modified ?evaluationDate.
  ?statResult foaf:primaryTopic ?dataset.
  ?statResult ldso:hasErrors "0"^^xsd:int.
  ?statResult ldso:links ?links.
  ?dataset dc:format ?format.
  ?dataset dc:identifier ?datasetName.
  ?dataset dc:isPartOf ?ckanCatalog.
  ?ckanCatalog dc:identifier ?ckanCatalogName.
  FILTER (?evaluationDate < "2012-01-01T00:00:00+00:00"^^xsd:dateTime && 
          ?evaluationDate > "2011-03-01T00:00:00+00:00"^^xsd:dateTime &&
          ?format != "sparql"^^<http://www.w3.org/2001/XMLSchema#string>)
}
"""

sparql.setQuery(getDatasetsTriplesQuery)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

datasetsTriples = {}
sum = 0

for result in results['results']['bindings']:
    links = int(result['links']['value'])
    datasetUri = result['dataset']['value']
    datasetsTriples[datasetUri] = links

for dataset in datasetsTriples:
    sum += datasetsTriples[dataset]

print sum

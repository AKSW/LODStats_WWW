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
Prefix foaf: <http://xmlns.com/foaf/0.1/>
Prefix api: <http://purl.org/linked-data/api/vocab#>

Create View CkanCatalog As
  Construct {
    ?ckanCatalogUri
      a ls-ontology:CkanCatalog;
      rdfs:subClassOf dcat:Catalog;
      dcterms:identifier ?nameLiteral;
      api:base ?apiUrl;
      foaf:homepage ?ckanCatalogUri.
  }
  With
    ?ckanCatalogUri = uri(?base)
    ?nameLiteral = TypedLiteral(?name, xsd:string)
    ?apiUrl = uri(?api_url)

  From
    [[SELECT name, 
             api_url,
             base
      FROM ckan_catalog]]



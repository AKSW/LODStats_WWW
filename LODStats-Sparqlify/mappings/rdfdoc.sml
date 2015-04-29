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

Create View RdfDoc As
  Construct {
    ?rdfdocUri
      a ls-ontology:Dataset;
      rdfs:subClassOf dcat:Dataset;
      dcat:downloadURL ?rdfdocDownloadUri;
      dcterms:identifier ?rdfdocIdLiteral;
      dcterms:format ?rdfdocFormatLiteral;
      dcterms:modified ?lastUpdated;
      ls-ontology:active ?active;
      ls-ontology:currentStats ?rdfdocCurrentStats;
      owl:sameAs ?rdfdocCatalogUri;
      dcterms:isPartOf ?ckanUri.
  }
  With
    ?rdfdocUri = uri(ls-rdfdocs:, ?id)
    ?rdfdocDownloadUri = uri(?uri)
    ?rdfdocIdLiteral = TypedLiteral(?name, xsd:string)
    ?rdfdocFormatLiteral = TypedLiteral(?format, xsd:string)
    ?lastUpdated = TypedLiteral(?last_updated, xsd:dateTime)
    ?rdfdocCurrentStats = uri(ls-statresult:, ?current_stats_id)
    ?rdfdocCatalogUri = uri(concat(?base, 'dataset/', ?name))
    ?active = TypedLiteral(?active, xsd:boolean)
    ?ckanUri = uri(?base)

  From
    [[SELECT id, 
             uri, 
             rdfdoc.name, 
             format, 
             last_updated, 
             current_stats_id, 
             rdfdoc.ckan_catalog,
             active,
             api_url,
             base
      FROM rdfdoc
      JOIN ckan_catalog
      ON rdfdoc.ckan_catalog=ckan_catalog.name]]



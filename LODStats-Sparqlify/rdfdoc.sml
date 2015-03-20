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

Create View RdfDoc As
  Construct {
    ?rdfdocUri
      a dcat:Dataset;
      dcat:accessURL ?rdfdocCatalogUri;
      dcterms:source ?rdfdocSrc;
      void:feature ?rdfdocFormatUri;
      dcat:mediaType ?rdfdocFormatLiteral;
      ls-ontology:lastUpdated ?lastUpdated;
      ls-ontology:currentStats ?rdfdocCurrentStats.
  }
  With
    ?rdfdocUri = uri(ls-rdfdocs:, ?id)
    ?rdfdocSrc = uri(?uri)
    ?rdfdocCatalogUri = uri(concat(?base, 'dataset/', ?name))

    ?rdfdocFormatUri = uri(rdf-formats:, ?format)
    ?rdfdocFormatLiteral = TypedLiteral(?format, xsd:string)

    ?lastUpdated = TypedLiteral(?last_updated, xsd:dateTime)
    ?rdfdocCurrentStats = uri(ls-statresult:, ?current_stats_id)

  From
    [[SELECT rdfdoc.id, 
             rdfdoc.uri, 
             rdfdoc.name, 
             rdfdoc.format, 
             rdfdoc.last_updated, 
             rdfdoc.current_stats_id, 
             rdfdoc.ckan,
             ckan_catalog.name,
             ckan_catalog.api_url,
             ckan_catalog.base
      FROM rdfdoc
      JOIN ckan_catalog
      ON rdfdoc.ckan_catalog=ckan_catalog.name]]



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

Create View StatResult As
  Construct {
    ?statresultUri
      a ls-ontology:StatResult;
      rdfs:subClassOf void:Dataset;
      owl:sameAs ?statresultVoidUri;
      foaf:primaryTopic ?rdfdocUri;
      dcterms:modified ?statresultLastUpdated;
      dcat:byteSize ?statresultBytesDownload;
      
      ls-ontology:hasErrors ?hasErrors;
      ls-ontology:errors ?errors;
      ls-ontology:warningsCount ?warningsCount;
      ls-ontology:lastWarning ?lastWarning;

      void:triples ?triples;
      void:entities ?entities;

      ls-ontology:literals ?literals;
      ls-ontology:blanks ?blanks;
      ls-ontology:blanksAsSubject ?blanks_as_subject;
      ls-ontology:blanksAsObject ?blanks_as_object;
      ls-ontology:subclasses ?subclasses;
      ls-ontology:typedSubjects ?typed_subjects;
      ls-ontology:labeledSubjects ?labeled_subjects;
      ls-ontology:classHierarchyDepth ?class_hierarchy_depth;
      ls-ontology:propertiesPerEntity ?properties_per_entity;
      ls-ontology:stringLengthTyped ?string_length_typed;
      ls-ontology:stringLengthUntyped ?string_length_untyped;
      ls-ontology:links ?links .
  }
  With
    ?statresultUri = uri(ls-statresult:, ?id)
    ?rdfdocUri = uri(ls-rdfdocs:, ?rdfdoc_id)
    ?statresultVoidUri = uri(concat(ls-statresult:, ?id, '.void'))
    ?statresultLastUpdated = TypedLiteral(?last_updated, xsd:dateTime)
    ?statresultBytesDownload = TypedLiteral(?bytes_download, xsd:int)

    ?hasErrors = TypedLiteral(?has_errors, xsd:boolean)
    ?errors = TypedLiteral(?errors, xsd:string)
    ?warningsCount = TypedLiteral(?warnings, xsd:int)
    ?lastWarning = TypedLiteral(?last_warning, xsd:string)

    ?triples = TypedLiteral(?triples, xsd:int)
    ?entities = TypedLiteral(?entities, xsd:int)

    ?literals = TypedLiteral(?literals, xsd:int)
    ?blanks = TypedLiteral(?blanks, xsd:int)
    ?blanks_as_subject = TypedLiteral(?blanks_as_subject, xsd:int)
    ?blanks_as_object = TypedLiteral(?blanks_as_object, xsd:int)
    ?subclasses = TypedLiteral(?subclasses, xsd:int)
    ?typed_subjects = TypedLiteral(?typed_subjects, xsd:int)
    ?labeled_subjects = TypedLiteral(?labeled_subjects, xsd:int)
    ?class_hierarchy_depth = TypedLiteral(?class_hierarchy_depth, xsd:int)
    ?properties_per_entity = TypedLiteral(?properties_per_entity, xsd:float)
    ?string_length_typed = TypedLiteral(?string_length_typed, xsd:float)
    ?string_length_untyped = TypedLiteral(?string_length_untyped, xsd:float)
    ?links = TypedLiteral(?links, xsd:int)

  From
    [[SELECT stat_result.id, 
             stat_result.void, 
             stat_result.triples, 
             stat_result.last_updated,
             stat_result.triples_done,
             stat_result.has_errors,
             stat_result.errors,
             stat_result.warnings,
             stat_result.last_warning,
             stat_result.bytes,
             stat_result.bytes_download,
             stat_result.content_length,
             stat_result.entities,
             stat_result.literals,
             stat_result.blanks,
             stat_result.blanks_as_object,
             stat_result.blanks_as_subject,
             stat_result.subclasses,
             stat_result.typed_subjects,
             stat_result.labeled_subjects,
             stat_result.class_hierarchy_depth,
             stat_result.properties_per_entity,
             stat_result.string_length_typed,
             stat_result.string_length_untyped,
             stat_result.links,
             stat_result.rdfdoc_id,
             rdfdoc.uri
      FROM stat_result
      JOIN rdfdoc
      ON stat_result.rdfdoc_id=rdfdoc.id
      ]]

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

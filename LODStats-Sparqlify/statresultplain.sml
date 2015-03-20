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

Create View RdfDoc As
  Construct {
    ?statresultUri
      foaf:primaryTopic ?rdfdocUri;
      void:inDataset ?voidDataset;
      ls-ontology:triples ?triples;
      ls-ontology:lastUpdated ?last_updated;
      ls-ontology:errors ?errors;
      ls-ontology:warnings ?warnings;
      ls-ontology:lastWarning ?last_warning;
      ls-ontology:bytes ?bytes;
      ls-ontology:bytesDownloaded ?bytes_download;
      ls-ontology:contentLength ?content_length;
      ls-ontology:entities ?entities;
      ls-ontology:literals ?literals;
      ls-ontology:blanks ?blanks;
      ls-ontology:blanks_as_subject ?blanks_as_subject;
      ls-ontology:blanks_as_object ?blanks_as_object;
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
    ?voidDataset = uri(?uri)
    ?rdfdocUri = uri(ls-rdfdocs:, ?rdfdoc_id)
    ?triples = PlainLiteral(?triples)
    ?last_updated = PlainLiteral(?last_updated)
    ?errors = PlainLiteral(?errors)
    ?warnings = PlainLiteral(?warnings)
    ?last_warning = PlainLiteral(?last_warning)
    ?bytes = PlainLiteral(?bytes)
    ?bytes_download = PlainLiteral(?bytes_download)
    ?content_length = PlainLiteral(?content_length)
    ?entities = PlainLiteral(?entities)
    ?literals = PlainLiteral(?literals)
    ?blanks = PlainLiteral(?blanks)
    ?blanks_as_subject = PlainLiteral(?blanks_as_subject)
    ?blanks_as_object = PlainLiteral(?blanks_as_object)
    ?subclasses = PlainLiteral(?subclasses)
    ?typed_subjects = PlainLiteral(?typed_subjects)
    ?labeled_subjects = PlainLiteral(?labeled_subjects)
    ?class_hierarchy_depth = PlainLiteral(?class_hierarchy_depth)
    ?properties_per_entity = PlainLiteral(?properties_per_entity)
    ?string_length_typed = PlainLiteral(?string_length_typed)
    ?string_length_untyped = PlainLiteral(?string_length_untyped)
    ?links = PlainLiteral(?links)

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



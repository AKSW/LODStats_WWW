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



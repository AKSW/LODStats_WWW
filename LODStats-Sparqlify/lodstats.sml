Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
Prefix void: <http://rdfs.org/ns/void#> 
Prefix void-ext: <http://stats.lod2.eu/rdf/void-ext/> 
Prefix qb: <http://purl.org/linked-data/cube#> 
Prefix dcterms: <http://purl.org/dc/terms/> 
Prefix ls-void: <http://stats.lod2.eu/rdf/void/> 
Prefix ls-qb: <http://stats.lod2.eu/rdf/qb/> 
Prefix ls-cr: <http://stats.lod2.eu/rdf/qb/criteria/> 

Create View Datasets As
  Construct {
    ?s
      a void:Dataset ;
      dcterms:source ?u .
  }
  With
    ?s = uri('http://stats.lod2.eu/rdf/void/?source=', ?uri)
    ?u = uri(?uri)
  From
    rdfdoc


Create View StatResults As
  Construct {
    ?triples
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:triples ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?triples_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .
     
    ?entities
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:entitiesMentioned ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?entities_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?literals
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:literals ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?literals_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?blanksAsSubject
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:blanksAsSubject ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?blanksAsSubject_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?blanksAsObject
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:blanksAsObject ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?blanksAsObject_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?subclasses
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:subclassUsage ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?subclasses_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?typedSubjects
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:typedSubjects ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?typedSubjects_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?labeledSubjects
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:labeledSubjects ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?labeledSubjects_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?classHierarchyDepth
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:classHierarchyDepth ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?classHierarchyDepth_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?propertyHierarchyDepth
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:propertyHierarchyDepth ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?propertyHierarchyDepth_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?averageTypedStringLength
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:averageTypedStringLength ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?averageTypedStringLength_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?averageUntypedStringLength
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:averageUntypedStringLength ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?averageUntypedStringLength_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?links
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:links ;
      ls-qb:timeOfMeasure ?t ;
      ls-qb:value ?links_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .
  }
  With
    ?triples = uri(ls-qb:, ?triples_hash)
    ?entities = uri(ls-qb:, ?entities_hash)
    ?literals = uri(ls-qb:, ?literals_hash)
    ?blanksAsSubject = uri(ls-qb:, ?blanksAsSubject_hash)
    ?blanksAsObject = uri(ls-qb:, ?blanksAsObject_hash)
    ?subclasses = uri(ls-qb:, ?subclasses_hash)
    ?typedSubjects = uri(ls-qb:, ?typedSubjects_hash)
    ?labeledSubjects = uri(ls-qb:, ?labeledSubjects_hash)
    ?classHierarchyDepth = uri(ls-qb:, ?classHierarchyDepth_hash)
    ?propertyHierarchyDepth = uri(ls-qb:, ?propertyHierarchyDepth_hash)
    ?averageTypedStringLength = uri(ls-qb:, ?stringLengthTyped_hash)
    ?averageUntypedStringLength = uri(ls-qb:, ?stringLengthUntyped_hash)
    ?links = uri(ls-qb:, ?links_hash)

    ?last_updated = typedLiteral(?last_updated, xsd:dateTime)
    ?triples_value = typedLiteral(?triples, xsd:integer)
    ?entities_value = typedLiteral(?triples, xsd:integer)
    ?literals_value = typedLiteral(?triples, xsd:integer)
    ?blanksAsSubject_value = typedLiteral(?triples, xsd:integer)
    ?blanksAsObject_value = typedLiteral(?triples, xsd:integer)
    ?subclasses_value = typedLiteral(?triples, xsd:integer)
    ?typedSubjects_value = typedLiteral(?triples, xsd:integer)
    ?labeledSubjects_value = typedLiteral(?triples, xsd:integer)
    ?classHierarchyDepth_value = typedLiteral(?triples, xsd:integer)
    ?propertyHierarchyDepth_value = typedLiteral(?triples, xsd:integer)
    ?averageTypedStringLength_value = typedLiteral(?triples, xsd:integer)
    ?averageUntypedStringLength_value = typedLiteral(?triples, xsd:integer)
    ?links_value = typedLiteral(?triples, xsd:integer)
    ?src = uri(?uri)
  From
    [[Select rdfdoc.uri, sr.last_updated, sr.triples,
    sr.entities, sr.literals, sr.blanks, sr.blanks_as_subject,
    sr.blanks_as_object, sr.subclasses, sr.typed_subjects,
    sr.labeled_subjects, sr.class_hierarchy_depth, sr.property_hierarchy_depth,
    sr.properties_per_entity, sr.string_length_typed, sr.string_length_untyped, sr.links,
    MD5(rdfdoc.uri || 'ls-cr:triples' || sr.triples) triples_hash,
    MD5(rdfdoc.uri || 'ls-cr:distinctEntities' || sr.entities) entities_hash,
    MD5(rdfdoc.uri || 'ls-cr:literals' || sr.literals) literals_hash,
    MD5(rdfdoc.uri || 'ls-cr:blanks' || sr.blanks) blanks_hash,
    MD5(rdfdoc.uri || 'ls-cr:blanksAsSubject' || sr.blanks_as_subject) blanksAsSubject_hash,
    MD5(rdfdoc.uri || 'ls-cr:blanksAsObject' || sr.blanks_as_object) blanksAsObject_hash,
    MD5(rdfdoc.uri || 'ls-cr:subclassUsage' || sr.subclasses) subclasses_hash,
    MD5(rdfdoc.uri || 'ls-cr:typedSubjects' || sr.typed_subjects) typedSubjects_hash,
    MD5(rdfdoc.uri || 'ls-cr:labeledSubjects' || sr.labeled_subjects) labeledSubjects_hash,
    MD5(rdfdoc.uri || 'ls-cr:classHierarchyDepth' || sr.class_hierarchy_depth) classHierarchyDepth_hash,
    MD5(rdfdoc.uri || 'ls-cr:propertyHierarchyDepth' || sr.property_hierarchy_depth) propertyHierarchyDepth_hash,
    MD5(rdfdoc.uri || 'ls-cr:propertiesPerEntity' || sr.properties_per_entity) properties_per_entity_hash,
    MD5(rdfdoc.uri || 'ls-cr:averageTypedStringLength' || sr.string_length_typed) stringLengthTyped_hash,
    MD5(rdfdoc.uri || 'ls-cr:averageUntypedStringLength' || sr.string_length_untyped) stringLengthUntyped_hash,
    MD5(rdfdoc.uri || 'ls-cr:links' || sr.links) links_hash
    JOIN stat_result sr ON (sr.rdfdoc_id = rdfdoc.id)]]



Create View static As
    Construct {
        ls-qb:LODStats
            a qb:DataSet ;
            qb:structure ls-qb:LODStatsStructure ;
            rdfs:label "LODStats Datacube Dataset" .

        ls-qb:LODStatsStructure
            a qb:DataStructureDefinition ;
            qb:component ls-qb:timeOfMeasureSpec ;
            qb:component ls-qb:sourceDatasetSpec ;
            qb:component ls-qb:statisticalCriterionSpec ;
            qb:component ls-qb:valueSpec ;
            qb:component ls-qb:unitSpec ;
            rdfs:label "LODStats DataCube Structure Definition" .

        ls-qb:timeOfMeasureSpec
            a qb:ComponentSpecification ;
            qb:dimension ls-qb:timeOfMeasure ;
            rdfs:label "Time of Measure (Component Specification)" .

        ls-qb:sourceDatasetSpec 
            a qb:ComponentSpecification ;
            qb:dimension ls-qb:sourceDataset ;
            rdfs:label "Source Dataset which is observed (Component Specification)" .

        ls-qb:statisticalCriterionSpec
            a qb:ComponentSpecification ;
            qb:dimension ls-qb:statisticalCriterion ;
            rdfs:label "Statistical Criterion (Component Specification)" .

        ls-qb:valueSpec
            a qb:ComponentSpecification ;
            qb:measure ls-qb:value ;
            rdfs:label "Measure of Observation (Component Specification)" .

        ls-qb:unitSpec
            a qb:ComponentSpecification ;
            qb:attribute ls-qb:unit ;
            rdfs:label "Unit of Measure (Component Specification)" .

        ls-qb:timeOfMeasure
            a qb:DimensonProperty ;
            rdfs:label "Time of Measure" .

        ls-qb:sourceDataset
            a qb:DimensonProperty ;
            rdfs:label "Source Dataset" .

        ls-qb:statisticalCriterion
            a qb:DimensonProperty ;
            rdfs:label "Statistical Criterion" .

        ls-qb:value
            a qb:MeasureProperty ;
            rdfs:label "Measure of Observation" .

        ls-qb:unit
            a qb:AttributeProperty ;
            rdfs:label "Unit of Measure" .

        ls-cr:StatisticalCriterion
            a owl:Class ;
            rdfs:label "Statistical Criterion" .
        
        ls-cr:usedClasses
            a ls-cr:StatisticalCriterion ;
            rdfs:label "used classes" ;
            rdfs:comment "Filtered By: ?p=rdf:type && isIRI(?o) ;Action: S+= ?o" .

        ls-cr:classUsageCount
            a ls-cr:StatisticalCriterion ;
            rdfs:label "class usage count" ;
            rdfs:comment "Filtered By: ?p=rdf:type && isIRI(?o) ;Action: M[?o]++
            ;Postproc.: top(M, 100)" .

        ls-cr:classesDefined
            a ls-cr:StatisticalCriterion ;
            rdfs:label "classes defined" ;
            rdfs:comment "Filtered By: ?p=rdf:type && isIRI(?s) &&
            (?o=rdfs:Class||?o=owl:Class) ;Action: S += ?s" .

        ls-cr:classHierarchyDepth
            a ls-cr:StatisticalCriterion ;
            rdfs:label "class hierarchy depth" ;
            rdfs:comment "Filtered By: ?p=rdfs:subClassOf && isIRI(?s) &&
            isIRI(?o) ;Action: G += (?s, ?o) ;Postproc.: hasCycles(G) ? Inf. :
            depth(G)" .

        ls-cr:propertyUsage
            a ls-cr:StatisticalCriterion ;
            rdfs:label "property usage" ;
            rdfs:comment "Action: M[?p]++ ;Postproc.: top(M,100)" .

        ls-cr:propertyUsageDistinctPerSubject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "property usage distinct per subject" ;
            rdfs:comment "Action: M[?s] += ?p ;Postproc.: sum(M)" .

        ls-cr:propertyUsageDistinctPerObject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "property usage distinct per object" ;
            rdfs:comment "Action: M[?o] += ?p ;Postproc.: sum(M)" .

        ls-cr:propertiesDistinctPerSubject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "properties distinct per subject" ;
            rdfs:comment "Action: M[?s] += ?p ;Postproc.: sum(M)/size(M)" .

        ls-cr:propertiesDistinctPerObject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "properties distinct per object" ;
            rdfs:comment "Action: M[?o] += ?p ;Postproc.: sum(M)/size(M)" .

        ls-cr:outdegree
            a ls-cr:StatisticalCriterion ;
            rdfs:label "outdegree" ;
            rdfs:comment "Action: M[?s]++ ;Postproc.: sum(M)/size(M)" .

        ls-cr:indegree
            a ls-cr:StatisticalCriterion ;
            rdfs:label "indegree" ;
            rdfs:comment "Action: M[?o]++ ;Postproc.: sum(M)/size(M)" .

        ls-cr:propertyHierarchyDepth
            a ls-cr:StatisticalCriterion ;
            rdfs:label "property hierarchy depth" ;
            rdfs:comment "Filtered by: ?p=rdfs:subPropertyOf && isIRI(?s) &&
            isIRI(?o) ;Action: G += (?s, ?o) ;Postproc.: hasCycles(G) ? Inf. :
            depth(G)" .

        ls-cr:subclassUsage
            a ls-cr:StatisticalCriterion ;
            rdfs:label "subclass usage" ;
            rdfs:comment "Filtered by: ?p=rdfs:subClassOf ;Action: i++" .

        ls-cr:triples
            a ls-cr:StatisticalCriterion ;
            rdfs:label "number of triples" ;
            rdfs:comment "Action: i++" .
            
        ls-cr:entitiesMentioned
            a ls-cr:StatisticalCriterion ;
            rdfs:label "entities mentioned" ;
            rdfs:comment "Action: i += size(iris({?s,?p,?o}))" .

        ls-cr:distinctEntities
            a ls-cr:StatisticalCriterion ;
            rdfs:label "distinct entities" ;
            rdfs:comment "Action: S += iris({?s,?p,?o})" .

        ls-cr:literals
            a ls-cr:StatisticalCriterion ;
            rdfs:label "number of literals" ;
            rdfs:comment "Filtered by: isLiteral(?o) ;Action: i++" .

        ls-cr:blanksAsSubject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "blanks as subject" ;
            rdfs:comment "Filtered by: isBlank(?s) ;Action: i++" .

        ls-cr:blanksAsObject
            a ls-cr:StatisticalCriterion ;
            rdfs:label "blanks as object" ;
            rdfs:comment "Filtered by: isBlank(?o) ;Action: i++" .

        ls-cr:datatypes
            a ls-cr:StatisticalCriterion ;
            rdfs:label "datatypes" ;
            rdfs:comment "Filtered by: isLiteral(?o) ;Action: M[type(?o)]++" .

        ls-cr:languages
            a ls-cr:StatisticalCriterion ;
            rdfs:label "languages" ;
            rdfs:comment "Filtered by: isLiteral(?o) ;Action: M[language(?o)]++" .

        ls-cr:averageTypedStringLength
            a ls-cr:StatisticalCriterion ;
            rdfs:label "Average typed string length" ;
            rdfs:comment "Filtered by: isLiteral(?o) && datatype(?o)=xsd:string
            ;Action: i++; len+=len(?o) ;Postproc.: len/i" .

        ls-cr:averageUntypedStringLength
            a ls-cr:StatisticalCriterion ;
            rdfs:label "Average untyped string length" ;
            rdfs:comment "Filtered by: isLiteral(?o) && datatype(?o)=NULL
            ;Action: i++; len+=len(?o) ;Postproc.: len/i" .

        ls-cr:typedSubjects
            a ls-cr:StatisticalCriterion ;
            rdfs:label "Typed subjects" ;
            rdfs:comment "Filtered by: ?p=rdf:type ;Action: i++" .

        ls-cr:labeledSubjects
            a ls-cr:StatisticalCriterion ;
            rdfs:label "Labeled subjects" ;
            rdfs:comment "Filtered by: ?p=rdfs:label ;Action: i++" .

        ls-cr:sameAs
            a ls-cr:StatisticalCriterion ;
            rdfs:label "same as links" ;
            rdfs:comment "Filtered by: ?p=owl:sameAs ;Action: i++" .

        ls-cr:links
            a ls-cr:StatisticalCriterion ;
            rdfs:label "links" ;
            rdfs:comment "Filtered by: ns(?s)!=ns(?o) ;Action: M[ns(?s)+ns(?o)]++" .

        ls-cr:maximumPerProperty
            a ls-cr:StatisticalCriterion ;
            rdfs:label "maximum per property" ;
            rdfs:comment "Filtered by:
            datatype(?o)={xsd:int|xsd:float|xsd:datetime} ;Action: M[?p] = max(M[?p], ?o)" .

        ls-cr:averagePerProperty
            a ls-cr:StatisticalCriterion ;
            rdfs:label "average per property" ;
            rdfs:comment "Filtered by: datatype(?o)={xsd:int|xsd:float|xsd:datetime} ;Action: M[?p] += ?o;
            M2[?p]++ ;Postproc.: M[?p]/M2[?p]" .

        ls-cr:subjectVocabularies
            a ls-cr:StatisticalCriterion ;
            rdfs:label "subject vocabularies" ;
            rdfs:comment "Action: M[ns(?s)]++" .

        ls-cr:predicateVocabularies
            a ls-cr:StatisticalCriterion ;
            rdfs:label "predicate vocabularies" ;
            rdfs:comment "Action: M[ns(?p)]++" .

        ls-cr:objectVocabularies
            a ls-cr:StatisticalCriterion ;
            rdfs:label "object vocabularies" ;
            rdfs:comment "Action: M[ns(?o)]++" .
    }

Prefix fn: <http://aksw.org/sparqlify/>
Prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
Prefix owl: <http://www.w3.org/2002/07/owl#>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>
Prefix void: <http://rdfs.org/ns/void#> 
Prefix void-ext: <http://stats.lod2.eu/rdf/void-ext/> 
Prefix qb: <http://purl.org/linked-data/cube#> 
Prefix dcterms: <http://purl.org/dc/terms/> 
Prefix dc: <http://purl.org/dc/elements/1.1/>
Prefix ls-void: <http://stats.lod2.eu/rdf/void/> 
Prefix ls-qb: <http://stats.lod2.eu/rdf/qb/> 
Prefix ls-cr: <http://stats.lod2.eu/rdf/qb/criteria/> 

Create View static As
  Construct {
    ls-qb:LODStats
      a qb:DataSet ;
      qb:structure ls-qb:LODStatsStructure ;
      rdfs:label "LODStats Datacube Dataset" .

    ls-qb:LODStatsStructure
      a qb:DataStructureDefinition ;
      qb:component ls-qb:timeOfMeasureSpec ;
      qb:component ls-qb:statisticalCriterionSpec ;
      qb:component ls-qb:sourceDatasetSpec ;
      qb:component ls-qb:valueSpec ;
      qb:component ls-qb:unitSpec ;
      rdfs:label "LODStats DataCube Structure Definition" .

    ls-qb:timeOfMeasureSpec
      a qb:ComponentSpecification ;
      qb:dimension ls-qb:timeOfMeasure ;
      rdfs:label "Time of Measure (Component Specification)" .

    ls-qb:timeOfMeasure
      a qb:DimensonProperty ;
      rdfs:label "Time of Measure" .

    ls-qb:statisticalCriterionSpec
      a qb:ComponentSpecification ;
      qb:dimension ls-qb:statisticalCriterion ;
      rdf:label "Statistical Criterion (Component Specification)" .

    ls-qb:statisticalCriterion 
      a qb:DimensonProperty ;
      rdfs:label "Statistical Criterion" .

    ls-qb:sourceDatasetSpec
      a qb:ComponentSpecification ;
      qb:dimension ls-qb:sourceDataset ;
      rdf:label "Source Dataset (Component Specification)" .

    ls-qb:sourceDataset 
      a qb:DimensionProperty ;
      rdfs:label "URL of the source dataset" .

    ls-qb:valueSpec
      a qb:ComponentSpecification ;
      qb:measure ls-qb:value ;
      rdfs:label "Measure of Observation (Component Specification)" .
      
    ls-qb:value
      a qb:MeasureProperty ;
      rdfs:label "Measure of Observation" .

    ls-qb:unitSpec
      a qb:ComponentSpecification ;
      qb:attribute ls-qb:unit ;
      rdfs:label "Unit of Measure (Component Specification)" .

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
        rdfs:comment "Filtered By: ?p=rdf:type && isIRI(?o) ;Action: M[?o]++ ;Postproc.: top(M, 100)" .

    ls-cr:classesDefined
        a ls-cr:StatisticalCriterion ;
        rdfs:label "classes defined" ;
        rdfs:comment "Filtered By: ?p=rdf:type && isIRI(?s) && (?o=rdfs:Class||?o=owl:Class) ;Action: S += ?s" .

    ls-cr:classHierarchyDepth
        a ls-cr:StatisticalCriterion ;
        rdfs:label "class hierarchy depth" ;
        rdfs:comment "Filtered By: ?p=rdfs:subClassOf && isIRI(?s) && isIRI(?o) ;Action: G += (?s, ?o) ;Postproc.: hasCycles(G) ? Inf. : depth(G)" .

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
        rdfs:comment "Filtered by: ?p=rdfs:subPropertyOf && isIRI(?s) && isIRI(?o) ;Action: G += (?s, ?o) ;Postproc.: hasCycles(G) ? Inf. : depth(G)" .

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
        rdfs:comment "Filtered by: isLiteral(?o) && datatype(?o)=xsd:string ;Action: i++; len+=len(?o) ;Postproc.: len/i" .

    ls-cr:averageUntypedStringLength
        a ls-cr:StatisticalCriterion ;
        rdfs:label "Average untyped string length" ;
        rdfs:comment "Filtered by: isLiteral(?o) && datatype(?o)=NULL ;Action: i++; len+=len(?o) ;Postproc.: len/i" .

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
        rdfs:comment "Filtered by: datatype(?o)={xsd:int|xsd:float|xsd:datetime} ;Action: M[?p] = max(M[?p], ?o)" .

    ls-cr:averagePerProperty
        a ls-cr:StatisticalCriterion ;
        rdfs:label "average per property" ;
        rdfs:comment "Filtered by: datatype(?o)={xsd:int|xsd:float|xsd:datetime} ;Action: M[?p] += ?o; M2[?p]++ ;Postproc.: M[?p]/M2[?p]" .

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
  
Create View StatResults As
  Construct {
    ?triples_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:triples ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?triples_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?entitiesMentioned_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:entitiesMentioned ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?entitiesMentioned_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?literals_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:literals ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?literals_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?blanksAsSubject_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:blanksAsSubject ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?blanksAsSubject_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?blanksAsObject_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:blanksAsObject ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?blanksAsObject_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?subclasses_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:subclassUsage ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?subclasses_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?typedSubjects_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:typedSubjects ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?typedSubjects_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .
      
    ?classHierarchyDepth_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:classHierarchyDepth ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?classHierarchyDepth_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?propertyHierarchyDepth_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:propertyHierarchyDepth ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?propertyHierarchyDepth_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?averageTypedStringLength_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:averageTypedStringLength ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?averageTypedStringLength_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?averageUntypedStringLength_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:averageUntypedStringLength ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?averageUntypedStringLength_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .

    ?links_uri
      a qb:Observation ;
      qb:dataSet ls-qb:LODStats ;
      ls-qb:statisticalCriterion ls-cr:links ;
      ls-qb:timeOfMeasure ?timeOfMeasure ;
      ls-qb:value ?links_value ;
      ls-qb:unit "total amount" ;
      ls-qb:sourceDataset ?src .
  }
  With
    ?triples_uri = uri(ls-qb:, ?triples_hash)
    ?triples_value = typedLiteral(?triples, xsd:integer)

    ?entitiesMentioned_uri = uri(ls-qb:, ?entities_hash)
    ?entitiesMentioned_value = typedLiteral(?entities, xsd:integer)

    ?literals_uri = uri(ls-qb:, ?literals_hash)
    ?literals_value = typedLiteral(?literals, xsd:integer)

    ?blanksAsSubject_uri = uri(ls-qb:, ?blanksAsSubject_hash)
    ?blanksAsSubject_value = typedLiteral(?blanks_as_subject, xsd:integer)

    ?blanksAsObject_uri = uri(ls-qb:, ?blanks_as_object_hash)
    ?blanksAsObject_value = typedLiteral(?blanks_as_object, xsd:integer)

    ?subclasses_uri = uri(ls-qb:, ?subclasses_hash)
    ?subclasses_value = typedLiteral(?subclasses, xsd:integer)

    ?typedSubjects_uri = uri(ls-qb:, ?typed_subjects_hash)
    ?typedSubjects_value = typedLiteral(?typed_subjects, xsd:integer)
    
    ?labeledSubjects_uri = uri(ls-qb:, ?labeled_subjects_hash)
    ?labeledSubjects_value = typedLiteral(?labeled_subjects, xsd:integer)
    
    ?classHierarchyDepth_uri = uri(ls-qb:, ?class_hierarchy_depth_hash)
    ?classHierarchyDepth_value = typedLiteral(?class_hierarchy_depth, xsd:integer)

    ?propertyHierarchyDepth_uri = uri(ls-qb:, ?property_hierarchy_depth_hash)
    ?propertyHierarchyDepth_value = typedLiteral(?property_hierarchy_depth, xsd:integer)
    
    ?averageTypedStringLength_uri = uri(ls-qb:, ?string_length_typed_hash)
    ?averageTypedStringLength_value = typedLiteral(?string_length_typed, xsd:float)

    ?averageUntypedStringLength_uri = uri(ls-qb:, ?string_length_untyped_hash)
    ?averageUntypedStringLength_value = typedLiteral(?string_length_untyped, xsd:float)

    ?links_uri = uri(ls-qb:, ?links_hash)
    ?links_value = typedLiteral(?links, xsd:integer)

    ?timeOfMeasure = plainLiteral(?last_updated_trunc)
    ?src = uri(?uri) 

  From
    [[Select DISTINCT ON(rd.uri, date_trunc('month', sr.last_updated)) 
    url_fix(rd.uri) uri, sr.last_updated,
    date_trunc('month', sr.last_updated) last_updated_trunc, 
    triples, MD5(rd.uri || 'ls-cr:usedClasses' || sr.last_updated) triples_hash,
    entities, MD5(rd.uri || 'ls-cr:entitiesMentioned' || sr.last_updated) entities_hash,
    literals, MD5(rd.uri || 'ls-cr:literals' || sr.last_updated) literals_hash,
    blanks, MD5(rd.uri || 'ls-cr:blanks' || sr.last_updated) blanks_hash,
    blanks_as_subject, MD5(rd.uri || 'ls-cr:blanksAsSubject' || sr.last_updated) "blanksAsSubject_hash",
    blanks_as_object, MD5(rd.uri || 'ls-cr:blanksAsObject' || sr.last_updated) blanks_as_object_hash,
    subclasses, MD5(rd.uri || 'ls-cr:subclassUsage' || sr.last_updated) subclasses_hash,
    typed_subjects, MD5(rd.uri || 'ls-cr:typedSubjects' || sr.last_updated) typed_subjects_hash,
    labeled_subjects, MD5(rd.uri || 'ls-cr:labeledSubjects' || sr.last_updated) labeled_subjects_hash,
    class_hierarchy_depth, MD5(rd.uri || 'ls-cr:classHierarchyDepth' || sr.last_updated) class_hierarchy_depth_hash,
    property_hierarchy_depth, MD5(rd.uri || 'ls-cr:propertyHierarchyDepth' || sr.last_updated) property_hierarchy_depth_hash,
    string_length_typed, MD5(rd.uri || 'ls-cr:averageTypedStringLength' || sr.last_updated) string_length_typed_hash,
    string_length_untyped, MD5(rd.uri || 'ls-cr:averageUntypedStringLength' || sr.last_updated) string_length_untyped_hash,
    links, MD5(rd.uri || 'ls-cr:links' || sr.last_updated) links_hash
    From rdfdoc rd JOIN stat_result sr ON (sr.rdfdoc_id = rd.id) 
    WHERE triples IS NOT NULL ORDER BY rd.uri]]



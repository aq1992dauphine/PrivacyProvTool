
:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'addsCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:addsCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'allowsRole'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:allowsRole]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'annotates'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:annotates]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'contains'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:contains]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsDR'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsDR]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsRC'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsRC]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'executes'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:executes]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'generatedPrivacyAnnotation'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:generatedPrivacyAnnotation]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasureRewriteRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasureRewriteRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasMintingRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasMintingRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasModelExposureMapping'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasModelExposureMapping]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasOperatorType'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasOperatorType]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasRiskRemovalRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasRiskRemovalRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasTransformationRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasTransformationRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasUsage'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasUsage]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'implies'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:implies]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsFromCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsFromCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsToCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsToCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'removesCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:removesCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesFromErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesFromErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesToErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesToErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'used'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:used]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usedPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usedPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usesPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usesPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasDerivedFrom'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasDerivedFrom]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///census_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasGeneratedBy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasGeneratedBy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'addsCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:addsCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'allowsRole'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:allowsRole]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'annotates'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:annotates]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'contains'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:contains]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsDR'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsDR]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsRC'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsRC]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'executes'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:executes]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'generatedPrivacyAnnotation'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:generatedPrivacyAnnotation]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasureRewriteRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasureRewriteRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasMintingRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasMintingRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasModelExposureMapping'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasModelExposureMapping]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasOperatorType'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasOperatorType]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasRiskRemovalRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasRiskRemovalRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasTransformationRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasTransformationRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasUsage'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasUsage]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'implies'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:implies]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsFromCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsFromCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsToCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsToCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'removesCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:removesCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesFromErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesFromErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesToErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesToErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'used'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:used]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usedPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usedPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usesPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usesPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasDerivedFrom'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasDerivedFrom]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///compas_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasGeneratedBy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasGeneratedBy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'addsCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:addsCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'allowsRole'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:allowsRole]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'annotates'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:annotates]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'contains'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:contains]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsDR'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsDR]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsRC'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsRC]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'executes'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:executes]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'generatedPrivacyAnnotation'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:generatedPrivacyAnnotation]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasureRewriteRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasureRewriteRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasMintingRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasMintingRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasModelExposureMapping'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasModelExposureMapping]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasOperatorType'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasOperatorType]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasRiskRemovalRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasRiskRemovalRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasTransformationRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasTransformationRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasUsage'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasUsage]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'implies'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:implies]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsFromCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsFromCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsToCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsToCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'removesCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:removesCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesFromErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesFromErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesToErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesToErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'used'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:used]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usedPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usedPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usesPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usesPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasDerivedFrom'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasDerivedFrom]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///german_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasGeneratedBy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasGeneratedBy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'addsCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:addsCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'allowsRole'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:allowsRole]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'annotates'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:annotates]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'contains'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:contains]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsDR'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsDR]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'containsRC'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:containsRC]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'executes'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:executes]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'generatedPrivacyAnnotation'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:generatedPrivacyAnnotation]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasErasureRewriteRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasErasureRewriteRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasMintingRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasMintingRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasModelExposureMapping'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasModelExposureMapping]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasOperatorType'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasOperatorType]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasRiskRemovalRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasRiskRemovalRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasTransformationRule'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasTransformationRule]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'hasUsage'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:hasUsage]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'implies'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:implies]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsFromCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsFromCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'mapsToCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:mapsToCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'removesCategory'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:removesCategory]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesFromErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesFromErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'rewritesToErasure'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:rewritesToErasure]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'used'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:used]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usedPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usedPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'usesPolicy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:usesPolicy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasDerivedFrom'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasDerivedFrom]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;


:auto
LOAD CSV WITH HEADERS FROM 'file:///asd_relationships_clean.csv' AS row
CALL (row) {
  WITH row
  WHERE row.type = 'wasGeneratedBy'
    AND row.source IS NOT NULL
    AND row.target IS NOT NULL
    AND trim(row.source) <> ''
    AND trim(row.target) <> ''

  MATCH (s:ProvNode {uid: row.pipeline + '::' + row.source})
  MATCH (t:ProvNode {uid: row.pipeline + '::' + row.target})

  CREATE (s)-[r:wasGeneratedBy]->(t)
  SET r.pipeline = row.pipeline,
      r.source_local_id = row.source,
      r.target_local_id = row.target,
      r.original_type = row.type,
      r.type = row.type,
      r.props_b64 = row.props_b64
} IN TRANSACTIONS OF 1000 ROWS;

# chembl_activity_target.py

import psycopg2
import pandas as pd
import pandas.io.sql as sqlio


def chembl_activity_target(db_user, db_password, organism_contains
                          ,db_name='chembl_31', db_host='localhost', db_port=5432):
    
    # Connect to chembl database
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    cursor = conn.cursor()
    
    # Run query first step
    cursor.execute(
f"""
CREATE TEMPORARY TABLE tmp_activity_protein_1 AS
WITH
  protein_details AS (
    SELECT
      td.tid,
      string_agg(cnt_s.accession || ' ' || pc.pref_name, ';') AS protein_accession_class
    FROM target_dictionary td
      LEFT JOIN target_components tc ON td.tid = tc.tid
      LEFT JOIN component_sequences cnt_s ON tc.component_id = cnt_s.component_id
      LEFT JOIN component_class cnt_c ON cnt_s.component_id = cnt_c.component_id
      LEFT JOIN protein_classification pc ON cnt_c.protein_class_id = pc.protein_class_id
    WHERE td.tax_id=1280
    GROUP BY td.tid
)
SELECT
  docs.doc_id,
  a.assay_id,
  act.activity_id,
  md.chembl_id AS compound_chembl_id,
  cnd_s.canonical_smiles,
  a.assay_type,
  a.confidence_score AS assay_confidence_score,
  a.bao_format AS assay_bao_format,
  act.standard_type,
  act.standard_value,
  act.standard_units,
  act.pchembl_value,
  td.chembl_id AS target_chembl_id,
  td.target_type,
  td.organism AS target_organism,
  td.pref_name AS target_pref_name,
  td.tax_id AS target_tax_id,
  prot_d.protein_accession_class,
  docs.year,
  docs.pubmed_id,
  a.description AS assay_description
FROM target_dictionary td
  JOIN assays a ON td.tid = a.tid
  JOIN docs ON a.doc_id = docs.doc_id
  JOIN activities act ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON act.molregno = md.molregno
  JOIN compound_structures cnd_s ON md.molregno = cnd_s.molregno
  LEFT JOIN protein_details prot_d ON td.tid = prot_d.tid
WHERE UPPER(td.organism) LIKE '%{organism_contains.upper()}%'
"""
    )
    
    # Run query second step
    cursor.execute(
"""
CREATE TEMPORARY TABLE tmp_activity_protein AS
SELECT
  min(doc_id) as doc_id,
  min(assay_id) as assay_id,
  min(activity_id) as activity_id,
  compound_chembl_id,
  max(canonical_smiles) AS canonical_smiles,
  assay_type,
  max(assay_confidence_score) as assay_confidence_score,
  assay_bao_format,
  standard_type,
  standard_value,
  standard_units,
  pchembl_value,
  target_chembl_id,
  max(target_type) AS target_type,
  max(target_organism) AS target_organism,
  max(target_pref_name) AS target_pref_name,
  max(target_tax_id) AS target_tax_id,
  max(protein_accession_class) AS protein_accession_class,
  max(year) AS year,
  max(pubmed_id) AS pubmed_id,
  count(*) as count_activity_rows,
  string_agg(cast(doc_id as varchar), ';') AS doc_id_all,
  string_agg(cast(assay_id as varchar), ';') AS assay_id_all,
  string_agg(cast(activity_id as varchar), ';') AS activity_id_all,
  max(assay_description) AS assay_description
FROM tmp_activity_protein_1
GROUP BY
  target_chembl_id,
  compound_chembl_id,
  assay_type,
  assay_bao_format,
  standard_type,
  standard_value,
  standard_units,
  pchembl_value
"""
    )
    
    # Count rows
    cursor.execute("SELECT count(*) FROM tmp_activity_protein")
    print('Count:', cursor.fetchone())
    
    # NOTE: Selected rows are limited in case there are too many - pending to give a warning if not all rows are shown
    sql = "SELECT * FROM tmp_activity_protein limit 500000"
    df = sqlio.read_sql_query(sql, conn)
    print('Resulting dataframe shape:', df.shape)
    print()
    print('Selected organisms:')
    print(df.target_organism.value_counts())
    
    # Close database connection
    conn.close()
    
    return df
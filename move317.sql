set pagesize 50000
set linesize 1500
set head off
set FEEDBACK off
set ECHO off
SET COLSEP '|'
SPOOL liquidaciones_317.txt

SELECT 
  rl.report_log_path--,
 --CONCAT('|', REPLACE(REPLACE(df.doc_def_label,' ',''),'-','')) AS carpeta 
--REPLACE(REPLACE(df.doc_def_label,' ',''),'-','') AS carpeta
FROM im_trans it,
  tch_im_transactions im,
  im_doc_trans_val dt,
  im_document d,
  im_doc_def df,
  im_report_log rl
WHERE franchise      IN ( '317')
AND it.trans_id       = im.id
AND it.insertion_dat BETWEEN TO_DATE('&1 00:00:00','DD-MM-YYYY HH24:MI:SS') AND TO_DATE('&2 23:59:59','DD-MM-YYYY HH24:MI:SS')
AND status           <> 'CANCELLED'
AND trans_label       = 'liquidation issued'
AND dt.trans_id       = im.id
AND dt.DOCUMENT_ID    = d.DOCUMENT_ID
AND d.report_log_id   = rl.report_log_id
AND d.doc_def_id      = df.DOC_DEF_ID
AND im.service is not null;
--AND df.doc_def_label NOT LIKE '%&3%'
--AND im.billing_period LIKE '&4'
--AND im.operator like '&5';

SPOOL OFF
exit;

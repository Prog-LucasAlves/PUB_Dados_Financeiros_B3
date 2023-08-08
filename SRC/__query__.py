# Query para deletar linhas em branco no banco de dados
delete_vazio_query = " DELETE FROM dados \
                              WHERE papel = ' ' OR papel IS NULL \
                                    OR tipo = ' ' OR tipo IS NULL \
                                    OR empresa = ' ' OR empresa IS NULL \
                                    OR cotacao = ' ' OR cotacao IS NULL \
                                    OR data_ult_cotacao IS NULL \
                                    OR min_52_sem = ' ' OR min_52_sem IS NULL \
                                    OR max_52_sem = ' ' OR max_52_sem IS NULL \
                                    OR vol_med_2m = ' ' OR vol_med_2m IS NULL \
                                    OR valor_mercado = ' ' OR valor_mercado IS NULL "

# Query para deletar linhas duplicadas no banco de dados
delete_duplicados_query = " DELETE FROM dados a USING (SELECT MAX(ctid) AS ctid, papel, data_ult_cotacao \
                                   FROM dados \
                                        GROUP BY papel, data_ult_cotacao HAVING COUNT(*) > 1) b \
                                                 WHERE a.papel = b.papel \
                                                       AND a.ctid <> b.ctid \
                                                       AND a.data_ult_cotacao = b.data_ult_cotacao \
                                                       AND a.ctid <> b.ctid "

# Query que realiza uma cópia(Bachup) de banco de dados
backup_query = " COPY (SELECT * FROM dados) TO STDOUT WITH CSV HEADER DELIMITER ';' ENCODING 'UTF-8' "

# Query remover espaços em branco na coluna 'papel'
espaco_query = " Update dados set papel = Trim(papel) "

#####

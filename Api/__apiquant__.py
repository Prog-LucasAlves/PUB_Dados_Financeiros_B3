"""
Descrição:
Esse código pega os dados upside ou dowside mês a mês em porcentagem
das empresas listadas na bolsa brasileira e armazena cada ação com os
dados coletados em um arquivo .csv

Local: pasta(histórico)
"""

# Bibliotecas utilizadas
import quantstats as qs
from tqdm import tqdm
import warnings

# Lista com o nome das ações
import __list__

acao = __list__.lst_acao

warnings.filterwarnings('ignore')

for i in tqdm(acao):

    qs.extend_pandas()
    data = qs.utils.download_returns(f"{i}.SA")
    if data.empty:
        pass
    else:
        datah = data.monthly_returns()
        datah[["JAN"]] = datah[["JAN"]].applymap("{0:.2%}".format)
        datah[["FEB"]] = datah[["FEB"]].applymap("{0:.2%}".format)
        datah[["MAR"]] = datah[["MAR"]].applymap("{0:.2%}".format)
        datah[["APR"]] = datah[["APR"]].applymap("{0:.2%}".format)
        datah[["MAY"]] = datah[["MAY"]].applymap("{0:.2%}".format)
        datah[["JUN"]] = datah[["JUN"]].applymap("{0:.2%}".format)
        datah[["JUL"]] = datah[["JUL"]].applymap("{0:.2%}".format)
        datah[["AUG"]] = datah[["AUG"]].applymap("{0:.2%}".format)
        datah[["SEP"]] = datah[["SEP"]].applymap("{0:.2%}".format)
        datah[["OCT"]] = datah[["OCT"]].applymap("{0:.2%}".format)
        datah[["NOV"]] = datah[["NOV"]].applymap("{0:.2%}".format)
        datah[["DEC"]] = datah[["DEC"]].applymap("{0:.2%}".format)
        datah[["EOY"]] = datah[["EOY"]].applymap("{0:.2%}".format)
        datah.to_csv(f"./historico/{i}.csv", sep=";")

#####

# This Python file uses the following encoding: utf-8

"""
Author: Lucas Alves
Linkedin: https://www.linkedin.com/in/lucasalves-ast/
"""

# TODO #4 Atualizar python 3.9.5 -> 3.10.2 - Realizado

import time
from datetime import date, timedelta

# Importar bibliotecas
import backoff
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import __check__
import __check_semana__
# Importar bibliotecas internas
import __conectdb__
import __list__
import __query__

# Cores utilizada no script
RED = "\033[1;31m"
GREEN = "\033[0;32m"
GREEN_T = "\033[92m"
RESET = "\033[0;0m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
GRAY = "\033[1;35m"

#####


@backoff.on_exception(backoff.expo, (), max_tries=10)
# Inicio da funcao para coleta dos dados
def dados():

    # Dados atual - Criando um DataFrame só com os dados atuais
    dados_atual = pd.DataFrame(
        columns=[
            "papel",
            "tipo",
            "empresa",
            "setor",
            "cotacao",
            "dt_ult_cotacao",
            "min_52_sem",
            "max_52_sem",
            "vol_med",
            "valor_mercado",
            "valor_firma",
            "ult_balanco_pro",
            "nr_acoes",
            "os_dia",
            "pl",
            "lpa",
            "pvp",
            "vpa",
            "p_ebit",
            "marg_bruta",
            "psr",
            "marg_ebit",
            "p_ativo",
            "marg_liquida",
            "p_cap_giro",
            "ebit_ativo",
            "p_ativo_circ_liq",
            "roic",
            "div_yield",
            "roe",
            "ev_ebitda",
            "liquidez_corr",
            "ev_ebit",
            "cres_rec",
            "ativo",
            "disponibilidades",
            "ativo_circulante",
            "divd_bruta",
            "divd_liquida",
            "patr_liquido",
            "lucro_liquido_12m",
            "lucro_liquido_3m",
        ]
    )

    # Variável(dt) - responsavel por informar qual (x) dia sera feita a coleta dos dados
    # Ex.: dt = date.today() - timedelta(days=3) -> volta 3 dias atras no calendario
    dt = date.today() - timedelta(days=0)
    dt_sem = dt.weekday()

    # Variavel dt_dia_sem - responsavel por verificar qual e o dia da semana
    # (Se for Sabado ou Domingo - nao havera coleta de dados)
    dt_dia_sem = __check_semana__.DIAS[dt_sem]
    dt = dt.strftime("%d/%m/%Y")

    # Faz a checagem se o dia da semana e Sabado ou Domingo
    if __check__.data_check != dt or dt_dia_sem == "Sábado" or dt_dia_sem == "Domingo":
        print(f"+{GRAY} Site não atualizado {RESET}+")
        print("--------------------------------------")
        print(f"Hoje é dia: {dt} - {dt_dia_sem} ")
        print(f"Data do site é: {__check__.data_check} - {__check__.day}")
        print("--------------------------------------")

    else:
        print(f"+{GREEN_T} Site atualizado vamos começar a coletar os dados. {RESET}+")

        # Faz checagem se a conexao com o banco de dados foi estabelecida
        if __conectdb__.verifica_conexao() is False:
            return print(
                f"""
+{RED} Conexão não estabelecida com o Banco de Dados, verifique: {RESET}+
-{RED} Docker {RESET}
                """
            )

        else:
            print(
                f"""
+{GREEN_T} Conexão estabelecida com sucesso ao Banco de Dados. {RESET}+ """
            )
            print("-------------------------------------------------------")

            # Inicio do contador de tempo de execução do script
            inicio = time.time()

            # Variável (acao) - armazena uma lista com os tickers da acoes
            acao = __list__.lst_acao

            # Variável contador
            n = 0

            # Percorre a lista com os códigos das ações
            for i in tqdm(acao):

                try:

                    # Consulta no banco de dados para verificar se os dados
                    # já se encontram no mesmo (Ref.: data_ult_cotacao / papel)
                    query_consult_bd = f" SELECT data_dado_inserido, papel\
                                                FROM dados \
                                                    WHERE data_ult_cotacao = '{dt}' \
                                                        AND papel = '{i}' "
                    result = __conectdb__.se_dados(query_consult_bd)
                    # --- #

                    if result != []:
                        print(f"+{YELLOW} Dados da ação: {i}, já cadastrados {RESET}+")

                    else:

                        # Aqui começa o script para coleta dos dados
                        hearder = {"user-agent": "Mozilla/5.0"}
                        url = f"https://fundamentus.com.br/detalhes.php?papel={i}"
                        page = requests.get(url, headers=hearder)
                        soup = BeautifulSoup(page.content, "html.parser")
                        soup1 = BeautifulSoup(page.text, "html.parser")

                        # Verificando o h1 do site
                        # Para verificar se o Ticker(Ação) tem os dados no site
                        hearder_site = str(soup1.h1)

                        if hearder_site == 'None':

                            dados = soup.findAll("div", {"class": "conteudo clearfix"})

                            # cria a lista das variaveis aonde seram armazenados os dados coletados
                            for data in dados:
                                dadosI = []
                                papel = []
                                tipo = []
                                empresa = []
                                setor = []
                                cotacao = []
                                dt_ult_cotacao = []
                                min_52_sem = []
                                max_52_sem = []
                                vol_med = []
                                valor_mercado = []
                                valor_firma = []
                                ult_balanco_pro = []
                                nr_acoes = []
                                os_dia = []
                                pl = []
                                lpa = []
                                pvp = []
                                vpa = []
                                p_ebit = []
                                marg_bruta = []
                                psr = []
                                marg_ebit = []
                                p_ativo = []
                                marg_liquida = []
                                p_cap_giro = []
                                ebit_ativo = []
                                p_ativo_circ_liq = []
                                roic = []
                                div_yield = []
                                roe = []
                                ev_ebitda = []
                                liquidez_corr = []
                                ev_ebit = []
                                cres_rec = []
                                ativo = []
                                disponibilidades = []
                                ativo_circulante = []
                                divd_bruta = []
                                divd_liquida = []
                                patr_liquido = []
                                lucro_liquido_12m = []
                                lucro_liquido_3m = []

                                dadosI = data.find_all("span", {"class": "txt"})
                                dadosO = data.find_all("span", {"class": "oscil"})

                                if dadosI:

                                    #
                                    papel.append(dadosI[0].text)
                                    if "Papel" in papel[0]:
                                        papel.append(dadosI[1].text.replace(" ", ""))
                                    else:
                                        papel.append(0)
                                    #
                                    tipo.append(dadosI[4].text)
                                    if "Tipo" in tipo[0]:
                                        tipo.append(dadosI[5].text)
                                    else:
                                        tipo.append(0)
                                    #
                                    empresa.append(dadosI[8].text)
                                    if "Empresa" in empresa[0]:
                                        empresa.append(dadosI[9].text)
                                    else:
                                        empresa.append(0)
                                    #
                                    setor.append(dadosI[12].text)
                                    if "Setor" in setor[0]:
                                        setor.append(dadosI[13].text)
                                    else:
                                        setor.append(0)
                                    #
                                    cotacao.append(dadosI[2].text)
                                    if "Cotação" in cotacao[0]:
                                        cotacao.append(dadosI[3].text)
                                    else:
                                        cotacao.append(0)
                                    #
                                    dt_ult_cotacao.append(dadosI[6].text)
                                    if "Data últ cot" in dt_ult_cotacao[0]:
                                        dt_ult_cotacao.append(dadosI[7].text)
                                    else:
                                        dt_ult_cotacao.append(0)
                                    #
                                    min_52_sem.append(dadosI[10].text)
                                    if "Min 52 sem" in min_52_sem[0]:
                                        min_52_sem.append(dadosI[11].text)
                                    else:
                                        min_52_sem.append(0)
                                    #
                                    max_52_sem.append(dadosI[14].text)
                                    if "Max 52 sem" in max_52_sem[0]:
                                        max_52_sem.append(dadosI[15].text)
                                    else:
                                        max_52_sem.append(0)
                                    #
                                    vol_med.append(dadosI[18].text)
                                    if "Vol $ méd (2m)" in vol_med[0]:
                                        vol_med.append(dadosI[19].text)
                                    else:
                                        vol_med.append(0)
                                    #
                                    valor_mercado.append(dadosI[20].text)
                                    if "Valor de mercado" in valor_mercado[0]:
                                        valor_mercado.append(dadosI[21].text)
                                    else:
                                        valor_mercado.append(0)
                                    #
                                    valor_firma.append(dadosI[24].text)
                                    if "Valor da firma" in valor_firma[0]:
                                        valor_firma.append(dadosI[25].text)
                                    else:
                                        valor_firma.append(0)
                                    #
                                    ult_balanco_pro.append(dadosI[22].text)
                                    if "Últ balanço processado" in ult_balanco_pro[0]:
                                        ult_balanco_pro.append(dadosI[23].text)
                                    else:
                                        ult_balanco_pro.append(0)
                                    #
                                    nr_acoes.append(dadosI[26].text)
                                    if "Nro. Ações" in nr_acoes[0]:
                                        nr_acoes.append(dadosI[27].text.replace(".", ""))
                                    else:
                                        nr_acoes.append(0)
                                    #
                                    os_dia.append(dadosI[30].text)
                                    if "Dia" in os_dia[0]:
                                        os_dia.append(
                                            dadosO[0]
                                            .text.replace("\n", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                    else:
                                        os_dia.append(0)
                                    #
                                    pl.append(dadosI[31].text)
                                    if "P/L" in pl[0]:
                                        pl.append(
                                            dadosI[32].text.replace(".", "").replace(",", ".")
                                        )
                                    else:
                                        pl.append(0)
                                    #
                                    lpa.append(dadosI[33].text)
                                    if "LPA" in lpa[0]:
                                        lpa.append(dadosI[34].text.replace(",", "."))
                                    else:
                                        lpa.append(0)
                                    #
                                    pvp.append(dadosI[36].text)
                                    if "P/VP" in pvp[0]:
                                        pvp.append(
                                            dadosI[37].text.replace(".", "").replace(",", ".")
                                        )
                                    else:
                                        pvp.append(0)
                                    #
                                    vpa.append(dadosI[38].text)
                                    if "VPA" in vpa[0]:
                                        vpa.append(
                                            dadosI[39].text.replace(".", "").replace(",", ".")
                                        )
                                    else:
                                        vpa.append(0)
                                    #
                                    p_ebit.append(dadosI[41].text)
                                    if "P/EBIT" in p_ebit:
                                        p_ebit.append(
                                            dadosI[42].text.replace("\n", "").replace(",", ".")
                                        )
                                        if len(p_ebit[1]) <= 1:
                                            p_ebit[1] = 0
                                        elif len(p_ebit[1]) >= 8:
                                            p_ebit[1] = 0
                                    else:
                                        p_ebit.append(0)
                                    #
                                    marg_bruta.append(dadosI[43].text)
                                    if "Marg. Bruta" in marg_bruta:
                                        marg_bruta.append(
                                            dadosI[44]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(marg_bruta[1]) <= 1:
                                            marg_bruta[1] = 0
                                    else:
                                        marg_bruta.append(0)
                                    #
                                    psr.append(dadosI[46].text)
                                    if "PSR" in psr:
                                        psr.append(
                                            dadosI[47]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(psr[1]) <= 1:
                                            psr[1] = 0
                                    else:
                                        psr.append(0)
                                    #
                                    marg_ebit.append(dadosI[48].text)
                                    if "Marg. EBIT" in marg_ebit:
                                        marg_ebit.append(
                                            dadosI[49]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(marg_ebit[1]) <= 1:
                                            marg_ebit[1] = 0
                                    else:
                                        marg_ebit.append(0)
                                    #
                                    p_ativo.append(dadosI[51].text)
                                    if "P/Ativos" in p_ativo:
                                        p_ativo.append(
                                            dadosI[52]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(p_ativo[1]) <= 1:
                                            p_ativo[1] = 0
                                    else:
                                        p_ativo.append(0)
                                    #
                                    marg_liquida.append(dadosI[53].text)
                                    if "Marg. Líquida" in marg_liquida:
                                        marg_liquida.append(
                                            dadosI[54]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(marg_liquida[1]) <= 1:
                                            marg_liquida[1] = 0
                                    else:
                                        marg_liquida.append(0)
                                    #
                                    p_cap_giro.append(dadosI[56].text)
                                    if "P/Cap. Giro" in p_cap_giro:
                                        p_cap_giro.append(
                                            dadosI[57]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(p_cap_giro[1]) <= 1:
                                            p_cap_giro[1] = 0
                                    else:
                                        p_cap_giro.append(0)
                                    #
                                    ebit_ativo.append(dadosI[58].text)
                                    if "EBIT / Ativo" in ebit_ativo:
                                        ebit_ativo.append(
                                            dadosI[59]
                                            .text.replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(ebit_ativo[1]) <= 1:
                                            ebit_ativo[1] = 0
                                    else:
                                        ebit_ativo.append(0)
                                    #
                                    p_ativo_circ_liq.append(dadosI[61].text)
                                    if "P/Ativ Circ Liq" in p_ativo_circ_liq:
                                        p_ativo_circ_liq.append(
                                            dadosI[62]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(p_ativo_circ_liq[1]) <= 1:
                                            p_ativo_circ_liq[1] = 0
                                    else:
                                        p_ativo_circ_liq.append(0)
                                    #
                                    roic.append(dadosI[63].text)
                                    if "ROIC" in roic:
                                        roic.append(
                                            dadosI[64]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(roic[1]) <= 1:
                                            roic[1] = 0
                                    else:
                                        roic.append(0)
                                    #
                                    div_yield.append(dadosI[66].text)
                                    if "Div. Yield" in div_yield:
                                        div_yield.append(
                                            dadosI[67].text.replace(",", ".").replace("%", "")
                                        )
                                        if len(div_yield[1]) <= 1:
                                            div_yield[1] = 0
                                    else:
                                        div_yield.append(0)
                                    #
                                    roe.append(dadosI[68].text)
                                    if "ROE" in roe:
                                        roe.append(
                                            dadosI[69]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                        )
                                        if len(roe[1]) <= 1:
                                            roe[1] = 0
                                    else:
                                        roe.append(0)
                                    #
                                    ev_ebitda.append(dadosI[71].text)
                                    if "EV / EBITDA" in ev_ebitda:
                                        ev_ebitda.append(
                                            dadosI[72]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(ev_ebitda[1]) <= 1:
                                            ev_ebitda[1] = 0
                                    else:
                                        ev_ebitda.append(0)
                                    #
                                    liquidez_corr.append(dadosI[73].text)
                                    if "Liquidez Corr" in liquidez_corr:
                                        liquidez_corr.append(
                                            dadosI[74].text.replace("\n", "").replace(",", ".")
                                        )
                                        if len(liquidez_corr[1]) <= 1:
                                            liquidez_corr[1] = 0
                                    else:
                                        liquidez_corr.append(0)
                                    #
                                    ev_ebit.append(dadosI[76].text)
                                    if "EV / EBIT" in ev_ebit:
                                        ev_ebit.append(
                                            dadosI[77]
                                            .text.replace("\n", "")
                                            .replace(".", "")
                                            .replace(",", ".")
                                        )
                                        if len(ev_ebit[1]) <= 1:
                                            ev_ebit[1] = 0
                                    else:
                                        ev_ebit.append(0)
                                    #
                                    cres_rec.append(dadosI[81].text)
                                    if "Cres. Rec (5a)" in cres_rec:
                                        cres_rec.append(
                                            dadosI[82]
                                            .text.replace("\n", "")
                                            .replace(",", ".")
                                            .replace("%", "")
                                            .replace("-", "0")
                                        )
                                        if len(cres_rec[1]) <= 1:
                                            cres_rec[1] = 0
                                        elif len(cres_rec[1]) >= 5:
                                            del cres_rec[1]
                                            cres_rec.append(
                                                dadosI[82]
                                                .text.replace("\n", "")
                                                .replace("%", "")
                                                .replace(".", "")
                                                .replace(",", ".")
                                            )
                                    else:
                                        cres_rec.append(0)
                                    #
                                    if setor[1] == "Intermediários Financeiros":
                                        ativo.append("Ativo")
                                        ativo.append(dadosI[87].text)
                                        disponibilidades.append("Disponibilidades")
                                        disponibilidades.append("0")
                                        ativo_circulante.append("Ativo Circulante")
                                        ativo_circulante.append("0")
                                        divd_bruta.append("Dív. Bruta")
                                        divd_bruta.append("0")
                                        divd_liquida.append("Dív. Líquida")
                                        divd_liquida.append("0")
                                        patr_liquido.append("Patrim. Líq")
                                        patr_liquido.append(dadosI[93].text)
                                        lucro_liquido_12m.append("Lucro Líquido")
                                        lucro_liquido_12m.append(dadosI[106].text)
                                        lucro_liquido_3m.append("Lucro Líquido")
                                        lucro_liquido_3m.append(dadosI[108].text)
                                    else:
                                        ativo.append(dadosI[86].text)
                                        if "Ativo" in ativo:
                                            ativo.append(dadosI[87].text)
                                        else:
                                            ativo.append(0)
                                        #
                                        disponibilidades.append(dadosI[90].text)
                                        if "Disponibilidades" in disponibilidades:
                                            disponibilidades.append(dadosI[91].text)
                                        else:
                                            disponibilidades.append(0)
                                        #
                                        ativo_circulante.append(dadosI[94].text)
                                        if "Ativo Circulante" in ativo_circulante:
                                            ativo_circulante.append(dadosI[95].text)
                                        else:
                                            ativo_circulante.append(0)
                                        #
                                        divd_bruta.append(dadosI[88].text)
                                        if "Dív. Bruta" in divd_bruta:
                                            divd_bruta.append(dadosI[89].text)
                                        else:
                                            divd_bruta.append(0)
                                        #
                                        divd_liquida.append(dadosI[92].text)
                                        if "Dív. Líquida" in divd_liquida:
                                            divd_liquida.append(dadosI[93].text)
                                        else:
                                            divd_liquida.append(0)
                                        #
                                        patr_liquido.append(dadosI[96].text)
                                        if "Patrim. Líq" in patr_liquido:
                                            patr_liquido.append(dadosI[97].text)
                                        else:
                                            patr_liquido.append(0)
                                        #
                                        lucro_liquido_12m.append(dadosI[109].text)
                                        if "Lucro Líquido" in lucro_liquido_12m:
                                            lucro_liquido_12m.append(dadosI[110].text)
                                        else:
                                            lucro_liquido_12m.append(0)
                                        #
                                        lucro_liquido_3m.append(dadosI[111].text)
                                        if "Lucro Líquido" in lucro_liquido_3m:
                                            lucro_liquido_3m.append(dadosI[112].text)
                                        else:
                                            lucro_liquido_3m.append(0)

                                    # Query para inserir os dados coletados no banco de dados Postgres
                                    query_insert_bd = f" INSERT INTO dados VALUES ( '{dt}','{papel[1]}\
                                ','{tipo[1]}','{empresa[1]}','{setor[1]}','{cotacao[1]}','\
                                {dt_ult_cotacao[1]}','{min_52_sem[1]}','{max_52_sem[1]}','\
                                {vol_med[1]}','{valor_mercado[1]}','{valor_firma[1]}','\
                                {ult_balanco_pro[1]}','{nr_acoes[1]}','{os_dia[1]}','\
                                {pl[1]}','{lpa[1]}','{pvp[1]}','{vpa[1]}','{p_ebit[1]}','\
                                {marg_bruta[1]}','{psr[1]}','{marg_ebit[1]}','{p_ativo[1]}','\
                                {marg_liquida[1]}','{p_cap_giro[1]}','{ebit_ativo[1]}','\
                                {p_ativo_circ_liq[1]}','{roic[1]}','{div_yield[1]}','\
                                {roe[1]}','{ev_ebitda[1]}','{liquidez_corr[1]}','{ev_ebit[1]}','\
                                {cres_rec[1]}','{ativo[1]}','{disponibilidades[1]}','\
                                {ativo_circulante[1]}','{divd_bruta[1]}','{divd_liquida[1]}','\
                                {patr_liquido[1]}','{lucro_liquido_12m[1]}','{lucro_liquido_3m[1]}' ) "

                                    # Inserindo os dados coletados no banco de dados Postgres
                                    __conectdb__.in_dados(query_insert_bd)

                                    print(
                                        f"+{GREEN} Dados da ação: {i}, gravados com sucesso {RESET}+"
                                    )
                                    # --- #
                                    n += 1

                            # Dados atual - Salvando os dados atuais no Dataframe
                            dados_atual.loc[dados_atual.shape[0]] = [
                                papel[1],
                                tipo[1],
                                empresa[1],
                                setor[1],
                                cotacao[1],
                                dt_ult_cotacao[1],
                                min_52_sem[1],
                                max_52_sem[1],
                                vol_med[1],
                                valor_mercado[1],
                                valor_firma[1],
                                ult_balanco_pro[1],
                                nr_acoes[1],
                                os_dia[1],
                                pl[1],
                                lpa[1],
                                pvp[1],
                                vpa[1],
                                p_ebit[1],
                                marg_bruta[1],
                                psr[1],
                                marg_ebit[1],
                                p_ativo[1],
                                marg_liquida[1],
                                p_cap_giro[1],
                                ebit_ativo[1],
                                p_ativo_circ_liq[1],
                                roic[1],
                                div_yield[1],
                                roe[1],
                                ev_ebitda[1],
                                liquidez_corr[1],
                                ev_ebit[1],
                                cres_rec[1],
                                ativo[1],
                                disponibilidades[1],
                                ativo_circulante[1],
                                divd_bruta[1],
                                divd_liquida[1],
                                patr_liquido[1],
                                lucro_liquido_12m[1],
                                lucro_liquido_3m[1],
                            ]

                            # Dados atual - Salvando os dados atuais em um arquivo .csv
                            dados_atual.to_csv("../Dados_Atual/dados.csv", sep=";")

                except NameError:
                    print(f"+{RED} Dados da ação: {i}, não gravados {RESET}+")
                    pass

            # Removendo linhas(tabela dados) do Banco de Dados com valores vazios (ref.: na coluna papel)
            delete_vazio = __query__.delete_vazio_query
            __conectdb__.in_dados(delete_vazio)

            # Removendo linhas(tabela dados) do Banco de Dados duplicados (ref.: na coluna papel / data_ult_cotacao )
            delete_duplicados = __query__.delete_duplicados_query
            __conectdb__.in_dados(delete_duplicados)

            # Removendo espaços em braco da coluna 'papel'
            remove_espaco = __query__.espaco_query
            __conectdb__.in_dados(remove_espaco)

            # Backup do banco de dados csv
            csv_file_name = "../Backup/some_file.csv"
            bk = __query__.backup_query
            with open(csv_file_name, "w") as f:
                __conectdb__.bk(bk, f)

            # Fim do contador de Tempo do script
            fim = time.time()
            hours, rem = divmod(fim - inicio, 3600)
            minutes, seconds = divmod(rem, 60)

            # Fim
            print(f"{RED}-----------------{RESET}")
            print(f"{BLUE}Finalizou. {n} Empresa(s) Cadastrada(s)")
            print(
                "Tempo: {:0>2}:{:0>2}:{:05.2f}".format(
                    int(hours), int(minutes), seconds
                )
            )
            print(f"{RESET}{RED}-----------------{RESET}")


if __name__ == "__main__":
    dados()

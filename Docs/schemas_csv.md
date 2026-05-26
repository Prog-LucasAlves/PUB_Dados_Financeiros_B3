# 📊 Schemas e Dicionários de Dados (CSV local)

Esta documentação descreve detalhadamente o formato físico, tipos de dados e propósitos das colunas para cada um dos arquivos CSV armazenados localmente sob a pasta `Api/` no projeto **Neo-B3 Obsidian**.

Todos os arquivos CSV usam codificação UTF-8, codificação de quebra de linha padrão do sistema e ponto e vírgula (`;`) como caractere delimitador de campos.

---

## 1. Preços Históricos (`Api/precos/{TICKER}.csv`)

Este arquivo contém a série temporal diária completa de cotações de fechamento, retornos estatísticos e volatilidade histórica do ativo.

| Coluna | Tipo | Formato | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Date** | Date | `YYYY-MM-DD` | Data do pregão. Chave primária temporal. | `2026-05-25` |
| **{TICKER}** | Float | Decimal | Preço de fechamento ajustado (ex: `AALR3`). | `12.45` |
| **Open** | Float | Decimal | Preço de abertura do ativo na sessão. | `12.30` |
| **ret** | Float | Percentual | Retorno percentual simples diário. | `1.22` (ou seja, 1.22%) |
| **tret** | Float | Percentual | Retorno acumulado (soma cumulativa simples de `ret`). | `15.89` |
| **Returns** | Float | Decimal | Retorno simples diário em formato decimal. | `0.0122` |
| **Target** | Float | Decimal | Retorno simples do dia seguinte (usado para IA). | `-0.005` |
| **Vol** | Float | Decimal | Volatilidade móvel anualizada (janela de 20 dias). | `0.2450` (24.50% a.a.) |
| **MM20** | Float | Decimal | Média Móvel Aritmética simples de 20 pregões. | `12.15` |
| **Detrend** | Float | Decimal | Preço atual menos a MM20 (indica oscilações da tendência). | `0.30` |

---

## 2. Histórico de Proventos (`Api/proventos/{TICKER}.csv`)

Lista as distribuições corporativas de proventos em dinheiro ocorridas historicamente para a companhia selecionada.

| Coluna | Tipo | Formato | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Unnamed: 0** | Int | Sequencial | Índice de linha incremental gerado pelo Pandas. | `0` |
| **Data** | Date | `DD/MM/YYYY` | Data-com (direito de receber o provento). | `27/04/2020` |
| **Valor** | Float | Moeda BRL | Valor distribuído por cada unidade de ação. | `0.0872` |
| **Tipo** | String | Texto | Tipo de provento distribuído pela empresa. | `DIVIDENDO` ou `JCP` |
| **Data de Pagamento** | String | `DD/MM/YYYY` | Data oficial em que os valores foram liquidados. | `07/05/2019` ou `-` |
| **Por quantas ações** | Int | Inteiro | Fator multiplicador unitário de direito ao provento. | `1` |
| **Acao** | String | Sigla B3 | Identificador (Ticker) do papel (redundante para verificação). | `AALR3` |

---

## 3. Releases Trimestrais (`Api/trimestre/{TICKER}.csv`)

Guarda os links para as demonstrações trimestrais oficiais e os respectivos PDFs contendo os releases de resultados corporativos.

| Coluna | Tipo | Formato | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Unnamed: 0** | Int | Sequencial | Índice numérico do registro. | `0` |
| **Acao** | String | Sigla B3 | Identificador do ativo na bolsa. | `AALR3` |
| **Data Referência** | Date | `DD/MM/YYYY` | Fim do trimestre contábil de referência do release. | `30/09/2025` |
| **Demonstração Financeira** | String | URL HTTP | Link oficial para a visualização da DFP/ITR na CVM. | `http://www.rad.cvm.gov.br/...` |
| **Release de Resultados** | String | URL HTTP | Link para download do release de resultados em formato PDF. | `http://www.rad.cvm.gov.br/...` |

---

## 4. Fatos Relevantes (`Api/fatos_relevantes/{TICKER}.csv`)

Armazena as notícias e os relatórios oficiais de Fatos Relevantes (IPE/Rad) publicados à CVM pelas companhias emissoras.

| Coluna | Tipo | Formato | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| **Unnamed: 0** | Int | Sequencial | Índice de registro incremental. | `43` |
| **Acao** | String | Sigla B3 | Ticker do ativo emissor da notícia. | `BBAS3` |
| **Data** | Date | `DD/MM/YYYY` | Data oficial de protocolamento da notícia. | `17/03/2025` |
| **Hora** | Time | `HH:MM` | Horário exato de recebimento oficial pela CVM. | `18:06` |
| **Descrição** | String | Texto livre | Título descritivo do relatório ou fato anunciado. | `Atualização dos proventos até o pagamento` |
| **Link** | String | URL HTTP | Link seguro para download ou visualização do protocolo oficial. | `https://www.rad.cvm.gov.br/...` |

# ⚙️ Pipelines de Captura e Processamento Financeiro (`Api/`)

Esta documentação descreve o funcionamento interno, arquitetura técnica e algoritmos contidos nos scripts da pasta `Api/` do ecossistema **Neo-B3 Obsidian**.

---

## 1. Engine de Preços & Cotações (`Api/__apiprecos__.py`)

Este módulo é o coração de captura histórica da plataforma, integrando-se diretamente à biblioteca pública `yfinance` para popular os arquivos de preços individuais de cada ativo.

### A. Parser Dinâmico MultiIndex vs. SingleIndex
O `yfinance` altera sua estrutura de colunas com base no número de ativos solicitados no download:
- **Download Multiativos**: Retorna um DataFrame com colunas agrupadas em um `MultiIndex` de dois níveis (ex: `('Close', 'AALR3')`, `('Adj Close', 'ABCB4')`).
- **Download de Ativo Único**: Retorna colunas em nível simples (`SingleIndex` contendo apenas `['Close', 'Adj Close', 'Open', ...]`).

Para garantir estabilidade, o script implementa uma camada adaptativa de extração:
```python
# Caso o retorno venha em estrutura MultiIndex
if isinstance(downloaded.columns, pd.MultiIndex):
    close_data = downloaded["Close"][ticker]
else:
    close_data = downloaded["Close"]
```
Isso evita quebras comuns de `KeyError` e garante compatibilidade com as versões recentes do Yahoo Finance.

### B. Algoritmo de Contingência por Passeio Aleatório Geométrico (GBM)
Se o download falhar completamente devido a problemas de rede/DNS local, o script ativa de forma imediata o motor de contingência. Ele recupera a última cotação contábil cadastrada no banco de dados e projeta uma série de 90 dias úteis simulando um passeio aleatório baseado em ruído gaussiano (médias de mercado realistas para modelar a cotação de forma crível):
* **Fórmula de Projeção**:
  $$S_t = S_{t-1} \times \left(1 + N(0.0002, 0.015)\right)$$
* **Garantia de Fluxo**: Todos os indicadores secundários (`ret`, `tret`, `Vol`, `MM20`, `Detrend`) são recalculados dinamicamente sobre a série gerada para permitir a plotagem perfeita no dashboard.

---

## 2. Engine de Performance & Retornos (`Api/__apiretorno__.py`)

Este pipeline coleta dados consolidados de múltiplos ativos simultaneamente com foco na comparação de performance temporal de curto e médio prazo.

### A. Construção da Matriz `cotacoes.csv`
O script baixa em lote as últimas 80 sessões de todos os ativos contidos no arquivo mestre `__list__.py`. Ele extrai as colunas `Close` de cada um deles e as consolida em uma única tabela pivotada, onde o índice temporal é a data de fechamento e cada coluna representa o preço de uma ação listada na B3.

### B. Cálculo de Retornos Acumulados Dinâmicos (Rolagem Temporal)
Através da função `retornoAcumuladodias(X)`, a matriz `cotacoes.csv` é segmentada para os últimos `X` pregões úteis. O script realiza os seguintes cálculos e transformações estruturais:
1. **Diferenciação Percentual**: Calcula a variação diária de cada ativo:
   $$\text{Variação}_t = \left(\frac{P_t}{P_{t-1}} - 1\right) \times 100$$
2. **Soma Acumulada**:
   $$\text{Total Acumulado} = \sum_{t=1}^{X} \text{Variação}_t$$
3. **Transposição e Ordenação**: Transpõe a matriz de modo que as linhas passem a ser os ativos e as colunas sejam as datas. O DataFrame final é ordenado de forma decrescente pelo `Total_Acumulado` para destacar as empresas mais eficientes do período e salvo como `retornos_acumulados_{X-1}d.csv`.

---

## 3. Engine de Proventos e Dividendos (`Api/__apipr__.py`)

Este módulo é responsável por extrair dados históricos corporativos de proventos em dinheiro diretamente da base pública do **Fundamentus**.

### A. Pipeline de Scraping
Para cada ticker da lista, o script monta a URL dinâmica de consulta:
```
https://fundamentus.com.br/proventos.php?papel={TICKER}&tipo=2
```
Ele realiza o parsing do código HTML por meio do `BeautifulSoup`, buscando a tabela de classe CSS padrão.

### B. Tratamento e Sanitização
Os dados contábeis de dividendos brutos e Juros sobre Capital Próprio (JCP) são sanitizados:
* Tratamento de vírgulas de moeda brasileira para pontos decimais padrões do sistema (`float`).
* Conversão de strings de data estruturadas (`DD/MM/YYYY`).
* Limpeza de caracteres vazios, tabulações ou dados de proventos declarados mas não-pagos. Os arquivos finais de proventos são exportados individualmente na pasta `./Api/proventos/` para consumo direto das abas financeiras.

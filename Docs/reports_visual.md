# 🎨 Visualização Gráfica e Templates de Relatório (`SRC/b3_reports/`)

Esta documentação descreve as diretrizes de design visual, paletas cromáticas e arquitetura técnica das ferramentas de geração de gráficos e templates de e-mail localizadas no pacote `SRC/b3_reports/` do ecossistema **Neo-B3 Obsidian**.

---

## 1. O Tema Visual "Obsidian Dark Theme"

Para manter consistência estética premium entre o painel Streamlit e os relatórios em PDF/e-mail gerados de forma programática, definimos um padrão visual de fundo escuro e acentos de alta legibilidade.

No Matplotlib, isso é configurado pela função `setup_obsidian_dark_theme()` que parametriza globalmente o `plt.rcParams`:
* **Cor de Fundo da Imagem**: `#0D0F12` (Escuro profundo).
* **Cor de Fundo dos Eixos**: `#161A1F` (Cinza chumbo).
* **Bordas dos Eixos**: Transparente e sutil com 8% de opacidade branca (`(1.0, 1.0, 1.0, 0.08)`).
* **Cores de Rótulos, Títulos e Escalas**: `#E2E8F0` (Gelo) e `#94A3B8` (Slate).
* **Grid interno**: Linhas discretas com 3% de opacidade branca.

---

## 2. Gráficos de Publicação (`charts.py`)

O módulo `charts.py` é responsável pela geração programática de gráficos de alta fidelidade (DPI 300) salvos localmente sob `./Api/relatorios/images/` para posterior anexo nos e-mails.

### A. Histórico de Cotações com Sombreado (`plot_stock_history`)
* **Visual**: Gráfico de linha que plota a evolução dos preços diários do ativo.
* **Cor da Linha**: `#00E676` (Verde esmeralda brilhante) de espessura `2.5`.
* **Fundo preenchido**: Uso do `ax.fill_between` aplicando opacidade suave de `8%` sob a curva de fechamento para conferir profundidade estética tridimensional.

### B. Comparativo de Graham Horizontal (`plot_graham_bar`)
* **Visual**: Gráfico de barras horizontais (`ax.barh`) comparando a cotação de mercado atual frente ao Valor Justo calculado pela fórmula de Benjamin Graham.
* **Inteligência Cromática**:
  - A barra de "Cotação Atual" é sempre renderizada em cinza neutro `#94A3B8`.
  - A barra de "Valor Justo" muda dinamicamente de cor: fica verde `#00E676` (Desconto/Margem positiva) ou vermelha `#FF3D71` (Prêmio/Margem negativa) de acordo com a atratividade do preço.
* **Text Overlay**: Os valores em R$ são renderizados de forma limpa diretamente na ponta de cada barra com fontes em negrito para facilitar o escaneamento do investidor.

### C. Heatmap Multivariado de Correlação do Setor (`plot_correlation_heatmap`)
* **Visual**: Matriz térmica gerada com `ax.imshow` para mapear a correlação estatística entre os principais indicadores financeiros (`PL`, `PVP`, `Dividend Yield`, `ROE` e `ROIC`) das empresas de um mesmo setor industrial.
* **Colormap Utilizado**: `coolwarm` (azul indica forte correlação negativa, vermelho indica forte correlação positiva e bege representa neutralidade).
* **Contraste Dinâmico de Texto**: O script escreve o coeficiente numérico exato no centro de cada bloco. A cor da fonte do texto se ajusta de forma autônoma para garantir legibilidade máxima: preto `#0D0F12` em células saturadas e branco `#F8FAFC` em células claras.

---

## 3. Arquitetura Premium de E-mail (`email_template.py`)

A criação do template de e-mail obedece às mais estritas diretrizes de exibição responsiva corporativa e compatibilidade cross-client (Outlook, Gmail e Mail do iOS/macOS).

### A. Diretrizes Técnicas de e-mail HTML:
* **Largura Máxima**: Travada estritamente em **`680px`** para evitar deformação ou alongamento excessivo da linha em telas grandes.
* **Layout Baseado em Tabelas**: Uso de tabelas tradicionais aninhadas (`<table border="0">`) com `cellpadding="0"` e `cellspacing="0"` em detrimento de CSS Flexbox/Grid moderno, que são rejeitados pela engine do Microsoft Outlook.
* **CSS Inline**: Todo o estilo visual é acoplado diretamente nas tags HTML via atributo `style="..."` para garantir renderização idêntica entre clientes que cortam cabeçalhos `<style>`.

### B. Elementos de Design Premium Obsidian:
- **Degradê de Cabeçalho**: Barra de acento com gradiente de alta precisão (Emerald para Coral) separando o topo do corpo da mensagem.
- **Dark Mode Nativo**: Fundo do corpo central configurado com `#161A1F` e blocos de conteúdo com bordas arredondadas e sombras sutis com `#1C232B` para simular uma interface premium "glassmorphism".
- **Botões Premium**: Botões interativos com bordas arredondadas e sombras suaves, com estados hover tratados de forma segura para aumentar o engajamento na leitura de relatórios detalhados.

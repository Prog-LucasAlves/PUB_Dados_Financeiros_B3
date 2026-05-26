# 💎 Design System & Componentes Frontend: Neo-B3 Obsidian

Esta documentação descreve os padrões visuais, tokens de design, componentes de layout e injeções de estilo CSS contidos na interface Streamlit (**`app.py`**) da plataforma **Neo-B3 Obsidian**.

---

## 1. Diretrizes de Design & Paleta Cromática

A identidade visual do painel foi projetada sob o conceito **Obsidian Lab**, adotando uma interface sóbria, elegante e de alto contraste otimizada para longos períodos de leitura analítica.

* **Fundo da Aplicação**: `#0B0F13` (Preto profundo com matiz azulado discreto).
* **Fundo de Cards e Widgets**: `#141820` (Cinza Obsidian escuro com 4% de opacidade de bordas brancas).
* **Borda Neutra Secundária**: `rgba(255, 255, 255, 0.04)` (Linhas finas discretas).
* **Cor de Destaque Primária (Brand Accent)**: `#10B981` (Esmeralda - utilizado para dados positivos, destaques, abas ativas e botões primários).
* **Cor de Alerta/Atenção**: `#EF4444` (Coral - utilizado para dados negativos, alertas de contingência e logs de erro).
* **Tipografia Curada**:
  - **Interface & Títulos**: `Outfit` (fonte geométrica moderna importada do Google Fonts).
  - **Valores e Séries Numéricas**: `JetBrains Mono` (fonte monoespaçada ideal para alinhamento simétrico de dados contábeis).

---

## 2. Injeção Dinâmica de CSS (`inject_custom_css()`)

Para contornar as limitações de estilo nativas do Streamlit e aplicar a estética **Obsidian**, injetamos uma folha de estilos CSS customizada no início da renderização por meio da função `inject_custom_css()`.

### A. Elementos Customizados no CSS:
* **`div[data-testid="stDataFrame"]`**: Customização de tabelas e dataframes do Pandas, aplicando fundo Obsidian chumbo `#141820`, borda sutil e cantos arredondados.
* **`button[data-baseweb="tab"]`**: Estilização premium das abas nativas, tornando-as transparentes por padrão com transição de cor suave (`transition: all 0.2s ease`). A aba selecionada ganha a cor verde esmeralda e uma borda inferior discreta.
* **`.custom-hr`**: Linha divisória horizontal customizada de 1px com transparência para ritmo de seção uniforme.
* **`.tooltip-text`**: Sistema interno de tooltips puramente em CSS para exibir dicas contextuais sem sobrecarregar a tela:
  - Fica oculto por padrão (`visibility: hidden`, `opacity: 0`).
  - É revelado suavemente no estado hover com efeitos tridimensionais (`transform: translateX(-50%) translateY(-2px)`).

---

## 3. Catálogo de Componentes Frontend

O Streamlit monta a tela utilizando componentes em blocos modulares estilizados por tags HTML inlines.

### A. Cartão de Métrica Premium (`render_metric_card`)
Este componente renderiza os dados operacionais mais relevantes no balanço patrimonial e nos demonstrativos de mercado.
- **Estrutura**:
```
+---------------------------------------+
| ROE  [ⓘ]                              | <- Label em caixa alta com tooltip
| R$ 12.450.000,00                      | <- Valor com fonte JetBrains Mono
| ▲ 15.42%                              | <- Delta indicador dinâmico (positivo/negativo)
+---------------------------------------+
```
- **Dinâmica de Deltas**: Se o valor do delta for positivo, ele ganha a cor esmeralda `#10B981` e o símbolo `▲`. Se for negativo, ganha a cor coral `#EF4444` e o símbolo `▼`.

### B. Painel de Integridade de Dados (`check_stock_data_integrity`)
Localizado na barra lateral (Sidebar), avalia a saúde física dos dados locais do ticker selecionado:
- **Estados Dinâmicos**:
  - **Disponível**: Renderizado com cor `#10B981` (Círculo esmeralda).
  - **Não se aplica**: Renderizado em cinza `#64748B` (Círculo cinza) para indicar ausência normal de proventos corporativos ou demonstrações secundárias sem gerar falsos-positivos na integridade.
  - **Ausente**: Vermelho `#EF4444` (apenas para arquivos críticos como Preços Históricos).

### C. Alerta de Modo de Contingência
Exibido de forma responsiva no topo da seção de gráficos se o Yahoo Finance estiver inacessível:
* **Visual**: Card chumbo escuro com borda esquerda rígida em coral (`border-left: 3px solid #EF4444`) e texto descritivo suave informando que o passeio aleatório foi acionado para simular o comportamento histórico a partir do último fechamento consolidado.

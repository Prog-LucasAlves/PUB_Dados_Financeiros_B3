---
name: Neo-B3 Obsidian
description: Painel financeiro de alto contraste e fidelidade técnica para análise de ativos.
colors:
  primary: "#00E676"
  negative: "#FF3D71"
  neutral-bg: "#0D0F12"
  neutral-sidebar: "#111418"
  neutral-card: "#161A1F"
  text-main: "#E2E8F0"
  text-muted: "#94A3B8"
  text-highlight: "#F8FAFC"
typography:
  display:
    fontFamily: "Outfit, -apple-system, BlinkMacSystemFont, sans-serif"
    fontWeight: 600
  body:
    fontFamily: "Outfit, -apple-system, BlinkMacSystemFont, sans-serif"
    fontWeight: 400
  mono:
    fontFamily: "JetBrains Mono, monospace"
    fontWeight: 500
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
spacing:
  sm: "12px"
  md: "18px"
  lg: "24px"
components:
  card:
    backgroundColor: "{colors.neutral-card}"
    rounded: "{rounded.md}"
    padding: "18px"
  tab-inactive:
    textColor: "{colors.text-muted}"
    padding: "10px 20px"
  tab-active:
    textColor: "{colors.primary}"
    padding: "10px 20px"
---

# Design System: Neo-B3 Obsidian

## 1. Overview

**Creative North Star: "O Laboratório Obsidiana" (The Obsidian Lab)**

"O Laboratório Obsidiana" é um ambiente de alta precisão analítica e imersão técnica. O visual é ancorado em uma atmosfera escura e relaxante que reduz drasticamente a fadiga ocular do investidor durante longas sessões de triagem de ações. O contraste é cirúrgico e funcional: o fundo preto obsidiana absoluto define a tela, enquanto as cores Verde Néon (lucro/sucesso) e Rosa (prejuízo/alerta) conduzem ativamente o olhar aos pontos vitais de dados de valuation.

O sistema rejeita explicitamente a estética confusa e desordenada do estilo Bloomberg tradicional, substituindo-a por um ritmo visual onde cada métrica tem espaço para respirar e cada tabela possui alinhamentos impecáveis.

**Key Characteristics:**
*   **Fundo Escuro Imersivo**: Neutros frios e profundos que proporcionam excelente legibilidade física.
*   **Contraste de Acentuação Cirúrgico**: Uso restrito de luz néon estritamente associado ao significado dos dados de mercado.
*   **Legibilidade Numérica Tabular**: Toda métrica quantitativa e numérica é disposta em uma fonte mono-espaçada precisa.
*   **Simplicidade e Respiro**: Segmentação clara por abas e cartões reativos que simplificam a usabilidade.

## 2. Colors

O esquema de cores é projetado para guiar as análises de forma intuitiva, onde a matiz sinaliza diretamente a saúde financeira do ativo pesquisado.

### Primary
*   **Verde Néon** (#00E676): Indica valor positivo, upside na fórmula de Graham, lucros ascendentes ou retornos históricos de mercado positivos. Utilizado em botões ativos, links importantes e valores financeiros saudáveis.

### Secondary
*   **Rosa Néon** (#FF3D71): Indica valor negativo, downside, empresas em prejuízo ou volatilidade/risco acentuado na cotação. Utilizado em alertas de segurança e valores em declínio.

### Neutral
*   **Fundo Obsidian** (#0D0F12): O plano de fundo absoluto da aplicação, minimizando o brilho da tela.
*   **Fundo Sidebar** (#111418): Tom ligeiramente mais claro para criar contraste e definir o painel lateral de seleção de ativos.
*   **Cartão Neutro** (#161A1F): Superfície elevada onde as informações de ativos são organizadas.
*   **Texto Principal** (#E2E8F0): Tom cinza-claro suave (slate) para leitura confortável do corpo de texto e títulos.
*   **Texto Mudo** (#94A3B8): Cinza médio para rótulos de métricas e informações secundárias.
*   **Destaque Brilhante** (#F8FAFC): Branco puro-gelo para ressaltar os números e valores finais.

### Named Rules
**The Neon Signal Rule.** As cores néon (#00E676 e #FF3D71) são condutoras de informação. Elas nunca devem ser usadas para decorações genéricas, fundos inteiros de blocos ou divisores. Se um elemento visual é colorido com néon, ele obrigatoriamente representa um estado ativo ou um dado financeiro positivo/negativo.

## 3. Typography

**Display Font:** Outfit (com fallbacks `-apple-system, BlinkMacSystemFont, sans-serif`)
**Body Font:** Outfit
**Label/Mono Font:** JetBrains Mono (com fallback `monospace`)

**Character:**
O pareamento combina a elegância moderna e geométrica de *Outfit* para os títulos e rótulos da interface com a extrema precisão mecânica e legibilidade de *JetBrains Mono* para todos os números, tabelas e cálculos.

### Hierarchy
*   **Subheader** (Outfit, weight 600, size 1.5rem, line-height 1.2): Títulos de seções principais do painel. Sempre acompanhado por uma borda esquerda de (4px) em Verde Néon para firmeza visual.
*   **Metric Label** (Outfit, weight 500, size 12px, letter-spacing 0.5px, uppercase): Rótulos curtos posicionados acima de valores financeiros.
*   **Metric Value** (JetBrains Mono, weight 700, size 24px): O número principal da métrica, garantindo alinhamento perfeito de caracteres em colunas.
*   **Body** (Outfit, weight 400, size 15px, line-height 1.6): Textos explicativos e descrições qualitativas.

## 4. Elevation

O sistema utiliza elevação **Estrutural** sutil para delimitar áreas de interesse e organizar visualmente o fluxo de triagem de ações, combatendo o achatamento visual.

### Shadow Vocabulary
*   **Card Shadow** (`box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3)`): Sombra sutil que eleva os cartões neutros acima do fundo Obsidian, indicando sua natureza interativa.
*   **Graham Shadow** (`box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4)`): Sombra mais profunda para destacar a seção crucial do cálculo do Valor Justo de Graham.

### Named Rules
**The Hover Glow Rule.** Cartões interativos reagem fisicamente ao ponteiro do mouse. Ao sofrer hover, o cartão realiza uma transição suave elevando-se (`transform: translateY(-2px)`), alterando a cor de sua borda para um tom translúcido de Verde Néon (`border-color: rgba(0, 230, 118, 0.2)`) e emitindo um leve brilho de fundo (`box-shadow: 0 6px 16px rgba(0, 230, 118, 0.05)`).

## 5. Components

### Buttons / Tabs
*   **Shape**: Bordas retas ou com acabamento plano no Streamlit.
*   **Tabs**: Abas de navegação utilizam fundo transparente com texto cinza mudo (#94A3B8) e tamanho (16px). A aba ativa transiciona para a cor Verde Néon (#00E676), adiciona uma borda inferior néon de (2px) e peso de fonte (600).
*   **Link Buttons**: Botões de link externo (como RI da Ação) usam fundo Cartão Neutro (#161A1F), texto Verde Néon (#00E676), borda de 1px em Verde Néon translúcido (`border: 1px solid rgba(0, 230, 118, 0.3)`) e cantos arredondados (8px). Em hover, o fundo ganha opacidade verde néon (`background: rgba(0, 230, 118, 0.1)`) e a borda se ilumina inteiramente em Verde Néon.

### Cards / Containers
*   **Metric Cards**: Cantos arredondados médios (12px), fundo Cartão Neutro (#161A1F), borda sutil de 1px translúcida (`border: 1px solid rgba(255, 255, 255, 0.05)`), estofamento (padding) de (18px) para garantir respiro físico.
*   **Graham Card**: Cantos arredondados grandes (16px), fundo com gradiente linear dinâmico (`linear-gradient(135deg, #161A1F 0%, #111418 100%)`). O contorno esquerdo recebe uma faixa sólida de (6px) em Verde Néon (caso haja desconto/margem positiva) ou Rosa Néon (se houver sobrepreço ou prejuízo).

### Tables / DataFrames
*   **Style**: Organizadas dentro de contêineres arredondados (12px) com borda de 1px (`rgba(255, 255, 255, 0.05)`), fundo Cartão Neutro (#161A1F) e estofamento interno de (6px). As linhas utilizam cores alternadas muito discretas e números estritamente formatados em `JetBrains Mono`.

## 6. Do's and Don'ts

### Do:
*   **Do** usar `JetBrains Mono` para cada algarismo numérico, porcentagem ou moeda, garantindo o alinhamento tabular vertical em tabelas e cartões de métricas.
*   **Do** manter um padding mínimo de (18px) em cartões e contêineres para preservar o respiro visual e o conforto de leitura.
*   **Do** aplicar a regra **Hover Glow** em todos os cartões interativos do painel de triagem de ações.
*   **Do** utilizar o Verde Néon e o Rosa Néon exclusivamente como indicadores de estado financeiro e interatividade.

### Don't:
*   **Don't** criar painéis semelhantes ao terminal Bloomberg com dezenas de tabelas amontoadas sem espaçamento e sem abas de segmentação.
*   **Don't** aplicar gradientes multicoloridos em textos da interface.
*   **Don't** utilizar bordas laterais coloridas de destaque (side-stripes) de espessura superior a 1px em cartões comuns, exceto para a barra sólida de 6px do cartão de destaque de Benjamin Graham.
*   **Don't** usar o preto puro (#000000) ou branco puro (#FFFFFF). Utilize sempre o cinza escuro Obsidian (#0D0F12) como fundo e o cinza claro suave (#E2E8F0) para o texto padrão.

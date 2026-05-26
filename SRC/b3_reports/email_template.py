import datetime


def generate_email_html(
    ticker: str,
    stock_name: str,
    sector: str,
    current_price: float,
    graham_price: float,
    metrics: dict,
    cids: dict,
) -> str:
    """
    Gera um relatório HTML premium responsivo com tema Obsidian Dark.
    Utiliza tabelas aninhadas para garantir máxima compatibilidade com clientes de e-mail (Gmail, Outlook, etc.).
    """
    # Cálculos de Valuation
    safety_margin = 0.0
    if graham_price > 0:
        safety_margin = ((graham_price - current_price) / graham_price) * 100

    margin_color = (
        "#00E676"
        if safety_margin >= 20
        else ("#FFB74D" if safety_margin > 0 else "#FF3D71")
    )
    margin_text = f"{safety_margin:.1f}%" if graham_price > 0 else "N/A"

    # Formatação de múltiplos
    pl = metrics.get("pl", 0.0)
    pvp = metrics.get("pvp", 0.0)
    dy = metrics.get("div_yield", 0.0)
    roe = metrics.get("roe", 0.0)
    roic = metrics.get("roic", 0.0)

    pl_color = "#00E676" if 0 < pl < 15 else "#FF3D71"
    pvp_color = "#00E676" if 0 < pvp < 1.5 else "#FF3D71"
    dy_color = "#00E676" if dy >= 6 else "#FFB74D"

    date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Financeiro B3 Premium - {ticker}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #0D0F12;
            color: #E2E8F0;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }}
    </style>
</head>
<body style="background-color: #0D0F12; color: #E2E8F0; font-family: 'Outfit', sans-serif; margin: 0; padding: 0;">

    <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #0D0F12; padding: 20px 0;">
        <tr>
            <td align="center">

                <!-- Main Container (680px width for premium display) -->
                <table width="680" border="0" cellpadding="0" cellspacing="0" style="background-color: #161A1F; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">

                    <!-- Header with Gradient Line -->
                    <tr>
                        <td height="4" style="background: linear-gradient(90deg, #00E676 0%, #00B0FF 100%);"></td>
                    </tr>

                    <!-- Header Content -->
                    <tr>
                        <td style="padding: 40px 40px 20px 40px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td>
                                        <span style="font-size: 11px; font-weight: 700; color: #00E676; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 6px;">B3 Relatório Anual Premium</span>
                                        <h1 style="font-size: 28px; font-weight: 700; color: #F8FAFC; margin: 0; padding: 0; letter-spacing: -0.5px;">Análise Fundamentalista</h1>
                                        <p style="font-size: 14px; color: #94A3B8; margin: 8px 0 0 0;">Análise detalhada de valuation para o ativo <strong>{ticker}</strong> ({stock_name})</p>
                                    </td>
                                    <td align="right" valign="top" style="font-size: 12px; color: #64748B; font-weight: 400;">
                                        Gerado em<br><span style="color: #94A3B8; font-weight: 600;">{date_str}</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Separator -->
                    <tr>
                        <td style="padding: 0 40px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="border-top: 1px solid rgba(255, 255, 255, 0.06);"></table>
                        </td>
                    </tr>

                    <!-- Key Ticker Information Grid -->
                    <tr>
                        <td style="padding: 30px 40px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                <tr>
                                    <!-- Card Setor -->
                                    <td width="30%" style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 16px; text-align: center;">
                                        <span style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px;">Setor de Atuação</span>
                                        <span style="font-size: 14px; font-weight: 600; color: #F8FAFC; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{sector}</span>
                                    </td>
                                    <td width="5%">&nbsp;</td>
                                    <!-- Card Cotacao -->
                                    <td width="30%" style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 16px; text-align: center;">
                                        <span style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px;">Cotação Atual</span>
                                        <span style="font-size: 18px; font-weight: 700; color: #F8FAFC; display: block;">R$ {current_price:.2f}</span>
                                    </td>
                                    <td width="5%">&nbsp;</td>
                                    <!-- Card Margem Seguranca -->
                                    <td width="30%" style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 16px; text-align: center;">
                                        <span style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 4px;">Margem de Segurança</span>
                                        <span style="font-size: 18px; font-weight: 700; color: {margin_color}; display: block;">{margin_text}</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Valuation Table & Multiple Stats -->
                    <tr>
                        <td style="padding: 0 40px 30px 40px;">
                            <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; padding: 20px;">
                                <tr>
                                    <td>
                                        <h3 style="font-size: 15px; font-weight: 600; color: #F8FAFC; margin: 0 0 15px 0; padding: 0;">Múltiplos Fundamentalistas Chave</h3>
                                        <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td width="20%" style="padding-bottom: 10px;">
                                                    <span style="font-size: 12px; color: #64748B; display: block;">Preço / Lucro (P/L)</span>
                                                    <span style="font-size: 15px; font-weight: 600; color: {pl_color};">{pl:.2f}</span>
                                                </td>
                                                <td width="20%" style="padding-bottom: 10px;">
                                                    <span style="font-size: 12px; color: #64748B; display: block;">Preço / VP (P/VP)</span>
                                                    <span style="font-size: 15px; font-weight: 600; color: {pvp_color};">{pvp:.2f}</span>
                                                </td>
                                                <td width="20%" style="padding-bottom: 10px;">
                                                    <span style="font-size: 12px; color: #64748B; display: block;">Div. Yield (DY)</span>
                                                    <span style="font-size: 15px; font-weight: 600; color: {dy_color};">{dy:.2f}%</span>
                                                </td>
                                                <td width="20%" style="padding-bottom: 10px;">
                                                    <span style="font-size: 12px; color: #64748B; display: block;">ROE</span>
                                                    <span style="font-size: 15px; font-weight: 600; color: #F8FAFC;">{roe:.2f}%</span>
                                                </td>
                                                <td width="20%" style="padding-bottom: 10px;">
                                                    <span style="font-size: 12px; color: #64748B; display: block;">ROIC</span>
                                                    <span style="font-size: 15px; font-weight: 600; color: #00E676;">{roic:.2f}%</span>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Chart 1: Price History -->
                    <tr>
                        <td style="padding: 0 40px 30px 40px; text-align: center;">
                            <h3 style="font-size: 16px; font-weight: 600; color: #F8FAFC; margin: 0 0 12px 0; text-align: left;">Histórico de Preços Recentes</h3>
                            <div style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; overflow: hidden; padding: 10px;">
                                <img src="cid:{cids["history"]}" alt="Histórico de Cotações" width="100%" style="max-width: 600px; height: auto; display: block; margin: 0 auto; border-radius: 8px;" />
                            </div>
                        </td>
                    </tr>

                    <!-- Chart 2: Graham Valuation -->
                    <tr>
                        <td style="padding: 0 40px 30px 40px; text-align: center;">
                            <h3 style="font-size: 16px; font-weight: 600; color: #F8FAFC; margin: 0 0 12px 0; text-align: left;">Avaliação de Valor Justo (Fórmula Graham)</h3>
                            <div style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; overflow: hidden; padding: 10px;">
                                <img src="cid:{cids["graham"]}" alt="Graham Valuation" width="100%" style="max-width: 600px; height: auto; display: block; margin: 0 auto; border-radius: 8px;" />
                            </div>
                        </td>
                    </tr>

                    <!-- Chart 3: Correlation Matrix -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px; text-align: center;">
                            <h3 style="font-size: 16px; font-weight: 600; color: #F8FAFC; margin: 0 0 12px 0; text-align: left;">Correlação Multidimensional do Setor</h3>
                            <div style="background-color: #0D0F12; border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 12px; overflow: hidden; padding: 10px;">
                                <img src="cid:{cids["heatmap"]}" alt="Correlação Setorial" width="100%" style="max-width: 600px; height: auto; display: block; margin: 0 auto; border-radius: 8px;" />
                            </div>
                            <p style="font-size: 12px; color: #64748B; text-align: left; margin: 10px 0 0 0; line-height: 1.5;">
                                * A matriz térmica acima exibe a correlação estatística entre os principais múltiplos do setor. Coeficientes próximos a +1.00 ou -1.00 indicam forte correlação linear direta ou inversa.
                            </p>
                        </td>
                    </tr>

                    <!-- Footer Section with Legal Disclaimer -->
                    <tr>
                        <td style="background-color: #0D0F12; padding: 40px; border-top: 1px solid rgba(255, 255, 255, 0.06); text-align: center;">
                            <span style="font-size: 14px; font-weight: 600; color: #E2E8F0; display: block; margin-bottom: 8px;">PUB Dados Financeiros B3</span>
                            <span style="font-size: 11px; color: #475569; display: block; line-height: 1.6; max-width: 500px; margin: 0 auto;">
                                AVISO LEGAL: As informações contidas neste relatório são estritamente de caráter informativo e educativo. A formulação de valuation de Benjamin Graham e demais múltiplos fundamentalistas não constituem ofertas, recomendações, relatórios de análise de investimentos ou conselhos de compra ou venda de quaisquer ativos financeiros.
                            </span>
                            <span style="font-size: 10px; color: #475569; display: block; margin-top: 20px;">
                                © 2026 PUB_Dados_Financeiros_B3. Desenvolvido sob arquitetura Open-Source.
                            </span>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""
    return html

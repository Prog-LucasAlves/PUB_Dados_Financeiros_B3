import os
import pathlib
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd

from b3_reports.charts import (
    plot_correlation_heatmap,
    plot_graham_bar,
    plot_stock_history,
)
from b3_reports.email_template import generate_email_html

# Diretorios locais
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
OUTPUT_DIR = BASE_DIR.parent / "Api" / "relatorios"


def build_and_dispatch_report(
    ticker: str,
    stock_name: str,
    sector: str,
    current_price: float,
    graham_price: float,
    metrics: dict,
    dates: list,
    prices: list,
    correlations_df: pd.DataFrame,
    force_local_save: bool = True,
) -> dict:
    """
    Controlador principal que:
    1. Gera as imagens do Matplotlib temporariamente.
    2. Compila o HTML utilizando o template premium.
    3. Envia por e-mail se SMTP estiver configurado.
    4. Salva uma versão HTML + PNG local para conferência offline (Api/relatorios/).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    images_dir = OUTPUT_DIR / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Nomes dos arquivos de imagem locais
    history_img_path = images_dir / f"history_{ticker.lower()}.png"
    graham_img_path = images_dir / f"graham_{ticker.lower()}.png"
    heatmap_img_path = images_dir / "correlation_heatmap.png"

    # 1. Gera os gráficos via Matplotlib
    plot_stock_history(ticker, dates, prices, history_img_path)
    plot_graham_bar(ticker, current_price, graham_price, graham_img_path)
    plot_correlation_heatmap(correlations_df, heatmap_img_path)

    # Definição dos Content-IDs para o e-mail
    cids = {
        "history": f"history_{ticker.lower()}",
        "graham": f"graham_{ticker.lower()}",
        "heatmap": "correlation_heatmap",
    }

    # 2. Compila o HTML para e-mail (com links cid:...)
    email_html = generate_email_html(
        ticker=ticker,
        stock_name=stock_name,
        sector=sector,
        current_price=current_price,
        graham_price=graham_price,
        metrics=metrics,
        cids=cids,
    )

    # Salva uma cópia local interativa onde as imagens apontam para arquivos locais relativos
    local_cids = {
        "history": f"images/history_{ticker.lower()}.png",
        "graham": f"images/graham_{ticker.lower()}.png",
        "heatmap": "images/correlation_heatmap.png",
    }
    local_html = generate_email_html(
        ticker=ticker,
        stock_name=stock_name,
        sector=sector,
        current_price=current_price,
        graham_price=graham_price,
        metrics=metrics,
        cids=local_cids,
    )

    # Substitui a tag "cid:" no local_html pelo caminho relativo real
    local_html = local_html.replace('src="cid:images/', 'src="images/')

    local_report_path = OUTPUT_DIR / f"relatorio_{ticker.lower()}.html"
    with open(local_report_path, "w", encoding="utf-8") as f:
        f.write(local_html)

    print(f"[OK] Cópia local do relatório compilada e salva em: {local_report_path}")

    # 3. Envia o e-mail se as credenciais SMTP estiverem presentes
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_recipients = os.getenv("SMTP_RECIPIENTS")

    status = {
        "email_sent": False,
        "local_saved": True,
        "local_path": str(local_report_path),
        "error": None,
    }

    if not all([smtp_server, smtp_port, smtp_user, smtp_password, smtp_recipients]):
        print(
            "[AVISO] Configurações de SMTP ausentes (.env). O relatório não será enviado por e-mail."
        )
        return status

    try:
        port = int(smtp_port)
        recipients_list = [r.strip() for r in smtp_recipients.split(",")]

        # Cria mensagem MIME multipart relacionada
        msg_root = MIMEMultipart("related")
        msg_root["Subject"] = f"📊 B3 Premium Financial Report - {ticker}"
        msg_root["From"] = smtp_user
        msg_root["To"] = ", ".join(recipients_list)

        # Parte alternativa para corpo de texto alternativo/HTML
        msg_alt = MIMEMultipart("alternative")
        msg_root.attach(msg_alt)

        # Corpo em texto puro alternativo
        text_body = f"Relatório Financeiro Premium B3 - {ticker}\nAcesse a versão em HTML para visualizar os gráficos de cotações, Graham Valuation e correlações."
        msg_alt.attach(MIMEText(text_body, "plain", "utf-8"))

        # Adiciona o HTML compilado com as tags cid
        msg_alt.attach(MIMEText(email_html, "html", "utf-8"))

        # Função auxiliar para anexar imagens MIME
        def attach_mime_image(path: pathlib.Path, cid: str):
            with open(path, "rb") as img_file:
                mime_img = MIMEImage(img_file.read())
                mime_img.add_header("Content-ID", f"<{cid}>")
                mime_img.add_header("Content-Disposition", "inline", filename=path.name)
                msg_root.attach(mime_img)

        # Anexa os 3 gráficos gerados pelo Matplotlib
        attach_mime_image(history_img_path, cids["history"])
        attach_mime_image(graham_img_path, cids["graham"])
        attach_mime_image(heatmap_img_path, cids["heatmap"])

        # Conecta e envia usando TLS seguro
        print(f"Conectando ao servidor SMTP {smtp_server}:{port}...")

        # Conexão SSL direta na porta 465 ou STARTTLS na porta 587
        if port == 465:
            server = smtplib.SMTP_SSL(smtp_server, port, timeout=15)
        else:
            server = smtplib.SMTP(smtp_server, port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()

        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipients_list, msg_root.as_string())
        server.quit()

        print(
            f"[OK] Relatório fundamentalista enviado com sucesso por e-mail para: {smtp_recipients}"
        )
        status["email_sent"] = True

    except Exception as e:
        print(f"[ERRO] Falha ao enviar o e-mail: {str(e)}")
        status["error"] = str(e)

    return status

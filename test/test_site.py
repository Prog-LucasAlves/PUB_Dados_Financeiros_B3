import requests

# URL utlilizada
url = "https://fundamentus.com.br/detalhes.php?papel=ITSA4"


# Função para testar o site
def test_api():
    header = {"user-agent": "Mozilla/5.0"}
    url = "http://economia.awesomeapi.com.br/json/last/USD-BRL"

    response = requests.get(url, headers=header)

    assert response.status_code == 200

"""
Código utilizado para verificar se o lacal aonde será coletado os dados já esta atualizado
"""

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Importando o código para verificar se o site está atualizado
import __check_semana__

# Inicializando o navegador
options = FirefoxOptions()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.add_argument("--headless")
check = webdriver.Firefox(options=options)

check.implicitly_wait(20)

# Coletando a data de atualização do site
url = "https://www.fundamentus.com.br/detalhes.php?papel=AALR3+"
check.get(url)

data_check = check.find_element(
    "xpath", "/html/body/div[1]/div[2]/table[1]/tbody/tr[2]/td[4]/span"
).text
check.quit()

# Verificando se a data de atualização do site é igual a data de hoje
data_check_dt = datetime.strptime(data_check, "%d/%m/%Y").date()
data_check_dt_t = data_check_dt.strftime("%d/%m/%Y")
data_check_sem = data_check_dt.weekday()
day = __check_semana__.DIAS[data_check_sem]

#####

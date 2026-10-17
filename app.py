"""Interface local para consulta de informações de sites via serviço de terceiros."""

import logging
import os

from flask import Flask, render_template, request

from url_validation import normalize_public_url

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
logger = logging.getLogger(__name__)


def consultar_site(url: str) -> str:
    """Consulta um serviço externo; não realiza verificação independente de segurança."""
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    options = webdriver.ChromeOptions()
    if os.getenv("VERIFICARSITE_HEADLESS", "0") == "1":
        options.add_argument("--headless=new")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)
        driver.get("https://www.siteconfiavel.com.br/")
        wait = WebDriverWait(driver, 25)
        search = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Cole o Link/URL do site"]'))
        )
        search.send_keys(url)
        search.send_keys(Keys.RETURN)
        result = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "app-trust-checker-result-screen"))
        )
        wait.until(lambda _: bool(result.text.strip()))
        return result.text.strip()
    except TimeoutException:
        logger.warning("Consulta não concluída no tempo limite.")
        raise RuntimeError("A consulta demorou demais. Tente novamente mais tarde.") from None
    except WebDriverException:
        logger.exception("Falha na automação do navegador.")
        raise RuntimeError("Não foi possível usar o Chrome nesta consulta.") from None
    finally:
        if driver is not None:
            driver.quit()


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        try:
            normalized_url = normalize_public_url(url)
        except ValueError as exc:
            erro = str(exc)
        else:
            try:
                resultado = consultar_site(normalized_url)
            except RuntimeError as exc:
                erro = str(exc)
            except Exception:
                logger.exception("Falha inesperada na consulta.")
                erro = "Não foi possível consultar o serviço no momento."

    return render_template("index.html", resultado=resultado, erro=erro, url=url)


if __name__ == "__main__":
    app.run(
        host=os.getenv("VERIFICARSITE_HOST", "127.0.0.1"),
        port=int(os.getenv("VERIFICARSITE_PORT", "5000")),
        debug=False,
    )

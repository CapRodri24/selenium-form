import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=es-ES")
    # options.add_argument("--headless")  # descomenta para correr sin ventana

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
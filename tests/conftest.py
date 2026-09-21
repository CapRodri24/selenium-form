"""
Configuración compartida de pytest:
- Fixture del driver (Chrome)
- Hook que captura pantalla automáticamente cuando un test falla
- Hook que guarda un log de texto con el resultado de cada test
"""
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Carpeta donde se guardan las evidencias
EVIDENCIAS_DIR = "evidencias"


def _asegurar_carpeta():
    """Crea la carpeta de evidencias si no existe."""
    os.makedirs(EVIDENCIAS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# Fixture del driver
# ═══════════════════════════════════════════════════════════
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=es-ES")
    # options.add_argument("--headless")  # descomenta para correr sin ventana

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


# ═══════════════════════════════════════════════════════════
# Hook: captura pantalla cuando un test falla
# ═══════════════════════════════════════════════════════════
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Se ejecuta después de cada fase de un test (setup, call, teardown).
    Si la fase 'call' falla, guarda una captura de pantalla en evidencias/.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            _asegurar_carpeta()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre = f"{EVIDENCIAS_DIR}/FAIL_{item.name}_{ts}.png"
            try:
                driver.save_screenshot(nombre)
                print(f"\n[evidencia] Captura guardada en: {nombre}")
            except Exception as e:
                print(f"\n[evidencia] No se pudo guardar captura: {e}")


# ═══════════════════════════════════════════════════════════
# Hook: crea la carpeta de evidencias al inicio de la sesión
# ═══════════════════════════════════════════════════════════
def pytest_sessionstart(session):
    _asegurar_carpeta()
"""
25 casos de prueba de caja negra para el formulario de Agenda de Citas.
Basados en specs/spec.md
"""
from datetime import date, timedelta
import pytest
from pages.formulario_page import FormularioPage


HOY = date.today()
FECHA_VALIDA = (HOY + timedelta(days=1)).strftime("%Y-%m-%d")
HORA_VALIDA = "10:00"

NOMBRE_VALIDO   = "Joel Sergio"
APELLIDO_VALIDO = "Teran Lima"
CARNET_VALIDO   = "8004815LP"
CELULAR_VALIDO  = "72253265"


def _preparar(driver, nombre=NOMBRE_VALIDO, apellido=APELLIDO_VALIDO,
              carnet=CARNET_VALIDO, celular=CELULAR_VALIDO,
              fecha=FECHA_VALIDA, hora=HORA_VALIDA):
    pagina = FormularioPage(driver).abrir()
    pagina.abrir_dialogo()
    pagina.rellenar_formulario(nombre, apellido, carnet, celular, fecha, hora)
    pagina.enviar()
    return pagina


# ═══ CASO 1 — Todos válidos ═══
def test_caso_01_todos_validos(driver):
    pagina = _preparar(driver)
    assert pagina.hay_exito(), "Se esperaba toast de 'Cita agendada correctamente'"


# ═══ CASOS 2-6 — Nombre inválido ═══
@pytest.mark.parametrize("nombre,descripcion", [
    ("@ndr!an", "caracteres especiales"),
    ("Jorge26", "contiene números"),
    ("L", "menor a 2 caracteres"),
    ("adrian valdelomar irusata ruiz", "mayor a 25 caracteres"),
    ("", "vacío"),
])
def test_caso_02_al_06_nombre_invalido(driver, nombre, descripcion):
    pagina = _preparar(driver, nombre=nombre)
    assert pagina.hay_error(), f"Se esperaba error de nombre ({descripcion})"


# ═══ CASOS 7-11 — Apellido inválido ═══
@pytest.mark.parametrize("apellido,descripcion", [
    ("L!m@", "caracteres especiales"),
    ("Saravia17", "contiene números"),
    ("T", "menor a 2 caracteres"),
    ("antofagasta tierrahermosa", "mayor a 20 caracteres"),
    ("", "vacío"),
])
def test_caso_07_al_11_apellido_invalido(driver, apellido, descripcion):
    pagina = _preparar(driver, apellido=apellido)
    assert pagina.hay_error(), f"Se esperaba error de apellido ({descripcion})"


# ═══ CASOS 12-16 — Carnet inválido ═══
@pytest.mark.parametrize("carnet,descripcion", [
    ("202", "menor a 5 caracteres"),
    ("1234567890cbba", "mayor a 12 caracteres"),
    ("1234SC", "menos de 5 números"),
    ("12345abcde", "más de 4 letras"),
    ("", "vacío"),
])
def test_caso_12_al_16_carnet_invalido(driver, carnet, descripcion):
    pagina = _preparar(driver, carnet=carnet)
    assert pagina.hay_error(), f"Se esperaba error de carnet ({descripcion})"


# ═══ CASOS 17-19 — Celular inválido ═══
@pytest.mark.parametrize("celular,descripcion", [
    ("1234567", "menos de 8 dígitos"),
    ("123456789", "más de 8 dígitos"),
    ("", "vacío"),
])
def test_caso_17_al_19_celular_invalido(driver, celular, descripcion):
    pagina = _preparar(driver, celular=celular)
    assert pagina.hay_error(), f"Se esperaba error de celular ({descripcion})"


# ═══ CASOS 20-21 — Fecha inválida ═══
@pytest.mark.parametrize("fecha,descripcion", [
    ((HOY - timedelta(days=30)).strftime("%Y-%m-%d"), "anterior a hoy"),
    ((HOY + timedelta(days=30)).strftime("%Y-%m-%d"), "más de 2 semanas"),
])
def test_caso_20_al_21_fecha_invalida(driver, fecha, descripcion):
    pagina = _preparar(driver, fecha=fecha)
    assert pagina.hay_error(), f"Se esperaba error de fecha ({descripcion})"


# ═══ CASO 22 — Fecha vacía ═══
def test_caso_22_fecha_vacia(driver):
    pagina = FormularioPage(driver).abrir()
    pagina.abrir_dialogo()
    pagina.rellenar_nombre(NOMBRE_VALIDO)
    pagina.rellenar_apellido(APELLIDO_VALIDO)
    pagina.rellenar_carnet(CARNET_VALIDO)
    pagina.rellenar_celular(CELULAR_VALIDO)
    pagina.rellenar_hora(HORA_VALIDA)
    # NO se selecciona fecha
    pagina.enviar()
    assert pagina.hay_error(), "Se esperaba error de fecha vacía"


# ═══ CASOS 23-24 — Hora fuera de rango ═══
@pytest.mark.parametrize("hora,descripcion", [
    ("07:00", "antes de las 8 am"),
    ("19:00", "después de las 6 pm"),
])
def test_caso_23_al_24_hora_invalida(driver, hora, descripcion):
    pagina = _preparar(driver, hora=hora)
    assert pagina.hay_error(), f"Se esperaba error de hora ({descripcion})"


# ═══ CASO 25 — Hora vacía ═══
def test_caso_25_hora_vacia(driver):
    pagina = FormularioPage(driver).abrir()
    pagina.abrir_dialogo()
    pagina.rellenar_nombre(NOMBRE_VALIDO)
    pagina.rellenar_apellido(APELLIDO_VALIDO)
    pagina.rellenar_carnet(CARNET_VALIDO)
    pagina.rellenar_celular(CELULAR_VALIDO)
    pagina.rellenar_fecha(FECHA_VALIDA)
    # NO se selecciona hora
    pagina.enviar()
    assert pagina.hay_error(), "Se esperaba error de hora vacía"
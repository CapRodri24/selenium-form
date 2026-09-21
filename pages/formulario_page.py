from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormularioPage:
    URL = "https://formularioselenium.netlify.app/"

    # ─── Botón para abrir el modal (único en el header, no depende del texto) ───
    BOTON_ABRIR_DIALOG = (
        By.XPATH,
        "//header//button[@aria-haspopup='dialog']"
    )

    # ─── Campos del formulario (dentro del modal) ───
    CAMPO_NOMBRE   = (By.ID, "nombres")
    CAMPO_APELLIDO = (By.ID, "apellidos")
    CAMPO_CARNET   = (By.ID, "carnet")
    CAMPO_CELULAR  = (By.ID, "celular")
    CAMPO_FECHA    = (By.CSS_SELECTOR, "input[type='date']")
    CAMPO_HORA     = (By.ID, "hora")

    BOTON_ENVIAR = (
        By.XPATH,
        "//button[@type='submit' and contains(., 'Guardar cita')]"
    )

    # ─── AlertDialog de errores (Radix usa role="alertdialog") ───
    ALERT_ERROR_TITULO = (
        By.XPATH,
        "//*[@role='alertdialog']//*[contains(text(), 'Errores en el formulario')]"
    )
    ALERT_ERROR_ITEMS = (By.CSS_SELECTOR, "[role='alertdialog'] ul li")
    ALERT_ERROR_BOTON = (
        By.XPATH,
        "//*[@role='alertdialog']//button[contains(., 'Entendido')]"
    )

    # ─── Toast de éxito (sonner) ───
    TOAST_EXITO = (By.CSS_SELECTOR, "li[data-sonner-toast]")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ─── Navegación ───
    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(EC.element_to_be_clickable(self.BOTON_ABRIR_DIALOG))
        return self

    def abrir_dialogo(self):
        """Abre el modal de agendar cita."""
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTON_ABRIR_DIALOG))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", boton
        )
        boton.click()
        # Esperar a que aparezca el input de nombre dentro del modal
        self.wait.until(EC.visibility_of_element_located(self.CAMPO_NOMBRE))

    # ─── Rellenar inputs ───
    def _escribir(self, localizador, valor):
        campo = self.wait.until(EC.element_to_be_clickable(localizador))
        campo.clear()
        if valor:
            campo.send_keys(valor)

    def rellenar_nombre(self, valor):   self._escribir(self.CAMPO_NOMBRE, valor)
    def rellenar_apellido(self, valor): self._escribir(self.CAMPO_APELLIDO, valor)
    def rellenar_carnet(self, valor):   self._escribir(self.CAMPO_CARNET, valor)
    def rellenar_celular(self, valor):  self._escribir(self.CAMPO_CELULAR, valor)

    def rellenar_fecha(self, fecha_iso):
        """
        fecha_iso en formato 'yyyy-MM-dd'.
        Se usa el setter nativo de HTMLInputElement para que React detecte el cambio.
        """
        campo = self.wait.until(EC.presence_of_element_located(self.CAMPO_FECHA))
        self.driver.execute_script(
            "const el = arguments[0];"
            "const setter = Object.getOwnPropertyDescriptor("
            "  window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(el, arguments[1]);"
            "el.dispatchEvent(new Event('input', { bubbles: true }));"
            "el.dispatchEvent(new Event('change', { bubbles: true }));",
            campo, fecha_iso
        )

    def rellenar_hora(self, hora_hhmm):
        """
        hora_hhmm en formato 'HH:MM'.
        Igual que la fecha: setter nativo + dispatch de eventos.
        """
        campo = self.wait.until(EC.presence_of_element_located(self.CAMPO_HORA))
        self.driver.execute_script(
            "const el = arguments[0];"
            "const setter = Object.getOwnPropertyDescriptor("
            "  window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(el, arguments[1]);"
            "el.dispatchEvent(new Event('input', { bubbles: true }));"
            "el.dispatchEvent(new Event('change', { bubbles: true }));",
            campo, hora_hhmm
        )

    def rellenar_formulario(self, nombre, apellido, carnet, celular, fecha, hora):
        self.rellenar_nombre(nombre)
        self.rellenar_apellido(apellido)
        self.rellenar_carnet(carnet)
        self.rellenar_celular(celular)
        if fecha:
            self.rellenar_fecha(fecha)
        if hora:
            self.rellenar_hora(hora)

    def enviar(self):
        boton = self.wait.until(EC.element_to_be_clickable(self.BOTON_ENVIAR))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", boton
        )
        boton.click()

    # ─── Verificaciones ───
    def obtener_errores(self):
        """Devuelve la lista de mensajes del AlertDialog de errores."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ALERT_ERROR_TITULO))
        except Exception:
            return []
        items = self.driver.find_elements(*self.ALERT_ERROR_ITEMS)
        return [i.text.strip() for i in items if i.text.strip()]

    def hay_error(self):
        return len(self.obtener_errores()) > 0

    def cerrar_dialogo_error(self):
        try:
            boton = self.wait.until(EC.element_to_be_clickable(self.ALERT_ERROR_BOTON))
            boton.click()
        except Exception:
            pass

    def obtener_toast_exito(self):
        try:
            toast = self.wait.until(EC.visibility_of_element_located(self.TOAST_EXITO))
            return toast.text.strip()
        except Exception:
            return ""

    def hay_exito(self):
        return "agendada" in self.obtener_toast_exito().lower()
# Especificación: Pruebas E2E para Formulario Clínica Dental UMSS

## 1. Visión General
Automatizar la validación del formulario de agenda de citas en
https://formularioselenium.netlify.app/ mediante pruebas de caja negra
basadas en clases de equivalencia. 25 casos de prueba sobre 6 campos.

## 2. Stack Tecnológico
- Python 3.10+
- Selenium 4.x (con Selenium Manager, sin chromedriver manual)
- Pytest + pytest-html
- Chrome (navegador objetivo)
- Patrón: Page Object Model (POM)

## 3. Modelo del Formulario (SUT) — Localizadores reales

| Campo    | Localizador                                       | Tipo             |
|----------|---------------------------------------------------|------------------|
| Abrir    | `//header//button[@aria-haspopup='dialog']`       | botón Radix      |
| Nombre   | `By.ID = "nombres"`                               | input text       |
| Apellido | `By.ID = "apellidos"`                             | input text       |
| Carnet   | `By.ID = "carnet"`                                | input text       |
| Celular  | `By.ID = "celular"`                               | input number     |
| Fecha    | `input[type='date']`                              | input nativo     |
| Hora     | `By.ID = "hora"` (input[type='time'])             | input nativo     |
| Submit   | `//button[@type='submit' and contains(., 'Guardar cita')]` | botón    |
| Éxito    | `li[data-sonner-toast]` con "agendada"            | toast sonner     |
| Error    | `[role='alertdialog'] ul li`                      | AlertDialog      |

## 4. Clases de Equivalencia (30 clases → 25 casos)

### Nombre (1-6)
1. Válida: 2-25 letras | 2. Especiales | 3. Números | 4. <2 | 5. >25 | 6. Vacío

### Apellido (7-12)
7. Válida: 2-20 letras | 8. Especiales | 9. Números | 10. <2 | 11. >20 | 12. Vacío

### Carnet (13-18)
13. Válida: 5-12 chars, ≥5 números, ≤4 letras | 14. <5 | 15. >12 |
16. <5 números | 17. >4 letras | 18. Vacío

### Celular (19-22)
19. Válida: 8 dígitos | 20. <8 | 21. >8 | 22. Vacío

### Fecha (23-26)
23. Válida: hoy a hoy+14d | 24. Anterior | 25. >14d | 26. Vacío

### Hora (27-30)
27. Válida: 08:00-18:00 | 28. <08:00 | 29. >18:00 | 30. Vacío

## 5. Reglas de validación (extraídas del código fuente)

- Zod schema en `appointment-form.tsx`
- Modo `onSubmit`: los errores **solo aparecen tras enviar** el formulario
- Fecha: `<input type="date">` directo (antes era Popover + react-day-picker)
- Hora: `<input type="time">` directo (antes era Select de shadcn)
- Errores: **AlertDialog** (role="alertdialog") con título
  "Errores en el formulario" y lista `<ul><li>` con los mensajes
- Éxito: toast de sonner "Cita agendada correctamente"
- El formulario vive dentro de un **Dialog** (role="dialog") que se abre
  con el botón `[aria-haspopup='dialog']` del header

## 6. Restricciones
- NO `time.sleep()` → usar `WebDriverWait`
- NO mezclar aserciones dentro del Page Object
- Los tests deben enviar el formulario para disparar la validación (modo onSubmit)
- Fechas calculadas dinámicamente con `date.today()`
- Para asignar valor a `input[type=date]` y `input[type=time]` usar el setter
  nativo de `HTMLInputElement.prototype.value` + dispatch de eventos
  `input` y `change` (React Hook Form no detecta la asignación directa)

## 7. Estructura del proyecto

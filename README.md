# MaxGest - Sistema de Gestión para Emprendedores

Este proyecto ha sido desarrollado como trabajo final para la carrera de **Diseño y Desarrollo de Software**.

* **Institución / Carrera:** Diseño y Desarrollo de Software
* **Sección:** C24S-A
* **Ciclo:** I Ciclo

---

## 📝Descripción del Proyecto

**MaxGest** es una aplicación de escritorio desarrollada en Python, diseñada específicamente para ayudar a pequeños emprendedores a administrar sus negocios de forma óptima. 

Muchos negocios locales pierden dinero al no saber con precisión qué mercancía tienen disponible, lo que genera compras duplicadas o quiebres de inventario. Con el fin de mitigar esta problemática y reducir la tasa de fracaso en nuevos emprendimientos, se creó este modelo de gestión de negocio que unifica el control de inventario, ventas y análisis gráfico en una sola herramienta.

---

## Funcionalidades Principales

Como asistente de gestión básico, **MaxGest** es capaz de cumplir con las siguientes funciones:

* **Gestión de Inventario (CRUD):** Almacenar, editar, buscar y eliminar productos cuando el usuario lo desee.
* **Control de Stock:** Contabilización de la cantidad de productos registrados, ítems totales y alertas visuales de productos con bajo stock.
* **Simulación de Ventas:** Registro de ventas afectando las cantidades disponibles en tiempo real, incluyendo el registro del tiempo exacto de cada transacción.
* **Historial y Reportes:** Visualización del historial de transacciones, registro del total de ventas diarias y acumulado mensual hasta el momento.
* **Análisis Gráfico:** Resumen visual y estadístico mediante gráficas de las ventas por hora (en el rango de un día) y ventas por día (en el rango de un mes).
* **Predicciones:** Realización de predicciones básicas según el comportamiento histórico de las ventas.

---

## 🛠️ Tecnologías y Herramientas Usadas

El sistema está construido íntegramente sobre el ecosistema de Python, utilizando una base de datos local y librerías avanzadas para la interfaz gráfica y análisis de datos:

* **Lenguaje principal:** Python
* **Base de Datos:** SQLite (`sqlite3`)
* **Interfaz Gráfica (GUI):** `customtkinter` (para un diseño moderno), `tkinter` y `PIL` (Pillow) para el manejo de imágenes.
* **Visualización de Datos:** `matplotlib` (para la generación de gráficos estadísticos).
* **Módulos del Sistema:** `datetime`, `sys` y `pathlib`.

---

## 📁 Estructura del Proyecto

El código fuente está organizado de la siguiente manera para separar el punto de entrada de la lógica de procesamiento y los recursos visuales:

```text
MaxGest/
├── Inicio/
│   └── comenzar.py               # Punto de entrada / Script principal de ejecución
│
└── Procesamiento/
    ├── bienvenida.py             # Pantalla de presentación de la app
    ├── principal.py              # Panel o Dashboard principal
    ├── Matamoros.py              # Módulos de lógica desarrollados por el equipo
    ├── miguel.py
    ├── Milder.py
    ├── Minchola.py
    └── assets/                   # Recursos visuales de la aplicación
        ├── fondo_inicio.png
        └── logo C.png
```

---

##  Instrucciones de Instalación y Ejecución

### Prerrequisitos
Asegúrate de tener instalado Python en tu sistema (versión 3.8 o superior recomendada).

### Paso 1: Clonar o descargar el proyecto
Descarga el proyecto en tu máquina local y abre una terminal en la carpeta raíz `MaxGest`.

### Paso 2: Instalar las dependencias necesarios
Para ejecutar el proyecto, se deben instalar las librerías externas que no vienen por defecto en Python. Ejecuta el siguiente comando en tu terminal:

```bash
pip install customtkinter matplotlib Pillow
```
*(Nota: `sqlite3`, `tkinter`, `datetime`, `sys` y `pathlib` ya vienen integrados en la instalación estándar de Python).*

### Paso 3: Ejecución de la aplicación
Para iniciar el programa, sitúate en la carpeta raíz del proyecto y ejecuta el archivo de inicio:

```bash
python Inicio/comenzar.py
```

---

##  Autores

El presente proyecto fue desarrollado por el equipo integrado por:

  ##Ayrton Adrián Matamoros Arteaga *
  *Milder Gustavo Quispe Ticona *
  *Miguel Rivera Cárdenas *
  *Mathías Minchola Alcarraz *
  

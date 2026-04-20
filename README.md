# Extractor de Imágenes de PDF

[cite_start]Herramienta técnica diseñada para la **recuperación de imágenes originales** desde archivos PDF generados a partir de sitios web (impresión a PDF). [cite_start]Está optimizada para filtrar contenido irrelevante como iconos, banners o miniaturas mediante criterios de peso y dimensiones[cite: 8, 16].

## Funcionamiento
[cite_start]El script localiza automáticamente el primer PDF en su directorio y realiza lo siguiente[cite: 9]:
1.  [cite_start]**Organización**: Crea una carpeta con el mismo nombre del archivo PDF[cite: 9].
2.  [cite_start]**Extracción**: Guarda las imágenes originales extraídas directamente en esa carpeta[cite: 10].
3.  [cite_start]**Ubicación**: Todo el proceso se ejecuta de forma local en la ruta del archivo `.py`[cite: 11].

## Vista Previa
![Menú de Selección](img/captura_menu.jpg)
[cite_start]*Interfaz del menú interactivo para seleccionar filtros de extracción.*

![Resultado de Extracción](img/captura_salida.jpg)
[cite_start]*Ejemplo de la estructura de carpetas e imágenes recuperadas.*

## Scripts de Automatización (Windows)
[cite_start]Se incluyen archivos por lotes (.bat) para simplificar el flujo de trabajo en Windows[cite: 12]:
* [cite_start]**extraer 100k.bat**: Ejecución rápida con un filtro predeterminado de **100 KB**[cite: 12, 13].
* [cite_start]**extraer100kmenu.bat**: Interfaz con menú para elegir entre diversos filtros de píxeles (100px a 300px) o peso (60KB a 200KB)[cite: 14].

### Notas sobre la automatización (PowerShell Integration)
[cite_start]El archivo `extraer100kmenu.bat` utiliza **PowerShell** para modificar dinámicamente la variable `FILTRO` dentro de `extract_pdf_images.py`[cite: 15, 16]:
* [cite_start]**Inyección de parámetros**: Usa expresiones regulares (`-replace`) para actualizar el código de Python en tiempo real.
* [cite_start]**Flujo sin intervención**: Permite cambiar la lógica de filtrado desde la consola de Windows sin necesidad de editar manualmente el script.

## Requisitos
* [cite_start]Python 3.x [cite: 15]
* [cite_start]Dependencias: `pip install -r requirements.txt` (incluye PyMuPDF y Pillow) [cite: 15, 17]
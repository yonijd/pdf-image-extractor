import os
import re
import sys
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO

def clean_filename(name):
    """
    Limpia el nombre de archivo eliminando solo caracteres prohibidos por Windows
    Conserva espacios, numeros, letras, guiones y otros caracteres seguros
    """
    # Caracteres prohibidos en Windows: < > : " / \ | ? *
    # Tambien elimina apostrofe y comilla simple por problemas
    name = re.sub(r'[<>:"/\\|?*\']', '', name)
    # Eliminar caracteres de control y no imprimibles
    name = ''.join(char for char in name if ord(char) >= 32)
    # Eliminar espacios al inicio o final
    name = name.strip()
    # Si queda vacio, usar nombre generico
    if not name:
        name = "imagen"
    return name

def extract_images_filter_by_size_or_weight(pdf_path, output_dir, filter_type, filter_value):
    """
    Extrae imagenes filtrando por tamaño (px) o peso (KB)
    filter_type: 'size' o 'weight'
    filter_value: valor del filtro (px o KB)
    """
    doc = fitz.open(pdf_path)
    saved_images = []
    
    # Mostrar tipo de filtro
    if filter_type == 'size':
        print(f"Filtro por dimension: {filter_value}x{filter_value} px minimo")
    elif filter_type == 'weight':
        print(f"Filtro por peso: {filter_value} KB minimo")
    else:
        print(f"Sin filtro: guardando todas las imagenes")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            # Obtener dimensiones
            img_pil = Image.open(BytesIO(image_bytes))
            width, height = img_pil.size
            
            # Calcular peso en KB
            weight_kb = len(image_bytes) / 1024
            
            # Aplicar filtro segun tipo
            keep_image = False
            
            if filter_type == 'size':
                if width >= filter_value and height >= filter_value:
                    keep_image = True
                else:
                    print(f"  [NO] Pag{page_num+1:03d}: Imagen {img_index+1} filtrada ({width}x{height} < {filter_value}px)")
                    
            elif filter_type == 'weight':
                if weight_kb >= filter_value:
                    keep_image = True
                else:
                    print(f"  [NO] Pag{page_num+1:03d}: Imagen {img_index+1} filtrada ({weight_kb:.1f}KB < {filter_value}KB)")
            else:
                # Sin filtro
                keep_image = True
            
            if keep_image:
                # Usar nombre completo limpio (sin truncar)
                base_name = clean_filename(Path(pdf_path).stem)
                
                filename = f"{base_name}_pag{page_num+1:03d}_img{img_index+1:03d}.{ext}"
                filepath = Path(output_dir) / filename
                
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                saved_images.append(filename)
                
                if filter_type == 'size':
                    print(f"  [OK] Pag{page_num+1:03d}: {filename} ({width}x{height})")
                elif filter_type == 'weight':
                    print(f"  [OK] Pag{page_num+1:03d}: {filename} ({weight_kb:.1f}KB)")
                else:
                    print(f"  [OK] Pag{page_num+1:03d}: {filename}")
    
    doc.close()
    return saved_images

def find_first_pdf(work_dir):
    """Encuentra el primer archivo PDF en el directorio"""
    pdf_files = list(Path(work_dir).glob("*.pdf")) + list(Path(work_dir).glob("*.PDF"))
    if not pdf_files:
        return None
    
    # Ordenar por fecha de modificacion
    pdf_files.sort(key=lambda x: x.stat().st_mtime)
    return pdf_files[0]

def main():
    work_dir = Path.cwd()
    
    print("="*50)
    print("    EXTRACTOR DE IMAGENES DE PDF")
    print("="*50)
    print("\nOPCIONES DE FILTRO:")
    print("  1 - Sin filtro (todas las imagenes)")
    print("  2 - Dimension 100x100 px")
    print("  3 - Dimension 150x150 px")
    print("  4 - Dimension 200x200 px")
    print("  5 - Dimension 250x250 px")
    print("  6 - Dimension 300x300 px")
    print("  7 - Peso minimo 60 KB")
    print("  8 - Peso minimo 100 KB")  # <--- PREDETERMINADO
    print("  9 - Peso minimo 150 KB")
    print(" 10 - Peso minimo 200 KB")
    
    # Configurar filtro (cambia este valor segun necesites)
    # VALOR PREDETERMINADO: 8 (100 KB)
    FILTRO = 8                   # <--- CAMBIA AQUI EL NUMERO (1 al 10)
    
    # Mapeo de opciones
    if FILTRO == 1:
        filter_type = 'none'
        filter_value = 0
        descripcion = "Sin filtro"
    elif FILTRO == 2:
        filter_type = 'size'
        filter_value = 100
        descripcion = "100x100 px"
    elif FILTRO == 3:
        filter_type = 'size'
        filter_value = 150
        descripcion = "150x150 px"
    elif FILTRO == 4:
        filter_type = 'size'
        filter_value = 200
        descripcion = "200x200 px"
    elif FILTRO == 5:
        filter_type = 'size'
        filter_value = 250
        descripcion = "250x250 px"
    elif FILTRO == 6:
        filter_type = 'size'
        filter_value = 300
        descripcion = "300x300 px"
    elif FILTRO == 7:
        filter_type = 'weight'
        filter_value = 60
        descripcion = "60 KB"
    elif FILTRO == 8:
        filter_type = 'weight'
        filter_value = 100
        descripcion = "100 KB"
    elif FILTRO == 9:
        filter_type = 'weight'
        filter_value = 150
        descripcion = "150 KB"
    elif FILTRO == 10:
        filter_type = 'weight'
        filter_value = 200
        descripcion = "200 KB"
    else:
        print("ERROR: Opcion de filtro no valida")
        return
    
    # Verificar si se paso un archivo PDF como argumento
    if len(sys.argv) > 1:
        pdf_file = Path(sys.argv[1])
        if not pdf_file.exists():
            print(f"ERROR: No se encuentra el archivo: {sys.argv[1]}")
            return
    else:
        pdf_file = find_first_pdf(work_dir)
        if not pdf_file:
            print("\nERROR: No se encontraron archivos PDF en el directorio.")
            return
    
    print(f"\nDirectorio: {work_dir}")
    print(f"Filtro activo: {descripcion}")
    
    print(f"Procesando: {pdf_file.name}")
    
    # Crear carpeta con nombre completo limpio (sin truncar)
    clean_name = clean_filename(pdf_file.stem)
    output_dir = work_dir / clean_name
    output_dir.mkdir(exist_ok=True)
    
    print(f"Carpeta destino: {output_dir}")
    print()
    
    # Extraer imagenes
    images = extract_images_filter_by_size_or_weight(
        pdf_file, output_dir, filter_type, filter_value
    )
    
    print(f"\n{'='*50}")
    print(f"Completado: {len(images)} imagenes extraidas")
    print(f"Ubicacion: {output_dir}")

if __name__ == "__main__":
    main()

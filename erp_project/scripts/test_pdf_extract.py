import os
import json

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
import django
django.setup()

from compras.utils import extraer_datos_pdf_completo

pdf_path = r'c:\Users\esteb\Desktop\factura_prueba.pdf'

try:
    print('START_EXTRACTION')
    result = extraer_datos_pdf_completo(pdf_path)
    print('EXTRACTION_RESULT:')
    formatted = json.dumps(result, ensure_ascii=False, indent=2)
    print(formatted)
    # Also save to file to inspect later
    with open('scripts/test_pdf_extract_output.json', 'w', encoding='utf-8') as f:
        f.write(formatted)
    print('END_EXTRACTION')
except Exception as e:
    print('ERROR:', str(e))

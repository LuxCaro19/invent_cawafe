from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string

def generar_pdf_comodato(contexto):
    html_string = render_to_string('asociacion/pdf_comodato.html', contexto)
    pdf_file = BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file

def generar_pdf_recepcion(contexto):
    from django.template.loader import render_to_string
    from xhtml2pdf import pisa
    from io import BytesIO

    html_string = render_to_string('asociacion/pdf_recepcion.html', contexto)
    pdf_file = BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_file)
    pdf_file.seek(0)
    return pdf_file
from xhtml2pdf import pisa
import cStringIO as StringIO


def create_pdf(pdf_data):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(pdf_data), dest=result)

    return result.getvalue()

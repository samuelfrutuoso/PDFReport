# from schemas.document_schema import DocumentSchema
# from weasyprint import HTML
# import os
# from jinja2 import Environment, FileSystemLoader

# TEMPLATES_DIR = "templates"
# PDF_DIR = "generated_pdfs"

# os.makedirs(TEMPLATES_DIR, exist_ok=True)
# os.makedirs(PDF_DIR, exist_ok=True)
# jinja_env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# def get_pdf_path(document_id: UUID) -> str:
#   return os.path.join(PDF_DIR, document_id, '.pdf')

# class DocumentService:

#   def create_pdf(self, pdf_request: DocumentSchema):
#     template = jinja_env.get_template(pdf_request.template_name)
#     html = template.render(pdf_request.data)
#     file_path = get_pdf_path(pdf_request.pdf_id)
#     HTML(string=html).write_pdf(file_path)

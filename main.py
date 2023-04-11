from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("KGPrimaryPenmanship", "fonts/KGPrimaryPenmanship.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", "fonts/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("ComicRelief", "fonts/ComicRelief.ttf"))

packet = io.BytesIO()
canvas_obj = canvas.Canvas(packet, pagesize=A4)

page_width, page_height = canvas_obj._pagesize
text_box_max_width = 490

certificate_no = "1234567890"
certificate_text = f"Certificate No: {certificate_no}"
certificate_font_name = "KGPrimaryPenmanship"
certificate_font_size = 24

canvas_obj.setFont(certificate_font_name, certificate_font_size)
canvas_obj.setFillColorRGB(1, 1, 1)

certificate_text_width = pdfmetrics.stringWidth(
    certificate_text, certificate_font_name, certificate_font_size
)
x_coordinate_of_centered_certificate_text = (page_width - certificate_text_width) / 2

canvas_obj.drawString(x_coordinate_of_centered_certificate_text, 558, certificate_text)

student_name = "John Doe"
student_name_font_name = "DejaVuSerif-Bold"
student_name_font_size = 30

canvas_obj.setFont(student_name_font_name, student_name_font_size)
canvas_obj.setFillColorRGB(0, 0, 0)

student_name_text_width = pdfmetrics.stringWidth(
    student_name, student_name_font_name, student_name_font_size
)
x_coordinate_of_centered_student_name_text = (page_width - student_name_text_width) / 2

canvas_obj.drawString(x_coordinate_of_centered_student_name_text, 410, student_name)

course_name = "Lorem ipsum"
course_text = f'"{course_name}" dolor sit amet, consectetur adipiscing elit. Nam ex lacus, suscipit sed mollis ac, sagittis vitae diam. Quisque at diam tempor, venenatis massa id, porta tortor.'
course_font_name = "ComicRelief"
course_font_size = 18.7

lines = []

canvas_obj.setFont(course_font_name, course_font_size)

course_text_width = pdfmetrics.stringWidth(
    course_text, course_font_name, course_font_size
)

if course_text_width > text_box_max_width:
    words = course_text.split()
    line = ""
    for word in words:
        if (
            pdfmetrics.stringWidth(
                line + " " + word, course_font_name, course_font_size
            )
            < text_box_max_width
        ):
            line += " " + word

        else:
            lines.append(line)
            line = word
    lines.append(line)

else:
    lines.append(course_text_width)

course_height = 360

for line in lines:
    line_width = pdfmetrics.stringWidth(line, course_font_name, course_font_size)
    x_coordinate_of_centered_line_text = (page_width - line_width) / 2

    canvas_obj.drawString(x_coordinate_of_centered_line_text, course_height, line)
    course_height -= course_font_size * 1.2

canvas_obj.save()

packet.seek(0)

new_pdf = PdfReader(packet)

existing_pdf = PdfReader(open("template.pdf", "rb"))
output = PdfWriter()

page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)

course_name_with_underscores = "_".join(course_name.split())
output_file_name = f"{student_name}_{course_name_with_underscores}_{certificate_no}.pdf"
output_stream = open(output_file_name, "wb")
output.write(output_stream)
output_stream.close()

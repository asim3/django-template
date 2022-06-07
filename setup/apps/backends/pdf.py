from fpdf import FPDF
from django.contrib.staticfiles import finders


class PDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.set_margins(left=0, top=0, right=0)
        self.set_font('Arial', size=8)
        self.add_page()

    def header(self):
        self.set_fill_color(79, 112, 134)
        self.cell(w=0, h=13, fill=True)
        self.set_y(0.5)
        logo = "./backends/tests/data/django-logo-positive.png"
        self.add_centered_image(logo, image_width=40)

    # def footer(self):
    #     self.set_y(-20)
    #     self.set_font('Arial', 'I', 8)
    #     self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def add_centered_image(self, image_path, image_width):
        x_coordinate = (self.fw / 2) - (image_width / 2)
        self.image(image_path, x=x_coordinate, w=image_width)

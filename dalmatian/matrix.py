# coding:utf-8

import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import colorsys

class Matrix:
    def __init__(self, classes, data):
        self.margin_header = 8.0*mm
        self.margin_footer = 2.0*mm
        self.cell_size = 10.0*mm
        self.font_size = 14
        self.label_font_size = 7
        self.title_font_size = 9
        self.cvs = canvas.Canvas("out.pdf")
        self.page_width = self.margin_header + len(classes)*self.cell_size + self.margin_footer
        self.cvs.setPageSize((self.page_width, self.page_width))
        self.percentage = False
        self.label_color = "black"
        self.cell_color = "black"
        self.line_type = "normal"
        self.data = data
        self.classes = classes

    def draw(self):
        if self.percentage:
            self.font_size -= 3
        percentage_matrix = self.calculate_percentage()
        for i in xrange(len(self.classes)):
            for j in xrange(len(self.classes)):
                x = self.margin_header + self.cell_size * i
                y = self.margin_footer + self.cell_size * (len(self.classes) - 1 - j )
                self.draw_data(x, y, str(self.data[j][i]), percentage_matrix[j][i])
        if self.label_color == "white":
            self.cvs.setFillColorRGB(1, 1, 1)
        else:
            self.cvs.setFillColorRGB(0, 0, 0)
        self.draw_line()
        self.draw_title()
        self.cvs.showPage()
        self.cvs.save()
        print ">> Exported a matrix to ./out.pdf"

    def draw_line(self):
        self.cvs.setLineWidth(0.5)
        self.cvs.rect(self.margin_header, self.margin_footer, self.cell_size * len(self.classes), self.cell_size * len(self.classes), stroke=1, fill=0)
        if self.line_type == "dot":
            self.cvs.setDash(1, 1)
        for i in range(len(self.classes)-1):
            self.cvs.line(self.margin_header, self.margin_footer + self.cell_size * (i+1), self.page_width - self.margin_footer, self.margin_footer + self.cell_size * (i+1))
            self.cvs.line(self.margin_header + self.cell_size * (i+1), self.margin_footer, self.margin_header + self.cell_size * (i+1), self.page_width - self.margin_header)

    def draw_data(self, x, y, text, percentage):
        if self.percentage:
            text = " %d%%" % int(percentage*100)
        cell_color = self.calculate_color(percentage)
        self.cvs.setFillColorRGB(cell_color[0],cell_color[1],cell_color[2])
        self.cvs.rect(x, y, self.cell_size, self.cell_size, stroke=0, fill=1)
        font_size = self.font_size_adjust(text, self.font_size, self.cell_size)
        if percentage > 0.40:
            self.cvs.setFillColorRGB(1, 1, 1)
            self.cvs.setFont("Helvetica-Bold", font_size)
        else:
            self.cvs.setFillColorRGB(0, 0, 0)
            self.cvs.setFont("Helvetica", font_size)
        text_width = self.cvs.stringWidth(text)
        x_position = x + self.cell_size/2 - text_width/2
        y_position = y + self.cell_size/2 - self.font_size/2.8
        self.cvs.drawString(x_position, y_position, text)

    def draw_title(self):
        # Predicted class
        self.cvs.setFont("Helvetica", self.title_font_size)
        title = "Predicted class"
        text_width = self.cvs.stringWidth(title)
        self.cvs.drawString(self.page_width/2 - text_width/2,
                self.page_width - self.title_font_size*1.1, title)

        font_size = self.label_font_size
        for label in self.classes:
            font_size = self.font_size_adjust(label, font_size, self.cell_size)
        for i in range(len(self.classes)):
            text = self.classes[i]
            self.cvs.setFont("Helvetica", font_size)
            text_width = self.cvs.stringWidth(text)
            x_position = self.margin_header + self.cell_size/2 - text_width/2 + self.cell_size*i
            y_position = self.margin_footer + self.cell_size * len(self.classes) + self.label_font_size/2
            self.cvs.drawString(x_position, y_position, text)

        # Actual class
        self.cvs.rotate(90)
        self.cvs.setFont("Helvetica", self.title_font_size)
        title = "Actual class"
        text_width = self.cvs.stringWidth(title)
        self.cvs.drawString(self.page_width/2 - text_width/2,
                - self.title_font_size*1.1, title)

        font_size = self.label_font_size
        for label in self.classes:
            font_size = self.font_size_adjust(label, font_size, self.cell_size)
        for i in range(len(self.classes)):
            text = self.classes[len(self.classes)-1 - i]
            self.cvs.setFont("Helvetica", font_size)
            text_width = self.cvs.stringWidth(text)
            x_position = self.margin_footer + self.cell_size/2 - text_width/2 + self.cell_size*i
            y_position = self.margin_header - self.label_font_size/2
            self.cvs.drawString(x_position, - y_position, text)
        self.cvs.rotate(90)

    def font_size_adjust(self, text, font_size, space_size):
        self.cvs.setFont("Helvetica", font_size)
        text_width = self.cvs.stringWidth(text)
        while text_width > space_size:
            font_size -= 1
            self.cvs.setFont("Helvetica", font_size)
            text_width = self.cvs.stringWidth(text)
        return font_size

    def calculate_percentage(self):
        size = len(self.data[0])
        percentage_matrix = [[0 for x in range(size)] for x in range(size)]
        for j in range(size):
            sum = np.sum(self.data[j])
            for i in range(size):
                percentage_matrix[j][i] = float(self.data[j][i])/float(sum)
        return percentage_matrix

    def calculate_color(self, percentage):
        h = 0
        s = percentage
        v = 1 - percentage*0.6
        if self.cell_color == "red":
            h = 0
        elif self.cell_color == "yellow":
            h = 0.15
            v = 1 - percentage*0.4
        elif self.cell_color == "green":
            h = 0.42
            v = 1 - percentage*0.7
        elif self.cell_color == "blue":
            h = 0.60
        elif self.cell_color == "purple":
            h = 0.84
            v = 1 - percentage*0.7
        else:
            s = 0
            v = 1 - percentage
        return colorsys.hsv_to_rgb(h, s, v)
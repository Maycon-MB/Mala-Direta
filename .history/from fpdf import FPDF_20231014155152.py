from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('Helvetica-BoldItalic', 'Helvetica-BoldOblique.ttf'))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

class MultiColumnSimplePDF(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.width, self.height = letter
        frame1 = Frame(self.leftMargin, self.bottomMargin, self.width/3-6, self.height, id='col1')
        frame2 = Frame(self.leftMargin + self.width/3, self.bottomMargin, self.width/3-6, self.height, id='col2')
        frame3 = Frame(self.leftMargin + 2*self.width/3, self.bottomMargin, self.width/3+6, self.height, id='col3')
        self.addPageTemplates(PageTemplate(id='ThreeCol', frames=[frame1, frame2, frame3]))

def main():
    doc = MultiColumnSimplePDF("MultiColumnSimplePDF.pdf")
    doc.build(getStory())

def getStory():
    story = []
    for i in range(30):
        story.append(Paragraph(str(i + 1), styles['Center']))

        text = "text text text text text text text text text text text text text text text text text text text text text text text text text text"
        p = Paragraph(text, styles['Normal'])
        story.append(Spacer(1, 12))
        story.append(p)
    return story

if __name__ == "__main__":
    main()

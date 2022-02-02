
# ---------------------------------------------------------------
# -----------------     R  E  P  O  R  T  S     -----------------
# ---------------------------------------------------------------

from reportlab.platypus import *
from reportlab.platypus.flowables import Image
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import TopPadder
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
from datetime import date
from time import gmtime, strftime
import locale

import inflect 


w=inflect.engine()
MaxWidth_Content = 530
styles = getSampleStyleSheet()
styles.leading = 24
styleB = styles["BodyText"]
styleN = styles['Normal']
styleH = styles['Heading1']
_style = ParagraphStyle('Courier',fontName="Courier", fontSize=10, leading = 15)
_styleD1 = ParagraphStyle('Courier',fontName="Courier", fontSize=9, leading = 15)
_stylePR = ParagraphStyle('Courier',fontName="Courier", fontSize=7,leading = 10)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=.8 * inch)#,showBoundary=1)
logo_path = request.folder + '/static/images/Merch.jpg'

_limage = Image(logo_path)
_limage.drawHeight = 2.55*inch * _limage.drawHeight / _limage.drawWidth
_limage.drawWidth = 2.25 * inch
_limage.hAlign = 'CENTER'

def landscape_header(canvas, doc):
    canvas.saveState()
    header = Table([[_limage]], colWidths='*')
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN', (0,0), (0,-1), 'CENTER')]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - .3 * cm)

    # Footer
    today = date.today()
    footer = Table([['Printed by: ' + str(auth.user.first_name) + ' ' + str(auth.user.last_name) + ' ' + str(request.now.strftime('%d/%m/%Y,%H:%M'))]], colWidths=['*'])
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('TEXTCOLOR',(0,0),(0,0), colors.gray),
        ('FONTSIZE',(0,-1),(0,-1),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(0,1),'RIGHT')]))
    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - .3 * inch)

    # Release the canvas
    canvas.restoreState()

def get_account_code_movement_report():
    ctr = _balance = 0
    _id = dc(dc.Master_Account.account_code == request.args(0)).select().first()
    _opening_balance = float(_id.opening_balance_1 or 0) + float(_id.opening_balance_2 or 0) + float(_id.opening_balance_3 or 0) + float(_id.opening_balance_4 or 0) + float(_id.opening_balance_5 or 0) + float(_id.opening_balance_6 or 0) + float(_id.opening_balance_9 or 0)
    _closing_balance = float(_id.credit_balance_1 or 0) + float(_id.credit_balance_2 or 0) + float(_id.credit_balance_3 or 0) + float(_id.credit_balance_4 or 0) + float(_id.credit_balance_5 or 0) + float(_id.credit_balance_6 or 0) + float(_id.credit_balance_9 or 0)
    _row = [
        [str(_id.account_code) + '-' +str(_id.account_name) + ', Opening Balance as of ' + str(request.args(1)) + ' : ' + str(locale.format('%.3F',_opening_balance or 0, grouping = True))],
        ['#','Date','Account Code','Dept.','Type','Description','Account Ref.No.','Debit','Credit','Balance']]
    _query = db((db.General_Ledger.account_code == request.args(0)) & (db.General_Ledger.transaction_date >= request.args(1)) & (db.General_Ledger.transaction_date <= request.args(2))).select()
    for n in _query:
        ctr += 1
        if n.debit > 0:                
            _balance = _balance + n.debit
        else:
            _balance = _balance - n.credit        
        _row.append([ctr,n.transaction_date,n.account_code,n.department,n.transaction_type,n.description,n.account_reference_no,locale.format('%.3F',n.debit or 0, grouping = True),locale.format('%.3F',n.credit or 0, grouping = True),locale.format('%.3F',_balance or 0, grouping = True)])
    _row.append(['Closing balance as of ' + str(request.args(1) + ': ' + str(locale.format('%.3F',_closing_balance or 0, grouping = True)))])
    _table = Table(_row, colWidths = [20,60,70,30,30,'*',80,80,70,70,70])
    _table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),      
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8), 
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,2), (-1,2), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN', (7,1), (-1,-1), 'RIGHT'),
    ]))
    row.append(_table)
    doc.pagesize = landscape(A4)
    doc.build(row, onFirstPage=landscape_header, onLaterPages= landscape_header)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data    


def get_account_card_grid():
    ctr = _balance = 0
    _row = [['#','Date','Transaction','Type','Invoice No.','Description','Debit','Credit','Balance']]
    for n in db(db.General_Ledger.account_code == session.account_code).select():
        ctr += 1
        _balance += n.debit - n.credit
        _row.append([
            ctr,
            n.transaction_date.strftime("%m/%d/%Y"), 
            str(n.transaction_prefix_id.prefix) + str(n.transaction_no),
            n.transaction_type,
            str(n.transaction_type_ref) + str(n.account_reference_no),
            n.description,
            locale.format('%.2F',n.debit or 0, grouping = True),
            locale.format('%.2F',n.credit or 0, grouping = True),
            locale.format('%.2F',_balance or 0, grouping = True)
        ])
    table = Table(_row, colWidths = [20,60,70,30,70,'*',80,80,80])
    table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),      
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8), 
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN', (6,1), (-1,-1), 'RIGHT'),

    ]))
    row.append(table)
    doc.pagesize = landscape(A4)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data    


def get_statement_of_account_grid():
    ctr = _balance = 0
    _row = [['#','Date','Transaction','Type','Invoice No.','Description','Debit','Credit','Balance']]
    for n in db(db.General_Ledger.account_code == session.account_code).select():
        ctr += 1
        _balance += n.debit - n.credit
        _row.append([
            ctr,
            n.transaction_date.strftime("%m/%d/%Y"), 
            str(n.transaction_prefix_id.prefix) + str(n.transaction_no),
            n.transaction_type,
            str(n.transaction_type_ref) + str(n.account_reference_no),
            n.description,
            locale.format('%.2F',n.debit or 0, grouping = True),
            locale.format('%.2F',n.credit or 0, grouping = True),
            locale.format('%.2F',_balance or 0, grouping = True)
        ])
    table = Table(_row, colWidths = [20,60,70,30,70,'*',80,80,80])
    table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),      
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8), 
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('ALIGN', (6,1), (-1,-1), 'RIGHT'),

    ]))
    row.append(table)
    doc.pagesize = landscape(A4)
    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data    


########################################################################
class WarehousePageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """                
        page = []
        _page_count = page_count / 2
        _page_number = self._pageNumber        
        if _page_number > _page_count:
            _page_number -= _page_count
        page = "Page %s of %s" % (_page_number, _page_count)                
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(200*mm, 28*mm, printed_on)
        self.drawRightString(115*mm, 28*mm, page)

 

########################################################################
class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """        Add the page number        """
        page = []
        _location = ''        
        _page_number = self._pageNumber
        page = "Page %s of %s" % (_page_number, page_count)        
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        self.drawRightString(200*mm, 28*mm, printed_on)
        self.drawRightString(115*mm, 28*mm, page)

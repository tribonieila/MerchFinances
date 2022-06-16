# ----------------------------------------------------------------------------------------------
# -----------------     A C C O U N T   T R A N S A C T I O N  R E P O R T     -----------------
# ----------------------------------------------------------------------------------------------

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
from reportlab.lib import colors
from uuid import uuid4
from cgi import escape
from functools import partial
import os
from reportlab.pdfgen import canvas

import string
from num2words import num2words

import time
import datetime
from time import gmtime, strftime
import locale
today = datetime.datetime.now()
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
_stylePR = ParagraphStyle('Courier',fontName="Courier", fontSize=8)
_table_heading = ParagraphStyle('Courier',fontName="Courier", fontSize=7, leading = 10)
styles.add(ParagraphStyle(name='Wrap', fontSize=8, wordWrap='LTR', firstLineIndent = 0,alignment = TA_LEFT))
row = []
ctr = 0
tmpfilename=os.path.join(request.folder,'private',str(uuid4()))
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=200,bottomMargin=200, showBoundary=1)
# doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.1 * inch, bottomMargin=1.5 * inch)#, showBoundary=1)
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=20,leftMargin=20, topMargin=2.7 * inch,bottomMargin=2.4 * inch)#, showBoundary=1)

_merchandpartners = request.folder + '/static/images/merchpartners.jpg' 
_img = Image(_merchandpartners)
_img.drawHeight = 2.55 *inch * _img.drawHeight / _img.drawWidth
_img.drawWidth = 3.25 * inch
_img.hAlign = 'CENTER'

_MerchAndPartners = Image(_merchandpartners, width = 550, height = 80, hAlign = 'CENTER')

_merchtrading = request.folder + '/static/images/merchtrading.jpg' 
_img = Image(_merchtrading)
_img.drawHeight = 2.55 *inch * _img.drawHeight / _img.drawWidth
_img.drawWidth = 3.25 * inch
_img.hAlign = 'CENTER'

_MerchTrading = Image(_merchtrading, width = 550, height = 80, hAlign = 'CENTER')

def get_account_voucher_canvas(canvas, doc):
    canvas.saveState()
    _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account_code).select().first()
    
    _top = [
        ['RECEIPT VOUCHER'],
        [str(_id.account_voucher_transaction_code) + str(_id.voucher_no)],
        ['Receive with thanks from: ' + str(_id.received_from),'','','','Date',':',_id.transaction_reference_date.strftime("%d/%b/%Y")], #.strftime("%d/%b/%Y")            
        ['Mode of Payment',':',_id.account_payment_mode_id.account_voucher_payment_name,'','Cheque No',':',_id.cheque_no],
        ['Bank Name',':',_id.bank_name_id,'','Cheque Dated',':',_id.cheque_dated], #.strftime('%d/%b/%Y')
    ]

    if _id.account_payment_mode_id == 1:
        _top = [
            ['RECEIPT VOUCHER'],
            [str(_id.account_voucher_transaction_code) + str(_id.voucher_no)],
            ['Receive with thanks from: ' + str(_id.received_from),'','','','Date',':',_id.transaction_reference_date.strftime("%d/%b/%Y")],            #.strftime("%d/%b/%Y")
            ['Mode of Payment',':',_id.account_payment_mode_id.account_voucher_payment_name,'','','',''],
            ['Account Code',':',str(_id.account_code) + ' - ' + str(_ma.account_name),'','','',''],
        ]
    header = Table(_top, colWidths=[110,20,'*',30,110,20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),10),        
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('ALIGN',(0,0),(-1,1),'CENTER'),    
        ('TOPPADDING',(0,1),(-1,1),10), 
        ('ALIGN',(4,2),(4,2),'RIGHT'),    
        ('BOTTOMPADDING',(0,1),(-1,1),25),   
        ('FONTNAME', (0, 1), (-1, 1), 'Courier-Bold'),           
        ('FONTSIZE',(0,1),(-1,1),13),
        ('FONTSIZE',(0,0),(-1,0),10),
        ('TOPPADDING',(0,2),(-1,-1),0),
        ('BOTTOMPADDING',(0,2),(-1,-1),0),
        ('TOPPADDING',(0,2),(-1,2),10), 
        ('BOTTOMPADDING',(0,-1),(-1,-1),10),
        ('BOX', (0,2), (-1,-1), 0.25, colors.black,None, (2,2)),
    ]))

    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin -.3 * inch)

    _bottom1 = [['',str(_id.created_by.first_name.upper()) + ' ' + str(_id.created_by.last_name.upper()),''],['','Prepared By','','Approved By','']]
    footer1 = Table(_bottom1, colWidths=[60,'*',50,'*',60])
    footer1.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),    
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),10),        
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),        
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('LINEBELOW', (1,0), (1,0), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (3,0), (3,0), 0.25,  colors.black,None, (2,2)),
    ]))

    footer1.wrap(doc.width, doc.bottomMargin)
    footer1.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 2 * cm)

    _bottom2 = [
        ['Purpose',':',_id.purpose,'','Received From',':',_id.received_from],
        ['Cost Center',':',_id.cost_center,'','Collected By',':',_id.collected_by],
        ['Remarks',':',_id.remarks,'','','','']]
    footer2 = Table(_bottom2, colWidths=[80,20,'*',30,80,20,'*'])
    footer2.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),    
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('TOPPADDING',(0,0),(-1,-1),0),        
    ]))
    footer2.wrap(doc.width, doc.bottomMargin)
    footer2.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 4.6 * cm)
    canvas.restoreState()

def get_account_voucher_request_id():
    row = []
    ctr = _total_amount = 0
    _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()
    _row = [['#','Code','Name','Dept.','Type','Ref.No.','Description','Amount']]
    for n in db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select():
        ctr += 1
        _ma =  dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        # _am = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        _account_name = 'None'
        if _ma:
            _account_name = _ma.account_name
        _row.append([
            ctr,
            n.account_credit_code,
            Paragraph(_account_name, style = _style),
            n.department_code,
            n.transaction_payment_type_id.transaction_payment_type,
            n.account_reference,
            Paragraph(n.description or '',style=_style),
            locale.format('%.2F',n.amount_paid or 0, grouping = True),
            ])
        _total_amount += float(n.amount_paid or 0)

    (_whole, _frac) = (int(_total_amount), locale.format('%.2f',_total_amount or 0, grouping = True))
    _amount_in_words = 'QAR ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100 DIRHAMS'

    _row.append(['','','','','','Total Amount (QAR): ','',locale.format('%.2F', _total_amount or 0, grouping = True)])
    _row.append(['AMOUNT IN WORDS: ' + str(_amount_in_words),'','','','','','',''])
    _row_table = Table(_row, colWidths=[20,50,130,40,30,70,130,85])
    _row_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),  
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),10),
        ('FONTSIZE',(0,-1),(-1,-1),8),
        ('ALIGN',(-1,1),(-1,-1),'RIGHT'),
        # ('ALIGN',(6,-1),(-1,-1),'RIGHT'),
        # ('ALIGN',(-2,6),(-2,-6),'RIGHT'),
        ('VALIGN',(0,1),(-1,-3),'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold', 12),
        ('FONTNAME', (6, -2), (-1, -2), 'Courier-Bold', 12),
        ('FONTNAME', (0, -1), (-1, -1), 'Courier-Bold', 12),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('BACKGROUND',(0,0),(-1,0), colors.Color(0, 0, 0, 0.4)),
        ('LINEBELOW', (0,0), (-1,0), 0.25,  colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25,  colors.black,None, (2,2)),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),5),        
        ('BOX', (0,0), (-1,-3), 0.25, colors.black,None, (2,2)),
    ]))
    row.append(_row_table)
    # doc.build(row)    
    doc.build(row, onFirstPage=get_account_voucher_canvas, onLaterPages = get_account_voucher_canvas, canvasmaker=PageNumCanvas)    

    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data

def get_debit_credit_note_canvas_id(canvas, doc):
    canvas.saveState()
    _id = db(db.Debit_Credit_Transaction.id == request.args(0)).select().first() # row transaction
    _hd = db(db.Debit_Credit.id == _id.serial_note_id).select().first() # row header    
    _ma = dc(dc.Master_Account.account_code == _hd.account_code).select().first()
    _account_name = ''
    if _ma:
        _account_name = _ma.account_name
    _title = _hd.transaction_type
    _logo = _MerchAndPartners
    if int(_hd.business_unit) == 2:
        _logo = _MerchTrading
    _rowHeader = [[_logo]]
    _rowHeaderTable = Table(_rowHeader)
    _rowHeaderTable.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
    ]))
    _rowHeaderTable.wrapOn(canvas, doc.width, doc.topMargin)
    _rowHeaderTable.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin + .3 * cm)

    
    _header = [
        [_title],
        [str(_id.serial_note_id.serial_note) + '-' +str(_id.serial_note_suffix_id)],
        ['Serial No.',':',str(_id.serial_note_id.serial_note) + '-' +str(_id.serial_note_suffix_id),'','Date',':',_hd.transaction_date.strftime('%d/%b/%Y')],
        ['Account Name',':',_account_name,'','Account Code',':',_id.account_code],
        # ['','','','','Period From',':',_id.date_from],
        # ['','','','','Period To',':',_id.date_to],
        ]
    _header_table = Table(_header, colWidths=['*',10,150,10,'*',10,150])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('FONTSIZE',(0,1),(0,1),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('FONTNAME', (0, 1), (0, 1), 'Courier-Bold'),        
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(0,1),(-1,1)),
        ('SPAN',(2,2),(2,2)),
        ('ALIGN',(0,0),(-1,1),'CENTER'),        
        ('BOTTOMPADDING',(0,0),(-1,0),0),
        ('BOTTOMPADDING',(0,1),(0,1),10),
        ('TOPPADDING',(0,2),(-1,2),10),
        ('BOTTOMPADDING',(0,-1),(-1,-1),10),
        ('LINEABOVE', (0,2), (-1,2), 0.25, colors.black,None, (2,2)),
        # ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ])) 
    _header_table.wrapOn(canvas, doc.width, doc.topMargin) 
    _header_table.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 1.5 * cm)

    _sgntr = [
        ['','','','','','',''],
        ['Prepared by:','','Department Head','','Finance Manager','','General Manager'],
        ['Posted By: ' + str(auth.user.first_name + ' ' + str(auth.user.last_name)) + ' ' +str(request.now.strftime('%d%b%Y %I:%M:%S %p')),'','','','','',''],
        ]
    _sgntr_table = Table(_sgntr, colWidths=['*',10,'*',10,'*',10,'*'])
    _sgntr_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,-1),(-1,-1),7),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,1),(-1,1),'CENTER'),
        ('LINEABOVE',(0,1), (0,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE',(2,1), (2,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE',(4,1), (4,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE',(6,1), (6,1), 0.25, colors.black,None, (2,2)),
        ]))  

    _sgntr_table.wrap(doc.width, doc.bottomMargin)
    _sgntr_table.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 2.3 * cm)

    canvas.restoreState()

def get_debit_credit_note_transaction_id():
    _id = db(db.Debit_Credit_Transaction.id == request.args(0)).select().first() # row transaction
    _hd = db(db.Debit_Credit.id == _id.serial_note_id).select().first() # row header    
    _ma = dc(dc.Master_Account.account_code == _hd.account_code).select().first()
    
    ctr = db((db.Debit_Credit_Transaction.serial_note_id == _id.serial_note_id) & (db.Debit_Credit_Transaction.delete == False)).count()
  
    (_whole, _frac) = (int(_id.amount), locale.format('%.2f',_id.amount or 0, grouping = True))
    _amount_in_words = str(_hd.currency_id.mnemonic) + ' ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100'
    _tranx = [
        ['DESCRIPTION','AMOUNT'],
        [Paragraph(_id.description,style=_styleD1),str(_hd.currency_id.mnemonic) + ' ' + str(locale.format('%.2F',_id.amount or 0, grouping = True))],        
        [_amount_in_words, str(_hd.currency_id.mnemonic) + ' ' + str(locale.format('%.2F',_id.amount or 0, grouping = True))]
        ]
    _tranx_table = Table(_tranx, colWidths=[455,100])
    _tranx_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        # ('FONTSIZE',(0,3),(0,3),8),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('ALIGN',(1,1),(1,-1),'RIGHT'),
        ('TOPPADDING',(0,1),(-1,1),20),
        ('BOTTOMPADDING',(0,1),(-1,2),20),
        # ('BOTTOMPADDING',(0,1),(-1,1),20),
        ('VALIGN',(0,1),(-1,-1),'TOP'), 
        ('LINEABOVE', (0,0), (-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,1), (-1,1), 0.25, colors.black,None, (2,2)),
        ('LINEABOVE', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW', (0,-1), (-1,-1), 0.25, colors.black,None, (2,2)),
        ]))    


    row.append(_tranx_table)
    row.append(Spacer(1,.5*cm))   
    
    doc.build(row, onFirstPage=get_debit_credit_note_canvas_id)    
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data

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
        _page_count = page_count
        _page_number = self._pageNumber
        PDFfile = 'For electronic mail purposes only.'
        page = "Page %s of %s" % (_page_number, _page_count)        
        printed_on = 'Printed On: '+ str(request.now.strftime('%d/%m/%Y,%H:%M'))
        self.setFont("Courier", 7)
        # self.drawRightString(61*mm, 10*mm, PDFfile)
        self.drawRightString(200*mm, 10*mm, printed_on)
        self.drawRightString(115*mm, 10*mm, page)

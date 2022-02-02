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
doc = SimpleDocTemplate(tmpfilename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=1 * inch,bottomMargin=1.5 * inch)

def get_debit_credit_note_id():
    _id = db(db.Debit_Credit_Transaction.id == request.args(0)).select().first() # row transaction
    _hd = db(db.Debit_Credit.id == _id.serial_note_id).select().first() # row header    
    _title = _hd.transaction_type
    _header = [
        [_title],
        ['Serial No.',':',_id.transaction_no,'','Date',':',_hd.transaction_date],
        ['Account Name',':','Account name here','','Account Code',':',_id.account_code],
        ['','','','','Period From',':',_id.date_from],
        ['','','','','Period From',':',_id.date_to],
        ]
    _header_table = Table(_header, colWidths=['*',10,150,10,'*',10,150])
    _header_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,0),(-1,0),12),
        ('FONTNAME',(0,0),(-1,-1), 'Courier'),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(2,2),(2,2)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('BOTTOMPADDING',(0,0),(-1,0),20),
        ]))    
    (_whole, _frac) = (int(_id.amount), locale.format('%.2f',_id.amount or 0, grouping = True))
    _amount_in_words = str(_hd.currency_id.mnemonic) + ' ' + string.upper(w.number_to_words(_whole, andword='')) + ' AND ' + str(str(_frac)[-2:]) + '/100'
    _tranx = [
        ['DESCRIPTION','AMOUNT'],
        [Paragraph(_id.description_1,style=_styleD1),str(_hd.currency_id.mnemonic) + ' ' + str(locale.format('%.2F',_id.amount or 0, grouping = True))],
        [Paragraph(_id.description_2,style=_styleD1)],
        [_amount_in_words, str(_hd.currency_id.mnemonic) + ' ' + str(locale.format('%.2F',_id.amount or 0, grouping = True))]
        ]
    _tranx_table = Table(_tranx, colWidths=['*',100])
    _tranx_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTSIZE',(0,0),(-1,-1),9),
        ('FONTSIZE',(0,3),(0,3),8),
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

    row.append(_header_table)
    row.append(Spacer(1,.5*cm))
    row.append(_tranx_table)
    row.append(Spacer(1,.5*cm))
    row.append(_sgntr_table)

    doc.build(row)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'    
    return pdf_data
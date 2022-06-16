# ----------------------------------------------------------------------------------------------
# -------------     A C C O U N T   R E C O N C I L I A T I O N  R E P O R T     ---------------
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

def get_account_reconciliation_canvas(canvas, doc):
    canvas.saveState()
    _id = db(db.Account_Reconciliation_Header.id == request.args(0)).select().first()
    _top = [
        ['ACCOUNT RECONCILIATION'],        
        ['Transaction No',':',_id.reconciliation_transaction_no,'','Transaction Date',':',_id.reconciliation_date],
        ['Voucher No.',':',_id.voucher_no,'','Voucher Amount',':',locale.format('%.2F',_id.rv_amount or 0, grouping = True)],
        ['Total Rec.Amount',':',locale.format('%.2F',_id.total_reconciled_amount or 0, grouping = True),'','Total Rec.Balance',':',locale.format('%.2F',_id.rv_balanced_amount or 0, grouping = True)]
    ]
    header = Table(_top, colWidths=[110,20,'*',30,110,20,'*'])
    header.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('SPAN',(0,0),(-1,0)),
        ('ALIGN',(0,0),(-1,0),'CENTER'),    

    ]))
    header.wrapOn(canvas, doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin -.3 * inch)

    foot = [['']]
    footer = Table(foot)
    footer.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),
    ]))

    footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, doc.bottomMargin - 2 * cm)

    canvas.restoreState()

def get_account_reconciliation_id():
    row = []
    ctr = 0
    _id = db(db.Account_Reconciliation_Header.id == request.args(0)).select().first()
    _row = [['#','Date','Account Code','Description','Debit','Credit','Last Pay.','Balance','New Payment']]
    for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(0)).select():
        ctr += 1
        _row.append([
            ctr,
            n.transaction_date,
            n.account_code,
            n.description,
            locale.format('%.2F',n.debit or 0, grouping = True),
            locale.format('%.2F',n.credit or 0, grouping = True),
            locale.format('%.2F',n.amount_paid or 0, grouping = True),
            locale.format('%.2F',n.balanced_amount or 0, grouping = True),
            locale.format('%.2F',n.new_amount_paid or 0, grouping = True),
        ])
    row_table = Table(_row, colWidths=[20,60,70,104,60,60,60,60,60])
    row_table.setStyle(TableStyle([
        # ('GRID',(0,0),(-1,-1),0.5, colors.Color(0, 0, 0, 0.2)),  
        ('FONTNAME', (0, 0), (-1, -1), 'Courier'),
        ('FONTSIZE',(0,0),(-1,-1),8),
        ('FONTSIZE',(0,0),(-1,-1),8),        
        ('ALIGN',(4,1),(-1,-1),'RIGHT'),
        ('LINEABOVE',(0,0),(-1,0), 0.25, colors.black,None, (2,2)),
        ('LINEBELOW',(0,0),(-1,0), 0.25, colors.black,None, (2,2)),
    ]))
    row.append(row_table)
    doc.build(row, onFirstPage = get_account_reconciliation_canvas, onLaterPages = get_account_reconciliation_canvas)
    pdf_data = open(tmpfilename,"rb").read()
    os.unlink(tmpfilename)
    response.headers['Content-Type']='application/pdf'
    return pdf_data


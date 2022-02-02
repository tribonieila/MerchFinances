import time, calendar
import datetime
import string
import locale
locale.setlocale(locale.LC_ALL,'')
from datetime import date

@auth.requires_login()
def get_statement_of_account_form():
    session.account_code = ''
    _year = date.today().year
    _year1 = _year - 1
    _year2 = _year - 2    
    form = SQLFORM.factory(
        Field('account_code','string', length = 15),
        Field('year','string',length = 4, default=_year, requires = IS_IN_SET([(_year,_year),(_year1, _year1),(_year2,_year2)],zero = 'Choose Year')),
        Field('type','string',length = 4, requires = IS_IN_SET([('S','S - Summarized'),('D','D - Detailed')],zero = 'Choose Type')),
        Field('start_date','date', default = request.now),
        Field('end_date','date', default = request.now))
    return dict(form = form)    

def patch_statement_of_account_id():        
    _id = db(db.General_Ledger.account_code == request.vars.account_code).select().first()
    response.js = "alertify.error('%s Not found!')" % (request.vars.account_code)
    if _id:        
        session.account_code = request.vars.account_code
        response.js = "$('#idPrint').removeAttr('disabled');$('#GEtbl').get(0).reload();alertify.success('Success!')"

@auth.requires_login()
def load_statement_of_account_grid():
    ctr = _balance = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction'),TD('Type'),TD('Invoice No.'),TD('Description'),TD('Debit'),TD('Credit'),TD('Balance')),_class='bg-red')
    _ma = dc(dc.Master_Account.account_code == str(session.account_code)).select().first()
    _closing_balance = 0
    if _ma:
        _closing_balance = _ma.closing_balance
    for n in db(db.General_Ledger.account_code == session.account_code).select():
        ctr += 1
        _balance += n.debit - n.credit
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date.strftime("%m/%d/%Y")),
            TD(n.transaction_prefix_id.prefix,n.transaction_no),
            TD(n.transaction_type),
            TD(n.transaction_type_ref,n.account_reference_no),            
            TD(n.description),
            TD(locale.format('%.2F',n.debit or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True),_align='right'),            
            TD(locale.format('%.2F',_balance or 0, grouping = True),_align='right')))            
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD(locale.format('%.2F',_closing_balance or 0, grouping = True),_align='right')))
    body = TBODY(*row)    
    table = TABLE(*[head, body, foot], _class='table table-stripe', _id='SOAtbl')
    return dict(table = table)

def validate_account_code_movement(form):    
    _id = dc(dc.Master_Account.account_code == request.vars.account_code).select().first()
    if not _id:
        form.errors.account_code = 'Account code not found...'
        
@auth.requires_login()
def get_account_code_movement_form():
    session.account_code = session.type = session.dept_code_id = session.entries = ''
    session.start_date = request.now
    session.end_date = request.now
    row = []
    ctr = _balance = _opening_balance = 0
    _year = date.today().year
    _year1 = _year - 1
    _year2 = _year - 2    
    session.account_no = ''
    form = SQLFORM.factory(
        Field('account_code','string', length = 15),
        Field('year','string',length = 4, default=_year, requires = IS_IN_SET([(_year,_year),(_year1, _year1),(_year2,_year2)],zero = 'Choose Year')),
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('type','string',length = 4, requires = IS_IN_SET([('S','S - Summarized'),('D','D - Detailed')],zero = 'Choose Type')),
        Field('entries','string',length = 4, requires = IS_IN_SET([('Y','Y - Yes'),('N','N - No')],zero = 'Choose Entries')),
        Field('start_date','date', default = request.now),
        Field('end_date','date', default = request.now))
    return dict(form = form, account_no = session.account_no)

@auth.requires_login()
def patch_account_card():
    _id = db(db.General_Ledger.account_code == request.vars.account_code).select().first()
    response.js = "alertify.error('%s Not found!')" % (request.vars.account_code)
    if _id:        
        session.account_code = request.vars.account_code
        session.type = request.vars.type
        session.dept_code_id = request.vars.dept_code_id
        session.entries = request.vars.entries
        session.start_date = request.vars.start_date
        session.end_date = request.vars.end_date
        session.account_no = ''
        response.js = "$('#ACtbl').get(0).reload();$('#idPrint').removeAttr('disabled');alertify.success('Success!')"

@auth.requires_login()    
def load_account_card_grid():    
    ctr = _balance = _debit = _credit = 0
    row = []
    _account_name = ''
    _id = db(db.General_Ledger.account_code == session.account_code).select().first() # dc(dc.Master_Account.account_code == str(session.account_code)).select().first()    
    if _id: 
        
        _account_name = dc(dc.Master_Account.account_code == _id.account_code).select().first()
        _sub_group =  ''       
        if _account_name.account_sub_group_id:
            _sub_group = str(_account_name.account_sub_group_id.account_group_name) +  ' - '
        _account_name = _sub_group,_account_name.account_name, ', ', SPAN(_account_name.account_code,_class='text-muted')        
    _opening_balanced = opening_balance(session.account_code, session.dept_code_id)
    _credit_balanced = credit_balance(session.account_code, session.dept_code_id)

    head = THEAD(
        TR(TD('',_colspan='6'),TD(),TD(B('Opening Balance for department ', session.dept_code_id,' : ',locale.format('%.3F',_opening_balanced or 0, grouping = True)),_align='right',_colspan='4')),
        TR(TD(_account_name,_colspan='6'),TD(),TD(B('Opening Balance for all department : ',locale.format('%.3F',total_opening_balance(session.account_code) or 0, grouping = True)),_align='right',_colspan='4')),
        TR(TD('#'),TD('Date'),TD('TXN Reference'),TD('Type'),TD('Dept.'),TD('Loc.'),TD('A/C Reference'),TD('Description'),TD('Debit'),TD('Credit'),TD('Balance'),_class='bg-red'))   
    
    _query = db((db.General_Ledger.account_code == session.account_code) & (db.General_Ledger.department == session.dept_code_id) &  (db.General_Ledger.transaction_date >= session.start_date) & (db.General_Ledger.transaction_date <= session.end_date)).select()              
    if session.entries == 'N':
        _query = db((db.General_Ledger.account_code == session.account_code) & (db.General_Ledger.department == session.dept_code_id) &  (db.General_Ledger.transaction_date >= session.start_date) & (db.General_Ledger.transaction_date <= session.end_date) & (db.General_Ledger.debit > 0) & (db.General_Ledger.credit > 0)).select()                  
    for n in _query:
        ctr += 1
        _balance += n.debit - n.credit        
        _debit += n.debit
        _credit += n.credit
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date.strftime("%m/%d/%Y")),
            TD(n.gl_entry_ref),
            TD(n.transaction_type_ref),
            TD(n.department),
            TD(n.location),
            TD(n.transaction_type_ref,n.account_reference_no),            
            TD(n.description),            
            TD(locale.format('%.3F',n.debit or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.credit or 0, grouping = True),_align='right'),            
            TD(locale.format('%.3F',_balance or 0, grouping = True),_align='right')))     
    body = TBODY(*row)
    footer = TFOOT(
        TR(TD(B('Closing Balance for department ', session.dept_code_id,' as of ',request.now.date(),' : ', locale.format('%.3F',_credit_balanced or 0, grouping = True)), _colspan='8'),TD(locale.format('%.3F',_debit or 0, grouping = True),_class='bg-gray-active color-palette', _align='right'),TD(locale.format('%.3F',_credit or 0, grouping = True),_class='bg-gray-active color-palette',_align='right'),TD(locale.format('%.3F',_balance or 0, grouping = True),_class='bg-gray-active color-palette',_align='right')),
        TR(TD(B('Closing Balance for all department as of ',request.now.date(),' : ',locale.format('%.3F',total_credit_balance(session.account_code) or 0, grouping = True)), _colspan='8'),TD(),TD(),TD()))
    table = TABLE(*[head, body, footer], _class='table table-striped table-hover', _id="ACtbl")        
    if session.type == 'S':
        ctr = _balance = 0
        row = []
        _debit = db.General_Ledger.debit.sum().coalesce_zero()
        _credit = db.General_Ledger.credit.sum().coalesce_zero()
        _account_name = dc(dc.Master_Account.account_code == session.account_code).select().first()
        head = THEAD(TR(TD('#'),TD('Start Date'),TD('End Date'),TD('Department'),TD('Account Code'),TD('Account Name'),TD('Debit'),TD('Credit'),TD('Total Amount'),TD()),_class='bg-red')
        for n in db((db.General_Ledger.account_code == session.account_code) & (db.General_Ledger.department == session.dept_code_id) & (db.General_Ledger.transaction_date >= session.start_date) & (db.General_Ledger.transaction_date <= session.end_date)).select(_debit, _credit, db.General_Ledger.account_code, db.General_Ledger.department, groupby=db.General_Ledger.department | db.General_Ledger.account_code  ):
            ctr += 1
            
            _balance += n[_debit] - n[_credit]
            trnx_lnk = A(I(_class='fa fa-chart-bar'), _title='Transaction Row', _type=' button', _role='button', _class='btn btn-icon-toggle', callback=URL('reports','patch_general_ledger_id'))
            btn_lnk = DIV(trnx_lnk)
            row.append(TR(
                TD(ctr),
                TD(session.start_date),
                TD(session.end_date),
                TD(n.General_Ledger.department),
                TD(n.General_Ledger.account_code),
                TD(_account_name.account_name),
                TD(locale.format('%.3F',n[_debit] or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n[_credit] or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',_balance or 0, grouping = True),_align='right'),
                TD(btn_lnk)))
        body = TBODY(*row)
        table = TABLE(*[head, body], _class='table table-bordered table-hover', _id='ACtbl')        
    return dict(table = table)

@auth.requires_login()
def patch_general_ledger_id():

    ctr = _balance = _total_debit = _total_credit = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction'),TD('Type'),TD('Invoice No.'),TD('Description'),TD('Debit'),TD('Credit'),TD('Balance')),_class='bg-red')
    # _query = db((db.General_Ledger.account_code == session.account_code) & (db.General_Ledger.transaction_date >= request.vars.start_date) & (db.General_Ledger.transaction_date <= request.vars.end_date)).select()        
    _query = db((db.General_Ledger.account_code == session.account_code) & (db.General_Ledger.transaction_date >= session.start_date) & (db.General_Ledger.transaction_date <= session.end_date)).select()        
    for n in _query:
        ctr += 1
        _balance += n.debit - n.credit
        _total_debit += n.debit
        _total_credit += n.credit
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date.strftime("%m/%d/%Y")),
            TD(n.transaction_prefix_id.prefix,n.transaction_no),
            TD(n.transaction_type),
            TD(n.transaction_type_ref,n.account_reference_no),            
            TD(n.description),
            TD(locale.format('%.3F',n.debit or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.credit or 0, grouping = True),_align='right'),            
            TD(locale.format('%.3F',_balance or 0, grouping = True),_align='right')))     
    body = TBODY(*row)
    footer = TFOOT(TR(TD(_colspan='6'),TD(locale.format('%.3F',_total_debit or 0, grouping = True),_class='bg-gray-active color-palette',_align='right'),TD(locale.format('%.3F',_total_credit or 0, grouping = True),_class='bg-gray-active color-palette',_align='right'),TD(locale.format('%.3F',_balance or 0, grouping = True),_class='bg-gray-active color-palette',_align='right')))
    table = TABLE(*[head, body, footer], _class='table table-hover', _id="ACtbl")       
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Details','message':'%s'}).show();" %(XML(table, sanitize = True))    



        
    
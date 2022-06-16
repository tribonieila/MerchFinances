# ----------------------------------------------------------------------------------------------
# --------------     J O U R N A L  V O U C H E R  C O N F I R M A T I O N     -----------------
# ----------------------------------------------------------------------------------------------
from datetime import datetime, date
import locale
import datetime
import random
import string
locale.setlocale(locale.LC_ALL, '')
x = datetime.datetime.now() # auth generate

def put_batch_posting_sequence_id():
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_jv_confirmation_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('JV Req.No.'),TD('Acct.Type'),TD('Acct.Code'),TD('Total Amount'),TD('Prepared By'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')    
    _query = db(db.Journal_Voucher_Header_Request.status_id == 18).select(orderby = db.Journal_Voucher_Header_Request.id)
    for n in _query:
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership('ACCOUNTS'):
            if (n.status_id == 18) and (n.created_by == auth.user_id):
                appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Confirm', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_jv_confirmation','post_journal_voucher',args = n.id, extension = False))
        btn_lnk = DIV(appr_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.journal_voucher_request_no),            
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align='right'),
            TD(n.created_by.first_name[0],'. ',n.created_by.last_name.upper()),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_journal_voucher():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _id = _total_amount = 0
    db.Journal_Voucher_Header_Request.journal_voucher_request_no.default = str(x.strftime('%d%y%H%M'))
    db.Journal_Voucher_Header_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'JV-TASK3'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(0)).select().first()      
    form = SQLFORM(db.Journal_Voucher_Header_Request, request.args(0))
    return dict(form = form, _id = _id)    

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_journal_voucher_transaction():
    db.Journal_Voucher_Transaction_Request.ticket_no_id.default = _ticket_no_ref = session.ticket_no_id
    db.Journal_Voucher_Transaction_Request.cost_center_category_id.requires= IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'),null=None)
    db.Journal_Voucher_Transaction_Request.cost_center_id.requires = IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'),null=None)
    form = SQLFORM(db.Journal_Voucher_Transaction_Request)    
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Debit Code'),TD('Dept.'),TD('Description'),TD('Credit Code'),TD('Amount'),TD()),_class='bg-red')
    _query = db((db.Journal_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id) & (db.Journal_Voucher_Transaction_Request.created_by == auth.user_id)).select()
    if request.args(0):
        _query = db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        _total_amount += float(n.amount or 0)
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , callback=URL('workflow_journal_voucher','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.account_debit_code),
            TD(n.dept_code_id),
            TD(n.description),
            TD(n.account_credit_code),
            TD(locale.format('%.2F',n.amount or 0, grouping = True), _align='right'),
            TD(btn_lnk)))            
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :')),_align='right',_class='bg-green color-palette'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True))), _align ='right',_class='bg-green color-palette'),TD(_class='bg-green color-palette')))
    table = TABLE(*[head, body, foot], _class='table',_id='JVTtbl')    
    return dict(form = form, table = table)


@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def patch_jv_confirmation_id():
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(1)).select().first()
    if int(request.args(0)) == 1: # account confirmation
        if _id.status_id == 1 or _id.status_id == 19:
            response.js = "alertify.notify('Already %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 19:
            _jou = db(db.Journal_Voucher_Header.journal_voucher_no == _id.journal_voucher_no).select().first()
            _jou.update_record(status_id = 19)
            _id.update_record(status_id = 19)
            sync_to_general_ledger()
            response.js = "alertify.success('JV Confirmed.');window.location.href = '%s'" % URL('workflow_jv_confirmation','get_jv_confirmation_grid')
        
def sync_to_general_ledger():    
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(1)).select().first()
    _seq = put_batch_posting_sequence_id()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _ga = db(db.General_Ledger.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 24).select().first()    
    _header = db(db.Journal_Voucher_Header.journal_voucher_no == _id.journal_voucher_no).select().first()
    for n in db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(1)).select():                
        _gl = db(db.General_Ledger.account_code == n.account_debit_code).select().first()        
        _ser.serial_number += 1
        _row.serial_number += 1
        _debit_no_serial = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(n.account_debit_code) + '/' + str(_row.serial_number)        
        db.General_Ledger.insert( # account_debit_code
            transaction_prefix_id = _ser.id, 
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_reference_date,
            transaction_type = _id.account_voucher_transaction_type,
            location = 99, 
            transaction_type_ref = n.account_voucher_transaction_code,
            transaction_date_entered = request.now,
            department = n.dept_code_id,
            type = _id.account_voucher_transaction_type,
            reference_no = n.account_reference,
            account_reference_no = _id.journal_voucher_no,
            account_code = n.account_debit_code,
            acct_code2 = n.account_credit_code,
            description = n.description,
            credit = 0,
            debit = n.amount,
            amount_paid = 0,
            gl_entry_ref = _debit_no_serial,
            batch_posting_seq = _seq,
            entrydate = request.now)
        _row.update_record()
        # n.update_record(gl_entry_ref = _debit_no_serial)
        
        _row.serial_number += 1
        _credit_no_serial = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(n.account_credit_code) + '/' + str(_row.serial_number)
        db.General_Ledger.insert( # account_credit_code
            transaction_prefix_id = _ser.id, 
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_reference_date,
            transaction_type = _id.account_voucher_transaction_type,
            location = 99, 
            transaction_type_ref = n.account_voucher_transaction_code,
            transaction_date_entered = request.now,
            department = n.dept_code_id,
            type = _id.account_voucher_transaction_type,
            reference_no = n.account_reference,
            account_reference_no = _id.journal_voucher_no,
            account_code = n.account_credit_code,
            acct_code2 = n.account_debit_code,
            description = n.description,
            credit = n.amount,
            debit = 0,
            amount_paid = 0,
            gl_entry_ref = str(_credit_no_serial),
            batch_posting_seq = _seq,
            entrydate = request.now)
        _row.update_record()        
        for x in db((db.Journal_Voucher_Transaction.journal_voucher_header_id == _header.id) & (db.Journal_Voucher_Transaction.account_reference == n.account_reference)).select():
            x.update_record(gl_entry_ref = str(_debit_no_serial)+ ' | ' + str(_credit_no_serial))
        n.update_record(gl_entry_ref = str(_debit_no_serial)+ ' | ' + str(_credit_no_serial))
    _ser.update_record()

    for n in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
        _mb = db(db.Master_Account_Balance_Current_Year.account_code == n.account_code).select().first()
        _ma = dc(dc.Master_Account.account_code == n.account_code).select().first()
        if _mb:
            if n.credit == 0:            
                _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) + float(n.debit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) + float(n.debit or 0))
            else:
                _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) - float(n.credit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) - float(n.credit or 0))
        elif not _mb:
            if n.credit == 0:
                db.Master_Account_Balance_Current_Year.insert(
                    financial_year = request.now, 
                    account_code = n.account_code,
                    account_name = _ma.account_name,
                    closing_balance_99 = float(n.debit or 0),
                    total_closing_balance = float(n.debit or 0))                
            else:
                x = 0                
                db.Master_Account_Balance_Current_Year.insert(
                    financial_year = request.now, 
                    account_code = n.account_code,
                    account_name = _ma.account_name,
                    closing_balance_99 = float(-n.credit or 0),
                    total_closing_balance = float(-n.credit or 0))                


    
    



# ----------------------------------------------------------------------------------------------
# --------------     P A Y M E N T  V O U C H E R  C O N F I R M A T I O N     -----------------
# ----------------------------------------------------------------------------------------------

from datetime import datetime, date
import locale
import datetime
import random
import string
locale.setlocale(locale.LC_ALL, '')

def patch_pv_confirmation_id():    
    if int(request.args(0)) == 1:
        _id = db(db.Payment_Voucher_Request.id == request.args(1)).select().first()
        if _id.status_id == 1 or _id.status_id == 15:
            response.js = "alertify.notify('Already %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 15:            
            _vou = db(db.Payment_Voucher_Header.payment_voucher_no == _id.payment_voucher_no).select().first()
            _vou.update_record(status_id = 15)
            _id.update_record(status_id = 15)
            sync_payment_voucher_to_general_ledger(_id.id)
            response.js = "alertify.success('PV Confirmed.');window.location.href = '%s'" % URL('workflow_pv_confirmation','get_pv_confirmation_grid')

def put_batch_posting_sequence_id():
    # _id = db(db.Batch_Posting_Sequence.prefix_seq == request.args(0)).select().first()
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq

def sync_payment_voucher_to_general_ledger(x):
    #---------------- confirmation from accounts creator ---------------
    #-------------------- posting to general ledger --------------------
    import datetime
    _id = db(db.Payment_Voucher_Request.id == x).select().first()
    _seq = put_batch_posting_sequence_id()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _ga = db(db.General_Ledger.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 23).select().first()    
    _header = db(db.Payment_Voucher_Header.payment_voucher_no == _id.payment_voucher_no).select().first()
    _gen = db((db.General_Ledger.account_reference_no == _id.payment_voucher_no) & (db.General_Ledger.transaction_type == 23) & (db.General_Ledger.account_code == _id.account_code)).select().first()
    if not _gen:
        _ser.serial_number += 1
        _row.serial_number += 1
        _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account_code) + '/' + str(_row.serial_number)
        _trnx = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(1)).select().first()
        db.General_Ledger.insert(
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_reference_date,
            location = 99,
            transaction_type_ref = _id.account_voucher_transaction_code,
            transaction_date_entered = request.now, 
            department = 99,
            transaction_type = _id.account_voucher_transaction_type,
            type = _id.account_voucher_transaction_type,
            reference_no = str(_gl.transaction_prefix_text) + str(_id.account_reference),
            account_reference_no = _id.payment_voucher_no,
            account_code = _id.account_code,
            acct_code2 = _trnx.account_debit_code, # trnx first entry - account debit code
            description = str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_id.account_reference),
            entrydate = request.now,
            credit = _id.total_amount,
            debit = 0,
            amount_paid = 0,
            gl_entry_ref = _voucher_no_serial,
            batch_posting_seq = _seq,
            bank_code = _id.account_code,
            cheque_no = _id.cheque_no,
            cheque_bank_name = _id.bank_name_id.account_code
        )
        _row.update_record()
        _id.update_record(gl_entry_ref = _voucher_no_serial)
        _header.update_record(gl_entry_ref = _voucher_no_serial)
        for n in db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(1)).select():            
            _gl = db(db.General_Ledger.account_code == n.account_debit_code).select().first()            
            _row.serial_number +=1
            _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(n.account_debit_code) + '/' + str(_row.serial_number)
            # from transaction debit entry for paying party, customer, staff account, etc...
            _bank_code = 'None'
            if _id.bank_name_id:
                _bank_code = _id.bank_name_id.account_code
            db.General_Ledger.insert(
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_reference_date,
                transaction_type = _id.account_voucher_transaction_type,
                location = 99,
                transaction_type_ref = _id.account_voucher_transaction_code,
                transaction_date_entered = request.now,
                department = n.dept_code_id,
                type = _id.account_voucher_transaction_type,
                reference_no = str(_gl.transaction_prefix_text) + str(n.account_reference),
                account_reference_no = _id.payment_voucher_no,
                account_code = n.account_debit_code,
                acct_code2 = _id.account_code,
                description = n.description,
                credit = 0,
                debit = n.amount,
                amount_paid = 0,
                gl_entry_ref = _voucher_no_serial,
                batch_posting_seq = _seq,
                entrydate = request.now,
                bank_code = _id.account_code,
                cheque_no = _id.cheque_no,
                cheque_bank_name = _bank_code
            )
            _row.update_record()
            n.update_record(gl_entry_ref = _voucher_no_serial)
        for n in db(db.Payment_Voucher_Transaction.payment_voucher_header_id == _header.id).select():
            n.update_record(gl_entry_ref = _voucher_no_serial)                
        _ser.update_record()
        
        # ---------------- update master account balance current year ----------------
        # 1. search account code from general ledger !use for loops
        # 2. if found update closing balance per department and total closing balance.
        # 3. if not found add new account code and account name with the financial year then update closing balance per department and total closing balance.
        # 4. if debit entry +closing balance, if credit entry -closing balance as per department entry
        
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
    elif _gen: # if exist
        response.js = "alertify.error('PV already posted.')"
        
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_pv_confirmation_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Payment Req. #'),TD('Payment Vou. #'),TD('Account Code'),TD('Payee'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    _query = db(db.Payment_Voucher_Request.status_id == 14).select(orderby = db.Payment_Voucher_Request.id)
    for n in _query:
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if n.created_by == auth.user_id:
            appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_pv_confirmation','post_pv_confirmation_id',args = n.id, extension = False))
        if auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership('ROOT'):
            appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_pv_confirmation','post_pv_confirmation_id',args = n.id, extension = False))
        btn_lnk = DIV(appr_lnk)            
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.payment_voucher_request_no),
            TD(n.payment_voucher_no),
            TD(n.account_code),
            TD(n.payee),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_pv_confirmation_id():
    _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
    db.Payment_Voucher_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'PV-TASK3'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
    db.Payment_Voucher_Request.status_id.default = 14
    form = SQLFORM(db.Payment_Voucher_Request, request.args(0))
    return dict(form = form, _id = _id)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_pv_confirmation_transaction():        
    db.Payment_Voucher_Transaction_Request.ticket_no_id.default = _ticket_no_ref = session.ticket_no_id
    form = SQLFORM(db.Payment_Voucher_Transaction_Request)
    if form.process().accepted:
        if request.args(0):
            _pvr = db(db.Payment_Voucher_Request.id == int(request.args(0))).select().first()
            _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
            _total_amount = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _pvr.update_record(total_amount = _total_amount)
        response.js = "$('#PVTtbl').get(0).reload();"        
    elif form.errors:
        response.flash = 'error'
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount')),_class='bg-red')
    _query = db(db.Payment_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id).select()
    if request.args(0):
        _query = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('workflow_payment_voucher','delete_account_transaction_id',args = n.id, extension = False))
        if n.created_by != auth.user_id:
            dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(dele_lnk)
        _am = dc(dc.Master_Account.account_code == n.account_debit_code).select().first()
        _serial = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _total_amount += float(n.amount or 0)
        row.append(TR(
            TD(ctr),            
            TD(n.account_debit_code),
            TD(_am.account_name),
            TD(n.department_code),            
            TD(n.description),
            TD(locale.format('%.2F', n.amount or 0, grouping = True), _align='right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :')),_align='right',_class='bg-green color-palette'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True))), _align ='right',_class='bg-green color-palette')))
    table = TABLE([head, body, foot], _class='table',_id='PVTtbl')
    return dict(form = form, table = table)

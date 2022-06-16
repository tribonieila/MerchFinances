from datetime import datetime, date
import locale
import datetime
import random
import string
# import date
locale.setlocale(locale.LC_ALL, '')
_arr = []

def get_item_description():
    _ma = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()
    if _ma:
        session.account_credit_code = request.vars.account_credit_code
        return DIV(SPAN(I(_class='fas fa-info-circle'),_class='info-box-icon bg-aqua'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN(str(_ma.account_code) + ' - ' + str(_ma.account_name),_class='info-box-number'),_class='info-box-content'),_class='info-box')
    elif not _ma:
        return DIV(SPAN(I(_class='fas fa-times-circle'),_class='info-box-icon bg-red'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN('Not Found!',_class='info-box-number'),_class='info-box-content'),_class='info-box')

def put_batch_posting_sequence_id():
    # _id = db(db.Batch_Posting_Sequence.prefix_seq == request.args(0)).select().first()
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq
# -------------------   R E C E I P T  V O U C H E R   ----------------------
@auth.requires_login()
def get_receipt_voucher_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.transaction_prefix == 'RV1').select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Acct.Ref.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db((db.Receipt_Voucher_Request.created_by == auth.user_id) & (db.Receipt_Voucher_Request.status_id == 9)).select(orderby = db.Receipt_Voucher_Request.id):
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-plus'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('account_transaction','post_receipt_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_receipt_voucher_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_reference),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return dict(table = table)

@auth.requires_login()
def get_receipt_voucher_approval_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.transaction_prefix == 'RV1').select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Acct.Ref.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db(db.Receipt_Voucher_Request.status_id != 11).select():
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-check'), _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        if auth.has_membership('ROOT'):            
            work_lnk = A(I(_class='fas fa-user-check'),_title='Update/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_receipt_voucher','post_receipt_voucher',args = n.id, extension = False))
        elif n.created_by != auth.user_id:
            work_lnk = A(I(_class='fas fa-user-check'),_title='Update/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_receipt_voucher','post_receipt_voucher',args = n.id, extension = False))
        if n.status_id == 10:
            work_lnk = A(I(_class='fas fa-user-check'),_type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(work_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_reference),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.created_by.first_name[:1],'.',n.created_by.last_name,' ',SPAN(n.status_id.description,_class='text-muted')),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table', _id='tblConf')
    return dict(table = table)

def patch_receipt_voucher():
    if int(request.args(0)) == 1:        
        _account_code = _account_name = ''
        _ga = db(db.General_Account.id == 1).select().first()
        if int(request.vars.account_payment_mode_id or 0) == 1 or (int(request.vars.account_payment_mode_id or 0) == 2):
            _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RV1').select().first()
            _account_code = _ga.receipt_voucher_account
            _voucher_type = _voucher_type.voucher_serial_no + 1
            _account_name = 'CASH-IN-HAND'
        elif (int(request.vars.account_payment_mode_id or 0) == 3):            
            _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RV2').select().first()
            _account_code = _ga.pdc_receipt_voucher_account
            _voucher_type = _voucher_type.voucher_serial_no + 1
            _account_name = 'BILLS RECIEVABLE (PDC)'
        response.js = "$('#Receipt_Voucher_Request_voucher_no').val('%s');$('#Receipt_Voucher_Request_account_code').val('%s');$('#account_name').val('%s');" % (_voucher_type, _account_code, _account_name)
    elif int(request.args(0)) == 2:
        _id = db(db.Receipt_Voucher_Request.id == request.args(1)).select().first()
        _id.update_record(status_id = 2)
        redirect(URL('workflow_receipt_voucher','get_receipt_voucher_grid'))
    elif int(request.args(0)) == 3:        
        _trnx = db(db.Transaction_Payment_Type.id == request.vars.transaction_payment_type_id).select().first()
        if int(request.vars.transaction_payment_type_id or 0) == 2:
            ctr = 0
            row = []
            head = THEAD(TR(TH('#'),TH('Acct.Code'),TH('A.Reff.'),TH('Dept.'),TH('Loc.'),TH('Type'),TH('Debit'),TH('Credit'),TD('Amount Paid'),TD('Paid'),TH()),_class='bg-red')
            for n in db((db.General_Ledger.account_code == request.vars.account_credit_code) & (db.General_Ledger.debit > 0) & (db.General_Ledger.debit != db.General_Ledger.amount_paid)).select():
                ctr += 1
                _balance = n.debit - n.amount_paid
                row.append(TR(
                    TD(ctr),
                    TD(n.account_code),
                    TD(n.account_reference_no),
                    TD(n.department),
                    TD(n.location),
                    TD(n.transaction_type),
                    TD(locale.format('%.2F',n.debit or 0, grouping = True)),
                    TD(locale.format('%.2F',n.credit or 0, grouping = True)),                    
                    TD(locale.format('%.2F',n.amount_paid or 0, grouping = True)),                    
                    TD(n.paid),
                    TD(BUTTON('Select',_class='btn btn-block btn-success btn-flat btn-xs', _id='BtnSelect',_name='BtnSelect',_onclick="ajax('%s')" % URL('workflow_receipt_voucher','patch_general_ledger_id', args = n.id)))
                ))
            body = TBODY(*row)
            table = TABLE(*[head,body],_class='table rvtbl')      
            response.js = " alertify.alert().setHeader('General Ledger'); alertify.alert('%s').set('resizable',true).resizeTo(940,500); " % XML(table)      
            # response.js = "alertify.confirm('%s', function(){ alertify.success('Ok') }, function(){ $('#Receipt_Voucher_Transaction_Request_description').val(''); $('#Receipt_Voucher_Transaction_Request_amount_paid').val(''); alertify.error('Cancel')}).set('resizable',true);" % XML(table, sanitize = True)

def get_general_ledger_id():    
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Acct.Code'),TH('A.Reff.'),TH('Dept.'),TH('Loc.'),TH('Type'),TH('Debit'),TH('Credit'),TH('Ref.'),TH()),_class='bg-red')
    for n in db((db.General_Ledger.account_code == session.account_credit_code)).select():
        ctr += 1
        _balance = n.debit - n.amount_paid
        row.append(TR(
            TD(ctr),
            TD(n.account_code),
            TD(n.account_reference_no),
            TD(n.department),
            TD(n.location),
            TD(n.transaction_type),
            TD(locale.format('%.3F',n.debit or 0, grouping = True)),
            TD(locale.format('%.3F',n.credit or 0, grouping = True)),
            TD(n.gl_entry_ref),           
            TD(BUTTON('Select',_class='btn btn-block btn-success btn-flat btn-xs', _id='BtnSelect',_name='BtnSelect',_onclick="ajax('%s')" % URL('sili','patch_testing_id', args = n.id)))
        ))
    body = TBODY(*row)    
    table = TABLE(*[head,body],_class='table table-striped table-hover responsive',_id='example')    
    return dict(table = table)    

def put_general_ledger_session():
    session.account_credit_code = request.vars.account_credit_code
    print('se:'), session.account_credit_code

def patch_general_ledger_id():
    _balance = 0
    _gl = db(db.General_Ledger.id == request.args(0)).select().first()    
    _balance = _gl.debit - _gl.amount_paid
    response.js = "alertify.success('AGAINST INV%s SELECTED.');$('#Receipt_Voucher_Transaction_Request_description').val('AGAINST INV%s'); $('#Receipt_Voucher_Transaction_Request_amount_paid').val('%s');$('#gl_id').val('%s');" % (_gl.account_reference_no,_gl.account_reference_no,locale.format('%.2F',_balance or 0),_gl.id)
    # if _gl.prepared == True:
    #     response.js = "alertify.notify('already prepared.','error')"
    
# @auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def check_membership():
    if not auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'):
        redirect(URL('default','forbidden'))

def validate_post_receipt_voucher(form):    
    _voucher_no = 0
   
    if not request.args(0):                    
        if request.vars.account_payment_mode_id == '':
            form.errors.account_payment_mode_id = 'Value not in database'
            return
        elif int(request.vars.account_payment_mode_id) == 1 or int(request.vars.account_payment_mode_id) == 2:
            _vn = db(db.Account_Voucher_Type.transaction_prefix == 'RV1').select().first()
            _voucher_no = _vn.voucher_serial_no + 1
            _vn.voucher_serial_no += 1            
            _vn.update_record()
        elif int(request.vars.account_payment_mode_id) == 3:
            _vn = db(db.Account_Voucher_Type.transaction_prefix == 'RV2').select().first()
            _voucher_no = _vn.voucher_serial_no + 1        
            _vn.voucher_serial_no += 1            
            _vn.update_record()
        form.vars.status_id = 9
        form.vars.ticket_no_id = request.vars.ticket_no_id
        form.vars.voucher_no = _voucher_no
        form.vars.account_voucher_transaction_type = _vn.account_voucher_transaction_type
        form.vars.account_voucher_transaction_code = _vn.account_voucher_transaction_code

        _trnx = db(db.Receipt_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).count()
        if int(_trnx) <= 0:
            form.errors.voucher_no = 'Transaction is empty'
            
            return 

    elif request.args(0):
        _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()        
        form.vars.ticket_no_id = _id.ticket_no_id        
        form.vars.account_voucher_transaction_type = _id.account_voucher_transaction_type
        form.vars.account_voucher_transaction_code = _id.account_voucher_transaction_code

        _trnx = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).count()
        if int(_trnx) <= 0:
            form.errors.status_id = 'Transaction is empty'
            return 
    _cheque_date = request.vars.cheque_dated
    if int(request.vars.account_payment_mode_id) == 1:
        _cheque_date = ''

    form.vars.received_from = request.vars.received_from.upper()
    form.vars.collected_by = request.vars.collected_by.upper()
    form.vars.manual_rv_no = request.vars.manual_rv_no
    form.vars.remarks = request.vars.remarks.upper()
    form.vars.transaction_reference_date = request.vars.transaction_reference_date
    form.vars.cheque_dated = _cheque_date

# @auth.requires(check_membership)
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_receipt_voucher(): 
    _total_amount = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    db.Receipt_Voucher_Request.voucher_no.default = 0 #_vn.rv_cash_cashcheque + 1
    db.Receipt_Voucher_Request.status_id.default = 9
    db.Receipt_Voucher_Request.account_payment_mode_id.requires= IS_EMPTY_OR(IS_IN_DB(db(db.Account_Voucher_Payment_Mode.id != 4),db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))
    _id = 0
    if request.args(0):        
        _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()
        db.Receipt_Voucher_Request.voucher_no.default = _id.voucher_no
        if _id.status_id == 10:
            db.Receipt_Voucher_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.id == 10), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
            db.Receipt_Voucher_Request.status_id.default = _id.status_id
    form = SQLFORM(db.Receipt_Voucher_Request, request.args(0))    
    if form.process(onvalidation = validate_post_receipt_voucher).accepted:
        response.flash = 'RECORD SAVE'
        if not request.args(0):            
            _id = db(db.Receipt_Voucher_Request.created_by == auth.user_id).select().last()
            _account_ref = str(_id.account_voucher_transaction_code) + str(_id.voucher_no)
            for n in db(db.Receipt_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select():
                _invoice = ''
                if n.transaction_payment_type_id == 2:
                    _gl = db(db.General_Ledger.id == n.gl_id).select().first()
                    _invoice = _gl.account_reference_no
                n.update_record(receipt_voucher_request_id = _id.id, voucher_no = _id.voucher_no, account_reference = _account_ref, account_code = _id.account_code, invoice_no = _invoice)
            _total_amount = db.Receipt_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Receipt_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select(_total_amount).first()[_total_amount]            
            _id.update_record(total_amount = _total_amount, account_reference = _account_ref)
        elif request.args(0):            
            _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()
            _account_ref = str(_id.account_voucher_transaction_code) + str(_id.voucher_no)
            for n in db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select():
                _invoice = ''
                if n.transaction_payment_type_id == 2:
                    _gl = db(db.General_Ledger.id == n.gl_id).select().first()
                    _invoice = _gl.account_reference_no
                n.update_record(receipt_voucher_request_id = _id.id, voucher_no = _id.voucher_no, account_reference = _account_ref, account_code = _id.account_code,invoice_no = _invoice)            
            _total_amount = db.Receipt_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _id.update_record(total_amount = _total_amount, account_reference = _account_ref)            
        redirect(URL('workflow_receipt_voucher','get_receipt_voucher_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
    return dict(form = form, ticket_no_id = ticket_no_id, _id = _id)

def validate_post_receipt_voucher_transaction(form):        
    _id = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()
    if not _id:
        form.errors.account_credit_code = 'Account code not found.'
        response.js = "alertify.error('Account code not found.')"    
    elif request.vars.account_credit_code == '' or request.vars.account_credit_code == None:
        form.errors.account_credit_code = 'Account credit code is empty.'
        response.js = "alertify.error('Account credit code is empty.')"
    elif _id:
        _vou = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _dep = db(db.General_Department_Cost_Center.id == request.vars.dept_code_id).select().first()
        _location = 99
        _department = 99
        if int(request.vars.transaction_payment_type_id) == 2: # against invoice selected.
            _gl = db(db.General_Ledger.id == request.vars.gl_id).select().first()        
            _department = request.vars.dept_code_id
            if not _gl:
                form.errors.description = 'Account credit code is empty or already exist.'
                response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Account credit code is empty or already exist.')"             
            elif db((db.Receipt_Voucher_Transaction_Request.account_credit_code == request.vars.account_credit_code) & (db.Receipt_Voucher_Transaction_Request.gl_id == request.vars.gl_id) & (db.Receipt_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id)).select().first(): 
                form.errors.account_credit_code = 'Same entry already exist.'
                response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Same entry already exist.')"             
            elif round(_gl.debit,2) < float(request.vars.amount_paid or 0):
                form.errors.amount_paid = "Entered amount should not exceed the total amount of invoice."
                response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Entered amount should not exceed the total amount of invoice.')"             
            else:
                _location = _gl.location
        # on account
        elif int(request.vars.transaction_payment_type_id) == 1: # on account
            if db((db.Receipt_Voucher_Transaction_Request.account_credit_code == request.vars.account_credit_code) & (db.Receipt_Voucher_Transaction_Request.transaction_payment_type_id == request.vars.transaction_payment_type_id) & (db.Receipt_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id)).select().first(): 
                form.errors.account_credit_code = 'Same entry already exist.'
                response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Same entry already exist.')"             
            _department = request.vars.dept_code_id
        if request.args(0):
            if int(request.vars.transaction_payment_type_id) == 1:
                if db((db.Receipt_Voucher_Transaction_Request.account_credit_code == request.vars.account_credit_code) & (db.Receipt_Voucher_Transaction_Request.transaction_payment_type_id == request.vars.transaction_payment_type_id) & (db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0))).select().first(): 
                    form.errors.account_credit_code = 'Same entry already exist.'
                    response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Same entry already exist.')"             
            elif int(request.vars.transaction_payment_type_id) == 2:
                _gl = db(db.General_Ledger.id == request.vars.gl_id).select().first()        
                _department = request.vars.dept_code_id                
                if not _gl:
                    form.errors.description = 'Account credit code is empty or already exist.'
                    response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Account credit code is empty or already exist.')"             
                elif db((db.Receipt_Voucher_Transaction_Request.account_credit_code == request.vars.account_credit_code) & (db.Receipt_Voucher_Transaction_Request.gl_id == request.vars.gl_id) & (db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0))).select().first(): 
                    form.errors.account_credit_code = 'Same entry already exist.'
                    response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Same entry already exist.')"             
                elif round(_gl.debit,2) < float(request.vars.amount_paid or 0):
                    form.errors.amount_paid = "Entered amount should not exceed the total amount of invoice."
                    response.js = "$('#BtnGenLed').prop('disabled', false);alertify.error('Entered amount should not exceed the total amount of invoice.')"             
                else:
                    _location = _gl.location

            _av = db(db.Receipt_Voucher_Request.id == int(request.args(0))).select().first()
            _trnx = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select().first()                                
            form.vars.ticket_no_id = _av.ticket_no_id
            form.vars.receipt_voucher_request_id = int(request.args(0))

        form.vars.account_voucher_transaction_type = _vou.account_voucher_transaction_type
        form.vars.account_voucher_transaction_code = _vou.account_voucher_transaction_code
        form.vars.department_code = _dep.department_code        
        form.vars.department = _department
        form.vars.location = _location
        form.vars.amount_paid = request.vars.amount_paid.replace(',','')       
            
@auth.requires_login()
def post_receipt_voucher_transaction():
    db.Receipt_Voucher_Transaction_Request.ticket_no_id.default = session.ticket_no_id
    _ticket_no_ref = session.ticket_no_id
    db.Receipt_Voucher_Transaction_Request.dept_code_id.default = 3
    form = SQLFORM(db.Receipt_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_post_receipt_voucher_transaction).accepted:
        if request.args(0):
            _av = db(db.Receipt_Voucher_Request.id == int(request.args(0))).select().first()
            _total_amount = db.Receipt_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _av.update_record(total_amount = _total_amount)
        response.js = "$('#AVTtbl').get(0).reload();"
    elif form.errors:
        response.flash = None
        response.js = "alertify.error('%s')" %(form.errors)
    ctr = _total_amount = 0
    row = []    
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
    _query = db(db.Receipt_Voucher_Transaction_Request.ticket_no_id == _ticket_no_ref).select()    
    if request.args(0):
        _query = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('workflow_receipt_voucher','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        _am = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        _serial = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _total_amount += float(n.amount_paid or 0)
        row.append(TR(
            TD(ctr),            
            TD(n.account_credit_code),
            TD(_am.account_name),
            TD(n.department_code),            
            TD(n.description),
            TD(locale.format('%.2F', n.amount_paid or 0, grouping = True), _align='right'),
            TD(btn_lnk),
        ))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :')),_align='right',_class='bg-green color-palette'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True))), _align ='right',_class='bg-green color-palette'),TD(_class='bg-green color-palette')
    ))
    table = TABLE([head, body, foot], _class='table',_id='AVTtbl')
    return dict(form = form, table = table)

def delete_account_transaction_id():
    response.js = "alertify.confirm('Account Voucher Receipt', 'Are you sure you want to delete?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('workflow_receipt_voucher','delete_transaction_id',args = request.args(0))

def delete_transaction_id():
    _trnx = db(db.Receipt_Voucher_Transaction_Request.id == request.args(0)).select().first()            
    if _trnx.receipt_voucher_request_id:
        if db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == _trnx.receipt_voucher_request_id).count() == 1:
            response.js = "alertify.notify('Empty transactions not allowed.','warning')"            
        elif db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == _trnx.receipt_voucher_request_id).count() > 1:
            _trnx.delete_record()
            _total_amount = 0  
            _head = db(db.Receipt_Voucher_Request.id == _trnx.receipt_voucher_request_id).select().first()
            _total_amount = db.Receipt_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == _trnx.receipt_voucher_request_id).select(_total_amount).first()[_total_amount]    
            _head.update_record(total_amount = _total_amount)    
            response.js = "$('#AVTtbl').get(0).reload();alertify.error('Record Deleted.');"
    elif not _trnx.receipt_voucher_request_id:
        _trnx.delete_record()
        response.js = "$('#AVTtbl').get(0).reload();alertify.error('Record Deleted.');"
                
def get_receipt_voucher_confirmation_id():    
    _id = db(db.Receipt_Voucher_Request.id == request.args(0)).select().first()
    table = TABLE(
        TR(TD('Date'),TD('Receipt No'),TD('Payment Mode'),TD('Account Code'),TD('Bank Name'),TD('Cheque No.'),TD('Cheque Dated')),
        TR(
            TD(_id.transaction_reference_date),
            TD(_id.voucher_no),
            TD(_id.account_payment_mode_id.account_voucher_payment_code, ' - ',_id.account_payment_mode_id.account_voucher_payment_name),
            TD(_id.account_code),
            TD(_id.bank_name_id),
            TD(_id.cheque_no),
            TD(_id.cheque_dated),
            ),
        _class='table table-condensed table-bordered')
    table += TABLE(
        TR(TD('Purpose'),TD('Received From'),TD('Cost Center'),TD('Location Cost Center'),TD('Remarks'),TD('Status')),
        TR(
            TD(_id.purpose),
            TD(_id.received_from),
            TD(_id.cost_center),
            TD(_id.location_cost_center),
            TD(_id.remarks),
            TD(_id.status_id.description),
        ),
    _class='table table-condensed table-bordered')

    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Code'),TD('Name'),TD('Dept'),TD('Type'),TD('Ref.No.'),TD('Description'),TD('Total Amount')))
    for n in db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(0)).select():
        ctr += 1
        _ma = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        _total_amount += n.amount_paid
        row.append(TR(
            TD(ctr),
            TD(n.account_credit_code),
            TD(_ma.account_name),
            TD(n.dept_code_id.department_code, ' - ', n.dept_code_id.department_name),
            TD(n.account_voucher_transaction_type),
            TD(n.account_reference),
            TD(n.description),
            TD(locale.format('%.3F', n.amount_paid or 0, grouping = True),_align='right'),
        ))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_align='right'),TD(locale.format('%.3F', _total_amount or 0, grouping = True),_align='right')
    ))
    table += TABLE(*[head, body, foot], _class='table table-condensed table-bordered')

    table += TABLE(TR(
        TD(BUTTON('Reject', _class='btn btn-block btn-danger btn-flat',_onclick="ajax('%s')" % URL('account_transaction','patch_receipt_voucher_confirmation_id',args = [1,_id.id]))),
        TD(BUTTON('Approved', _class='btn btn-block btn-success btn-flat',_onclick="ajax('%s')" % URL('account_transaction','patch_receipt_voucher_confirmation_id',args = [2,_id.id])))
    ),_class='table table-condensed')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Receipt Voucher Request','message':'%s'}).show();" %(XML(table, sanitize = True))   

def patch_receipt_voucher_approval_id():
    if int(request.args(0)) == 1: # reject
        _id = db(db.Receipt_Voucher_Request.id == request.args(1)).select().first()
        if _id.status_id == 1:
            response.js = "alertify.alert('Receipt Voucher', 'Receipt Voucher already rejected!', function(){ alertify.success('Ok'); });"
        else:
            _id.update_record(status_id = 1)
            response.js = "alertify.alert().close();$('#tblConf').get(0).reload();alertify.error('Rejected!');"
    elif int(request.args(0)) == 2: # approved
        _id = db(db.Receipt_Voucher_Request.id == request.args(1)).select().first()
        if _id.status_id == 10:
            response.js = "alertify.alert('Receipt Voucher', 'Receipt Voucher already approved!', function(){ alertify.success('Ok'); });"
        else:
            _id.update_record(status_id = 10)
            sync_posting_confirmation()
            response.js = "alertify.success('Approved!');alertify.alert().close();window.location.replace('%s');" % URL('workflow_receipt_voucher','get_receipt_voucher_grid')

def sync_posting_confirmation(): # change to rv approval
    _id = db(db.Receipt_Voucher_Request.id == request.args(1)).select().first()
    db.Receipt_Voucher_Header.insert(
        voucher_no = _id.voucher_no,
        transaction_reference_date = _id.transaction_reference_date,
        account_voucher_transaction_type = _id.account_voucher_transaction_type,
        account_voucher_transaction_code = _id.account_voucher_transaction_code,
        account_payment_mode_id = _id.account_payment_mode_id,
        account_voucher_payment_code = _id.account_voucher_payment_code,
        account_reference = _id.account_reference,
        total_amount = _id.total_amount,
        account_code = _id.account_code,
        bank_name_id = _id.bank_name_id,
        cheque_no = _id.cheque_no,
        cheque_dated = _id.cheque_dated,
        purpose = _id.purpose,
        received_from = _id.received_from,
        collected_by = _id.collected_by,
        entry_date = _id.entry_date,
        cost_center = _id.cost_center,
        location_cost_center = _id.location_cost_center,
        gl_entry_ref = _id.gl_entry_ref,
        status_id = _id.status_id,
        posting_ref_no = _id.posting_ref_no,
        manual_rv_no = _id.manual_rv_no,
        remarks = _id.remarks,
        requested_on = _id.requested_on,
        requested_by = _id.requested_by)
    _head = db(db.Receipt_Voucher_Header.voucher_no == _id.voucher_no).select().first()
    for n in db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(1)).select():
        db.Receipt_Voucher_Transaction.insert(
            receipt_voucher_header_id = _head.id,
            account_voucher_transaction_type = n.account_voucher_transaction_type,
            account_voucher_transaction_code = n.account_voucher_transaction_code,
            account_code = n.account_code,
            account_reference = n.account_reference,
            account_credit_code = n.account_credit_code,
            account_debit_code = n.account_debit_code,
            dept_code_id = n.dept_code_id,
            department_code = n.department_code,
            location_cost_center_id = n.location_cost_center_id,
            location_code = n.location_code,
            transaction_payment_type_id = n.transaction_payment_type_id,
            amount_paid = n.amount_paid,
            description = n.description,
            voucher_no = n.voucher_no,
            gl_entry_ref = n.gl_entry_ref,
            department = n.department, 
            invoice_no = n.invoice_no,
            location = n.location)
    
    # --------------- POSTING ON GEN. LEDGER ---------------
    import datetime
    _seq = put_batch_posting_sequence_id()    
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first() 
    _ga = db(db.General_Account.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 21).select().first()
    _gen = db((db.General_Ledger.account_reference_no == _id.voucher_no) & (db.General_Ledger.transaction_type == 21) & (db.General_Ledger.account_code == _id.account_code)).select().first()
    if not _gen: 
        # gl entry for 02-20 and 08-02 account
        # cash in hand and pdc bills receivable (pdc)
        _ser.serial_number += 1
        _row.serial_number += 1
        _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account_code) + '/' + str(_row.serial_number)        
        db.General_Ledger.insert(
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_reference_date,
            transaction_type = _id.account_voucher_transaction_type,
            location = 99, # general
            transaction_type_ref = _id.account_voucher_transaction_code,
            transaction_date_entered = request.now,
            department = 99, # general
            type = _id.account_voucher_transaction_type,
            reference_no = _id.account_reference,
            account_reference_no = _id.voucher_no,
            account_code = _id.account_code,
            description = str(_gl.common_text) + ' ' + str(_id.account_reference),
            entrydate = request.now,
            credit = 0,
            debit = _id.total_amount,
            amount_paid = 0,
            gl_entry_ref = _voucher_no_serial,
            batch_posting_seq = _seq,
            bank_code = _id.account_code
        )
        _row.update_record()
        
        # gl entry for 02-20 and 08-02 account end

        # transaction gl entries AND UPDATION OF AMOUNT PAID for any account code ------
        # 
        for n in db(db.Receipt_Voucher_Transaction_Request.receipt_voucher_request_id == request.args(1)).select():
            _gl = db((db.General_Ledger.id == n.gl_id) & (db.General_Ledger.account_reference_no == n.invoice_no) & (db.General_Ledger.account_code == n.account_credit_code)).select().first()
            if _gl: # if against invoice
                _paid = False
                _cheque_no = 'None'
                _bank_name = 'None'
                _payment_reference = 'None'
                
                if int(_id.account_payment_mode_id) == 3:    # if account payment mode == PDC           
                    _cheque_no = _id.cheque_no
                    _bank_name = _id.bank_name_id.bank_code
                    _payment_reference = _id.account_reference
                    if _gl.cheque_no:
                        _cheque_no = str(_gl.cheque_no) + ' | ' + str(_id.cheque_no)
                        _bank_name = str(_gl.cheque_bank_name) +  ' | ' + str(_id.bank_name_id.bank_code)
                        _payment_reference = str(_gl._payment_reference) + ' | ' + str(_id.account_reference)
                elif int(_id.account_payment_mode_id) == 2: # for cash cheque
                    _cheque_no = _id.cheque_no
                    _bank_name = _id.bank_name_id.bank_code                    
                    if _gl.cheque_no:
                        _cheque_no = str(_gl.cheque_no) + ' | ' + str(_id.cheque_no)
                        _bank_name = str(_gl.cheque_bank_name) + ' | ' + str(_id.bank_name_id.bank_code)
                        _payment_reference = str(_gl._payment_reference) + ' | ' + str(_id.account_reference)
                    else:
                        _payment_reference = str(_id.account_reference)
                if round(_gl.debit,2) == round(n.amount_paid,2):
                    _paid = True
                _gl.amount_paid = float(_gl.amount_paid or 0) + float(n.amount_paid or 0)
                _gl.cheque_no = _cheque_no
                _gl.cheque_bank_name = _bank_name
                _gl.rv_payment_reference = _payment_reference
                _gl.paid = _paid # to check if debit amount is less than to amount paid
                _gl.update_record()
                
            _row.serial_number += 1       
            _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(n.account_credit_code) + '/' + str(_row.serial_number)
            # from transaction credit entry for paying party, customer, staff account, etc...
            _bank_code = 'None'
            if _id.bank_name_id:
                _bank_code = _id.bank_name_id.bank_code
            db.General_Ledger.insert(
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_reference_date,
                transaction_type = _id.account_voucher_transaction_type,
                location = n.location,
                transaction_type_ref = _id.account_voucher_transaction_code,
                transaction_date_entered = request.now,
                department = n.department,
                type = _id.account_voucher_transaction_type,
                reference_no = n.account_reference,
                account_reference_no = n.voucher_no,
                account_code = n.account_credit_code,
                description = n.description,
                credit = n.amount_paid,
                debit = 0,
                amount_paid = 0,
                gl_entry_ref = _voucher_no_serial,
                batch_posting_seq = _seq,
                entrydate = request.now,
                bank_code = _id.account_code,
                cheque_no = _id.cheque_no,
                cheque_bank_name = _bank_code
            )
            _row.update_record()
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

    elif _gen:
        response.js = "alertify.error('RV Already posted.')"

            # if n.transaction_payment_type_id == 2: # if against invoice
            # search on gl then update amount paid += n.amount_paid
            # _gen = db((db.General_Ledger.account_reference_no == n.account_reference) & (db.General_Ledger.transaction_type == 21) & location & department & (db.General_Ledger.account_code == _id.account_code)).select().first()
            # then validate
            # if _gl.debit - n.amount_paid == 0:
            # status = true

            # if on account :
            # credit = n.amount_paid
            # department = n.department
            # location  = n.locaiton
            # amount_paid = 0
            # status = False
            # else if against invoice:
            # insert below
            # update 


    # --------------- POSTING ON GEN. LEDGER ---------------

# ----------------------------------------------------------------------------
# --------------------   R E C E I P T  V O U C H E R  ----------------------
# -------------------------------- E N D -------------------------------------

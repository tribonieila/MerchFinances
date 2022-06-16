from datetime import datetime, date
import locale
import datetime
import random
import string
locale.setlocale(locale.LC_ALL, '')
x = datetime.datetime.now()

def get_item_description():
    _ma = dc(dc.Master_Account.account_code == request.vars.account_debit_code).select().first()
    if _ma:
        session.account_debit_code = request.vars.account_debit_code
        return DIV(SPAN(I(_class='fas fa-info-circle'),_class='info-box-icon bg-aqua'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN(str(_ma.account_code) + ' - ' + str(_ma.account_name),_class='info-box-number'),_class='info-box-content'),_class='info-box')
    elif not _ma:
        return DIV(SPAN(I(_class='fas fa-times-circle'),_class='info-box-icon bg-red'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN('Not Found!',_class='info-box-number'),_class='info-box-content'),_class='info-box')

def patch_general_ledger_id():
    _balance = 0
    _gl = db(db.General_Ledger.id == request.args(0)).select().first()
    _balance = _gl.debit - _gl.amount_paid
    response.js = "alertify.success('AGAINST INV%s SELECTED.');$('#Payment_Voucher_Transaction_Request_description').val('AGAINST INV%s'); $('#Payment_Voucher_Transaction_Request_amount').val('%s');$('#gl_id').val('%s');" % (_gl.account_reference_no,_gl.account_reference_no,locale.format('%.2F',_balance or 0),_gl.id)

def patch_payment_voucher_id():
    _account_code = _account_name = ''
    _ga = db(db.General_Account.id == 1).select().first()
    if int(request.args(0)) == 1: # from merch bank master table
        _bm = db(db.Merch_Bank_Master.id == request.vars.bank_name_id).select().first()
        response.js = "$('#Payment_Voucher_Request_account_code').val('%s');$('#account_name').val('%s');" % (_bm.account_code, _bm.bank_name)
    elif int(request.args(0)) == 2: #    
        if int(request.vars.transaction_payment_type_id or 0) == 2:
            ctr = 0
            row = []
            head = THEAD(TR(TD('#'),TD('Acct.Code'),TD('A.Reff.'),TD('Dept.'),TD('Loc.'),TD('Type'),TD('Debit'),TD('Credit'),TD('Amount Paid'),TD('Paid'),TD()),_class='bg-red')
            for n in db((db.General_Ledger.account_code == request.vars.account_debit_code) & (db.General_Ledger.debit > 0) & (db.General_Ledger.debit != db.General_Ledger.amount_paid)).select():
                ctr += 1
                _balance = n.debit - n.amount_paid
                row.append(TR(
                    TD(ctr),
                    TD(n.account_code),
                    TD(n.account_reference_no),
                    TD(n.department),
                    TD(n.location),
                    TD(n.transaction_type),
                    TD(locale.format('%.2F',n.debit or 0, grouping = True),_align='right'),
                    TD(locale.format('%.2F',n.credit or 0, grouping = True),_align='right'),
                    TD(locale.format('%.2F',n.amount_paid or 0, grouping = True),_align='right'),                    
                    TD(n.paid),
                    TD(BUTTON('Select',_class='btn btn-block btn-success btn-flat btn-xs', _id='BtnSelect',_name='BtnSelect',_onclick="ajax('%s')" % URL('workflow_payment_voucher','patch_general_ledger_id', args = n.id)))
                ))
            body = TBODY(*row)
            table = TABLE(*[head,body],_class='table table-condensed table-hover')
            response.js = " alertify.alert().setHeader('General Ledger'); alertify.alert('%s').set('resizable',true).resizeTo(940,500); " % XML(table)

    elif int(request.args(0)) == 3: # submit button != request.args(0)
        _trnx = db(db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).count()
        if _trnx <= 0:
            response.js = "alertify.alert('Payment Voucher', 'Payment Voucher Transaction is empty!');"
            return 
        _account_code = db(db.Merch_Bank_Master.id == request.vars.bank_name_id).select().first()
        _inv = db(db.Payment_Voucher_Request.custom_invoice_no == request.vars.custom_invoice_no.upper()).select().first()
        if _inv:
            response.js = "alertify.alert('Custom Invoice No','Already exist!');"
            return
        db.Payment_Voucher_Request.insert(
            ticket_no_id = request.vars.ticket_no_id,
            payment_voucher_request_no = request.vars.payment_voucher_request_no,
            transaction_reference_date = request.vars.transaction_reference_date,
            account_payment_mode_id = request.vars.account_payment_mode_id,
            payee = request.vars.payee.upper(),
            bank_name_id = request.vars.bank_name_id,
            account_code = _account_code.account_code,
            cheque_no = request.vars.cheque_no.upper(),
            cheque_dated = request.vars.cheque_dated,
            custom_invoice_no = request.vars.custom_invoice_no.upper(),
            custom_declaration_no = request.vars.custom_declaration_no.upper(),
            manual_pv_no = request.vars.manual_pv_no.upper(),
            status_id = request.vars.status_id,
            remarks = request.vars.remarks.upper()
        )
        _id = db(db.Payment_Voucher_Request.ticket_no_id == request.vars.ticket_no_id).select().first()
        _total_amount = 0
        for n in db(db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select():
            n.update_record(payment_voucher_request_id = _id.id)
        _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
        _total_amount = db(db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select(_total_amount).first()[_total_amount]
        _id.update_record(total_amount = _total_amount)
        response.js = "alertify.success('Success!');window.location.href = '%s'" % URL('workflow_payment_voucher','get_payment_voucher_grid')
    
    elif int(request.args(0)) == 4: # accounts manager or root/admin approval/reject
        _id = db(db.Payment_Voucher_Request.id == request.args(1)).select().first()
        if _id.status_id == 1 or _id.status_id == 13:
            response.js = "alertify.notify('ALREADY %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 13:
            if int(request.args(2)) == 1:            
                _id.update_record(status_id = 13)                                
                sync_payment_voucher_header()
                response.js = "alertify.success('Approved!');window.location.href = '%s'" % URL('workflow_payment_voucher','get_payment_voucher_grid')
            elif int(request.args(2)) == 2:
                _id.update_record(status_id = 1)
                response.js = "alertify.warning('Rejected!');window.location.href = '%s'" % URL('workflow_payment_voucher','get_payment_voucher_grid')
    elif int(request.args(0)) == 5: # management or root/admin approval/reject
        _id = db(db.Payment_Voucher_Request.id == request.args(1)).select().first()
        if _id.status_id == 1 or _id.status_id == 14:
            response.js = "alertify.notify('ALREADY %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 14:
            if int(request.args(2)) == 1:            
                _vou = db(db.Payment_Voucher_Header.payment_voucher_no == _id.payment_voucher_no).select().first()
                _vou.update_record(status_id = 14)
                _id.update_record(status_id = 14)                        
                response.js = "alertify.warning('Approved!');window.location.href = '%s'" % URL('workflow_payment_voucher','get_payment_voucher_grid')
            elif int(request.args(2)) == 2:
                _id.update_record(status_id = 1)                                
                response.js = "alertify.warning('Rejected!');window.location.href = '%s'" % URL('workflow_payment_voucher','get_payment_voucher_grid')
    elif int(request.args(0)) == 6: # custom invoice no validation
        _req = db(db.Payment_Voucher_Request.custom_invoice_no == request.vars.custom_invoice_no).select().first()
        _pay = db(db.Payment_Voucher_Header.custom_invoice_no == request.vars.custom_invoice_no).select().first()
        if _req or _pay:
            response.js = "$('#Payment_Voucher_Request_custom_invoice_no').val('');alertify.warning('Custom Invoice No. Already Exist!')"

def put_batch_posting_sequence_id():
    # _id = db(db.Batch_Posting_Sequence.prefix_seq == request.args(0)).select().first()
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq

def sync_payment_voucher_header():    
    _id = db(db.Payment_Voucher_Request.id == request.args(1)).select().first()
    if int(_id.account_payment_mode_id) == 2: # cash cheque
        _vn = db(db.Account_Voucher_Type.transaction_prefix == 'PV1').select().first()
        _voucher_no = _vn.voucher_serial_no + 1
        _vn.voucher_serial_no += 1
        _vn.update_record()
    elif int(_id.account_payment_mode_id) == 3: # post dated cheque
        _vn = db(db.Account_Voucher_Type.transaction_prefix == 'PV2').select().first()
        _voucher_no = _vn.voucher_serial_no + 1
        _vn.voucher_serial_no += 1
        _vn.update_record()
    _id.update_record(payment_voucher_no = _voucher_no,payment_voucher_date = _id.transaction_reference_date, status_id = 13,account_reference = _voucher_no)
    db.Payment_Voucher_Header.insert(
        payment_voucher_no = _voucher_no,
        payment_voucher_date = _id.transaction_reference_date,
        payment_voucher_request_no = _id.payment_voucher_request_no,
        account_reference = _voucher_no,
        payee = _id.payee,
        custom_declaration_no = _id.custom_declaration_no,
        custom_invoice_no = _id.custom_invoice_no,
        transaction_reference_date = _id.transaction_reference_date,
        account_voucher_transaction_type = _id.account_voucher_transaction_type,
        account_voucher_transaction_code = _id.account_voucher_transaction_code,
        account_payment_mode_id = _id.account_payment_mode_id,
        total_amount = _id.total_amount,
        account_code = _id.account_code,
        bank_name_id = _id.bank_name_id,
        cheque_no = _id.cheque_no,
        cheque_dated = _id.cheque_dated,
        entry_date = _id.entry_date,
        status_id = _id.status_id,
        remarks = _id.remarks,
        manual_pv_no = _id.manual_pv_no,
        requested_on = _id.requested_on,
        requested_by = _id.requested_by)
    _header = db(db.Payment_Voucher_Header.payment_voucher_no == _voucher_no).select().first()
    
    for n in db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(1)).select():
        n.update_record(account_code = _id.account_code, account_reference = _voucher_no)
        db.Payment_Voucher_Transaction.insert(
            payment_voucher_header_id = _header.id,
            account_voucher_transaction_type = _id.account_voucher_transaction_type,
            account_voucher_transaction_code = _id.account_voucher_transaction_code,
            account_code = _id.account_code,
            account_debit_code = n.account_debit_code,
            dept_code_id = n.dept_code_id,
            department_code = n.department_code,
            transaction_payment_type_id = n.transaction_payment_type_id,
            amount = n.amount,
            description = n.description,
            account_reference = _voucher_no,
            department = n.department,
            invoice_no = n.invoice_no,
            location = n.location,
            cost_center_category_id = n.cost_center_category_id,
            cost_center_category_code = n.cost_center_category_code,
            cost_center_id = n.cost_center_id,
            cost_center_code = n.cost_center_code,
            payment_voucher_request_no = _id.payment_voucher_request_no,
            payment_voucher_no = _header.payment_voucher_no
        )

def delete_account_transaction_id():
    response.js = "alertify.confirm('Payment Voucher', 'Are you sure you want to delete?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('workflow_payment_voucher','delete_transaction_id',args = request.args(0))

def delete_transaction_id():
    _trnx = db(db.Payment_Voucher_Transaction_Request.id == request.args(0)).select().first()            
    if _trnx.payment_voucher_request_id:
        if db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == _trnx.payment_voucher_request_id).count() == 1:
            response.js = "alertify.notify('Empty transactions not allowed.','warning')"            
        elif db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == _trnx.payment_voucher_request_id).count() > 1:
            _trnx.delete_record()
            _total_amount = 0  
            _head = db(db.Payment_Voucher_Request.id == _trnx.payment_voucher_request_id).select().first()
            _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
            _total_amount = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == _trnx.payment_voucher_request_id).select(_total_amount).first()[_total_amount]    
            _head.update_record(total_amount = _total_amount)    
            response.js = "$('#PVTtbl').get(0).reload();alertify.error('Record Deleted.');"
    elif not _trnx.payment_voucher_request_id:
        _trnx.delete_record()
        response.js = "$('#PVTtbl').get(0).reload();alertify.error('Record Deleted.');"

def put_payment_voucher_upload_id():
    _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
    _pv = db(db.Payment_Voucher_Header.payment_voucher_no == _id.payment_voucher_no).select().first()
    db.Payment_Voucher_Header.payment_voucher_no.writable = False
    db.Payment_Voucher_Header.payment_voucher_date.writable = False
    db.Payment_Voucher_Header.payment_voucher_request_no.writable = False
    db.Payment_Voucher_Header.account_reference.writable = False
    db.Payment_Voucher_Header.payee.writable = False
    db.Payment_Voucher_Header.custom_declaration_no.writable = False
    db.Payment_Voucher_Header.custom_invoice_no.writable = False
    db.Payment_Voucher_Header.transaction_reference_date.writable = False
    db.Payment_Voucher_Header.account_voucher_transaction_type.writable = False
    db.Payment_Voucher_Header.account_voucher_transaction_code.writable = False
    db.Payment_Voucher_Header.account_payment_mode_id.writable = False
    db.Payment_Voucher_Header.total_amount.writable = False
    db.Payment_Voucher_Header.account_code.writable = False
    db.Payment_Voucher_Header.bank_name_id.writable = False
    db.Payment_Voucher_Header.cheque_no.writable = False
    db.Payment_Voucher_Header.cheque_dated.writable = False
    db.Payment_Voucher_Header.entry_date.writable = False
    db.Payment_Voucher_Header.status_id.writable = False
    db.Payment_Voucher_Header.remarks.writable = False
    db.Payment_Voucher_Header.manual_pv_no.writable = False
    db.Payment_Voucher_Header.gl_entry_ref.writable = False

    form = SQLFORM(db.Payment_Voucher_Header, _pv.id, upload=URL('default','download'))
    if form.process().accepted:
        response.flash = 'File upload.'
    elif form.errors:
        response.flash = 'File upload error'        
    return dict(form = form)
# --------------------- p a y m e n t  v o u c h e r  g r i d--------------------------
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_payment_voucher_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Payment Req. #'),TD('Payment Vou. #'),TD('Account Code'),TD('Payee'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    if auth.has_membership('ACCOUNTS'):
        _query = db((db.Payment_Voucher_Request.status_id != 15) & (db.Payment_Voucher_Request.created_by == auth.user_id)).select(orderby = db.Payment_Voucher_Request.id)
    elif auth.has_membership('ACCOUNTS MANAGER'):
        _query = db(db.Payment_Voucher_Request.status_id != 15).select(orderby = db.Payment_Voucher_Request.id)
    elif auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'):
        _query = db(db.Payment_Voucher_Request.status_id != 15).select(orderby = db.Payment_Voucher_Request.id)
    for n in _query:
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        uplo_lnk = A(I(_class='fas fa-file-upload'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_payment_voucher','put_payment_voucher_upload_id',args = n.id, extension = False))
        if n.status_id == 13:            
            prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_payment_voucher_reports','get_payment_voucher_no_id',args = n.payment_voucher_no, extension = False))    
        btn_lnk = DIV(prin_lnk)
        if auth.has_membership('ACCOUNTS'):            
            if n.status_id == 13:
                work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')                
            btn_lnk = DIV(uplo_lnk, work_lnk, prin_lnk)    
        elif auth.has_membership('ACCOUNTS MANAGER'):
            if n.status_id == 13:
                appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
            btn_lnk = DIV(appr_lnk, prin_lnk)    
        elif auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'):
            if (n.created_by == auth.user_id) & (n.status_id == 12):
                work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_payment_voucher','post_root_payment_voucher',args = n.id, extension = False))
                btn_lnk = DIV(work_lnk,prin_lnk)                
            elif (n.created_by != auth.user_id) & (n.status_id == 13):
                appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
                btn_lnk = DIV(appr_lnk,prin_lnk)            
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
def get_payment_voucher_management_approval_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Payment Req. #'),TD('Payment Vou. #'),TD('Account Code'),TD('Payee'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    _query = db(db.Payment_Voucher_Request.status_id == 13).select(orderby = db.Payment_Voucher_Request.id)
    for n in _query:
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('account_transaction','post_receipt_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_receipt_voucher_reports','get_account_voucher_request_id',args = n.id, extension = False))
        down_lnk = A(I(_class='fas fa-file-download'), _title='File View/Download', _target=' blank', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_payment_voucher','get_payment_voucher_upload_id',args = n.id, extension = False))
        if auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'):
            appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        btn_lnk = DIV(down_lnk, appr_lnk)            
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
    table = TABLE([head, body],_class='table',_id='MGMtbl')
    return dict(table = table)

def get_payment_voucher_upload_id():
    import os
    _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
    _pv = db(db.Payment_Voucher_Header.payment_voucher_no == _id.payment_voucher_no).select().first()        
    filepath = URL('default', 'download', args =_pv.file_upload)
    pdf_data = open(filepath,"rb").read()
    response.headers['Content-Type']='application/pdf'
    return pdf_data

    # return open(URL('default', 'download', args =_pv.file_upload))

def validate_post_payment_voucher(form):
    # validate custom invoice number if double entry (final)
    _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
    _trnx = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).count()
    if int(_trnx or 0) <= 0:
        response.js = "alertify.notify('Not allowed.','warning')"
        form.errors.account_payment_mode_id = 'Transaction is empty.'
        return
    elif db(db.Payment_Voucher_Request.custom_invoice_no == request.vars.custom_invoice_no).select().first():
        form.errors.custom_invoice_no = 'Already exists.'
        response.js = "alertify.warning('Custom Invoice No. Already Exists.');"
    form.vars.payee = request.vars.payee.upper()
    form.vars.cheque_no = request.vars.cheque_no.upper()
    form.vars.custom_invoice_no = request.vars.custom_invoice_no.upper()
    form.vars.custom_declaration_no = request.vars.custom_declaration_no.upper()
    form.vars.manual_pv_no = request.vars.manual_pv_no.upper()
    form.vars.remarks = request.vars.remarks.upper()

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_payment_voucher():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _id = _total_amount = 0        
    db.Payment_Voucher_Request.payment_voucher_request_no.default = str(x.strftime('%d%y%H%M'))
    db.Payment_Voucher_Request.account_payment_mode_id.requires = IS_IN_DB(db(db.Account_Voucher_Payment_Mode.id != 4),db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode')
    db.Payment_Voucher_Request.status_id.default = 12
    if request.args(0):
        _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
        if _id.status_id == 13:
            db.Payment_Voucher_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'PV-TASK2'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')   
            db.Payment_Voucher_Request.status_id.default = 13
    form = SQLFORM(db.Payment_Voucher_Request, request.args(0))
    if form.process(onvalidation = validate_post_payment_voucher).accepted:
        _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
        if not request.args(0):
            _req = db(db.Payment_Voucher_Request.ticket_no_id == request.vars.ticket_no_id).select().first()
            _total_amount = db(db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select(_total_amount).first()[_total_amount]
            _req.update_record(total_amount = _total_amount)
        elif request.args(0):            
            _total_amount = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _id.update_record(total_amount = _total_amount)
        redirect(URL('workflow_payment_voucher','get_payment_voucher_grid'))
    elif form.errors:
        response.flash = 'form error'
    return dict(form = form, ticket_no_id = ticket_no_id, _id = _id)

def validate_payment_voucher_transaction(form):
    _id = dc(dc.Master_Account.account_code == request.vars.account_debit_code).select().first()
    if not _id:
        form.errors.account_debit_code = 'Account code not found.'
    elif request.vars.account_debit_code == '' or request.vars.account_debit_code == None:
        form.errors.account_debit_code = 'Account code is empty.'
    elif request.vars.account_debit_code == '' or request.vars.transaction_payment_type_id == None:
        form.errors.transaction_payment_type_id = 'Payment type is empty.'
    elif request.vars.dept_code_id == '' or request.vars.dept_code_id == None:
        form.errors.dept_code_id = 'Department is empty.'
    elif request.vars.description == '' or request.vars.description == None:
        form.errors.description = 'Description is empty.'
    elif request.vars.amount == '' or request.vars.amount == None:
        form.errors.amount = 'Amount is empty.'
    elif _id: 
        _loc = _dep = 99        
        _gl_acct_ref = _gl_id = _gl_dept = _gl_loc = None
        _dept = db(db.General_Department_Cost_Center.id == request.vars.dept_code_id).select().first()
        _cost_ctgr = db(db.Cost_Center_Category.id == request.vars.cost_center_category_id).select().first()
        _cost_cntr = db(db.Cost_Center.id == request.vars.cost_center_id).select().first()        
        if request.args(0): # with id
            if int(db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).count()) > 30:
                form.errors.account_debit_code = 'Transaction entry already exceeds!'
                response.js = "alertify.alert('Payment Voucher Transaction', 'Transaction entry already exceeds!');"                
            _pv = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
            if int(request.vars.transaction_payment_type_id) == 2: # against invoice selected
                _gl = db(db.General_Ledger.id == request.vars.gl_id).select().first()                                                
                # if db((db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)) & (db.Payment_Voucher_Transaction_Request.account_code == request.vars.account_debit_code) & (db.Payment_Voucher_Transaction_Request.invoice_no == _gl.account_reference_no)).select().first():
                if not _gl:
                    form.errors.account_debit_code = 'Account credit code is empty or already exist.'                    
                elif db((db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)) & (db.Payment_Voucher_Transaction_Request.gl_id == request.vars.gl_id)).select().first():
                    form.errors.account_debit_code = 'Same entry already exist.'
                    response.js = "alertify.error('Same entry already exist.')"
                elif _gl:
                    form.vars.invoice_no = _gl.account_reference_no
                    form.vars.gl_id = request.vars.gl_id
                    form.vars.department = _gl.department
                    form.vars.location = _gl.location

            form.vars.ticket_no_id = _pv.ticket_no_id
            form.vars.account_code = _pv.account_code
            form.vars.payment_voucher_request_id = request.args(0)

        elif not request.args(0): # without id
            if int(db(db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).count()) > 30:
                form.errors.account_debit_code = 'Transaction entry already exceeds!'
                response.js = "alertify.alert('Payment Voucher Transaction', 'Transaction entry already exceeds!');"                
            if int(request.vars.transaction_payment_type_id) == 2: # against invoice selected
                _gl = db(db.General_Ledger.id == request.vars.gl_id).select().first()                                                  
                if not _gl:
                    form.errors.account_debit_code = 'Account credit code is empty or already exist.'                    
                elif db((db.Payment_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id) & (db.Payment_Voucher_Transaction_Request.gl_id == request.vars.gl_id)).select().first():
                    form.errors.account_debit_code = 'Same entry already exist.'
                    response.js = "alertify.error('Same entry already exist.')"
                elif _gl:
                    form.vars.invoice_no = _gl.account_reference_no
                    form.vars.gl_id = request.vars.gl_id
                    form.vars.department = _gl.department
                    form.vars.location = _gl.location
        form.vars.cost_center_category_id = request.vars.cost_center_category_id
        form.vars.cost_center_category_code = _cost_ctgr.cost_center_category_code
        form.vars.cost_center_id = request.vars.cost_center_id
        form.vars.cost_center_code = _cost_cntr.cost_center_code
        form.vars.description = request.vars.description.upper()
        form.vars.department_code = _dept.department_code
        form.vars.account_voucher_transaction_type = 23
        form.vars.account_voucher_transaction_code = 'PV'
               
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_payment_voucher_transaction():        
    db.Payment_Voucher_Transaction_Request.ticket_no_id.default = _ticket_no_ref = session.ticket_no_id
    form = SQLFORM(db.Payment_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_payment_voucher_transaction).accepted:
        if request.args(0):
            _pvr = db(db.Payment_Voucher_Request.id == int(request.args(0))).select().first()
            _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
            _total_amount = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _pvr.update_record(total_amount = _total_amount)
        response.js = "$('#PVTtbl').get(0).reload();"        
    elif form.errors:
        response.flash = 'error'
        print('err:->'), form.errors
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
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
            TD(locale.format('%.2F', n.amount or 0, grouping = True), _align='right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :')),_align='right',_class='bg-green color-palette'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True))), _align ='right',_class='bg-green color-palette'),TD(_class='bg-green color-palette')))
    table = TABLE([head, body, foot], _class='table',_id='PVTtbl')
    return dict(form = form, table = table)

# ---------------- root access --------------------------------
@auth.requires(auth.has_membership('ROOT'))
def post_root_payment_voucher():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _id = _total_amount = 0        
    db.Payment_Voucher_Request.payment_voucher_request_no.default = str(x.strftime('%d%y%H%M'))
    db.Payment_Voucher_Request.account_payment_mode_id.requires = IS_IN_DB(db(db.Account_Voucher_Payment_Mode.id != 4),db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode')
    db.Payment_Voucher_Request.status_id.default = 12
    if request.args(0):
        _id = db(db.Payment_Voucher_Request.id == request.args(0)).select().first()
        if _id.status_id == 13:
            db.Payment_Voucher_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'PV-TASK2'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')   
            db.Payment_Voucher_Request.status_id.default = 13
    form = SQLFORM(db.Payment_Voucher_Request, request.args(0))
    if form.process(onvalidation = validate_post_payment_voucher,id='thisformid').accepted:
        _total_amount = db.Payment_Voucher_Transaction_Request.amount.sum().coalesce_zero()
        _total_amount = db(db.Payment_Voucher_Transaction_Request.payment_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
        _id.update_record(total_amount = _total_amount)
        redirect(URL('workflow_payment_voucher','get_payment_voucher_grid'))
    elif form.errors:
        response.flash = 'form error'
        # print('err:'), form.errors, request.now
    
    return dict(form = form, ticket_no_id = ticket_no_id, _id = _id)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_payment_voucher_root_transaction():        
    db.Payment_Voucher_Transaction_Request.ticket_no_id.default = _ticket_no_ref = session.ticket_no_id
    form = SQLFORM(db.Payment_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_payment_voucher_transaction).accepted:
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
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
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
            TD(locale.format('%.2F', n.amount or 0, grouping = True), _align='right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    # text-green
    # foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :'),_class='text-red'),_align='right'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True),_class='text-red')), _align ='right'),TD()))
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(H4(B('TOTAL AMOUNT :')),_align='right',_class='bg-green color-palette'),TD(H4(B(locale.format('%.2F', _total_amount or 0, grouping = True))), _align ='right',_class='bg-green color-palette'),TD(_class='bg-green color-palette')))
    table = TABLE([head, body, foot], _class='table',_id='PVTtbl')
    return dict(form = form, table = table)
# ---------------- root access --------------------------------
# --------------------- p a y m e n t  v o u c h e r  g r i d--------------------------    

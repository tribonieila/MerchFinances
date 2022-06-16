# ----------------------------------------------------------------------------------------------
# --------------     J O U R N A L  V O U C H E R  T R A N S A C T I O N S     -----------------
# ----------------------------------------------------------------------------------------------
from datetime import datetime, date
import locale
import datetime
import random
import string
locale.setlocale(locale.LC_ALL, '')
x = datetime.datetime.now() # auth generate

def get_item_description():
    if int(request.args(0)) == 1:        
        _debit = dc(dc.Master_Account.account_code == request.vars.account_debit_code).select().first()
        if _debit:
            _account_code = _debit.account_code
            _account_name = _debit.account_name
            session.account_debit_code = request.vars.account_debit_code
            return DIV(SPAN(I(_class='fas fa-info-circle'),_class='info-box-icon bg-aqua'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN(str(_account_code) + ' - ' + str(_account_name),_class='info-box-number'),_class='info-box-content'),_class='info-box')        
        elif not _debit:
            return DIV(SPAN(I(_class='fas fa-times-circle'),_class='info-box-icon bg-red'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN('Not Found!',_class='info-box-number'),_class='info-box-content'),_class='info-box')
    elif int(request.args(0)) == 2:
        _credit = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()
        if _credit:
            _account_code = _credit.account_code
            _account_name = _credit.account_name
            session.account_debit_code = request.vars.account_credit_code
            return DIV(SPAN(I(_class='fas fa-info-circle'),_class='info-box-icon bg-aqua'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN(str(_account_code) + ' - ' + str(_account_name),_class='info-box-number'),_class='info-box-content'),_class='info-box')        
        elif not _credit:
            return DIV(SPAN(I(_class='fas fa-times-circle'),_class='info-box-icon bg-red'),DIV(SPAN('Master Account',_class='info-box-text'),SPAN('Not Found!',_class='info-box-number'),_class='info-box-content'),_class='info-box')
            
def patch_journal_voucher_id(): # submit button != request.args(0)
    
    if int(request.args(0)) == 1:
        _trnx = db(db.Journal_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).count()
        if _trnx <= 0:
            response.js = "alertify.alert('Journal Voucher','Journal Voucher Transaction is empty!');"    
            return
        db.Journal_Voucher_Header_Request.insert(
            ticket_no_id = request.vars.ticket_no_id,
            journal_voucher_request_no = request.vars.journal_voucher_request_no,
            journal_voucher_type_id = request.vars.journal_voucher_type_id,
            transaction_reference_date = request.vars.transaction_reference_date,
            account_voucher_transaction_type = 24,
            account_voucher_transaction_code = 'JV',
            status_id = request.vars.status_id,
            remarks = request.vars.remarks
        )
        
        _id = db(db.Journal_Voucher_Header_Request.journal_voucher_request_no == request.vars.journal_voucher_request_no).select().first()
        _total_amount = 0
        for n in db(db.Journal_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select():
            n.update_record(journal_voucher_header_request_id = _id.id, journal_voucher_request_no = _id.journal_voucher_request_no)
        _total_amount = db.Journal_Voucher_Transaction_Request.amount.sum().coalesce_zero()
        _total_amount = db(db.Journal_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select(_total_amount).first()[_total_amount]
        _id.update_record(total_amount = _total_amount)
        response.js = "alertify.success('Success!');window.location.href = '%s'" % URL('workflow_journal_voucher','get_journal_voucher_grid')

    elif int(request.args(0)) == 2: # accounts manager 1-approval/2-rejection, request.args(0): param, request.args(1): id, request.args(2): 1:apprvd/2:rejct        
        _id = db(db.Journal_Voucher_Header_Request.id == request.args(1)).select().first()
        if _id.status_id == 1 or _id.status_id == 17:
            response.js = "alertify.notify('Already %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 17:
            if int(request.args(2)) == 1: # finance manager approval
                _id.update_record(status_id = 17)
                sync_journal_voucher_header()
                response.js = "alertify.success('Approved!'); window.location.href = '%s'" % URL('workflow_journal_voucher','get_journal_voucher_grid')
            elif int(request.args(2)) == 2: # finance manager rejection
                _id.update_record(status_id = 1)
                response.js = "alertify.warning('Rejected!'); window.location.href = '%s'" % URL('workflow_journal_voucher','get_journal_voucher_grid')
            
    elif int(request.args(0)) == 3: # finance/audit manager approval/rejection
        _id = db(db.Journal_Voucher_Header_Request.id == request.args(1)).select().first()
        if _id.status_id == 1 or _id.status_id == 18:
            response.js = "alertify.notify('Already %s','message')" % (_id.status_id.description)
        elif not _id.status_id == 1 or _id.status_id == 18:
            if int(request.args(2)) == 1: # audit manager approved
                _id.update_record(status_id = 18)
                response.js = "alertify.success('Approved!'); window.location.href = '%s'" % URL('workflow_journal_voucher','get_journal_voucher_grid')
            elif int(request.args(2)) == 2:
                _id.update_record(status_id = 1)
                response.js = "alertify.warning('Rejected!'); window.location.href = '%s'" % URL('workflow_journal_voucher','get_journal_voucher_grid')
                
                # response.js = "alertify.prompt( 'Journal Voucher', 'Rejection Remarks', 'Prompt Value', function(evt, value) { ajax('%s',['value']) }, function() { alertify.error('Cancel') });" % URL('workflow_journal_voucher','patch_journal_voucher_remarks_id', args = request.args(1))
    elif int(request.args(0)) == 4: # accounts confirmation
        print('accounts confirmation')

def patch_journal_voucher_remarks_id():
    print('rejects'), request.args(0), request.args(1), request.vars.value

def sync_journal_voucher_header():
    _ctr = 0
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(1)).select().first()
    _vn = db(db.Account_Voucher_Type.transaction_prefix == 'JV').select().first()
    _voucher_no = _vn.voucher_serial_no + 1
    _vn.voucher_serial_no += 1
    _vn.update_record()
    _id.update_record(journal_voucher_no = _voucher_no,journal_voucher_date = request.now, account_reference = _voucher_no, status_id = 17)
    db.Journal_Voucher_Header.insert(
        journal_voucher_no = _voucher_no,
        journal_voucher_date = _id.journal_voucher_date,
        journal_voucher_request_no = _id.journal_voucher_request_no,
        account_reference = str(_vn.transaction_prefix) + str(_id.account_reference),
        journal_voucher_type_id = _id.journal_voucher_type_id,
        transaction_reference_date = _id.transaction_reference_date,
        account_voucher_transaction_type = _id.account_voucher_transaction_type,
        account_voucher_transaction_code = _id.account_voucher_transaction_code,
        total_amount = _id.total_amount,
        entry_date = _id.entry_date,
        status_id = _id.status_id,
        remarks = _id.remarks,
        requested_on = _id.requested_on,
        requested_by = _id.requested_by)
    _hdr = db(db.Journal_Voucher_Header.journal_voucher_no == _voucher_no).select().first()    
    for n in db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(1)).select():
        _ctr += 1
        _account_ref = str(_vn.transaction_prefix) + str(_voucher_no) + '-' +str(_ctr)
        n.update_record(account_reference = _account_ref)
        db.Journal_Voucher_Transaction.insert(
            journal_voucher_header_id = _hdr.id, 
            account_voucher_transaction_type = n.account_voucher_transaction_type,
            account_voucher_transaction_code = n.account_voucher_transaction_code,
            account_debit_code = n.account_debit_code,
            account_credit_code = n.account_credit_code,
            dept_code_id = n.dept_code_id,
            department_code = n.department_code,
            amount = n.amount,
            description = n.description,
            account_reference = _account_ref,
            department = n.department,
            cost_center_category_id = n.cost_center_category_id,
            cost_center_category_code = n.cost_center_category_code,
            cost_center_id = n.cost_center_id,
            cost_center_code = n.cost_center_code,
            journal_voucher_request_no = _id.journal_voucher_request_no,
            journal_voucher_no = _id.journal_voucher_no)

def delete_account_transaction_id():
    response.js = "alertify.confirm('Payment Voucher', 'Are you sure you want to delete?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('workflow_journal_voucher','delete_transaction_id',args = request.args(0))    

def delete_transaction_id():
    _trnx = db(db.Journal_Voucher_Transaction_Request.id == request.args(0)).select().first()
    if _trnx.journal_voucher_header_request_id:
        if db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == _trnx.journal_voucher_header_request_id).count() == 1:
            response.js = "alertify.notify('Empty transactions not allowed.','warning')"            
        elif db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == _trnx.journal_voucher_header_request_id).count() > 1:
            _trnx.delete_record()
            _total_amount = 0  
            _head = db(db.Payment_Voucher_Request.id == _trnx.journal_voucher_header_request_id).select().first()
            _total_amount = db.Journal_Voucher_Transaction_Request.amount.sum().coalesce_zero()
            _total_amount = db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == _trnx.journal_voucher_header_request_id).select(_total_amount).first()[_total_amount]    
            _head.update_record(total_amount = _total_amount)    
            response.js = "$('#JVTtbl').get(0).reload();alertify.error('Record Deleted.');"
    elif not _trnx.journal_voucher_header_request_id:
        _trnx.delete_record()
        response.js = "$('#JVTtbl').get(0).reload();alertify.error('Record Deleted.');"

def put_journal_voucher_upload_id():
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(0)).select().first()
    _jv = db(db.Journal_Voucher_Header.journal_voucher_no == _id.journal_voucher_no).select().first()    
    
    db.Journal_Voucher_Header.journal_voucher_no.writable = False
    db.Journal_Voucher_Header.journal_voucher_date.writable = False
    db.Journal_Voucher_Header.journal_voucher_request_no.writable = False
    db.Journal_Voucher_Header.account_reference.writable = False
    db.Journal_Voucher_Header.journal_voucher_type_id.writable = False
    db.Journal_Voucher_Header.transaction_reference_date.writable = False
    db.Journal_Voucher_Header.account_voucher_transaction_type.writable = False
    db.Journal_Voucher_Header.account_voucher_transaction_code.writable = False
    db.Journal_Voucher_Header.total_amount.writable = False
    db.Journal_Voucher_Header.entry_date.writable = False
    db.Journal_Voucher_Header.status_id.writable = False
    db.Journal_Voucher_Header.remarks.writable = False
    db.Journal_Voucher_Header.gl_entry_ref.writable = False

    form = SQLFORM(db.Journal_Voucher_Header, _jv.id, upload=URL('default','download'))
    if form.process().accepted:
        response.flash = 'File uploaded'
    elif form.errors:
        response.flash = 'File some error'
    return dict(form = form, _id = _id)

# --------------------- j o u r n a l  v o u c h e r  g r i d--------------------------
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_journal_voucher_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('JV Req.No.'),TD('Acct.Type'),TD('Acct.Code'),TD('Total Amount'),TD('Prepared By'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')    
    _query = db(db.Journal_Voucher_Header_Request.status_id != 19).select(orderby = db.Journal_Voucher_Header_Request.id)
    for n in _query:
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))        
        work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        uplo_lnk = A(I(_class='fas fa-file-upload'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','put_journal_voucher_upload_id',args = n.id, extension = False))
        if auth.has_membership('ACCOUNTS'):
            if (n.status_id == 16) and (n.created_by == auth.user_id):
                uplo_lnk = A(I(_class='fas fa-file-upload'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))
                work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))
            btn_lnk = DIV(uplo_lnk, work_lnk, prin_lnk)
        # elif auth.has_membership('ACCOUNTS'):
        #     if (n.status_id == 17) and (n.created_by == auth.user_id):
        #         work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))
        #     btn_lnk = DIV(uplo_lnk, prin_lnk)

        elif auth.has_membership('ACCOUNTS MANAGER'):
            if n.status_id == 16:
                appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))                
            btn_lnk = DIV(appr_lnk)        
        elif auth.has_membership('MANAGEMENT') | auth.has_membership('ROOT'):
            if n.status_id == 17:
                appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))                
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

def validate_post_journal_voucher(form):
    _id = db(db.Journal_Voucher_Header_Request.id == request.args(0)).select().first()
    _trnx = db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(0)).count()
    if int(_trnx or 0) <= 0:
        response.js = "alertify.notify('Not Allowed.','warning')"
        form.errors.journal_voucher_type_id = 'Transaction is empty.'
        return 
    form.vars.remarks = request.vars.remarks.upper()
    form.vars.journal_voucher_no = request.vars.journal_voucher_no,
    form.vars.journal_voucher_request_no = request.vars.journal_voucher_request_no

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_journal_voucher():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id    
    _id = _total_amount = 0
    db.Journal_Voucher_Header_Request.journal_voucher_request_no.default = str(x.strftime('%d%y%H%M'))
    db.Journal_Voucher_Header_Request.status_id.default = 16
    if request.args(0):
        _id = db(db.Journal_Voucher_Header_Request.id == request.args(0)).select().first()
        if _id.status_id == 17:
            db.Journal_Voucher_Header_Request.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'JV-TASK2'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
    form = SQLFORM(db.Journal_Voucher_Header_Request, request.args(0))
    if form.process(onvalidation = validate_post_journal_voucher,id='thisformid').accepted:
        _total_amount = db.Journal_Voucher_Transaction_Request.amount.sum().coalesce_zero()
        if not request.args(0):
            _req_trnx = db(db.Journal_Voucher_Header_Request.ticket_no_id == request.vars.ticket_no_id).select().first()
            _total_amount = db(db.Journal_Voucher_Transaction_Request.ticket_no_id == request.vars.ticket_no_id).select(_total_amount).first()[_total_amount]
            _req_trnx.update_record(total_amount = _total_amount)
        elif request.args(0):
            _total_amount = db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _id.update_record(total_amount = _total_amount)
        redirect(URL('workflow_journal_voucher','get_journal_voucher_grid'))
    elif form.errors:
        response.flash = 'Form has error.'
    return dict(form = form, _id = _id, ticket_no_id = ticket_no_id)

def validate_journal_voucher_transaction(form):
    _debit = dc(dc.Master_Account.account_code == request.vars.account_debit_code).select().first()
    _credit = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()
    if not _debit:
        form.errors.account_debit_code = 'Account not found.'
    elif not _credit:
        form.errors.account_credit_code = 'Account not found.'
    elif request.vars.account_debit_code == request.vars.account_credit_code:
        form.errors.account_credit_code = 'Duplicate entry not allowed.'
    elif request.vars.account_debit_code == '' or request.vars.account_debit_code == None:
        form.errors.account_debit_code = 'Account code is empty.'
    elif request.vars.account_credit_code == '' or request.vars.account_credit_code == None:
        form.errors.account_credit_code = 'Account code is empty.'
    elif request.vars.dept_code_id == '' or request.vars.dept_code_id == None:
        form.errors.dept_code_id = 'Department is empty.'
    elif request.vars.description == '' or request.vars.description == None:
        form.errors.description = 'Description is empty.'
    elif request.vars.amount == '' or request.vars.amount == None:
        form.errors.amount = 'Amount is empty.'    
    elif _debit == _credit:
        form.errors.account_debit_code = 'Same account code entry not allowed.'
    if _debit and _credit:
        _dept = db(db.General_Department_Cost_Center.id == request.vars.dept_code_id).select().first()
        _cost_center_category_id = _cost_center_category_code = _cost_center_id = _cost_center_code = None

        if request.vars.cost_center_category_id:
            _cost_ctgr = db(db.Cost_Center_Category.id == request.vars.cost_center_category_id).select().first()
            _cost_center_category_id = request.vars.cost_center_category_id
            _cost_center_category_code = _cost_ctgr.cost_center_category_code
            # form.vars.cost_center_category_id = request.vars.cost_center_category_id
            # form.vars.cost_center_category_code = _cost_ctgr.cost_center_category_code
        elif request.vars.cost_center_id:
            _cost_cntr = db(db.Cost_Center.id == request.vars.cost_center_id).select().first()
            _cost_center_id = request.vars.cost_center_id
            _cost_center_code = _cost_cntr.cost_center_code
            # form.vars.cost_center_id = request.vars.cost_center_id
            # form.vars.cost_center_code = _cost_cntr.cost_center_code

        if request.args(0): # with id
            if int(db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(0)).count()) > 30:
                form.errors.account_debit_code = 'Transaction entry already exceeds!'
            _jv = db(db.Journal_Voucher_Header_Request.id == request.args(0)).select().first()
        
            form.vars.ticket_no_id = _jv.ticket_no_id
            form.vars.journal_voucher_header_request_id = request.args(0)
            # form.vars.account_code = _jv.account_code

        elif not request.args(0): # without id
            if int(db(db.Journal_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id).count()) > 30:
                form.errors.account_debit_code = 'Transaction entry already exceeds!'
    
        form.vars.cost_center_category_id = _cost_center_category_id or None
        form.vars.cost_center_category_code = _cost_center_category_code
        form.vars.cost_center_id = _cost_center_id or None
        form.vars.cost_center_code = _cost_center_code    
        form.vars.department_code = _dept.department_code
        form.vars.description = request.vars.description.upper()
        form.vars.account_voucher_transaction_type = 24
        form.vars.account_voucher_transaction_code = 'JV'
        form.vars.department = request.vars.dept_code_id
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_journal_voucher_transaction():
    db.Journal_Voucher_Transaction_Request.ticket_no_id.default = _ticket_no_ref = session.ticket_no_id
    db.Journal_Voucher_Transaction_Request.cost_center_category_id.requires= IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'),null=None)
    db.Journal_Voucher_Transaction_Request.cost_center_id.requires = IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'),null=None)
    form = SQLFORM(db.Journal_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_journal_voucher_transaction).accepted:
        response.js = "$('#JVTtbl').get(0).reload();"
    elif form.errors:        
        response.js = "console.log('%s')" %(form.errors)
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Debit Code'),TD('Dept.'),TD('Description'),TD('Credit Code'),TD('Amount'),TD()),_class='bg-red')
    _query = db((db.Journal_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id) & (db.Journal_Voucher_Transaction_Request.created_by == auth.user_id)).select()
    if request.args(0):
        _query = db(db.Journal_Voucher_Transaction_Request.journal_voucher_header_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        _total_amount += float(n.amount or 0)
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('workflow_journal_voucher','delete_account_transaction_id',args = n.id, extension = False))
        if n.created_by != auth.user_id:
            dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
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
def get_journal_voucher_finance_manager_approval_grid():
    ctr = 0
    row = []
    # head = THEAD(TR(TD('#'),TD('Date'),TD('Acct.Type'),TD('Acct.Code'),TD('Total Amount'),TD('Prepared By'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')    
    head = THEAD(TR(TD('#'),TD('Date'),TD('JV Req.No.'),TD('Acct.Type'),TD('Acct.Code'),TD('Total Amount'),TD('Prepared By'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')    
    for n in db(db.Journal_Voucher_Header_Request.status_id == 17).select(orderby = db.Journal_Voucher_Header_Request.id):
        ctr += 1
        appr_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        work_lnk = A(I(_class='fas fa-user-edit'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled' , _href=URL('workflow_payment_voucher','post_payment_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        down_lnk = A(I(_class='fas fa-file-download'), _title='File View/Download', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','put_journal_voucher_upload_id',args = n.id, extension = False))
        if auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership('ROOT'):
            if n.status_id == 17:
                work_lnk = A(I(_class='fas fa-user-check'), _title='View/Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('workflow_journal_voucher','post_journal_voucher',args = n.id, extension = False))
        btn_lnk = DIV(down_lnk, work_lnk)
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
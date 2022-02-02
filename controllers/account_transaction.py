
import string, random, locale, datetime

def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def get_item_description():
    _ma = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()
    if _ma:
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
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('VOU.No.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db((db.Account_Voucher_Request.created_by == auth.user_id) & (db.Account_Voucher_Request.status_id == 9)).select(orderby = db.Account_Voucher_Request.id):
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-plus'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('account_transaction','post_receipt_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(work_lnk, prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(_vn.account_voucher_transaction_code,n.voucher_no),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.3F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return dict(table = table)

@auth.requires_login()
def get_receipt_voucher_confirmation_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('VOU.No.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db((db.Account_Voucher_Request.created_by == auth.user_id) & (db.Account_Voucher_Request.status_id == 9)).select(orderby = db.Account_Voucher_Request.id):
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-check'), _title='Approved/Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle' , callback=URL('account_transaction','get_receipt_voucher_confirmation_id',args = n.id, extension = False))
        btn_lnk = DIV(work_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(_vn.account_voucher_transaction_code,n.voucher_no),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.3F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.created_by.first_name[:1],'.',n.created_by.last_name,' ',SPAN(n.status_id.description,_class='text-muted')),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table', _id='tblConf')
    return dict(table = table)

def patch_receipt_voucher():
    if int(request.args(0)) == 1:        
        _account_code = ''
        _ga = db(db.General_Account.id == 1).select().first()
        if int(request.vars.account_payment_mode_id or 0) == 1 or (int(request.vars.account_payment_mode_id or 0) == 2):
            _account_code = _ga.receipt_voucher_account
        elif (int(request.vars.account_payment_mode_id or 0) == 3):            
            _account_code = _ga.pdc_receipt_voucher_account
        response.js = "$('#Account_Voucher_Request_account_code').val('%s')" % (_account_code)
    elif int(request.args(0)) == 2:
        _id = db(db.Account_Voucher_Request.id == request.args(1)).select().first()
        _id.update_record(status_id = 2)
        redirect(URL('account_transaction','get_receipt_voucher_grid'))
    elif int(request.args(0)) == 3:        
        _trnx = db(db.Transaction_Payment_Type.id == request.vars.transaction_payment_type_id).select().first()
        if int(request.vars.transaction_payment_type_id or 0) == 2:
            ctr = 0
            row = []
            head = THEAD(TR(TD('#'),TD('A.Reff.'),TD('Inv.Amt.'),TD('Amt.Paid'),TD('Balance'),TD()))
            for n in db((db.General_Ledger.account_code == request.vars.account_credit_code) & (db.General_Ledger.debit > 0)).select():
                ctr += 1
                _balance = n.debit - n.amount_paid
                row.append(TR(
                    TD(ctr),
                    TD(n.account_reference_no),
                    TD(locale.format('%.3F',n.debit or 0, grouping = True)),
                    TD(locale.format('%.3F',n.amount_paid or 0, grouping = True)),
                    TD(locale.format('%.3F',_balance or 0, grouping = True)),                    
                    TD(BUTTON('Select',_class='btn btn-block btn-success btn-flat btn-xs', _id='BtnSelect',_name='BtnSelect',_onclick="ajax('%s')" % URL('account_transaction','get_general_ledger_id', args = n.id)))
                ))
            body = TBODY(*row)
            table = TABLE(*[head,body],_class='table')
            response.js = "alertify.confirm('%s').setHeader('General Ledger');alertify.confirm().set('resizable',true).resizeTo('50%','50%'); " %(XML('<table><tr><td>Header</td></tr><tr><td>Row</td></tr><tr><td>Header</td></tr><tr><td>Row</td></tr></table>'),sanitize = True)
            # response.js = "alertify.confirm().set('resizable',true).resizeTo('50%','50%');alertify.confirm('General Ledger', '%s', function(){ alertify.success('Ok') }, function(){ $('#Account_Voucher_Transaction_Request_description').val(''); $('#Account_Voucher_Transaction_Request_amount_paid').val(''); alertify.error('Cancel')});" %(table) 


def get_general_ledger_id():
    _gl = db(db.General_Ledger.id == request.args(0)).select().first()
    _balance = _gl.debit - _gl.amount_paid
    response.js = "$('#Account_Voucher_Transaction_Request_description').val('AGAINST INV%s'); $('#Account_Voucher_Transaction_Request_amount_paid').val('%s');" % (_gl.account_reference_no,_balance)
    if _gl.prepared == True:
        response.js = "alertify.notify('already prepared.','error')"

def validate_post_receipt_voucher(form):
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    if not request.args(0):        
        form.vars.status_id = 9
        form.vars.ticket_no_id = request.vars.ticket_no_id
        form.vars.voucher_no = _vn.voucher_serial_no + 1
        _vn.update_record(voucher_serial_no = _vn.voucher_serial_no + 1)
    elif request.args(0):
        _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()        
        form.vars.ticket_no_id = _id.ticket_no_id        
    form.vars.account_voucher_transaction_type = _vn.account_voucher_transaction_type
    form.vars.account_voucher_transaction_code = _vn.account_voucher_transaction_code

# @auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def check_membership():
    if not auth.has_membership('ACCOUNTS') | auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'):
        redirect(URL('default','forbidden'))

@auth.requires_login()
# @auth.requires(check_membership)
def post_receipt_voucher(): 
    _total_amount = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    db.Account_Voucher_Request.voucher_no.default = _vn.voucher_serial_no + 1
    db.Account_Voucher_Request.status_id.default = 9
    db.Account_Voucher_Request.account_payment_mode_id.requires= IS_EMPTY_OR(IS_IN_DB(db(db.Account_Voucher_Payment_Mode.id != 4),db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))

    if request.args(0):
        _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Account_Voucher_Request, request.args(0))    
    if form.process(onvalidation = validate_post_receipt_voucher).accepted:
        response.flash = 'RECORD SAVE'
        if not request.args(0):
            _vn.voucher_serial_no += 1
            _id = db(db.Account_Voucher_Request.created_by == auth.user_id).select().last()
            for n in db(db.Account_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select():
                _gl = db((db.General_Ledger.account_code == n.account_credit_code) & (db.General_Ledger.debit > 0)).select().first()
                n.update_record(account_voucher_request_id = _id.id, department = _gl.department, invoice_no = _gl.account_reference_no, location = _gl.location, voucher_no = _id.voucher_no, account_reference = _id.voucher_no, account_code = _id.account_code)
                _gl.update_record(prepared = True)
            _vn.update_record()
            _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Account_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select(_total_amount).first()[_total_amount]            
            _id.update_record(total_amount = _total_amount)
        elif request.args(0):            
            _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()
            for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select():
                _gl = db((db.General_Ledger.account_code == n.account_credit_code) & (db.General_Ledger.debit > 0)).select().first()
                n.update_record(account_voucher_request_id = _id.id, department = _gl.department, invoice_no = _gl.account_reference_no, voucher_no = _id.voucher_no, account_reference = _id.voucher_no, account_code = _id.account_code)            
                _gl.update_record(prepared = True)
            _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _id.update_record(total_amount = _total_amount)
        redirect(URL('account_transaction','get_receipt_voucher_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_post_receipt_voucher_transaction(form):        
    _id = dc(dc.Master_Account.account_code == request.vars.account_credit_code).select().first()

    if not _id:
        form.errors.account_credit_code = 'Account code not found.'
        response.js = "alertify.error('Account code not found.')"
    
    elif request.vars.account_credit_code == '' or request.vars.account_credit_code == None:
        form.errors.account_credit_code = 'Account credit code is empty.'
        response.js = "alertify.error('Account credit code is empty.')"

    elif db((db.Account_Voucher_Transaction_Request.account_credit_code == request.vars.account_credit_code) & (db.Account_Voucher_Transaction_Request.transaction_payment_type_id == request.vars.transaction_payment_type_id)).select().first(): # & (db.Account_Voucher_Transaction_Request.ticket_no_id == session.ticket_no_id)
        form.errors.account_credit_code = 'Account code already exist.'
        response.js = "alertify.error('Account code already exist.')"
    elif _id:
        _vou = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _dep = db(db.General_Department_Cost_Center.id == request.vars.dept_code_id).select().first()
        _gl = db(db.General_Ledger.account_code == request.vars.account_credit_code).select().first()
        _loc = None
        if request.vars.location_cost_center_id:
            _loc = db(db.General_Location_Cost_Center.id == request.vars.location_cost_center_id).select().first()
            _loc = _loc.location_code

        if request.args(0):
            _av = db(db.Account_Voucher_Request.id == int(request.args(0))).select().first()
            _trnx = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select().first()
            
            form.vars.ticket_no_id = _av.ticket_no_id
            form.vars.account_voucher_request_id = request.args(0)
            # form.vars.account_reference = _trnx.account_reference

        form.vars.account_voucher_transaction_type = _vou.account_voucher_transaction_type
        form.vars.account_voucher_transaction_code = _vou.account_voucher_transaction_code
        form.vars.department_code = _dep.department_code
        form.vars.location_code = _loc
        # form.vars.account_reference = _gl.account_reference_no
            
@auth.requires_login()
def post_receipt_voucher_transaction():
    db.Account_Voucher_Transaction_Request.ticket_no_id.default = session.ticket_no_id
    _ticket_no_ref = session.ticket_no_id
    form = SQLFORM(db.Account_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_post_receipt_voucher_transaction).accepted:
        if request.args(0):
            _av = db(db.Account_Voucher_Request.id == int(request.args(0))).select().first()
            _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _av.update_record(total_amount = _total_amount)
        response.js = "$('#AVTtbl').get(0).reload();"
    elif form.errors:
        response.flash = None
        response.js = "alertify.error('%s')" %(form.errors)
    ctr = _total_amount = 0
    row = []    
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Acct.Ref.'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
    _query = db(db.Account_Voucher_Transaction_Request.ticket_no_id == _ticket_no_ref).select()    
    if request.args(0):
        _query = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('account_transaction','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        _am = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        _serial = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _total_amount += float(n.amount_paid or 0)
        row.append(TR(
            TD(ctr),            
            TD(n.account_credit_code),
            TD(_am.account_name),
            TD(n.dept_code_id.department_code),
            TD(n.account_reference),
            TD(n.description),
            TD(locale.format('%.3F', n.amount_paid or 0, grouping = True), _align='right'),
            TD(btn_lnk),
        ))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align ='right'),TD()
    ))
    table = TABLE([head, body, foot], _class='table',_id='AVTtbl')
    return dict(form = form, table = table)

@auth.requires_login()
def put_receipt_voucher_id(): # to remove
    form = SQLFORM(db.Account_Voucher_Request, request.args(0))
    if form.process(onvalidation = validate_post_receipt_voucher).accepted:
        response.flash = 'Form updated.'
    elif form.errors:
        response.flash = 'Form has error.'
    return dict(form = form)

@auth.requires_login()
def put_receipt_voucher_transaction_id(): # to remove
    _total_amount = 0
    form = SQLFORM(db.Account_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_post_receipt_voucher_transaction).accepted:
        response.flash = 'Form updated.'
        _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
        _total_amount = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
        _rv = db(db.Account_Voucher_Transaction_Request.id == request.args(0)).select().first()
        _rv.update_record(total_amount = _total_amount)
    elif form.errors:
        response.flash = 'Form has error.'

    ctr = _total_amount = 0
    row = []
    
    head = THEAD(TR(TD('#'),TD('Serial #'),TD('Dept.'),TD('Account Code'),TD('Account Name'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
    for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select():
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('account_transaction','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        _am = dc(dc.Master_Account.account_code == n.account_code).select().first()
        _serial = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _total_amount += n.amount_paid
        row.append(TR(
            TD(ctr),
            TD(_serial.account_voucher_transaction_code,n.serial_no),
            TD(n.department_id.department_name),
            TD(n.account_code),
            TD(_am.account_name),
            TD(n.description),
            TD(locale.format('%.3F', n.amount_paid or 0, grouping = True), _align='right'),
            TD(btn_lnk),
        ))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align ='right'),TD()
    ))
    table = TABLE([head, body, foot], _class='table',_id='AVTtbl')
    return dict(form = form, table = table)

def delete_account_transaction_id():
    response.js = "alertify.confirm('Account Voucher Receipt', 'Are you sure you want to delete?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('account_transaction','delete_transaction_id',args = request.args(0))

def delete_transaction_id():
    db(db.Account_Voucher_Transaction_Request.id == request.args(0)).delete()    
    response.js = "$('#AVTtbl').get(0).reload();alertify.error('Record Deleted.');"
    # _total_amount = 0
    # _trnx = db(db.Account_Voucher_Transaction_Request.id == request.args(0)).select().first()
    # _head = db(db.Account_Voucher_Request.ticket_no_id == _trnx.ticket_no_id).select().first()

    # _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
    # _total_amount = db(db.Account_Voucher_Transaction_Request.ticket_no_id == _trnx.ticket_no_id).select(_total_amount).first()[_total_amount]    
    # _head.update_record(total_amount = _total_amount)    
    # print(':'), _total_amount, _trnx.ticket_no_id, _head.ticket_no_id
    
def get_receipt_voucher_confirmation_id():    
    _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()
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
    for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select():
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

def patch_receipt_voucher_confirmation_id():
    if int(request.args(0)) == 1: # reject
        _id = db(db.Account_Voucher_Request.id == request.args(1)).select().first()
        _id.update_record(status_id = 1)
        response.js = "alertify.alert().close();$('#tblConf').get(0).reload();alertify.error('Rejected!');"
    elif int(request.args(0)) == 2: # approved
        _id = db(db.Account_Voucher_Request.id == request.args(1)).select().first()
        _id.update_record(status_id = 10)
        sync_receipt_voucher_confirmation()
        response.js = "alertify.alert().close();$('#tblConf').get(0).reload();alertify.success('Approved!');"

def sync_receipt_voucher_confirmation():
    _id = db(db.Account_Voucher_Request.id == request.args(1)).select().first()
    # bank code
    db.Account_Voucher_Header.insert(
        voucher_no = _id.voucher_no,
        transaction_reference_date = _id.transaction_reference_date,
        account_voucher_transaction_type = _id.account_voucher_transaction_type,
        account_voucher_transaction_code = _id.account_voucher_transaction_code,
        account_payment_mode_id = _id.account_payment_mode_id,
        account_voucher_payment_code = _id.account_voucher_payment_code,
        receipt_voucher_confirmation_type_id = _id.receipt_voucher_confirmation_type_id,
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
        remarks = _id.remarks)
    _head = db(db.Account_Voucher_Header.voucher_no == _id.voucher_no).select().first()
    for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(1)).select():
        db.Account_Voucher_Transaction.insert(
            account_voucher_id = _head.id,
            account_voucher_transaction_type = n.account_voucher_transaction_type,
            account_voucher_transaction_code = n.account_voucher_transaction_code,
            account_code = n.account_code,
            account_credit_code = n.account_credit_code,
            account_debit_code = n.account_debit_code,
            dept_code_id = n.dept_code_id,
            department_code = n.department_code,
            location_cost_center_id = n.location_cost_center_id,
            location_code = n.location_code,
            transaction_payment_type_id = n.transaction_payment_type_id,
            amount_paid = n.amount_paid,
            description = n.description,
            account_reference = n.account_reference,
            voucher_no = n.voucher_no,
            gl_entry_ref = n.gl_entry_ref)
    
    # --------------- POSTING ON GEN. LEDGER ---------------
    import datetime
    _seq = put_batch_posting_sequence_id()    
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first() 
    _ga = db(db.General_Account.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 21).select().first()
    _gen = db((db.General_Ledger.account_reference_no == _id.voucher_no) & (db.General_Ledger.transaction_type == 21) & (db.General_Ledger.account_code == _id.account_code)).select().first()
    if not _gen:
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
            department = 13, # general
            type = _id.account_voucher_transaction_type,
            reference_no = str(_id.account_voucher_transaction_code) + str(n.account_reference),
            account_reference_no = n.account_reference,
            account_code = _id.account_code,
            description = str(_gl.common_text) + ' ' + str(n.account_reference),
            entrydate = request.now,
            credit = 0,
            debit = _id.total_amount,
            amount_paid = _id.total_amount,
            gl_entry_ref = _voucher_no_serial,
            batch_posting_seq = _seq,
            bank_code = _id.account_code
        )
        _row.update_record()
        
        for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(1)).select():
            _row.serial_number += 1       
            
            _amount_paid = 0
            _status = False
            _location = 99
            if n.transaction_payment_type_id == 2: # if against invoice
                _amount_paid = n.amount_paid
                _status = True
                _location = 1

            db.General_Ledger.insert(
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_reference_date,
                transaction_payment_type = n.transaction_payment_type.transaction_payment_type,
                transaction_type = _id.account_voucher_transaction_type,
                location = _location,
                transaction_type_ref = _id.account_voucher_transaction_code,
                transaction_date_entered = request.now,
                department = 13,
                type = _id.account_voucher_transaction_type,
                reference_no = str(_id.account_voucher_transaction_code) + str(n.account_reference),
                account_reference_no = n.account_reference,
                account_code = n.account_code,
                description = n.description,
                credit = n.amount_paid,
                debit = 0,
                amount_paid = _amount_paid,
                gl_entry_ref = _voucher_no_serial,
                batch_posting_seq = _seq,
                entrydate = request.now,
                bank_code = _id.account_code,
                status = _status
            )
            _row.update_record()

        _ser.update_record()
    elif _gen:
        response.js = "alertify.error('RV Already posted.')"

    # --------------- POSTING ON GEN. LEDGER ---------------

# -------------------   R E C E I P T  V O  U C H E R   ----------------------
# --------------------   RV  C O N F I R M A T I O N   -----------------------
def get_rv_confirmation_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('VOU.No.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db((db.Account_Voucher_Request.created_by == auth.user_id) & (db.Account_Voucher_Request.account_payment_mode_id == 4)).select(orderby = db.Account_Voucher_Request.id):
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-plus'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('account_transaction','post_receipt_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(work_lnk, prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(_vn.account_voucher_transaction_code,n.voucher_no),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.3F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return dict(table = table)

def post_receipt_voucher_confirmation():
    _total_amount = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    db.Account_Voucher_Request.voucher_no.default = _vn.voucher_serial_no + 1
    db.Account_Voucher_Request.status_id.default = 9
    if request.args(0):
        _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()
    form = SQLFORM(db.Account_Voucher_Request, request.args(0))    
    if form.process(onvalidation = validate_post_receipt_voucher).accepted:
        response.flash = 'RECORD SAVE'
        if not request.args(0):
            _vn.voucher_serial_no += 1
            _id = db(db.Account_Voucher_Request.created_by == auth.user_id).select().last()
            for n in db(db.Account_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select():
                _gl = db((db.General_Ledger.account_code == n.account_code_id) & (db.General_Ledger.account_reference_no == n.account_reference) & (db.General_Ledger.debit > 0)).select().first()
                n.update_record(account_voucher_request_id = _id.id)
                _gl.update_record(prepared = True)
            _vn.update_record()
            _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Account_Voucher_Transaction_Request.ticket_no_id == form.vars.ticket_no_id).select(_total_amount).first()[_total_amount]            
            _id.update_record(total_amount = _total_amount)
        elif request.args(0):            
            _id = db(db.Account_Voucher_Request.id == request.args(0)).select().first()
            for n in db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select():
                _gl = db((db.General_Ledger.account_code == n.account_code_id) & (db.General_Ledger.account_reference_no == n.account_reference) & (db.General_Ledger.debit > 0)).select().first()
                n.update_record(account_voucher_request_id = _id.id)            
                _gl.update_record(prepared = True)
            _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
            _id.update_record(total_amount = _total_amount)
        redirect(URL('account_transaction','get_receipt_voucher_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

def validate_post_receipt_voucher_confirmation_transaction(form):
    _id = db(db.Account_Voucher_Transaction_Request.account_reference == request.vars.account_reference).select().first()


@auth.requires_login()
def post_receipt_voucher_confirmation_transaction():
    db.Account_Voucher_Transaction_Request.ticket_no_id.default = session.ticket_no_id
    _ticket_no_ref = session.ticket_no_id
    form = SQLFORM.factory(db.Account_Voucher_Transaction_Request)
    if form.process(onvalidation = validate_post_receipt_voucher_confirmation_transaction).accepted:
        # if request.args(0):
        #     _av = db(db.Account_Voucher_Request.id == int(request.args(0))).select().first()
        #     _total_amount = db.Account_Voucher_Transaction_Request.amount_paid.sum().coalesce_zero()
        #     _total_amount = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
        #     _av.update_record(total_amount = _total_amount)
        response.js = "$('#AVTtbl').get(0).reload();"
    elif form.errors:
        response.flash = None
        response.js = "alertify.error('%s')" %(form.errors)
    ctr = _total_amount = 0
    row = []    
    head = THEAD(TR(TD('#'),TD('AC Code'),TD('Account Name'),TD('Dept.'),TD('Acct.Ref.'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
    _query = db(db.Account_Voucher_Transaction_Request.ticket_no_id == _ticket_no_ref).select()    
    if request.args(0):
        _query = db(db.Account_Voucher_Transaction_Request.account_voucher_request_id == request.args(0)).select()
    for n in _query:
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('account_transaction','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        _am = dc(dc.Master_Account.account_code == n.account_code_id).select().first()
        _serial = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
        _total_amount += float(n.amount_paid or 0)
        row.append(TR(
            TD(ctr),            
            TD(n.account_code_id),
            TD(_am.account_name),
            TD(n.dept_code_id.department_code),
            TD(n.account_reference),
            TD(n.description),
            TD(locale.format('%.3F', n.amount_paid or 0, grouping = True), _align='right'),
            TD(btn_lnk),
        ))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD(),TD(),TD('Total Amount'),TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align ='right'),TD()
    ))
    table = TABLE([head, body, foot], _class='table',_id='AVTtbl')
    return dict(form = form, table = table)

# --------------------   RV  C O N F I R M A T I O N   -----------------------


@auth.requires_login()
def get_business_unit_grid():
    row = []    
    form = SQLFORM(db.Business_Unit)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Business Name'),TH('Action')))
    for n in db().select(db.Business_Unit.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.business_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)    

@auth.requires_login()
def get_payment_voucher_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Receipt No.'),TH('Name'),TH('Amount'),TH('Status'),TH('Action')))
    for n in db().select(db.acctvou.ALL):
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.refdte),
            TD(n.refno),
            TD(n.person),
            TD(),
            TD(),
            TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(table = table)

@auth.requires_login()
def put_payment_voucher_form():
    form = SQLFORM(db.Account_Voucher)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

@auth.requires_login()
def load_payment_voucher_transaction_form():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Code'),TH('Department'),TH('Type'),TH('Ref.No.'),TH('Description'),TH('Amount'),TH('Action')))
    for n in db(db.Account_Transaction).select():
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD('Code'),
            TD('Department'),
            TD('Type'),
            TD('Ref.No.'),
            TD('Description'),
            TD('Amount'),
            TD('Control')))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    form = SQLFORM(db.Account_Transaction)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors: 
        resopnse.flash = 'FORM HAS ERRORS'
    return dict(form = form, table = table)

@auth.requires_login()
def get_department_grid():
    row = []    
    form = SQLFORM(db.Department)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Department Code'),TH('Department'),TH('Action')))
    for n in db().select(db.Department.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.department_code),TD(n.department_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)   

@auth.requires_login()
def get_department_head_grid():
    row = []    
    form = SQLFORM(db.Department_Head_Assignment)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Users ID'),TH('Department'),TH('Action')))
    for n in db().select(db.Department_Head_Assignment.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.users_id.first_name,' ', n.users_id.last_name),TD(n.department_id.department_code,' - ',n.department_id.department_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)   

# @auth.requires(lambda: auth.has_membership('BACK OFFICE DEPARTMENT') | auth.has_membership('ACCOUNTS') | auth.has_membership('DEPARTMENT MANAGERS') |  auth.has_membership('ACCOUNTS MANAGER')|  auth.has_membership('MANAGEMENT') |  auth.has_membership('ROOT'))
def get_debit_credit_note_grid():
    _headD = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Serial Note'),TH('Account Code'),TH('Department'),TH('Business Unit'),TH('Type'),TH('Amount',_style = "width:100px;"),TH('Status'),TH('Action Required'),TH('Action Control'),_class='bg-red'))
    if auth.has_membership('ACCOUNTS MANAGER'):
        _query = db(db.Debit_Credit.status_id == 1).select(db.Debit_Credit.ALL)
    elif auth.has_membership('ACCOUNTS'):
        _query = db((db.Debit_Credit.created_by == auth.user_id) & (db.Debit_Credit.status_id != 5)).select(db.Debit_Credit.ALL)
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        _query = db((db.Debit_Credit.department_id == _headD.department_id) & (db.Debit_Credit.status_id == 3)).select(db.Debit_Credit.ALL)
    elif auth.has_membership('MANAGEMENT') or auth.has_membership('ROOT'):
        _query = db(db.Debit_Credit.status_id == 4).select(db.Debit_Credit.ALL)    

    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('account_transaction','get_debit_credit_note_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')         
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD('DCN',n.serial_note),
            TD(n.account_code),
            TD(n.department_id.department_code,' - ',n.department_id.department_name),
            TD(n.business_unit.business_name),
            TD(n.transaction_type.upper()),
            TD(n.currency_id.mnemonic, ' ', locale.format('%.2F',n.total_amount or 0, grouping = True), _align = 'right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires_login()
def post_debit_credit_note_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    ctr = db(db.Transaction_Prefix.prefix_key == 'DCN').select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1
    db.Debit_Credit.serial_note.default = _skey
    # db.Debit_Credit.account_code.requires = SQLFORM.widgets.autocomplete(request, dc.Master_Account.account_code, id_field = dc.Master_Account.id, limitby = (0,10), min_length = 2)
    db.Debit_Credit.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.description == 'REQUESTED'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
    db.Debit_Credit.status_id.default = 4
    form = SQLFORM.factory(db.Debit_Credit)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        db.Debit_Credit_Transaction_Temporary.amount.sum()
        _sum = db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Debit_Credit_Transaction_Temporary.amount.sum()).first()[db.Debit_Credit_Transaction_Temporary.amount.sum()]
        _query = db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).select()
        db(db.Transaction_Prefix.prefix_key == 'DCN').update(current_year_serial_key = _skey)
        db.Debit_Credit.insert(
            serial_note = _skey,
            account_code = request.vars.account_code_id,
            account_type = form.vars.account_type,
            account_name = form.vars.account_name,
            account_address = form.vars.account_address,
            account_city = form.vars.account_city,
            account_country = form.vars.account_country,
            department_id = form.vars.department_id,
            business_unit = form.vars.business_unit,
            transaction_date = form.vars.transaction_date,
            transaction_type = form.vars.transaction_type,
            note_type = form.vars.note_type,
            currency_id = form.vars.currency_id,
            brand_code_id = form.vars.brand_code_id,                
            remarks = form.vars.remarks,
            status_id = form.vars.status_id,
            total_amount = _sum)
        _id = db(db.Debit_Credit.serial_note == _skey).select().first()
        ctr = _qr_value = 0
        for n in _query:
            ctr += 1
            _xrate = db(db.Currency.id == _id.currency_id).select().first()            
            _qr_value = float(_xrate.exchange_rate or 0) * float(n.amount or 0)
            db.Debit_Credit_Transaction.insert(
                serial_note_id = _id.id,
                serial_note_suffix_id = ctr, 
                transaction_date = request.now,
                # transaction_no = n.account_code,
                transaction_type = _id.account_type,
                account_code = n.account_code,
                description = n.description,
                date_from = n.date_from,
                date_to = n.date_to,
                amount = n.amount,
                qr_value = float(_qr_value or 0))
        db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).delete()
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        

    form2 = SQLFORM.factory(db.Debit_Credit_Transaction_Temporary)
    if form2.process(onvalidation = validate_trnx_load).accepted:
        response.flash = 'FORM SAVE'
        response.js = '$("#dctTemp").get(0).reload()'
        if db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnSubmit').removeAttr('disabled'), $('#dctTemp').get(0).reload()"        
    elif form2.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, form2 = form2, ctr = str('DCN%s') % (_skey), ticket_no_id = ticket_no_id)

def get_master_account_code():    
    _id = dc(dc.Master_Account.account_code == str(request.vars.account_code_id)).select().first()    
    response.js = "$('#btnMap').attr('disabled', 'disabled');console.log('%s')"  %(request.vars.account_code_id)
    if _id:
        _ad = dc(dc.Customer.customer_account_no == str(request.vars.account_code_id)).select().first()    
        response.js = "$('#account_name').val('%s'); $('#btnMap').removeAttr('disabled')" % (_id.account_name)

def put_account_code_address():
    _id = dc(dc.Master_Account.account_code == str(request.vars.account_code_id)).select().first()
    if _id:
        _ad = dc(dc.Customer.customer_account_no == st(request.vars.account_code_id)).select().first()
        response.js = "$('#account_name').val('%s');$('#account_address').val('%s');$('#account_city').val('%s');$('#account_address').val('%s');" % (_ad.contact_person, _ad.street_no, _ad.state, _ad.country)


def validate_trnx_load(form):
    form.vars.ticket_no_id = request.args(0)    
    if (float(request.vars.amount or 0) < 0.0) or (request.vars.amount == ""):
        form.errors.amount = 'value not allowed'
        response.js = "alertify.error('Amount value not allowed.');"
    if request.vars.account_code == "":
        form.errors.account_code = 'value not allowed'
        response.js = "alertify.error('Account Code should not empty.');"

@auth.requires_login()
def post_debit_credit_tranx_load():
    row = []
    ctr = _total_amount = 0
    
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Account Name'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')),_class='bg-red')
    for n in db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(session.ticket_no_id)).select(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1        
        _total_amount += n.amount or 0
        _id = dc(dc.Master_Account.account_code == n.account_code).select().first()
        _account_name = ''
        if _id:
            _account_name = _id.account_name
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _onclick="ajax('%s')" %URL('account_transaction','delete_debit_credit_tranx', args = [n.id, 1]))
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(TD(ctr),TD(n.account_code),TD(_account_name),TD(n.description),TD(n.date_from),TD(n.date_to),TD(locale.format('%.2F',n.amount or 0, grouping = True),_align='right'),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD('TOTAL AMOUNT: ',_colspan="5",_align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align='right'),TD()))
    table = TABLE(*[head, body, foot], _class='table table-condensed',_id='dctTemp')

    form = SQLFORM(db.Debit_Credit_Transaction_Temporary)
    if form.process(onvalidation = validate_trnx_load).accepted:
        response.flash = 'FORM SAVE'
        response.js = '$("#dctTemp").get(0).reload()'
        if db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
            response.js = "$('#btnSubmit').removeAttr('disabled'), $('#dctTemp').get(0).reload()"
        
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(table = table, form = form)

def delete_debit_credit_tranx():
    if int(request.args(1)) == 1:
        response.js = "alertify.confirm('Delete Record', 'Are you sure you want to delete this record?', function(){ ajax('%s'); alertify.success('Record Deleted.') }, function(){ alertify.error('Cancel')});" % URL('account_transaction','delete_debit_credit_tranx_id', args = [request.args(0), 1])
    elif int(request.args(1)) == 2:
        response.js = "alertify.confirm('Delete Record', 'Are you sure you want to delete this record?', function(){ ajax('%s'); alertify.success('Record Deleted.') }, function(){ alertify.error('Cancel')});" % URL('account_transaction','delete_debit_credit_tranx_id', args = [request.args(0), 2])

def delete_debit_credit_tranx_id():        
    if int(request.args(1)) == 1:
        db(db.Debit_Credit_Transaction_Temporary.id == request.args(0)).delete()
        response.js = '$("#dctTemp").get(0).reload()'
    elif int(request.args(1)) == 2:        
        _id = db(db.Debit_Credit_Transaction.id == request.args(0)).select().first()
        _id.update_record(delete = True)
        _total_amount = db.Debit_Credit_Transaction.amount.sum().coalesce_zero()
        _total_amount = db((db.Debit_Credit_Transaction.serial_note_id == _id.serial_note_id) & (db.Debit_Credit_Transaction.delete == False)).select(_total_amount).first()[_total_amount]
        db(db.Debit_Credit.id == _id.serial_note_id).update(total_amount = _total_amount)
        response.js = '$("#dctTrnx").get(0).reload()'


def get_account_info_id():
    _id = dc(dc.Master_Account.account_code == request.vars.account_code).select().first()    
    if _id:        
        _info = TABLE(
            TR(TD('Account Code'),TD('Account Name')),
            TR(TD(_id.account_code),TD(_id.account_name))        
        ,_style="width:100%")
        response.js = "notie.alert({ type:'info',text: '%s', position: 'bottom'  }) " % (_info)
    else:
        # response.js = "notie.alert({ type: 'error', text: '%s not found!',position: 'bottom'  })" % (request.vars.account_code)
        response.js = "alertify.set('notifier','position', 'bottom-center'); alertify.error('%s not found.');" % (request.vars.account_code)

def put_debit_credit_note_id():
    _row = db(db.Debit_Credit.id == request.args(0)).select().first()
    db.Debit_Credit.status_id.requires = IS_IN_DB(db((db.Note_Status.id == 1) | (db.Note_Status.id == 2)), db.Note_Status.id, '%(status)s', zero = 'Choose Status')
    db.Debit_Credit.status_id.default = 1
    form = SQLFORM(db.Debit_Credit, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, row = _row)

def put_debit_credit_tranx_load():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()    
    row = []
    ctr = _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(_id.ticket_no)).select(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1        
        _total_amount += n.amount
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete='tr',_id='del',callback=URL('put_del_tmp', args = n.id,extension=False))        
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_colspan="5"),TD('TOTAL AMOUNT: '),TD(_total_amount),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='dctTemp')
    form = SQLFORM(db.Debit_Credit_Transaction_Temporary)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        resposne.flash = 'FORM HAS ERROR'
    return dict(table = table, form = form)

def post_debit_credit_tranx_tmp():
    print 'send...', request.vars.account_code,request.vars.description_1,request.vars.description_2,request.vars.date_from,request.vars.date_to,request.vars.amount

def post_debit_credit_tranx_tmp_():
    # print 'send...', request.vars.account_code,request.vars.description_1,request.vars.description_2,request.vars.date_from,request.vars.date_to,request.vars.amount
    db.Debit_Credit_Transaction_Temporary.insert(
        account_code = request.vars.account_code,
        description_1 = request.vars.description_1,
        description_2 = request.vars.description_2,
        date_from = request.vars.date_from,
        date_to = request.vars.date_to,
        amount = request.vars.amount,
        ticket_no_id = request.vars.ticket_no_id
    )
    
    if db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == session.ticket_no_id).count() != 0:
        response.js = "$('#btnSubmit').removeAttr('disabled'), $('#dctTemp').get(0).reload()"
    else:
        response.js = "$('#btnsubmit').attr('disabled','disabled')"        
    # response.js="$('#dctTemp').get(0).reload()"

def put_debit_credit_tranx_tmp():
    print 'put_debit_credit_tranx_tmp: ', request.vars.account_code, request.vars.ticket_no_id
    # db.Debit_Credit_Transaction_Temporary.insert(
    #     account_code = request.vars.account_code,
    #     description_1 = request.vars.description_1,
    #     description_2 = request.vars.description_2,
    #     date_from = request.vars.date_from,
    #     date_to = request.vars.date_to,
    #     amount = request.vars.amount,
    #     ticket_no_id = request.vars.ticket_no_id
    # )

def put_account_code_address_id():
    print(":"), request.vars.account_name
    db(db.Debit_Credit.id == request.args(0)).update(
        account_name = request.vars.account_name,
        account_address = request.vars.account_address,
        account_city = request.vars.account_city,
        account_country = request.vars.account_country
    )
    # _id = dc(dc.Debit_Credit.id == request.vars.account_code).select().first()
    # response.js = "$('#account_name').val('%s');$('#account_address').val('%s');$('#account_city').val('%s');$('#account_address').val('%s');" % (_ad.contact_person, _ad.street_no, _ad.state, _ad.country)

def get_debit_credit_trnax_tmp():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()    
    row = []
    ctr = _total_amount = 0
    # print 'od', request.args(0)
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(_id.ticket_no)).select(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1        
        _total_amount += n.amount
        # print 'get_debit_credit_trnax_tmp', n.ticket_no_id
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', delete='tr',_id='del',callback=URL('put_del_tmp', args = n.id,extension=False))                
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD(btn_lnk)))
    
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_colspan="5"),TD('TOTAL AMOUNT: '),TD(_total_amount),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='dctTemp')
    print 'get_debit_credit_trnax_tmp'
    return XML(table)
 
@auth.requires_login()
def get_debit_credit_note_id():
    _row = db(db.Debit_Credit.id == request.args(0)).select().first()
    _id = dc(dc.Master_Account.account_code == _row.account_code).select().first()
    _account_name = ''
    if _id:
        _account_name = str(_row.account_code)+ ', ' + str(_id.account_name)
    form = SQLFORM(db.Debit_Credit, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM UPDATED'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, row = _row, _account_name = _account_name)

def get_debit_credit_trnax():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()    
    row = []
    ctr = _total_amount = 0

    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Account Name'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')),_class='bg-red')
    for n in db((db.Debit_Credit_Transaction.serial_note_id == int(request.args(0))) & (db.Debit_Credit_Transaction.delete == False)).select(db.Debit_Credit_Transaction.ALL):
        ctr += 1        
        _total_amount += n.amount
        _id = dc(dc.Master_Account.account_code == n.account_code).select().first()
        _account_name = ''
        if _id:
            _account_name = _id.account_name        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _onclick="ajax('%s')" % URL('account_transaction','delete_debit_credit_tranx', args = [n.id, 2]))
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target='_blank', _class='btn btn-icon-toggle', _href=URL('account_transaction_reports','get_debit_credit_note_transaction_id',args = n.id, extension=False))
        btn_lnk = DIV(dele_lnk, prin_lnk)
        row.append(TR(TD(ctr),TD(n.account_code),TD(_account_name),TD(n.description),TD(n.date_from),TD(n.date_to),TD(locale.format('%.2F',n.amount or 0, grouping = True),_align ='right'),TD(btn_lnk)))    
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_colspan="5"),TD('TOTAL AMOUNT: '),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align ='right'),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='dctTrnx')    
    form = SQLFORM.factory(
        Field('account_code','string', length = 20),
        Field('description','string'),    
        Field('date_from','date'),
        Field('date_to','date'),
        Field('amount','decimal(10,2)'))
    if form.process(onvalidation = validate_trnx_load):
        print('submit')
    elif form.errors:
        print('form errors'), form.errors        
    return dict(form = form, table = table)
 
def put_del_tmp():        
    db(db.Debit_Credit_Transaction_Temporary.id == request.args(0)).delete()
    response.js = "$('#dctTemp').get(0).reload()"
    # response.js="$('#del').parent('div').parent('td').parent('tr').fadeOut('slow');"

def put_debit_credit_note_approved_id():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()
    if auth.has_membership('ACCOUNTS MANAGER'):
        db(db.Debit_Credit.id == request.args(0)).update(status_id = 3)
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        db(db.Debit_Credit.id == request.args(0)).update(status_id = 4)
    elif auth.has_membership('MANAGEMENT'):
        db(db.Debit_Credit.id == request.args(0)).update(status_id = 5)
        if _id.transaction_type == "Debit Note": # debit note
            if _id.business_unit == 1: # business unit 'Merch & Partners WLL'
                _px = db(db.Transaction_Prefix.prefix_key == 'DMP').select().first()                
                process(_px.prefix, _px.current_year_serial_key, _px.id)
            else: # business unit 'Merch Trading Company'
                _px = db(db.Transaction_Prefix.prefix_key == 'DMT').select().first()
                process(_px.prefix, _px.current_year_serial_key, _px.id)
        else: # credit note
            if _id.business_unit == 1: # business unit 'Merch & Partners WLL'
                _px = db(db.Transaction_Prefix.prefix_key == 'CMP').select().first()
                process(_px.prefix, _px.current_year_serial_key, _px.id)
            else: # business unit 'Merch Trading Company'
                _px = db(db.Transaction_Prefix.prefix_key == 'CMT').select().first()
                process(_px.prefix, _px.current_year_serial_key, _px.id)
        redirect(URL('account_transaction','get_debit_credit_note_grid'))

def process(x, y, z):
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()
    _query = db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(_id.ticket_no)).select()    
    for n in _query:        
        y+=1        
        _tnx = str(x)+str(y)
        db.Debit_Credit_Transaction.insert(
            serial_note_id = _id.id,
            transaction_no = _tnx,
            account_code = n.account_code,
            description_1 = n.description_1,
            description_2 = n.description_2,
            date_from = n.date_from,
            date_to = n.date_to,
            amount =  n.amount)
    db(db.Transaction_Prefix.id == int(z)).update(current_year_serial_key = y) # updated prefix transaction
    db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(_id.ticket_no)).delete() 

def put_debit_credit_note_reject_id():
    db(db.Debit_Credit.id == request.args(0)).update(status_id = 2)

def put_debit_credit_note_remarks_id():
    if auth.has_membership('ACCOUNTS MANAGER'):
        db(db.Debit_Credit.id == request.args(0)).update(account_remarks = request.vars.account_remarks)
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        db(db.Debit_Credit.id == request.args(0)).update(department_remarks = request.vars.department_remarks)
    elif auth.has_membership('MANAGEMENT'):
        db(db.Debit_Credit.id == request.args(0)).update(management_remakrs = request.vars.management_remakrs)
    else:        
        db(db.Debit_Credit.id == request.args(0)).update(remarks = request.vars.remarks)        
    response.js = "alertify.success('Remarks posted.')"

def cancel_debit_credit_note_id():    
    db(db.Debit_Credit.id == request.args()).update(cancelled = True)

def get_debit_credit_note_grid_reports():
    _headD = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Serial Note'),TH('Department'),TH('Business Unit'),TH('Type'),TH('Status'),TH('Action Required'),TH('Action Control')))
    if auth.has_membership('ACCOUNTS MANAGER'):
        _query = db(db.Debit_Credit.status_id == 1).select(db.Debit_Credit.ALL)
    elif auth.has_membership('ACCOUNTS'):
        _query = db((db.Debit_Credit.created_by == auth.user_id) & (db.Debit_Credit.status_id == 5)).select(db.Debit_Credit.ALL)
    elif auth.has_membership('DEPARTMENT MANAGERS'):
        _query = db((db.Debit_Credit.department_id == _headD.department_id) & (db.Debit_Credit.status_id == 3)).select(db.Debit_Credit.ALL)
    elif auth.has_membership('MANAGEMENT'):
        _query = db(db.Debit_Credit.status_id == 4).select(db.Debit_Credit.ALL)    

    for n in _query:
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('account_transaction','get_debit_credit_note_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = (URL('account_transaction','put_debit_credit_note_id', args = n.id)))         
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _class='btn btn-icon-toggle disabled')
        if n.status_id > 2:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href = (URL('account_transaction','put_debit_credit_note_id', args = n.id)))
        else:
            edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href = (URL('account_transaction','put_debit_credit_note_id', args = n.id)))                 
        if int(n.status_id) == 5:                
            prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target=' blank',_class='btn btn-icon-toggle',_href = URL('transaction_reports','get_debit_credit_note_id', args = n.id))

        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk, prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD('DCN',n.serial_note),
            TD(n.department_id.department_code,' - ',n.department_id.department_name),
            TD(n.business_unit.business_name),
            TD(n.transaction_type),
            TD(n.status_id.status),
            TD(n.status_id.action_required),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)    


def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


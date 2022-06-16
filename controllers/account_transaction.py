
import string, random, locale, datetime
locale.setlocale(locale.LC_ALL, '')

def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

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

def get_general_ledger_account_transaction_id():
    if int(request.args(0)) == 21:
        _id = db(db.Receipt_Voucher_Header.id == request.args(1)).select().first()
        if not _id:
            response.js = "alertify.notify('Account Ref. is empty or not found.','warning')"
            return
        elif _id:
            table = TABLE('TABLE')

    elif int(request.args(0)) == 22:
        _id = db(db.Receipt_Voucher_Confirmation.id == request.args(1)).select().first()
        if not _id:
            response.js = "alertify.notify('Account Ref. is empty or not found.','warning')"
            return
        elif _id: 
            table = TABLE(
                TR(TD('Trnx Date'),TD('Trnx Code'),TD('Voucher No'),TD('Account Ref.'),TD('Payment Mode'),TD('Payment Code'),TD('Total Amount'),TD('Bank Name'),TD('Cheque No.'),TD('Cheque Date')),
                    TR(
                        TD(_id.transaction_reference_date),
                        TD(_id.account_voucher_transaction_code),
                        TD(),
                        TD(),
                        TD(),
                        TD(),
                        TD(),
                        TD(),
                        TD(),
                        TD(),
                        TD())
                )
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'General Ledger','message':'%s'}).show();" %(XML(table, sanitize = True))    

def get_general_ledger_account_transaction_idx():
    _id = db(db.General_Ledger.id == request.args(0)).select().first()
    table = TABLE(
        TR(TD('Date'),TD('Transaction Type'),TD('Transaction No'),TD('Account Ref No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Amount Paid'),TD('Description'),TD('Reff.')),
        TR(
            TD(_id.transaction_date),
            TD(_id.transaction_type),
            TD(_id.transaction_prefix_id.prefix,_id.transaction_no),
            TD(_id.account_reference_no),
            TD(_id.account_code),
            TD(locale.format('%.3F',_id.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.3F',_id.credit or 0, grouping = True), _align='right'),
            TD(locale.format('%.3F',_id.amount_paid or 0, grouping = True), _align='right'),
            TD(_id.description),
            TD(_id.gl_entry_ref)),_class='table')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'General Ledger','message':'%s'}).show();" %(XML(table, sanitize = True))    
    
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
# -------------------------------- BEGIN ---------------------------------
# -------------------   ACCOUNT TRANSACTIONS GRID   ----------------------
# ------------------------------------------------------------------------
@auth.requires_login()
def get_account_transaction_grid_id():
    if int(request.args(0)) == 1:
        header = 'Receipt Voucher Transaction Grid'
        table = LOAD('account_transaction','get_receipt_voucher_grid.load', ajax = True, extension = False)
    elif int(request.args(0)) == 2:
        header = 'RV Confirmation Transaction Grid'
        table = LOAD('account_transaction','get_rv_confirmation_grid.load', ajax = True, extension = False)
    elif int(request.args(0)) == 3:
        header = 'Payment Voucher Transaction Grid'
        table = LOAD('account_transaction','get_payment_voucher_grid.load', ajax = True, extension = False)
    elif int(request.args(0)) == 4:
        header = 'Journal Voucher Transaction Grid'
        table = LOAD('account_transaction','get_journal_voucher_grid.load', ajax = True, extension = False)
    elif int(request.args(0)) == 5:
        header = 'Debit/Credit Note Transaction Grid'
        table = LOAD('account_transaction','get_debit_credit_note_grid.load', ajax = True, extension = False)
    elif int(request.args(0)) == 6:
        header = 'Account Reconciliation Transaction Grid'
        table = LOAD('account_transaction','get_account_reconciliation_grid.load', ajax = True, extension = False)

    return dict(header=header, table = table)

@auth.requires_login()
def get_receipt_voucher_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Type'),TD('Code'),TD('Account Code'),TD('Account Reference'),TD('RVC Ref.'),TD('RVC Type'),TD('Total Amount'),TD('Created By'),TD('Status'),TD()),_class='bg-red')
    for n in db(db.Receipt_Voucher_Header.status_id == 11).select(orderby = db.Receipt_Voucher_Header.id):
        ctr += 1
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Record', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),            
            TD(n.account_code),            
            TD(n.account_reference),
            TD(n.rv_confirmation_reference),
            TD(n.receipt_voucher_confirmation_type_id),

            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.requested_by),
            # TD(n.requested_by.first_name,' ',n.requested_by.last_name[0],'.'),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table table-hover',_id='TBLAct')
    return table

def get_rv_confirmation_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Type'),TD('Code'),TD('Account Code'),TD('Account Reference'),TD('Total Amount'),TD('Created By'),TD('Status'),TD()),_class='bg-red')
    for n in db(db.Receipt_Voucher_Confirmation.status_id == 11).select(orderby = db.Receipt_Voucher_Confirmation.id):
        ctr += 1
        prin_lnk = A(I(_class='fas fa-print'), _title='Print Record', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),
            TD(n.account_code),
            TD(n.account_reference),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.created_by),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table table-hover')
    return table

@auth.requires_login()
def get_payment_voucher_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Type'),TD('Code'),TD('Payment Vou. #'),TD('Account Code'),TD('Payee'),TD('Payment Mode'),TD('Cheque No.'),TD('Cheque Dated'),TD('Inv #'),TD('Total Amount'),TD('Created By'),TD('Status'),TD()),_class='bg-red')
    _query = db().select(orderby = db.Payment_Voucher_Header.id)
    for n in _query:
        ctr += 1
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('workflow_payment_voucher_reports','get_payment_voucher_no_id',args = n.payment_voucher_no, extension = False))    
        btn_lnk = DIV(prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),
            TD(n.account_voucher_transaction_code,n.payment_voucher_no),
            TD(n.account_code),
            TD(n.payee),
            TD(n.account_payment_mode_id.account_voucher_payment_name),
            TD(n.cheque_no),
            TD(n.cheque_dated),
            TD(n.custom_invoice_no),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.requested_by),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return table

@auth.requires_login()
def get_journal_voucher_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Type'),TD('Code'),TD('Account Ref.'),TD('Total Amount'),TD('Created By'),TD('Status'),TD()),_class='bg-red')    
    _query = db(db.Journal_Voucher_Header.status_id == 19).select(orderby = db.Journal_Voucher_Header.id)
    for n in _query:
        ctr += 1
        prin_lnk = A(I(_class='fas fa-print'), _title='Print', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(prin_lnk)        
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),
            TD(n.account_reference),            
            TD(locale.format('%.2F',n.total_amount or 0, grouping = True),_align='right'),            
            TD(n.requested_by),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return table

@auth.requires_login()
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
    return table

@auth.requires_login()
def get_account_reconciliation_grid():
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Trnx No'),TD('Voucher No'),TD('Total Amount'),TD('Current Amount Recon.'),TD('Total Amount Recon.'),TD('Balanced'),TD('Requestd By'),TD('Status'),TD()),_class='bg-red')    
    _query = db(db.Account_Reconciliation_Header.status_id == 22).select()
    for n in _query:
        ctr += 1
        
        view_lnk = A(I(_class='fas fa-search'), _title='View', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_account_reconciliation_id',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='Reconcile RV', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('account_reconciliation_reports','get_account_reconciliation_id',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk,prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.reconciliation_date),
            TD('AR',n.reconciliation_transaction_no),            
            TD('RV',n.voucher_no),            
            TD(locale.format('%.2F', n.rv_amount or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F', n.reconciled_amount_entry or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F', n.total_reconciled_amount or 0, grouping = True),_align='right'),            
            TD(locale.format('%.2F', n.rv_balanced_amount or 0, grouping = True),_align='right'),
            TD(n.requested_by.first_name,' ',n.requested_by.last_name[0],'.'),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table table-striped table-hover',_id='TBLAct')
    return table

# ----------------------------------------------------------------------------
# -------------------   ACCOUNT TRANSACTIONS GRID   --------------------------
# -------------------------------- END ---------------------------------------

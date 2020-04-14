import string, random

def get_transaction_prefix_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Prefix'),TH('Name'),TH('CS'),TH('PS'),TH('Prefix Key'),TH('Action Control')))
    for n in db().select(db.Transaction_Prefix.ALL):
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)

        row.append(TR(
            TD(ctr),
            TD(n.prefix),
            TD(n.prefix_name),
            TD(n.current_year_serial_key),
            TD(n.previous_year_serial_key),
            TD(n.prefix_key),
            TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    
    form = SQLFORM(db.Transaction_Prefix)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, table = table)

def get_debit_credit_status_grid():
    row = []    
    form = SQLFORM(db.Note_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action Required'),TH('Description'),TH('Action')))
    for n in db().select(db.Note_Status.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.action_required),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)    

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

def put_payment_voucher_form():
    form = SQLFORM(db.Account_Voucher)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form)

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

def get_currency_grid():
    row = []    
    form = SQLFORM(db.Currency)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Status'),TH('Action')))
    for n in db().select(db.Currency.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.status_id.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)       

def get_status_grid():
    row = []    
    form = SQLFORM(db.Record_Status)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action')))
    for n in db().select(db.Record_Status.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)   

def get_brand_grid():
    row = []    
    form = SQLFORM(db.Stand_Rent_Brand)
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Brand Code'),TH('Brand Name'),TH('Action')))
    for n in db().select(db.Stand_Rent_Brand.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.brand_code),TD(n.brand_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)   

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

@auth.requires(lambda: auth.has_membership('BACK OFFICE DEPARTMENT') | auth.has_membership('ACCOUNTS') | auth.has_membership('DEPARTMENT MANAGERS') |  auth.has_membership('ACCOUNTS MANAGER')|  auth.has_membership('MANAGEMENT') |  auth.has_membership('ROOT'))
def get_debit_credit_note_grid():
    _headD = db(db.Department_Head_Assignment.users_id == auth.user_id).select().first()
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Serial Note'),TH('Department'),TH('Business Unit'),TH('Type'),TH('Status'),TH('Action Required'),TH('Action Control')))
    if auth.has_membership('BACK OFFICE DEPARTMENT'): # accounts users as requestor
        _query = db(db.Debit_Credit.created_by == auth.user_id).select(db.Debit_Credit.ALL)    
    elif auth.has_membership('ACCOUNTS MANAGER'):
        _query = db(db.Debit_Credit.status_id == 1).select(db.Debit_Credit.ALL)
    elif auth.has_membership('ACCOUNTS'):
        _query = db(db.Debit_Credit.status_id == 1).select(db.Debit_Credit.ALL)
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
        if auth.has_membership('BACK OFFICE DEPARTMENT'):      
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

def post_debit_credit_note_form():
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id

    ctr = db(db.Transaction_Prefix.prefix_key == 'DCN').select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1

    db.Debit_Credit.status_id.requires = IS_IN_DB(db(db.Note_Status.id == 1), db.Note_Status.id, '%(status)s', zero = 'Choose Status')
    db.Debit_Credit.status_id.default = 1
    db.Debit_Credit.serial_note.default = _skey
    form = SQLFORM.factory(db.Debit_Credit)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
        db.Debit_Credit_Transaction_Temporary.amount.sum()
        _sum = db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).select(db.Debit_Credit_Transaction_Temporary.amount.sum()).first()[db.Debit_Credit_Transaction_Temporary.amount.sum()]
        _query = db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(request.vars.ticket_no_id)).select()
        db(db.Transaction_Prefix.prefix_key == 'DCN').update(current_year_serial_key = _skey)
        db.Debit_Credit.insert(
            serial_note = _skey,
            department_id = form.vars.department_id,
            business_unit = form.vars.business_unit,
            transaction_date = form.vars.transaction_date,
            transaction_type = form.vars.transaction_type,
            note_type = form.vars.note_type,
            currency_id = form.vars.currency_id,
            brand_code_id = form.vars.brand_code_id,                
            remarks = form.vars.remarks,
            status_id = form.vars.status_id,
            total_amount = _sum,
            ticket_no = request.vars.ticket_no_id
        )
        # print 'insert: ', _skey, _sum, request.vars.ticket_no_id
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
    return dict(form = form, ctr = str('DCN%s') % (_skey), ticket_no_id = ticket_no_id)

def post_debit_credit_tranx_load():
    row = []
    ctr = _total_amount = 0
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(session.ticket_no_id)).select(db.Debit_Credit_Transaction_Temporary.ALL):
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

def get_debit_credit_note_id():
    _row = db(db.Debit_Credit.id == request.args(0)).select().first()
    return dict(row = _row)

def get_debit_credit_trnax_tmp():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()    
    row = []
    ctr = _total_amount = 0
    print 'od', request.args(0)
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction_Temporary.ticket_no_id == str(_id.ticket_no)).select(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1        
        _total_amount += n.amount
        print 'get_debit_credit_trnax_tmp', n.ticket_no_id
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', delete='tr',_id='del',callback=URL('put_del_tmp', args = n.id,extension=False))                
        btn_lnk = DIV(dele_lnk)                
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD(btn_lnk)))
    
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_colspan="5"),TD('TOTAL AMOUNT: '),TD(_total_amount),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='dctTemp')
    print 'get_debit_credit_trnax_tmp'
    return XML(table)
 
def get_debit_credit_trnax():
    _id = db(db.Debit_Credit.id == request.args(0)).select().first()    
    row = []
    ctr = _total_amount = 0

    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction.serial_note_id == int(request.args(0))).select(db.Debit_Credit_Transaction.ALL):
        ctr += 1        
        _total_amount += n.amount
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', delete='tr',_id='del',callback=URL('put_del_tmp', args = n.id,extension=False))        
        prin_lnk = A(I(_class='fa fa-print'), _title='Print', _type='button ', _role='button', _target='_blank', _class='btn btn-icon-toggle')
        btn_lnk = DIV(dele_lnk, prin_lnk)
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD(btn_lnk)))
    
    body = TBODY(*row)
    foot = TFOOT(TR(TD(_colspan="5"),TD('TOTAL AMOUNT: '),TD(_total_amount),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='dctTrnx')
    print 'get_debit_credit_trnax'
    return XML(table)
 
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
        print 'else'


def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

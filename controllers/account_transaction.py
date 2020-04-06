import string, random

def get_transaction_prefix_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Prefix'),TH('Name'),TH('CS'),TH('PS'),TH('Prefix Key'),TH('Action Control')))
    for n in db().select(db.Transaction_Prefix.ALL):
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD(n.prefix),
            TD(n.prefix_name),
            TD(n.current_year_serial_key),
            TD(n.previous_year_serial_key),
            TD(n.prefix_key),
            TD()))
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

def get_debit_credit_note_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Date'),TH('Serial Note'),TH('Department'),TH('Type'),TH('Status'),TH('Action Required'),TH('Action Control')))
    _query = db().select(db.Debit_Credit.ALL)
    for n in _query:
        ctr+=1
        row.apped(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD(n.serial_note),
            TD(n.department_id),
            TD(n.transaction_type),
            TD(n.status_id),
            TD()
        ))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)


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

def post_debit_credit_note_form():
    ctr = db(db.Transaction_Prefix.prefix_key == 'DCN').select().first()
    _skey = ctr.current_year_serial_key
    _skey += 1

    db.Debit_Credit.status_id.requires = IS_IN_DB(db(db.Note_Status.id == 1), db.Note_Status.id, '%(status)s', zero = 'Choose Status')
    db.Debit_Credit.status_id.default = 1
    db.Debit_Credit.serial_note.default = _skey
    form = SQLFORM(db.Debit_Credit)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id

    return dict(form = form, ctr = str('DCN%s') % (_skey), ticket_no_id = ticket_no_id)

def post_debit_credit_tranx_load():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db().select(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1        
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', delete='tr',_id='del',callback=URL('put_del_tmp', args = n.id,extension=False))        
        btn_lnk = DIV(dele_lnk)        
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table',_id='dctTemp')
    form = SQLFORM(db.Debit_Credit_Transaction_Temporary)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        resposne.flash = 'FORM HAS ERROR'
    return dict(table = table, form = form)

def put_del_tmp():    
    # print 'delete'
    db(db.Debit_Credit_Transaction_Temporary.id == request.args(0)).delete()
    # response.js="$('#del').parent('div').parent('td').parent('tr').fadeOut('slow');"

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
        response.js = "$('#btnsubmit').removeAttr('disabled')"
    else:
        response.js = "$('#btnsubmit').attr('disabled','disabled')"        
    response.js="$('#dctTemp').get(0).reload()"

def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

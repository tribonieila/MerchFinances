def get_transaction_prefix_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Prefix'),TH('Name'),TH('CS'),TH('PS'),TH('Action Control')))
    for n in db().select(db.Transaction_Prefix.ALL):
        ctr+=1
        row.append(TR(
            TD(ctr),
            TD(n.prefix),
            TD(n.prefix_name),
            TD(n.current_year_serial_key),
            TD(n.previous_year_serial_key),
            TD(n.prefix_key)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    
    form = SQLFORM(db.Transaction_Prefix)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, table = table)

def get_account_transaction_prefix_grid():
    row = []
    head = THEAD(TR(TH('#'),TH('Prefix'),TH('Prefix Name'),TH('')))
    return dict(table = 'table')

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

def put_debit_credit_note_form():

    form = SQLFORM(db.Debit_Credit)
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, ctr = 'ctr')

def put_debit_credit_tranx_load():
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Account Code'),TH('Description'),TH('Description'),TH('Date From'),TH('Date To'),TH('Amount'),TH('Action')))
    for n in db(db.Debit_Credit_Transaction_Temporary.ALL):
        ctr += 1
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.description_1),TD(n.description_2),TD(n.date_from),TD(n.date_to),TD(n.amount),TD('action')))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)
def get_account_transaction_prefix_grid():
    row []
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
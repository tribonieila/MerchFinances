@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_receipt_voucher_draft_grid():
    table = SQLFORM.smartgrid(db.Account_Voucher_Request)
    return dict(table = table)
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_bank_master_grid():
    db.Bank_Master.status_id.default = 1
    form = SQLFORM(db.Bank_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Bank Code'),TH('Bank Name Name'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Bank_Master.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_bank_master_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.bank_code),TD(n.bank_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_general_department_grid():
    form = SQLFORM(db.General_Department_Cost_Center, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Department Code'),TH('Department Name'),TH('Cost Center'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.General_Department_Cost_Center.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_general_department_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.department_code),TD(n.department_name),TD(n.cost_center),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_location_cost_grid():
    form = SQLFORM(db.General_Location_Cost_Center, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Location Code'),TH('Location Name'),TH('Cost Center'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.General_Location_Cost_Center.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_location_cost_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.location_code),TD(n.location_name),TD(n.cost_center),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_transaction_payment_type_grid():
    form = SQLFORM(db.Transaction_Payment_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('TXN Payment Type'),TH('TXN Payment Name'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Transaction_Payment_Type.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_transaction_payment_type_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.transaction_payment_type),TD(n.transaction_payment_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_gl_transaction_serial_grid():
    form = SQLFORM(db.GL_Transaction_Serial, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Prefix'),TH('Prefix Name'),TH('Serial'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.GL_Transaction_Serial.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_gl_transaction_serial_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.serial_number),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_accounts_workflow_status_grid():
    form = SQLFORM(db.Accounts_Workflow_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Required Action'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Accounts_Workflow_Status.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_accounts_workflow_status_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.required_action),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_general_account_grid():
    form = SQLFORM(db.General_Account, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Selective Tax Payable Account'),TH('Selective Tax Receivable Account'),TH('Claim Receivable Account'),TH('Provision E-Commerce Delivery Income'),TH('Receipt Voucher Account'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.General_Account.id):        
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_general_account_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.selective_tax_payable_account),TD(n.selective_tax_receivable_account),TD(n.claim_receivable_account),TD(n.provision_delivery_income),TD(n.receipt_voucher_account),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_gl_description_library_grid():
    form = SQLFORM(db.GL_Description_Library, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []    
    thead = THEAD(TR(TH('#'),TH('Trnx Type'),TH('Prefix'),TH('Order No'),TH('Purchase Receipt No'),TH('Short Supply'),TH('Excise Tax'),TH('Damaged Supply'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.GL_Description_Library.id):                
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_gl_description_library_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.transaction_type),TD(n.transaction_prefix_text),TD(n.order_no_text),TD(n.purchase_receipt_no_text),TD(n.short_supply_text),TD(n.excise_tax_text),TD(n.damaged_supply_text),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))
def get_account_transaction_type_grid():
    form = SQLFORM(db.Account_Voucher_Type, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    thead = THEAD(TR(TD('#'),TD('VOU.Serial.No.'),TD('Transaction Type'),TD('Transaction Code'),TD('Transaction Name'),TD('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Account_Voucher_Type.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_account_transaction_type_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.voucher_serial_no),TD(n.account_voucher_transaction_type),TD(n.account_voucher_transaction_code),TD(n.account_voucher_transaction_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_account_transaction_payment_mode_grid():
    form = SQLFORM(db.Account_Voucher_Payment_Mode, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    thead = THEAD(TR(TD('#'),TD('VOU.Payment Code'),TD('VOU.Payment Name'),TD('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Account_Voucher_Payment_Mode.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_account_transaction_payment_mode_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_voucher_payment_code),TD(n.account_voucher_payment_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)


@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_financial_statement_group_grid():
    form = SQLFORM(dc.Financial_Statement_Group, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Financial Statement Group Name'),TH('Action'),_class = 'bg-red'))
    for n in dc().select(orderby = dc.Financial_Statement_Group.id):        
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_financial_statement_group_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.financial_statement_group_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_chart_of_accounts_grid():
    _id = dc(dc.Master_Chart_Account_Prefix_Serial.id).count()
    form = SQLFORM(dc.Master_Chart_Account_Prefix_Serial, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error'
    row = []
    head = THEAD(TR(TD('#'),TD('Prefix'),TD('Prefix Name'),TD('Account Sub-Group Name'),TD('Serial'),TD('Prefix Key'),TD('Action')),_class='bg-red')
    for n in dc().select(orderby = dc.Master_Chart_Account_Prefix_Serial.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('get_chart_of_accounts_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.account_group_name),TD(n.serial_key),TD(n.prefix_key),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_transaction_prefix_grid():   
    form = SQLFORM(db.Transaction_Prefix, request.args(0))
    if form.process().accepted:
        response.flash = 'FORM SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'        
    row = []
    ctr = 0
    head = THEAD(TR(TH('#'),TH('Prefix'),TH('Name'),TH('CS'),TH('PS'),TH('Prefix Key'),TH('Action Control'),_class = 'bg-red'))
    for n in db().select(orderby = db.Transaction_Prefix.id):
        ctr+=1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_transaction_prefix_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix),TD(n.prefix_name),TD(n.current_year_serial_key),TD(n.previous_year_serial_key),TD(n.prefix_key),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='TRNXtbl')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_debit_credit_status_grid():
    row = []    
    form = SQLFORM(db.Note_Status, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Status'),TH('Action Required'),TH('Description'),TH('Action'),_class = 'bg-red'))
    for n in db().select(db.Note_Status.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_debit_credit_status_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.status),TD(n.action_required),TD(n.description),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)    

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))            
def get_chart_account_main_group():
    form = SQLFORM(dc.Chart_Account_Main_Group, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    ctr = 0
    row = []
    thead = THEAD(TR(TH('#'),TH('Chart Account Main Group'),TH('Financial Statement Group'),TH('Action'),_class = 'bg-red'))
    for n in dc().select(orderby = dc.Chart_Account_Main_Group.id):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_chart_account_main_group', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        if n.financial_statement_id == None:
            _fin = 'None'
        else:
            _fin = n.financial_statement_id.financial_statement_group_name
        row.append(TR(TD(n.id),TD(n.chart_account_main_group_name),TD(_fin),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_batch_posting_sequence():
    form = SQLFORM(db.Batch_Posting_Sequence, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []    
    thead = THEAD(TR(TH('#'),TH('Prefix Sequence'),TH('Prefix Sequence Description'),TH('Sequence No'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Batch_Posting_Sequence.id):                
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_batch_posting_sequence', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.prefix_seq),TD(n.prefix_seq_name),TD(n.sequence_no),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table table-hover')
    return dict(form = form, table = table)

def get_stand_rent_grid():
    row = []    
    form = SQLFORM(db.Stand_Rent_Brand, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'

    thead = THEAD(TR(TH('#'),TH('Brand Code'),TH('Brand Name'),TH('Action'),_class='bg-red'))
    for n in db().select(db.Stand_Rent_Brand.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _href=URL('#', args = n.id))        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.brand_code),TD(n.brand_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)  

def get_currency_grid():
    row = []    
    db.Currency.status_id.default = 'Active'
    form = SQLFORM(db.Currency, request.args(0))
    if form.process().accepted:
        response.flash = 'RECORD SAVE'
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    thead = THEAD(TR(TH('#'),TH('Mnemonic'),TH('Description'),TH('Exchange Rate'),TH('Status'),TH('Action')),_class='bg-red')
    for n in db().select(db.Currency.ALL):        
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('settings','get_currency_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')        
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.mnemonic),TD(n.description),TD(n.exchange_rate),TD(n.status_id),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class='table table-hover')
    return dict(form = form, table=table)    
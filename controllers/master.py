import locale

def patch_master_account_group_id():    
    _id = dc(dc.Master_Chart_Account_Prefix_Serial.id == request.vars.account_sub_group_id).select().first()    
    response.js = "$('#Master_Account_chart_of_account_group_code').val('%s')" % (_id.prefix)

def patch_master_account_id():
    if request.args(0):
        _id = dc(dc.Master_Account.id == request.args(0)).select().first()
        _id.update_record(
            account_sub_group_id = request.vars.account_sub_group_id, 
            account_code = request.vars.account_code, 
            account_name = request.vars.account_name, 
            master_account_type_id = request.vars.master_account_type_id, 
            chart_of_account_group_code = request.vars.chart_of_account_group_code)
        response.js = "alertify.success('Success!')"
    elif not request.args(0):
        if request.vars.account_sub_group_id and request.vars.master_account_type_id:
            dc.Master_Account.insert(
                account_sub_group_id = request.vars.account_sub_group_id, 
                account_code = request.vars.account_code, 
                account_name = request.vars.account_name, 
                master_account_type_id = request.vars.master_account_type_id, 
                chart_of_account_group_code = request.vars.chart_of_account_group_code)            
            response.js = "window.location.href = '%s';alertify.success('Success!')" % URL('master','get_master_account_grid')   
        elif not request.vars.account_sub_group_id or not request.vars.master_account_type_id:
            # print('empty')
            response.js = "alertify.error('Form Error!')"    
                    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_master_account_grid():
    form = SQLFORM(dc.Master_Account, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'        
    elif form.errors:
        response.flash = 'Form has error.'            
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Account Code'),TD('Account Name'),TD('Account Group'),TD('Chart Code'),TD('Action')),_class='bg-red')    
    for n in dc((dc.Master_Account.status == 0) & ((dc.Master_Account.delete == False) | (dc.Master_Account.delete == None)) & ((dc.Master_Account.blocked == False) | (dc.Master_Account.blocked == None))).select(orderby = dc.Master_Account.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback = URL('master','get_master_account_id', args = n.id))
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('master','get_master_account_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        if n.account_sub_group_id == None:            
            _sub_group = 'None'
        else:
            _sub_group = str(n.account_sub_group_id.account_group_name) + ' - ' + str(n.account_sub_group_id.prefix_name)
        row.append(TR(TD(ctr),TD(n.account_code),TD(n.account_name),TD(_sub_group),TD(n.chart_of_account_group_code),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table')
    return dict(form = form, table = table)

def get_master_account_id():
    _id = dc(dc.Master_Account.id == request.args(0)).select().first()
    _credit_balance = float(_id.credit_balance_1 or 0) + float(_id.credit_balance_2 or 0) + float(_id.credit_balance_3 or 0) + float(_id.credit_balance_4 or 0) + float(_id.credit_balance_5 or 0) + float(_id.credit_balance_6 or 0) + float(_id.credit_balance_9 or 0) 
    _opening_balance = float(_id.opening_balance_1 or 0) + float(_id.opening_balance_2 or 0) + float(_id.opening_balance_3 or 0) + float(_id.opening_balance_4 or 0) + float(_id.opening_balance_5 or 0) + float(_id.opening_balance_6 or 0) + float(_id.opening_balance_9 or 0) 
    if _id.account_sub_group_id == None:
        _account_group = 'None'
    else:
        _account_group = _id.account_sub_group_id.serial_key, ' - ', _id.account_sub_group_id.account_group_name
    table = TABLE(
        TR(TD('Account Group'),TD('Account Code'),TD('Account Name')),
        TR(TD(_account_group),TD(_id.account_code),TD(_id.account_name)),_class='table table-bordered')
    table += TABLE(
        TR(TD('Credit Balance 1'),TD('Credit Balance 2'),TD('Credit Balance 3'),TD('Credit Balance 4'),TD('Credit Balance 5'),TD('Credit Balance 6'),TD('Credit Balance 9'),TD('Balance')),
        TR(TD(locale.format('%.3F',_id.credit_balance_1 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_2 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_3 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_4 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_5 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_6 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.credit_balance_9 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_credit_balance or 0, grouping = True),_align ='right')),_class='table table-bordered')
    table += TABLE(
        TR(TD('Opening Balance 1'),TD('Opening Balance 2'),TD('Opening Balance 3'),TD('Opening Balance 4'),TD('Opening Balance 5'),TD('Opening Balance 6'),TD('Opening Balance 9'),TD('Balance')),
        TR(TD(locale.format('%.3F',_id.opening_balance_1 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_2 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_3 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_4 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_5 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_6 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_id.opening_balance_9 or 0, grouping = True),_align ='right'),TD(locale.format('%.3F',_opening_balance or 0, grouping = True),_align ='right')),_class='table table-bordered')
    

    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Master Account','message':'%s'}).show();" %(XML(table, sanitize = True))    

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))            
def get_merch_bank_master_grid():
    db.Merch_Bank_Master.status_id.default = 1
    form = SQLFORM(db.Merch_Bank_Master, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    row = []
    ctr = 0
    thead = THEAD(TR(TH('#'),TH('Account Code'),TH('Bank Name'),TH('Action'),_class = 'bg-red'))
    for n in db().select(orderby = db.Merch_Bank_Master.id):
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-user-edit'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle', _href=URL('master','get_merch_bank_master_grid', args = n.id))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(n.id),TD(n.account_code),TD(n.bank_name),TD(btn_lnk)))
    tbody = TBODY(*row)
    table = TABLE(*[thead, tbody], _class = 'table')
    return dict(form = form, table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_currency_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Mnemonic'),TD('Description'),TD('Status'),TD('Action')),_class='bg-yellow')
    for n in db().select(orderby = db.Currency.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        edit_lnk = A(I(_class='fa fa-pencil-alt'), _title='Edit Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        btn_lnk = DIV(view_lnk, edit_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.mnemonic),TD(n.description),TD(n.status),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(table = table)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_master_account_balanced_grid():
    ctr = 0
    row = []
    form = SQLFORM(db.Master_Account_Balance_Current_Year, request.args(0))
    if form.process().accepted:
        response.flash = 'Form save.'
    elif form.errors:
        response.flash = 'Form has error.'
    head = THEAD(TR(TD('#'),TD('Financial Year'),TD('Account Code'),TD('Account Name'),TD('Opening Bal.'),TD('Closing Bal.')),_class='bg-red')
    for n in db().select(orderby = db.Master_Account_Balance_Current_Year.id):
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.financial_year.year),
            TD(n.account_code),
            TD(n.account_name),
            TD(locale.format('%.2F', n.total_opening_balance or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F', n.total_closing_balance or 0, grouping = True),_align='right')))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table')
    return dict(form = form, table = table)

# 
import locale
def testing():
    print('--------------')
    form = SQLFORM.factory(
        Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
        Field('cost_center_category_id','reference Cost_Center_Category',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'))), # ex:
        Field('cost_center_id','reference Cost_Center',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'))))   
    if form.process().accepted:
        response.flash = "save"
    elif form.errors:
        response.flash = 'error'


    print('----------------------------------------------------------------'), request.now.year
    
    calculate_master_account(9000341)
    # for n in db(db.General_Ledger.transaction_no == '9000269').select():
    #     _mb = db(db.Master_Account_Balance_Current_Year.account_code == n.account_code).select().first()
    #     _ma = dc(dc.Master_Account.account_code == n.account_code).select().first()
    #     if _mb:
    #         if n.credit == 0:            
    #             _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) + float(n.debit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) + float(n.debit or 0))
    #         else:
    #             _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) - float(n.credit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) - float(n.credit or 0))
    #     elif not _mb:
    #         if n.credit == 0:
    #             db.Master_Account_Balance_Current_Year.insert(
    #                 financial_year = request.now, 
    #                 account_code = n.account_code,
    #                 account_name = _ma.account_name,
    #                 closing_balance_99 = float(n.debit or 0),
    #                 total_closing_balance = float(n.debit or 0))                
    #         else:
    #             x = 0                
    #             db.Master_Account_Balance_Current_Year.insert(
    #                 financial_year = request.now, 
    #                 account_code = n.account_code,
    #                 account_name = _ma.account_name,
    #                 closing_balance_99 = float(-n.credit or 0),
    #                 total_closing_balance = float(-n.credit or 0))                
    return dict(form = form)

def patch_testing():
    ctr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('A.Reff.'),TH('Dept.'),TH('Loc.'),TH('Type'),TH('Inv.Amt.'),TH('Amt.Paid'),TH('Balance'),TH('Ref.'),TH()),_class='bg-red')
    for n in db((db.General_Ledger.account_code == '10-4922') & (db.General_Ledger.debit > 0)).select():
        ctr += 1
        _balance = n.debit - n.amount_paid
        row.append(TR(
            TD(ctr),
            TD(n.account_reference_no),
            TD(n.department),
            TD(n.location),
            TD(n.transaction_type),
            TD(locale.format('%.3F',n.debit or 0, grouping = True)),
            TD(locale.format('%.3F',n.amount_paid or 0, grouping = True)),
            TD(locale.format('%.3F',_balance or 0, grouping = True)),         
            TD(n.gl_entry_ref),           
            TD(BUTTON('Select',_class='btn btn-block btn-success btn-flat btn-xs', _id='BtnSelect',_name='BtnSelect',_onclick="ajax('%s')" % URL('sili','patch_testing_id', args = n.id)))
        ))
    body = TBODY(*row)    
    table = TABLE(*[head,body],_class='table table-striped table-hover responsive',_id='example')
    return dict(table = table)

    # response.js = "alertify.alert('%s').set('resizable', true);$('.table').DataTable();" %(XML(table, sanitize = True))
    # response.js = "alertify.confirm('Title','%s', function(){ alertify.success('Ok') }, function(){ alertify.error('Cancel')}); " %(XML(table, sanitize = True))
    # response.js = " alertify.alert(%s).set('resizable',true).resizeTo('100%',250); " %(table)
    # response.js = "alertify.confirm().setHeader('Title'); alertify.confirm().setting({'resizable':true,'message':'Content Here'}).resizeTo('50%','50%')" #%('table')
    # response.js = "var closable = alertify.alert().setting('closable');alertify.alert().setting({'label':'Ok','message': '%s' ,'onok': function(){ alertify.success('Great');}}).show();" %(table)    

def patch_testing_id():
    print(':'),request.args(0)
    response.js = "alertify.success('Success!')"

def get_generate():
    print('---------------')
    _lib = db(db.GL_Description_Library.transaction_type == 23).select().first()
    print('::>'), _lib.transaction_type, _lib.transaction_prefix_text
    # for d in db(db.General_Department_Cost_Center.id == 3).select():
    #     for c in db(db.Cost_Center_Category.id == 2).select(orderby = db.Cost_Center_Category.id):
    #         for n in db((db.Cost_Center.dept_code_id == d.id) & (db.Cost_Center.cost_center_category_group_id == c.cost_center_category_group_id)).select():
    #             print n.id, ': ', n.cost_center_name
    # for n in d2().select(orderby=d2.General_Location_Cost_Center.id):
    #     _id = db(db.General_Location_Cost_Center.id == n.id).select().first()
    #     if _id:
    #         _id.update_record(
    #             location_code = n.location_code,
    #             location_name = n.location_name,
    #             cost_center = n.cost_center
    #         )
    #     elif not _id:
    #         db.General_Location_Cost_Center.insert(
    #             location_code = n.location_code,
    #             location_name = n.location_name,
    #             cost_center = n.cost_center
    #         )

    

    # for n in d2().select(orderby = d2.Cost_Center.id):        
    #     # _cc = db(db.Cost_Center.cost_center_code == n.cost_center_code).select().first()
    #     # if not _cc:
    #     db.Cost_Center.insert(
    #         cost_center_category_group_id = n.cost_center_category_group_id, 
    #         cost_center_code = n.cost_center_code, 
    #         cost_center_name = n.cost_center_name, 
    #         dept_code_id = n.dept_code_id, 
    #         location_cost_center_id = n.location_cost_center_id
    #         )
    return dict()

def get_pull_master_account(): # not required
    print '--- get_pull_master_account ---'
    for n in dc().select(orderby = dc.Master_Account.id):
        _id = db(db.Master_Account.id == n.id).select().first()
        if _id:
            _id.update_record(account_code = n.account_code,account_name = n.account_name,master_account_type_id=n.master_account_type_id,master_account=n.master_account,stock_adjustment_account=n.stock_adjustment_account,transfer_switch=n.transfer_switch)
        else:
            db.Master_Account.insert(account_code = n.account_code,account_name = n.account_name,master_account_type_id=n.master_account_type_id,master_account=n.master_account,stock_adjustment_account=n.stock_adjustment_account,transfer_switch=n.transfer_switch)

def get_settings_pull_sync(): # not required
    print '--- get_settings_pull_sync ---'
    for n in dc().select(orderby = dc.Financial_Statement_Group.id):
        _id = db(db.Financial_Statement_Group.id == n.id).select().first()
        if _id:
            _id.update_record(financial_statement_group_name = n.financial_statement_group_name)
        else:
            db.Financial_Statement_Group.insert(financial_statement_group_name = n.financial_statement_group_name)

    for n in dc().select(orderby = dc.Chart_Account_Main_Group.id):
        _id = db(db.Chart_Account_Main_Group.id == n.id).select().first()
        if _id:
            _id.update_record(chart_account_main_group_name = n.chart_account_main_group_name,financial_statement_id = n.financial_statement_id)
        else:            
            db.Chart_Account_Main_Group.insert(chart_account_main_group_name = n.chart_account_main_group_name,financial_statement_id = n.financial_statement_id)

    for n in dc().select(orderby = dc.Master_Chart_Account_Prefix_Serial.id): 
        _id = db(db.Master_Chart_Account_Prefix_Serial.id == n.id).select().first()
        if _id:            
            _id.update_record(prefix = n.prefix,prefix_name = n.prefix_name,serial_key = n.serial_key,account_group_name = n.account_group_name,prefix_key = n.prefix_key,chart_account_main_group_id = n.chart_account_main_group_id)
        else:
            db.Master_Chart_Account_Prefix_Serial.insert(prefix = n.prefix,prefix_name = n.prefix_name,serial_key = n.serial_key,account_group_name = n.account_group_name,prefix_key = n.prefix_key,chart_account_main_group_id = n.chart_account_main_group_id)

def get_auth_pull_sync():
    print '--- get_auth_pull_sync ---'
    # print '                  ---- group sync ----'
    for n in dc().select(orderby = dc.auth_group.id): # group sync
        _id = db(db.auth_group.id == n.id).select().first()
        if _id:
            _id.update_record(role = n.role,description = n.description)
        else:
            db.auth_group.insert(role = n.role,description = n.description)
    
    # print '                  ---- user sync ----'
    for n in dc().select(orderby = dc.auth_user.id): # user sync
        _id = db(db.auth_user.id == n.id).select().first()
        if _id:
            _id.update_record(first_name = n.first_name,last_name = n.last_name,username = n.username,email = n.email,password = n.password)
        else:            
            db.auth_user.insert(first_name = n.first_name,last_name = n.last_name,username = n.username,email = n.email,password = n.password)
    
    # print '                  ---- member sync ----'
    for n in dc().select(orderby = dc.auth_membership.id): # group member sync
        _id = db(db.auth_membership.id == n.id).select().first()
        if _id:            
            _id.update_record(user_id = n.user_id,group_id = n.group_id)
        else:            
            db.auth_membership.insert(user_id = n.user_id,group_id = n.group_id)
    return dict()

def get_push_sync():
    print '--- push sync ---'
    return dict()

def get_generatex():
    count = dc.Master_Account.id.count()
    for n in dc(dc.Master_Account.id > 0).select(count, dc.Master_Account.account_code, groupby = dc.Master_Account.account_code):
        print count, n.Master_Account.account_code
def testing():
    return dict()

def get_generate():
    for n in db(db.General_Ledger.transaction_type == 1).select():
        _trnx = dc((dc.Merch_Stock_Header.transaction_type == 1) & (dc.Merch_Stock_Header.voucher_no == n.account_reference_no)).select().first()
        if _trnx:
            n.update_record(location = _trnx.location)
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
# -------------------------------- SETTINGS SCHEMA --------------------------------

db.define_table('GL_Transaction_Serial',
    Field('prefix','string',length = 5),
    Field('prefix_name','string',length = 50), 
    Field('serial_number','integer', default = 0), # 8 digits example 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Accounts_Workflow_Status',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('required_action','string', length = 50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('General_Account',
    Field('selective_tax_payable_account','string',length = 15),
    Field('selective_tax_receivable_account','string',length = 15),
    Field('claim_receivable_account','string',length = 15),
    Field('provision_delivery_income','string',length = 15),
    Field('receipt_voucher_account','string',length = 15),
    Field('pdc_receipt_voucher_account','string',length = 15),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('GL_Description_Library',
    Field('transaction_type','integer',default = 0), #transaction type
    Field('transaction_prefix_text','string',length = 5),
    Field('order_no_text','string',length = 30),
    Field('purchase_receipt_no_text','string',length = 30),
    Field('short_supply_text','string',length = 30),
    Field('excise_tax_text','string',length = 30),    
    Field('damaged_supply_text','string',length = 30),
    Field('common_text','string',length = 30),
    Field('ib_text','string',length = 30),    
    Field('common_text2','string',length = 30),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table("Financial_Statement_Group",
    Field('financial_statement_group_name','string'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format='area_name')

db.define_table('Chart_Account_Main_Group',
    Field('chart_account_main_group_name','string',length = 50),
    Field('financial_statement_id', 'reference Financial_Statement_Group', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Financial_Statement_Group.id,'%(financial_statement_group_name)s', zero = 'Choose Financial Statement Group'))),     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Master_Chart_Account_Prefix_Serial',
    Field('prefix', 'string',length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), # 07
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),  # 07-Customer Account, Group Name    
    Field('serial_key','integer',length = 5 ), # serial 00000    
    Field('account_group_name','string'), # account sub-group name
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]),     
    Field('chart_account_main_group_id', 'reference Chart_Account_Main_Group', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(db, db.Chart_Account_Main_Group.id,'%(chart_account_main_group_name)s', zero = 'Choose Account Group'))), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

db.define_table('Transaction_Prefix',
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('current_year_serial_key', 'integer'),
    Field('previous_year_serial_key', 'integer', writable = False),
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

db.define_table('Note_Status',
    Field('status', 'string', length = 10),
    Field('action_required','string', length = 50),
    Field('description', 'string', length = 50),         
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Business_Unit',
    Field('business_name','string',length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format='%(business_name)s')

db.define_table('Department',    
    Field('department_code','string', length = 5, label ='Department Code', requires = IS_NOT_IN_DB(db, 'Department.department_code')),
    Field('department_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.department_name')]),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(department_code)s')

db.define_table('General_Department_Cost_Center',    
    Field('department_code','string', length = 5, label ='Department Code', requires = IS_NOT_IN_DB(db, 'General_Department_Cost_Center.department_code')),
    Field('department_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'General_Department_Cost_Center.department_name')]),    
    Field('cost_center','string',length = 15),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(department_code)s')

db.define_table('General_Location_Cost_Center',    
    Field('location_code','string', length = 5, label ='Location Code', requires = IS_NOT_IN_DB(db, 'General_Location_Cost_Center.location_code')),
    Field('location_name','string', length = 50, label = 'Location Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'General_Location_Cost_Center.location_name')]),    
    Field('cost_center','string',length = 15),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(location_code)s')

db.define_table('Currency',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('exchange_rate','decimal(20,6)',default=0),
    Field('status_id','string',length=25,requires = IS_IN_SET(['Active','Inactive'], zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Stand_Rent_Brand',
    Field('brand_code','string',length=10),
    Field('brand_name','string',length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Department_Head_Assignment',
    Field('users_id', db.auth_user, ondelete = 'NO ACTION'),    
    Field('department_id','reference Department',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Department.id,'%(department_code)s - %(department_name)s',zero='Choose Department')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Merch_Bank_Master',
    Field('account_code', 'string',length=20),
    Field('bank_name', 'string',length=50),                
    Field('status_id','string',length=25,requires = IS_IN_SET([('1','Active'),('2','Inactive')], zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Bank_Master',
    Field('bank_code', 'string',length=20),
    Field('bank_name', 'string',length=50),                
    Field('status_id','string',length=25,requires = IS_IN_SET([('1','Active'),('2','Inactive')], zero = 'Choose Status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Cost_Center_Category_Group',
    Field('cost_center_category_group_code', 'string', length=15),
    Field('cost_center_category_group_name', 'string', length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Cost_Center_Category',
    Field('cost_center_category_group_id', 'reference Cost_Center_Category_Group', ondelete = 'NO ACTION', requires = IS_IN_DB(db,db.Cost_Center_Category_Group.id,'%(cost_center_category_group_code)s : %(cost_center_category_group_name)s',zero='Choose Cost Group Category')),
    Field('cost_center_category_code', 'string', length=15),
    Field('cost_center_category_name', 'string', length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Cost_Center',
    Field('cost_center_category_group_id', 'reference Cost_Center_Category_Group', ondelete = 'NO ACTION', requires = IS_IN_DB(db,db.Cost_Center_Category_Group.id,'%(cost_center_category_group_code)s : %(cost_center_category_group_name)s',zero='Choose Cost Group Category')),
    Field('cost_center_code', 'string', length=15),
    Field('cost_center_name', 'string', length=50),
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('location_cost_center_id','reference General_Location_Cost_Center', ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Location_Cost_Center.id,'%(location_code)s - %(location_name)s',zero='Choose Location'))),# location cost center id
    Field('driver','string', length=15), # account code     
    Field('cost_center_exemption','boolean',default=False),
    Field('status_id','string',length=25,requires = IS_IN_SET([('1','Active'),('2','Inactive')], zero = 'Choose Status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Batch_Posting_Sequence',
    Field('prefix_seq','integer', 1),
    Field('prefix_seq_name','string', length = 30),
    Field('sequence_no','integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))
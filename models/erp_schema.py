dc.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128),
    Field('last_name', length=128),
    Field('username', unique = True, readable = False),
    Field('email', length=128), # required
    Field('password', 'password', length=512,readable=False, label='Password'), # required
    Field('registration_key', length=512, writable=False, readable=False, default=''),# required
    Field('reset_password_key', length=512,writable=False, readable=False, default=''),# required
    Field('registration_id', length=512, writable=False, readable=False, default=''), format = '%(first_name)s %(last_name)s')# required

dc.define_table('auth_group',
    Field('role', length=512),
    Field('description','string'))
 
dc.define_table('auth_membership',
    Field('user_id',dc.auth_user),
    Field('group_id',dc.auth_group))

dc.define_table('Status', # Item Master
    Field('status','string',length=20, requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

dc.define_table('Record_Status',
    Field('status','string',length=20, requires = [IS_LENGTH(20),IS_UPPER(), IS_NOT_IN_DB(dc, 'Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

dc.define_table('Supplier_Trade_Terms',
    Field('trade_terms', 'string', requires = [IS_UPPER(),IS_NOT_IN_DB(dc,'Supplier_Trade_Terms.trade_terms')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'trade_terms')

dc.define_table('Prefix_Data',        
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('serial_key', 'integer', default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

dc.define_table('Division',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code','string', length = 5, label = 'Division Code', writable = False, requires = IS_NOT_IN_DB(dc, 'Division.div_code')),
    Field('div_name','string', length = 50, label = 'Division Name', requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Division.div_name')]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(div_code)s')

dc.define_table('Department',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(dc(dc.Division.status_id == 1), dc.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code','string', length = 5, label ='Department Code', writable = False, requires = IS_NOT_IN_DB(dc, 'Department.dept_code')),
    Field('dept_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Department.dept_name')]),
    Field('order_qty', 'integer', default = 40),
    Field('stock_adjustment_account', 'string', length = 10), # stock adjustment account
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(dept_code)s')

dc.define_table('Made_In',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Currency',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Supplier_Master',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='value not in department')),
    Field('supp_code','string', length=10, writable = False),
    Field('supp_sub_code','string', length=10, writable = True, requires = IS_LENGTH(10)),
    Field('supp_name','string',requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Supplier_Master.supp_name')]),
    Field('supplier_type','string', length = 10, requires = IS_IN_SET(['FOREIGN','LOCAL'], zero = 'Choose Type')), # foriegn or local supplier
    Field('contact_person', 'string'),
    Field('address_1','string'),
    Field('address_2','string'),
    Field('country_id','reference Made_In', requires = IS_IN_DB(dc, dc.Made_In.id, '%(mnemonic)s - %(description)s', zero = 'Choose Country')),
    Field('contact_no','string'),
    Field('fax_no','string'),
    Field('email_address','string',  requires = IS_EMAIL(error_message='invalid email!')),
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('purchase_budget', 'decimal(10,2)'),
    Field('supplier_ib_account','string',length = 10, writable = False),
    Field('supplier_purchase_account', 'string', length = 10, writable = False),
    Field('supplier_sales_account', 'string', length = 10, writable = False),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('item_serial_key','string', length = 25),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(supp_code)s')

dc.define_table('Location_Group',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_group_code', 'string', length=10,writable = False),
    Field('location_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(dc, 'Location_Group.location_group_name')]),
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user,ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_group_code)s')

dc.define_table('Location_Sub_Group',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_sub_group_code','string',length=10, writable =False),
    Field('location_sub_group_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(dc, 'Location_Sub_Group.location_sub_group_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

dc.define_table('Location',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('location_group_code_id','reference Location_Group', ondelete = 'NO ACTION',label = 'Location Group Code', requires = IS_IN_DB(dc, dc.Location_Group.id, '%(location_group_code)s - %(location_group_name)s', zero = 'Choose Location Group')),    
    Field('location_sub_group_id','reference Location_Sub_Group', ondelete = 'NO ACTION',label = 'Location Sub-Group Code', requires = IS_IN_DB(dc, dc.Location_Sub_Group.id, '%(location_sub_group_code)s - %(location_sub_group_name)s', zero = 'Choose Location Sub-Group')),
    Field('location_code','string',length=10, writable =False),
    Field('location_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(dc, 'Location.location_name')]),    
    Field('location_phone','string',length=50),
    Field('stock_adjustment_code', 'string', length = 10), # stock adjustment account
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('old_location_no','integer',default = 0),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(location_code)s')

dc.define_table("Financial_Statement_Group",
    Field('financial_statement_group_name','string'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format='area_name')

dc.define_table('Chart_Account_Main_Group',
    Field('chart_account_main_group_name','string',length = 50),
    Field('financial_statement_id', 'reference Financial_Statement_Group', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Financial_Statement_Group.id,'%(financial_statement_group_name)s', zero = 'Choose Financial Statement Group'))),     
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Master_Chart_Account_Prefix_Serial',
    Field('prefix', 'string',length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), # 07
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),  # 07-Customer Account
    Field('serial_key','integer',length = 5 ), # serial 00000    
    Field('account_group_name','string'), # account sub-group name
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]),     
    Field('chart_account_main_group_id', 'reference Chart_Account_Main_Group', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Chart_Account_Main_Group.id,'%(chart_account_main_group_name)s', zero = 'Choose Account Group'))), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Master_Account', # standy by for accounts/finance module account code each location
    Field('account_sub_group_id','reference Master_Chart_Account_Prefix_Serial', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Master_Chart_Account_Prefix_Serial.id,'%(prefix)s %(account_group_name)s - %(prefix_name)s', zero = 'Choose Account Sub-Group'))),     
    Field('chart_of_account_group_code','string', length = 10),
    Field('account_code','string', length = 15, requires = [IS_UPPER(),IS_NOT_EMPTY(),IS_NOT_IN_DB(dc,'Master_Account.account_code')]),
    Field('account_name','string'),    
    Field('master_account_type_id','string',length=25,requires = IS_IN_SET([('A', 'A - Accounts'), ('C', 'C - Customer'), ('E', 'E - Employee'),('S','S - Supplier'),('G','G - General Account'),('SAC','SAC - Stock Adjustment Code'),('OOS','OOS - Obselensce Of Stock')],zero='Choose Account Type')), #Customer,Accounts,Supplier,Employees    
    Field('credit_balance_1','decimal(20,6)',default=0),
    Field('credit_balance_2','decimal(20,6)',default=0),
    Field('credit_balance_3','decimal(20,6)',default=0),
    Field('credit_balance_4','decimal(20,6)',default=0),
    Field('credit_balance_5','decimal(20,6)',default=0),
    Field('credit_balance_6','decimal(20,6)',default=0),
    Field('credit_balance_9','decimal(20,6)',default=0),
    Field('opening_balance_1','decimal(20,6)',default=0),
    Field('opening_balance_2','decimal(20,6)',default=0),
    Field('opening_balance_3','decimal(20,6)',default=0),
    Field('opening_balance_4','decimal(20,6)',default=0),
    Field('opening_balance_5','decimal(20,6)',default=0),
    Field('opening_balance_6','decimal(20,6)',default=0),
    Field('opening_balance_9','decimal(20,6)',default=0),   
    Field('closing_balance','decimal(20,6)',default=0),   # opending blance + credit balance
    Field('master_account','string'),
    Field('stock_adjustment_account', 'string'), # stock adjustment account
    Field('transfer_switch','boolean',default=False),
    Field('delete','boolean', default = False),
    Field('status','boolean', default = False),    
    Field('blocked','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

dc.define_table('Customer_Account_Type',# cash, credit, bill
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','string'))

dc.define_table('Customer_Group_Code',# assets, receivable, payables, journals
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','string'))

dc.define_table('Customer_Category', # hypermarket, restaurant
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','string'))

dc.define_table('Area_Name',
    Field('area_name', 'string',length=50),
    Field('zone_no','integer'),    
    Field('municipality','string',legnth=50))

dc.define_table('Customer',
    Field('customer_account_no','string',length = 15),
    Field('customer_group_code_id', 'reference Customer_Group_Code', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Customer_Group_Code.id,'%(description)s', zero = 'Choose Group Code'))), 
    Field('customer_name','string', length = 50),
    Field('customer_category_id', 'reference Customer_Category', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Customer_Category.id,'%(description)s', zero = 'Choose Category'))), 
    Field('customer_account_type', 'reference Customer_Account_Type', ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Customer_Account_Type.id,'%(description)s', zero = 'Choose Account Type')), 
    Field('customer_branch_code','string', length = 20),
    Field('parent_outlet','string',length=50),
    Field('department_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),    
    Field('cr_no','string',length=25),
    Field('po_box_no', 'integer'),    
    Field('unit_no', 'integer'),
    Field('building_no', 'integer'),
    Field('street_no', 'integer'),
    Field('zone', 'integer'),
    Field('area_name_id','reference Area_Name', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Area_Name.id,'%(area_name)s', zero = 'Choose Area Name'))), 
    Field('area_name','string',legnth=50),
    Field('municipality','string',legnth=50),
    Field('state','string', length = 50),
    Field('country','string', length = 50),
    Field('telephone_no','string',length = 25),
    Field('mobile_no','string',length = 25),
    Field('fax_no','string',length = 25),
    Field('email_address','string', length = 50),
    Field('contact_person','string',length = 50),
    Field('longtitude','string',length=50),
    Field('latitude','string',length=50),
    
    Field('outlet_category','string',length=50),
    Field('outlet_type','string',length=50),
    Field('outlet_classification','string',length=50),

    Field('sponsor_name','string', length = 50),  
    Field('sponsor_id_no','string',length=50),
    Field('sponsor_id_expiry_date','date'),
    Field('sponsor_contact_no','string', length = 50),

    ## upload files to fill in here (5 fields)
    
    Field('cr_license','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    Field('guarantee','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('customer_form','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('sponsor_id','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),
    Field('transfer_switch','boolean', default = False, writable  = False))

dc.define_table('Merch_Stock_Header',
    Field('voucher_no','integer'), # 10 length
    Field('voucher_no2','integer'), # for ledger
    Field('voucher_no_reference','string', length = 50), # 10 length / delivery note / PO / SReturn / SRecipt
    Field('location', 'integer'),   # from location master
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction
    Field('account', 'string', length = 50), #adjustment code, customer code, supplier code. etc...
    Field('order_account','string',length=15), # purchase receipt only, order account for ledger
    Field('dept_code','integer'), # from item master
    Field('total_amount','decimal(20,6)', default = 0),    
    Field('total_amount_after_discount','decimal(20,6)', default = 0),        
    Field('total_amount_without_tax','decimal(20,6)', default = 0),        # 2, 4, 6, 7, 9 -> without tax total_amount - total_selective_tax - total-selective_tax_foc
    Field('discount_percentage','decimal(20,6)', default = 0),
    Field('discount_added','decimal(20,6)', default = 0),
    Field('supplier_reference_order','string', length = 25),   # from the customer 
    Field('supplier_invoice','string', length = 25),    
    Field('exchange_rate','decimal(20,6)', default = 0, required = True),    
    Field('landed_cost','decimal(20,6)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(dc, dc.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  
    Field('other_charges','decimal(20,6)', default = 0),    
    Field('custom_duty_charges','decimal(20,6)', default = 0),    
    Field('total_selective_tax','decimal(20,6)', default = 0),
    Field('total_selective_tax_foc','decimal(20,6)', default = 0),
    Field('stock_destination','integer'),
    Field('sales_man_code','string',length=15),    
    Field('sales_man_on_behalf', 'string',length=15),    
    Field('customer_return_reference','string', length = 25),
    Field('customer_good_receipt_no','string', length = 50), # customer  grn no from invoice table/header  transaction type 2    
    Field('returned_remarks','string'),    
    Field('delivery_charges','decimal(20,6)', default = 0),
    Field('batch_code_id','integer'),
    Field('cancelled','boolean', default=False),
    Field('gl_batch_posting','boolean',default=False),
    Field('gl_batch_posting_seq','integer',default=0),
    Field('gl_batch_posting_date','date'),
    Field('gl_entry_ref','string'),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Merch_Stock_Transaction',
    Field('merch_stock_header_id','reference Merch_Stock_Header',ondelete='NO ACTION',requires = IS_IN_DB(dc,dc.Merch_Stock_Header.id,'%(voucher_no)s',zero='Choose Transaction')),
    Field('voucher_no','string',length=25), # 10 length
    Field('voucher_no2','integer'), # for ledger
    Field('location', 'integer'),   # from location master
    Field('transaction_type','integer'),  # 1,2,3,4,5,6,7,8
    Field('transaction_date', 'date'), # from date of transaction    
    Field('account', 'string', length = 50), #adjustment code, customer code, supplier code. etc...
    Field('item_code', 'string', length = 15), # item master
    Field('category_id','string', lenght=10), # n-normal, p-promotional
    Field('uom', 'integer'), # from transaction
    Field('quantity', 'integer'), # from transaction
    Field('average_cost','decimal(20,6)', default = 0), # average cost
    Field('price_cost', 'decimal(20,6)', default = 0), # pieces
    Field('sale_cost','decimal(20,6)', default = 0), # after discount, outer
    Field('sale_cost_pcs', 'decimal(20,6)', default = 0), # per piece
    Field('sale_cost_notax_pcs', 'decimal(20,6)', default = 0), # sales cost without tax    
    Field('discount', 'decimal(10,2)', default = 0), # normal discount from pos
    Field('wholesale_price', 'decimal(20,6)', default = 0), # from item prices
    Field('retail_price', 'decimal(20,6)', default = 0), # from item prices
    Field('vansale_price', 'decimal(20,6)', default = 0), # from item prices
    Field('tax_amount', 'decimal(20,6)', default = 0), # in sales
    Field('selected_tax','decimal(20,6)', default = 0), # in sales
    Field('price_cost_after_discount','decimal(20,6)', default = 0), # included in sales invoice transaction
    Field('sales_man_code','string',length=15),
    Field('sales_man_on_behalf', 'string',length=15),
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.
    Field('selective_tax_price','decimal(20,6)', default = 0), # from item_prices
    Field('supplier_code','string', length = 10), # from item code
    Field('dept_code','integer'), # from item master
    Field('stock_destination','integer'), # destination of stock transfer
    Field('customer_return_reference','string', length = 25),
    Field('delete','boolean', default = False),    
    Field('cancelled','boolean', default = False),
    Field('gl_batch_posting','boolean',default=False),
    Field('gl_batch_posting_seq','integer',default=0),
    Field('gl_batch_posting_date','date'),
    Field('gl_entry_ref','string'),    
    Field('item_code_id','integer',default = 0),
    Field('aged_supplier_code','string', length = 10), # old supplier code Ex: 16-xxx, 17-xxx
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Transaction_Prefix',    
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('prefix', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('prefix_name','string', length = 30, requires = [IS_UPPER(), IS_NOT_EMPTY()]),    
    Field('current_year_serial_key', 'integer'),
    Field('previous_year_serial_key', 'integer', writable = False),
    Field('prefix_key','string', length = 10, requires = [IS_UPPER(), IS_NOT_EMPTY()]), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(prefix)s')

dc.define_table('Gender',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format='%(gender_code)s')
    
dc.define_table('UOM',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Weight',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Item_Type',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Product',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(dc(dc.Division.status_id == 1), dc.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Product.product_code')]), # Field 
    Field('product_name', 'string', length = 50, requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Product.product_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(product_code)s')

dc.define_table('SubProduct',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('div_code_id', 'reference Division', ondelete = 'NO ACTION', requires = IS_IN_DB(dc(dc.Division.status_id == 1), dc.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('product_code_id','reference Product', ondelete = 'NO ACTION', label = 'Product Code',requires = IS_IN_DB(dc(dc.Product.status_id == 1), dc.Product.id, '%(product_code)s - %(product_name)s', zero = 'Choose Product Code')),
    Field('subproduct_code','string', length = 10, writable = False, requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'SubProduct.subproduct_code')]),    
    Field('subproduct_name','string', length = 50, requires = [IS_UPPER(),IS_NOT_IN_DB(db, 'SubProduct.subproduct_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(subproduct_code)s')

dc.define_table('GroupLine',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Supplier_Master.id, '%(supp_code)s - %(supp_name)s, %(supp_sub_code)s', zero =  'Choose Supplier')),
    Field('group_line_code','string',length=8, writable = False),
    Field('group_line_name', 'string', length=50, requires=[IS_UPPER(), IS_NOT_IN_DB(dc, 'GroupLine.group_line_name')]),
    Field('transfer_switch','boolean',default=False),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False),format = '%(group_line_code)s')

dc.define_table('Brand_Line',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')),
    Field('supplier_id', 'reference Supplier_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Supplier_Master.id, '%(supp_code)s - %(supp_name)s', zero =  'Choose Supplier')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('brand_line_code','string',length=8, writable = False),
    Field('brand_line_name','string',length=50, requires = [IS_LENGTH(50),IS_UPPER(), IS_NOT_IN_DB(dc, 'Brand_Line.brand_line_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

dc.define_table('Brand_Classification',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.GroupLine.id, '%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line')), #ERROR - * Field should not be empty
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Brand_Line.id, '%(brand_line_code)s - %(brand_line_name)s', zero= 'Choose Brand Line')),
    Field('brand_cls_code','string', length=8, writable = False),
    Field('brand_cls_name','string',length=100, requires = [IS_LENGTH(100),IS_UPPER(), IS_NOT_IN_DB(dc, 'Brand_Classification.brand_cls_name')]),
    Field('old_brand_code','string',length=10),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('transfer_switch','boolean',default=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_cls_code)s')

dc.define_table('Brand_Classificatin_Department',
    Field('brand_cls_code_id','reference Brand_Classification',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification')),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION', label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department', error_message='Field should not be empty')),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = '%(brand_line_code)s')

dc.define_table('Fragrance_Type',        
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Item_Color',    
    Field('color_name','string',length=25, requires = [IS_UPPER(), IS_NOT_IN_DB(dc, 'Item_Color.color_name')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Item_Size',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Item_Collection',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Section',
    Field('prefix_id','reference Prefix_Data', ondelete = 'NO ACTION', writable = False),
    Field('section_code','string',length=5, writable = False),
    Field('section_name','string',length=50, requires = [IS_UPPER(), IS_LENGTH(25), IS_NOT_IN_DB(db, 'Section.section_name')]),
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION',label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

dc.define_table('Transaction_Item_Category',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user,ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Color_Code',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status',ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(dc, dc.Record_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))

dc.define_table('Item_Master',
    Field('item_code', 'string', length = 15, label = 'Item Code'), #requires = [IS_LENGTH(15),IS_NOT_IN_DB(db, 'Item_Master.item_code')]),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),    
    Field('item_description_ar', 'string', length = 50, label = 'Arabic Name', requires = [IS_LENGTH(50), IS_UPPER()]),
    Field('supplier_item_ref', 'string', length = 20), #requires = [IS_LENGTH(20) ,IS_UPPER(), IS_NOT_IN_DB(db, 'Item_Master.supplier_item_ref')]),   #unique
    Field('int_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.int_barcode')]), #unique
    Field('loc_barcode', 'string', length = 20), #requires = [IS_LENGTH(20), IS_UPPER(), IS_NOT_IN_DB(db,'Item_Master.loc_barcode')]), #unique
    Field('purchase_point', 'integer', default = 40),
    Field('ib', 'decimal(10,2)', default = 0),
    Field('uom_value', 'integer'),    
    Field('uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
    Field('supplier_uom_value', 'integer'),
    Field('supplier_uom_id', 'reference UOM', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.UOM.id, '%(description)s', zero = 'Choose UOM Pack Size')),
    Field('weight_value', 'integer'),
    Field('weight_id', 'reference Weight', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Weight.id, '%(mnemonic)s', zero = 'Choose Weight')),
    Field('type_id', 'reference Item_Type',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Item_Type.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), # saleable/non-saleable => item_type_id    
    Field('selectivetax','decimal(10,2)', default = 0, label = 'Selective Tax'),    
    Field('vatpercentage','decimal(10,2)', default = 0, label = 'Vat Percentage'),    
    Field('division_id', 'reference Division', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Division.id,'%(div_code)s - %(div_name)s', zero = 'Choose Division'), label='Division Code'),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(dc, dc.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('product_code_id','reference Product', ondelete = 'NO ACTION',label = 'Product Code',requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Product.id,'%(product_code)s - %(product_name)s', zero = 'Choose Product Code'))),
    Field('subproduct_code_id', 'reference SubProduct', ondelete = 'NO ACTION',label = 'SubProduct', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.SubProduct.id, '%(subproduct_code)s - %(subproduct_name)s', zero = 'Choose SubProduct'))),
    Field('group_line_id','reference GroupLine', ondelete = 'NO ACTION',requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.GroupLine.id,'%(group_line_code)s - %(group_line_name)s', zero = 'Choose Group Line Code'))),
    Field('brand_line_code_id','reference Brand_Line', ondelete = 'NO ACTION',requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Brand_Line.id,'%(brand_line_code)s - %(brand_line_name)s', zero = 'Choose Brand Line'))),
    Field('brand_cls_code_id','reference Brand_Classification',ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Brand_Classification.id,'%(brand_cls_code)s - %(brand_cls_name)s', zero = 'Choose Brand Classification'))),
    Field('section_code_id', 'reference Section',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Section.id, '%(section_code)s - %(section_name)s', zero = 'Choose Section')),
    Field('size_code_id','reference Item_Size', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Item_Size.id, '%(description)s', zero = 'Choose Size')),    
    Field('gender_code_id','reference Gender', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Gender.id,'%(description)s', zero = 'Choose Gender')),
    Field('fragrance_code_id','reference Fragrance_Type',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Fragrance_Type.id, '%(description)s', zero = 'Choose Fragrance Code')),
    Field('color_code_id','reference Color_Code',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Color_Code.id, '%(description)s', zero = 'Choose Color')),
    Field('collection_code_id','reference Item_Collection', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Item_Collection.id, '%(description)s', zero = 'Choose Collection')),
    Field('made_in_id','reference Made_In', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Made_In.id, '%(description)s', zero = 'Choose Country')),
    Field('item_status_code_id','reference Status',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Status.id, '%(status)s', zero = 'Choose Status')),
    Field('transfer_switch','boolean', default = False, writable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'item_code')

dc.define_table('Stock_Status',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]),     
    Field('required_action','string', length = 50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', dc.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

dc.define_table('Purchase_Receipt',            
    Field('purchase_request_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_request_no', 'integer', writable = False),
    Field('purchase_request_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_request_date_approved','date', writable = False),
    Field('purchase_request_date', 'date', default = request.now, writable = False),
    Field('order_account','string',length=15),
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(dc, dc.Supplier_Master.id,'%(supp_sub_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),    
    Field('location_code_id','reference Location', ondelete = 'NO ACTION',label = 'Stock Source', requires = IS_IN_DB(dc, dc.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),
    Field('estimated_time_of_arrival', 'date', default = request.now), #requires = IS_DATE_IN_RANGE(format=T('%Y-%m-%d'), minimum=datetime.date(2008, 1, 1),error_message='must be YYYY-MM-DD!')),
    Field('total_amount','decimal(20,6)', default = 0),    
    Field('total_amount_after_discount','decimal(20,6)', default = 0),    
    Field('insured', 'boolean', default = False),
    Field('foreign_currency_value','decimal(10,3)', default = 0),
    Field('local_currency_value','decimal(20,6)', default = 0),
    Field('exchange_rate','decimal(10,4)', default = 0),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(dc, dc.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),    
    Field('discount_percentage', 'decimal(10,2)',default =0), # on hold structure    
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure    
    Field('currency_id','reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('remarks', 'string'),
    Field('remarks_created_by',dc.auth_user,ondelete='NO ACTION',writable=False,readable=False),
    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'integer', writable = False),
    Field('purchase_order_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_order_date_approved','date', writable = False),
    Field('purchase_order_date','date', writable = False),        
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_approved_by','reference auth_user', ondelete = 'NO ACTION',writable = False),
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('purchase_receipt_date','date', writable = False),
    Field('supplier_account_code','string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account'], zero = 'Choose Supplier')),
    Field('supplier_account_code_description','string', length = 50),
    Field('supplier_invoice','string', length = 25),
    Field('landed_cost','decimal(20,6)', default = 0),
    Field('other_charges','decimal(20,6)', default = 0),    
    Field('custom_duty_charges','decimal(20,6)', default = 0),        
    Field('selective_tax','decimal(20,6)', default = 0.0, label = 'Selective Tax'),
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Stock_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('submitted','boolean', default = False),
    Field('posted','boolean', default = False),
    Field('draft','boolean', default = True),
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),
    Field('partial','boolean', default = False), 
    Field('received','boolean', default = False),
    Field('archives', 'boolean', default = False),   
    Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),    
    Field('purchase_receipt_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('section_id','string',length=25,requires = IS_IN_SET([('F','Food Section'),('N','Non-Food Section')],zero ='Choose Section')),
    Field('processed','boolean', default = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

dc.define_table('Purchase_Receipt_Transaction',    
    Field('purchase_receipt_no_id','reference Purchase_Receipt',ondelete = 'NO ACTION',writable = False),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code','string', length = 50),
    Field('item_description', 'string', length = 50, label = 'Description', requires = [IS_LENGTH(50),IS_UPPER()]),
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # quantity requested
    Field('quantity_ordered','integer', default = 0), # quantity ordered
    Field('quantity_received','integer', default = 0), # quantity received/warehouse
    Field('quantity_invoiced','integer', default = 0), # quantity invoiced/accounts
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,6)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0),
    Field('wholesale_price', 'decimal(20,6)', default = 0),
    Field('retail_price', 'decimal(20,6)',default = 0),
    Field('vansale_price', 'decimal(20,6)',default =0),
    Field('discount_percentage', 'decimal(10,2)',default =0),
    Field('net_price', 'decimal(20,6)',default =0),
    Field('selective_tax','decimal(20,6)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(20,6)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('old_average_cost','decimal(20,6)', default = 0), # get the old average cost
    Field('old_landed_cost','decimal(20,6)', default = 0), # get the old landed cost
    Field('production_date', 'date'),
    Field('expiration_date', 'date'),    
    Field('selected','boolean', default = False), 
    Field('consolidated','boolean', default = False),            
    Field('delete', 'boolean', default = False),    
    Field('item_remarks', 'string'),
    Field('partial','boolean', default = False), 
    Field('new_item','boolean', default=False),
    Field('quantity_ordered_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_received_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('quantity_invoiced_by', 'reference auth_user', ondelete = 'NO ACTION', writable = False, readable = False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))


dc.define_table('Direct_Purchase_Receipt',  
    Field('transaction_no', 'integer', default = 0, writable = False),
    Field('transaction_date', 'date', default=request.now, writable = False),
    Field('purchase_receipt_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_receipt_no', 'integer', writable = False),    
    Field('purchase_receipt_date', 'date',default = request.now),
    Field('purchase_order_no_prefix_id', 'reference Transaction_Prefix', ondelete = 'NO ACTION',writable = False),   
    Field('purchase_order_no', 'string', length = 25, requires=IS_NOT_EMPTY() ),    
    Field('purchase_receipt_date_approved','date', writable = False),
    Field('purhcase_receipt_approved_by','reference auth_user', ondelete='NO ACTION',writable = False),    
    Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
    Field('location_code_id','reference Location', ondelete = 'NO ACTION', label = 'Stock Source', requires = IS_IN_DB(dc(dc.Location.status_id == 1), dc.Location.id, '%(location_code)s - %(location_name)s', zero = 'Choose Location')),
    Field('supplier_reference_order','string', length = 25),    
    Field('supplier_code_id', 'reference Supplier_Master',ondelete = 'NO ACTION', label = 'Supplier Code', requires = IS_IN_DB(dc, dc.Supplier_Master.id,'%(supp_code)s - %(supp_name)s', zero = 'Choose Supplier Code')),    
    Field('account_code','string',length=25),
    Field('trade_terms_id', 'reference Supplier_Trade_Terms', ondelete = 'NO ACTION',label = 'Trade Terms', requires = IS_IN_DB(dc, dc.Supplier_Trade_Terms.id, '%(trade_terms)s', zero = 'Choose Terms')),  #'string', length = 25, requires = IS_IN_SET(['EX-WORKS','FOB','C&F','CIF','LANDED COST'], zero = 'Choose Terms')),        
    Field('status_id','reference Stock_Status',ondelete = 'NO ACTION', default = 4, requires = IS_IN_DB(dc, dc.Stock_Status.id, '%(description)s', zero = 'Choose Status')),       
    Field('mode_of_shipment','string',length = 25, requires = IS_IN_SET(['BY AIR','BY SEA','BY LAND'], zero = 'Choose Type')),
    Field('supplier_account_code', 'string',length = 25, requires = IS_IN_SET(['Supplier Account','IB Account','Promo Pack'], zero = 'Choose Supplier')),
    Field('total_amount','decimal(20,6)', default = 0, writable = False),    # total net amount
    Field('total_amount_after_discount','decimal(20,6)', default = 0, writable = False),    
    Field('exchange_rate','decimal(20,6)', default = 0, required = True),    
    Field('landed_cost','decimal(20,6)', default = 0),
    Field('other_charges','decimal(20,6)', default = 0),    
    Field('custom_duty_charges','decimal(20,6)', default = 0),        
    Field('selective_tax','decimal(20,6)', default = 0.0, label = 'Selective Tax'),
    Field('supplier_invoice','string', length = 25),    
    Field('supplier_account_code_description', 'string'),
    Field('added_discount_amount', 'decimal(10,3)',default =0), # on hold structure
    Field('currency_id', 'reference Currency', ondelete = 'NO ACTION', requires = IS_IN_DB(dc, dc.Currency.id,'%(mnemonic)s - %(description)s', zero = 'Choose Currency')),    
    Field('remarks', 'string'),    
    Field('received','boolean', default = False, writable = False),
    Field('archives', 'boolean', default = False, writable = False),   
    Field('posted_by','reference auth_user', ondelete='NO ACTION', writable = False),
    Field('date_posted','datetime',default=request.now),
    Field('processed','boolean', default = False),
    Field('proforma_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),    
    Field('purchase_receipt_file','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf'))),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = True),
    Field('updated_by', dc.auth_user,ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = 'purchase_receipt_no')

dc.define_table('Direct_Purchase_Receipt_Transaction',    
    Field('purchase_receipt_no_id','reference Direct_Purchase_Receipt',ondelete = 'NO ACTION',writable = False),    
    Field('item_code_id', 'reference Item_Master', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Item_Master.id, '%(item_code)s', zero = 'Choose Item Code')),        
    Field('item_code', 'string', length = 25), 
    Field('category_id','reference Transaction_Item_Category', ondelete = 'NO ACTION',requires = IS_IN_DB(dc, dc.Transaction_Item_Category.id, '%(mnemonic)s - %(description)s', zero = 'Choose Type')), 
    Field('quantity','integer', default = 0), # manoj
    Field('uom','integer', default = 0),    
    Field('price_cost', 'decimal(20,6)', default = 0),
    Field('net_price', 'decimal(20,6)',default =0),
    Field('discount_percentage', 'decimal(20,6)',default =0),
    Field('total_amount','decimal(20,6)', default = 0),
    Field('average_cost','decimal(20,6)', default = 0),
    Field('sale_cost', 'decimal(20,6)', default = 0),
    Field('wholesale_price', 'decimal(20,6)', default = 0),
    Field('retail_price', 'decimal(20,6)',default = 0),
    Field('vansale_price', 'decimal(20,6)',default =0),
    Field('selective_tax','decimal(20,6)', default = 0, label = 'Selective Tax'),
    Field('selective_tax_foc','decimal(20,6)', default = 0, label = 'Selective Tax'),
    Field('vat_percentage','decimal(10,2)', default = 0, label = 'Vat Percentage'), 
    Field('landed_cost','decimal(20,6)', default = 0),    
    Field('price_cost_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('average_cost_pcs','decimal(20,6)', default = 0), # per pcs.   
    Field('wholesale_price_pcs', 'decimal(20,6)', default = 0), # per pcs.
    Field('retail_price_pcs', 'decimal(20,6)',default = 0), # per pcs.
    Field('location_code_id','reference Location', ondelete = 'NO ACTION', writable = False),
    Field('transaction_type','integer', default = 1),
    Field('transaction_date', 'datetime', default=request.now, writable = False),
    Field('supplier_reference_order','string', length = 25),
    Field('delete', 'boolean', default = False),  
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', 'reference auth_user', ondelete = 'NO ACTION',default = auth.user_id, writable = False, readable = False, represent = lambda row: row.first_name.upper() + ' ' + row.last_name.upper()),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', dc.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False))


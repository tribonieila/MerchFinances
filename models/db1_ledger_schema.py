# header settings
db.define_table('Account_Voucher_Type', # receipt voucher, payment voucher, journal voucher
    Field('voucher_serial_no','integer'), 
    Field('transaction_prefix','string',length=5),
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV
    Field('account_voucher_transaction_name','string',length=50), # ex. full name
    Field('financial_year','date',writable=False,readable = True), # year only
    Field('created_on','datetime', default=request.now, writable = False, readable = False),
    Field('created_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on','datetime', update=request.now, writable = False, readable = False),
    Field('updated_by',db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))    

db.define_table('Account_Voucher_Payment_Mode', # cash, cash cheque, post-dated-cheque
    Field('account_voucher_payment_code','string',length=5), # ex. C, CC, PDC, RVC
    Field('account_voucher_payment_name','string',length=50), # EX. CASH, CASH CHECK, Post dated check, rv. confirmation
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(account_voucher_payment_code)s')

db.define_table('Transaction_Payment_Type',
    Field('transaction_payment_type','string',length=5),
    Field('transaction_payment_name','string',length=20),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Voucher_Header', 
    Field('voucher_no','string',length=20), # account voucher transaction code + voucher serial no
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('account_payment_mode_id','reference Account_Voucher_Payment_Mode',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))),    
    Field('account_voucher_payment_code','string',length=5),
    Field('receipt_voucher_confirmation_type_id','string',length=10,requires = IS_EMPTY_OR(IS_IN_SET([('A','CASH/CHEQUE'),('B','POST DATED CHEQUE')], zero = 'Choose Confirmation Type'))),
    Field('total_amount','decimal(20,6)',default=0),
    Field('account_code','string',length=20), # bank code
    Field('bank_name_id','reference Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Bank_Master.id,'%(bank_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date',default=request.now),
    Field('purpose','string',length=50),
    Field('received_from','string',length=50),
    Field('collected_by','string',length=50),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('cost_center','string',length=15),
    Field('location_cost_center','string',length=15),
    Field('gl_entry_ref','string'),
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'RV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('posting_ref_no','string',length=20), # ex: RV,RV,JV etc
    Field('remarks','text'),            
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(voucher_no)s')

db.define_table('Account_Voucher_Transaction',    
    Field('account_voucher_id','reference Account_Voucher_Header', ondelete = 'NO ACTION', writable=False,readable= False),
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_credit_code','string',length=20), # to rv and jv
    Field('account_debit_code','string',length=20),# to pv and jv
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department')),    # department id
    Field('department_code', 'string', length = 10), # department normal
    Field('location_cost_center_id','reference General_Location_Cost_Center', ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Location_Cost_Center.id,'%(location_code)s - %(location_name)s',zero='Choose Location'))),# location cost center id
    Field('location_code','string',length = 10), # location cost center normal
    Field('transaction_payment_type_id','reference Transaction_Payment_Type',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Transaction_Payment_Type.id,'%(transaction_payment_type)s - %(transaction_payment_name)s',zero='Choose Payment Type')),# transaction_payment_type
    Field('amount_paid','decimal(20,6)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('voucher_no','string',length=20), # voucher serial no
    Field('gl_entry_ref','string'),
    Field('department','integer'), # from general ledger
    Field('invoice_no','string',length=30), # from general ledger 
    Field('location','integer'), # from general ledger    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Voucher_Request', 
    Field('ticket_no_id','string',length=20),
    Field('voucher_no','string',length=20), # voucher serial no
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('account_payment_mode_id','reference Account_Voucher_Payment_Mode',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))),    
    Field('account_voucher_payment_code','string',length=5),
    Field('receipt_voucher_confirmation_type_id','string',length=10,requires = IS_EMPTY_OR(IS_IN_SET([('A','CASH/CHEQUE'),('B','POST DATED CHEQUE')], zero = 'Choose Confirmation Type'))),
    Field('total_amount','decimal(20,6)',default=0),
    Field('account_code','string',length=20), # bank code
    Field('bank_name_id','reference Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Bank_Master.id,'%(bank_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date',default=request.now),
    Field('purpose','string',length=50),
    Field('received_from','string',length=50),
    Field('collected_by','string',length=50),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('cost_center','string',length=15),
    Field('location_cost_center','string',length=15),
    Field('gl_entry_ref','string'),
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'RV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('posting_ref_no','string',length=20), # ex: RV,RV,JV etc
    Field('remarks','text'),        
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(voucher_no)s')

db.define_table('Account_Voucher_Transaction_Request',    
    Field('account_voucher_request_id','reference Account_Voucher_Request', ondelete = 'NO ACTION', writable = False),
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_credit_code','string',length=20), # to rv and jv
    Field('account_debit_code','string',length=20),# to pv and jv
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal
    Field('location_cost_center_id','reference General_Location_Cost_Center', ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Location_Cost_Center.id,'%(location_code)s - %(location_name)s',zero='Choose Location'))),# location cost center id
    Field('location_code','string',length = 10), # location cost center normal
    Field('transaction_payment_type_id','reference Transaction_Payment_Type',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Transaction_Payment_Type.id,'%(transaction_payment_type)s - %(transaction_payment_name)s',zero='Choose Payment Type'))),# transaction_payment_type
    Field('amount_paid','decimal(20,6)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('voucher_no','string',length=20), # voucher serial no
    Field('ticket_no_id','string',length=20,writable=False,readable=False),
    Field('gl_entry_ref','string'),    
    Field('department','integer'), # from general ledger if against invoice type
    Field('invoice_no','string',length=30), # from general ledger if against invoice type
    Field('location','integer'), # from general ledger if against invoice type
    Field('gl_id','integer',default=0), # for duplicate entry from general ledger = rv against invoice
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Record_Status',
    Field('status','string',length=20, requires = [IS_LENGTH(20),IS_UPPER(), IS_NOT_IN_DB(db, 'Record_Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Debit_Credit',
    Field('serial_note','string',length=15), # voucher no
    Field('account_code', 'string'),
    Field('account_type','string', length=10,requires = IS_IN_SET([('C', 'C - Customer'), ('E', 'E - Employee'),('S','S - Supplier')],zero='Choose Account Type')), #Customer,Accounts,Supplier,Employees
    Field('account_name','string'),
    Field('account_address','string'),
    Field('account_city','string'),
    Field('account_country','string'),
    Field('department_id','reference Department',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Department.id,'%(department_code)s - %(department_name)s',zero='Choose Department')),    
    Field('business_unit','reference Business_Unit',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Business_Unit.id,'%(business_name)s', zero='Choose Business Unit')),
    Field('transaction_date','date',request.now),
    Field('transaction_type','string',length=25,requires = IS_IN_SET(['Debit Note','Credit Note'], zero = 'Transaction Type')),
    Field('note_type','string',length=25,requires=IS_IN_SET(['Normal','Stand Rent'],zero='Type of Note')),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id, '%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('brand_code_id','reference Stand_Rent_Brand',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Stand_Rent_Brand.id,'%(brand_code)s - %(brand_name)s',zero='Choose Brand Name'))),
    Field('total_amount','decimal(20,6)',default=0),
    Field('remarks','string'),
    Field('account_remarks','string'),
    Field('department_remarks','string'),
    Field('management_remakrs','string'),
    Field('status_id','reference Accounts_Workflow_Status', ondelete = 'NO ACTION', label = 'Status', requires = IS_IN_DB(db, db.Accounts_Workflow_Status.id,'%(description)s', zero = 'Choose status')), 
    Field('cancelled','boolean',default=False),
    # Field('ticket_no', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Debit_Credit_Transaction',
    Field('serial_note_id','reference Debit_Credit',ondelete='NO ACTION',writable=False,readable=False), # voucher no
    Field('serial_note_suffix_id','integer',length=5), # sub-voucher no
    Field('transaction_date','date',default = request.now), # transaction date
    Field('transaction_no','integer',length=20),
    Field('transaction_type','string',length=10), # transaction type ex. A,C,E,S
    Field('account_code','string', length = 20), # EX. 07-1565, 07-101
    Field('description','string'),  # description
    Field('date_from','date'), # date from
    Field('date_to','date'), # date to
    Field('amount','decimal(20,6)'), # amount
    Field('qr_value','decimal(20,6)'), # local amount
    Field('receipt_voucher_no','integer'), # rent code
    Field('paid','boolean', default = False),
    Field('status','string',length=25,requires=IS_IN_SET(['Cancel','Approved'],zero='Type of Status')),    # status
    Field('delete','boolean', default = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Debit_Credit_Transaction_Temporary',    
    Field('account_code','string', length = 20),
    Field('description','string'),    
    Field('date_from','date'),
    Field('date_to','date'),
    Field('amount','decimal(10,2)'),
    Field('ticket_no_id', 'string', length = 10))

db.define_table('General_Ledger',
    Field('transaction_prefix_id', 'reference GL_Transaction_Serial', ondelete = 'NO ACTION',writable = False),   # TRNX        
    Field('transaction_no','integer',default=0,writable = False), # transaction ref => serial ex: 
    Field('transaction_date','date',default=request.now), # grv date/ purchase receipt date
    Field('transaction_payment_type','string',length = 10), 
    Field('transaction_type','integer'), # from consolidated merch stock header, specific tranx type of inventory and accounting transaction
    Field('transaction_group_type','integer'),
    Field('location', 'integer'),   # from location master
    Field('transaction_type_ref', 'string', length = 10), # from library
    Field('transaction_date_entered', 'date',default=request.now), # entry date  = > to remove
    Field('department','integer'), # from consolidated merch stock header        
    Field('type','integer'),  # 1-ACCOUNT TRNX / 2-INVENTORY TRANX => GROUP TYPE OF TRANX ex: ACCT,INVT
    Field('reference_no','string',length=30), # prefix + voucher no
    Field('account_reference_no','string',length=30), # ex: no prefix, only voucher no 
    Field('account_code','string',length=15), # general account suppler, customer, etc
    Field('description','string'), 
    Field('credit','decimal(20,6)',default=0), # computed credit  amount
    Field('debit','decimal(20,6)',default=0), # computed debit amount 
    Field('due_date','date'), # selective transaction from invoices
    Field('amount_paid','decimal(20,6)',default=0),# actual paid, accumulate
    Field('paid','boolean',default = False), # rv confirmation and account reconcillation
    Field('prepared','boolean',default = False), # from receipt voucher prepartion
    Field('status','boolean',default = False), # cancelled / deleted, for admin purpose
    Field('posted','boolean',default = False), #flag_post
    Field('person','string',length = 50),
    Field('entrydate','date'), # actual transaction date of entry to ledger
    Field('bank_code','string',length = 10), # from master acccount 
    Field('cheque_no','string',length = 25), # for cash check and pdc
    Field('cheque_bank_name','string',length=50),    
    Field('rv_payment_reference','string'), # rv payment
    Field('cost_center','string',length=15), # like account code from master account
    Field('location_cost_center','string',lenght=5), # like account code from master account
    Field('acct_code2','string',length=8),    
    Field('voucher_no_id','integer'), # 10 length  
    Field('gl_entry_ref','string'),
    Field('batch_posting_seq','integer',default=0),    
    Field('reconciliation_transaction_no','string'), # automated serial from reconciliation table
    Field('mark','boolean',default = False), # marking for reconciliation
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('General_Ledger_Summary', # Financial year commulative
    Field('financial_year', 'date'), #
    Field('month', 'date'),
    Field('general_ledger_id','integer'),
    Field('department','integer'), # from consolidated merch stock header
    Field('account_code','string',length=15), # general account suppler, customer, etc
    Field('description','string'), 
    Field('credit','decimal(20,6)',default=0), # computed credit  amount
    Field('debit','decimal(20,6)',default=0), # computed debit amount 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('General_Ledger_Detail',
    Field('transaction_date','date',default=request.now),
    Field('transaction_type','string',length=3),
    Field('department','integer'),
    Field('type','integer'),
    Field('account_reference_no','string',length=20),
    Field('account_code','string',length=15),
    Field('description','string',length=50),
    Field('credit','decimal(20,6)',default=0),
    Field('debit','decimal(20,6)',default=0),
    Field('due_date','date'),
    Field('amount_paid','decimal(20,6)',default=0),
    Field('status','boolean',default = False),
    Field('flgpost','boolean',default = False),
    Field('person','string',length = 50),
    Field('entrydate','date'),
    Field('accsref','integer'),
    Field('bank_code','string',length = 10), # from master acccount
    Field('cost_center','string',length=15), # like account code from master account
    Field('location_cost_center','string',lenght=5), # like account code from master account
    Field('acct_code2','string',length=8),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))



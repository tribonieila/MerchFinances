# ----------  receipt voucher  -----------
db.define_table('Receipt_Voucher_Header',     
    Field('voucher_no','string',length=20), # voucher serial no
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('rv_confirmation_reference','string',length=50), # from rv confirmation, updated
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('account_payment_mode_id','reference Account_Voucher_Payment_Mode',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))),    
    Field('account_voucher_payment_code','string',length=5), # remove
    Field('receipt_voucher_confirmation_type_id','string',length=10,requires = IS_EMPTY_OR(IS_IN_SET([('A','CASH/CASH CHEQUE'),('B','POST DATED CHEQUE')], zero = 'Choose Confirmation Type'))), # remove
    Field('total_amount','decimal(20,6)',default=0),
    Field('amount_paid','decimal(20,6)',default=0), # during receipt voucher confirmation / actual amount deposited to the bank
    Field('account_code','string',length=20), # bank code
    Field('bank_name_id','reference Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Bank_Master.id,'%(bank_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date'),
    Field('purpose','string',length=50), # to remove
    Field('received_from','string',length=50),
    Field('collected_by','string',length=50),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('cost_center','string',length=15), # to remove
    Field('location_cost_center','string',length=15), # remove
    Field('gl_entry_ref','string'),
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'RV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('posting_ref_no','string',length=20), # ex: RV,RV,JV etc # to remove
    Field('remarks','text'),       
    Field('manual_rv_no','string',length=20), 
    Field('last_reconciled_amount','decimal(20,6)',default=0), # update from account recon confirmation/accumulative
    Field('reconciliation_request','boolean',default = False), # mark true as requested
    Field('reconciled','boolean',default = False), # mark from reconciliation_transaction_no
    Field('reconciled_amount','decimal(20,6)',default=0), # update from reconciled amount header
    Field('reconciliation_transaction_ref','string'), # -> to string
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(voucher_no)s')

db.define_table('Receipt_Voucher_Transaction',    
    Field('receipt_voucher_header_id','reference Receipt_Voucher_Header', ondelete = 'NO ACTION', writable = False),
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_credit_code','string',length=20), # to rv and jv
    Field('account_debit_code','string',length=20),# to pv and jv # to remove
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal
    Field('location_cost_center_id','reference General_Location_Cost_Center', ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Location_Cost_Center.id,'%(location_code)s - %(location_name)s',zero='Choose Location'))),# location cost center id to remove
    Field('location_code','string',length = 10), # location cost center normal to remove
    Field('transaction_payment_type_id','reference Transaction_Payment_Type',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Transaction_Payment_Type.id,'%(transaction_payment_type)s - %(transaction_payment_name)s',zero='Choose Payment Type'))),# transaction_payment_type
    Field('amount_paid','decimal(20,6)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('rv_confirmation_reference','string',length=50), # from rv confirmation, updated
    Field('voucher_no','string',length=20), # voucher serial no
    Field('ticket_no_id','string',length=20,writable=False,readable=False), # to remove
    Field('gl_entry_ref','string'),    
    Field('department','integer'), # from general ledger if against invoice type
    Field('invoice_no','string',length=30), # from general ledger if against invoice type
    Field('location','integer'), # from general ledger if against invoice type 
    Field('gl_id','integer',default=0), # for duplicate entry from general ledger = rv against invoice
    Field('mark','boolean',default = False), # marking for reconciliation
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Receipt_Voucher_Request', 
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
    Field('cheque_dated','date'),
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
    Field('manual_rv_no','string',length=20),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(voucher_no)s')

db.define_table('Receipt_Voucher_Transaction_Request',    
    Field('receipt_voucher_request_id','reference Receipt_Voucher_Request', ondelete = 'NO ACTION', writable = False),
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
# ----------  receipt voucher  -----------
# ----------  receipt voucher confirmation -----------
db.define_table('Receipt_Voucher_Confirmation', 
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
    Field('account_code2','string',length=20), # HEADER CREDIT ENTRY/ PDC/CASH + CASH CHEQUE (02-20 , 08-02)
    Field('bank_name_id','reference Merch_Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Merch_Bank_Master.id,'%(account_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date'),
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
    Field('manual_rv_no','string',length=20),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(voucher_no)s')

db.define_table('Receipt_Voucher_Transaction_Confirmation',    
    Field('receipt_voucher_confirmation_id','reference Receipt_Voucher_Confirmation', ondelete = 'NO ACTION', writable = False),
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
    Field('bank_name_id','reference Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Bank_Master.id,'%(bank_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date'),
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

db.define_table('Receipt_Voucher_Transaction_Confirmation_Request',    
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
    Field('bank_name_id','reference Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Bank_Master.id,'%(bank_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date',default=request.now),
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

# ----------  receipt voucher confirmation -----------

# ----------  payment voucher confirmation -----------
db.define_table('Payment_Voucher_Header', 
    Field('payment_voucher_no','string',length=20), # voucher serial no
    Field('payment_voucher_date','date'), 
    Field('payment_voucher_request_no','integer', default=0), # auto generate
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('payee','string',length=50), # 
    Field('custom_declaration_no','string',length=35), 
    Field('custom_invoice_no','string',length=35),     
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('account_payment_mode_id','reference Account_Voucher_Payment_Mode',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))),    
    Field('total_amount','decimal(20,2)',default=0),
    Field('account_code','string',length=20), # bank code
    Field('bank_name_id','reference Merch_Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Merch_Bank_Master.id,'%(account_code)s - %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date'),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'RV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('remarks','text'),       
    Field('manual_pv_no','string',length=20), 
    Field('gl_entry_ref','string',writable=False,readable=False),
    Field('file_upload','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),        
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Payment_Voucher_Transaction',    
    Field('payment_voucher_header_id','reference Payment_Voucher_Header', ondelete = 'NO ACTION', writable = False),    
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_debit_code','string',length=20),# to pv and jv 
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal        
    Field('transaction_payment_type_id','reference Transaction_Payment_Type',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Transaction_Payment_Type.id,'%(transaction_payment_type)s - %(transaction_payment_name)s',zero='Choose Payment Type'))),# transaction_payment_type
    Field('amount','decimal(20,2)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), 
    Field('department','integer'), 
    Field('invoice_no','string',length=30),
    Field('location','integer'), 
    Field('cost_center_category_id','reference Cost_Center_Category',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_category_code','string',length=20), 
    Field('cost_center_id','reference Cost_Center',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_code','string',length=20), 
    Field('gl_id','integer',default=0,writable=False,readable=False), 
    Field('gl_entry_ref','string',writable=False,readable=False),    
    Field('payment_voucher_request_no','integer', default=0), # auto generate
    Field('payment_voucher_no','string',length=20), # voucher serial no    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Payment_Voucher_Request', 
    Field('payment_voucher_request_no','integer', default=0), # auto generate
    Field('payment_voucher_no','string',length=20), # voucher serial no    
    Field('payment_voucher_date','date'), 
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('payee','string',length=50), # 
    Field('custom_declaration_no','string',length=35), 
    Field('custom_invoice_no','string',length=35),     
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=23), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10,default='PV'), # ex. RV,PV,JV    
    Field('account_payment_mode_id','reference Account_Voucher_Payment_Mode',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Account_Voucher_Payment_Mode.id,'%(account_voucher_payment_code)s - %(account_voucher_payment_name)s',zero='Choose Payment Mode'))),    
    Field('total_amount','decimal(20,2)',default=0),
    Field('account_code','string',length=20), # bank code
    Field('bank_name_id','reference Merch_Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Merch_Bank_Master.id,'%(account_code)s : %(bank_name)s',zero='Choose Bank'))),    
    Field('cheque_no','string',length=15),
    Field('cheque_dated','date'),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('manual_pv_no','string',length=20),     
    Field('remarks','text'),       
    Field('management_remarks','text'),
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'PV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('gl_entry_ref','string',writable=False,readable=False),
    Field('ticket_no_id','string',length=20),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Payment_Voucher_Transaction_Request',    
    Field('payment_voucher_request_id','reference Payment_Voucher_Request', ondelete = 'NO ACTION', writable = False),
    Field('account_voucher_transaction_type','integer',default=23), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10,default='PV'), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_debit_code','string',length=20),# to pv and jv 
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal        
    Field('transaction_payment_type_id','reference Transaction_Payment_Type',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Transaction_Payment_Type.id,'%(transaction_payment_type)s - %(transaction_payment_name)s',zero='Choose Payment Type'))),# transaction_payment_type
    Field('amount','decimal(20,2)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('voucher_no','string',length=20), # voucher serial no        
    Field('department','integer'), # from general ledger if against invoice type
    Field('invoice_no','string',length=30), # from general ledger if against invoice type
    Field('location','integer'), # from general ledger if against invoice type 
    Field('cost_center_category_id','reference Cost_Center_Category',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_category_code','string',length=20), 
    Field('cost_center_id','reference Cost_Center',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_code','string',length=20), 
    Field('gl_id','integer',default=0), # for duplicate entry from general ledger = rv against invoice
    Field('gl_entry_ref','string',writable=False,readable=False),    
    Field('ticket_no_id','string',length=20,writable=False,readable=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))
# ----------  payment voucher confirmation -----------


# ----------  journal voucher confirmation -----------
db.define_table('Journal_Voucher_Header', 
    Field('journal_voucher_no','string',length=20), # voucher serial no
    Field('journal_voucher_date','date'), 
    Field('journal_voucher_request_no','integer', default=0), # auto generate
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('journal_voucher_type_id','string',length=10, requires = IS_EMPTY_OR(IS_IN_SET([('A','Adjustment'),('P','Payment'),('S','Sales')], zero = 'Choose Adjustment Type'))), # ex: Adjustment, Payment, Sales
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('total_amount','decimal(20,2)',default=0),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'RV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('remarks','text'),       
    Field('gl_entry_ref','string',writable=False,readable=False),
    Field('file_upload','upload',requires=IS_EMPTY_OR(IS_UPLOAD_FILENAME(extension='pdf',error_message='pdf file required.'))),        
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Journal_Voucher_Transaction',    
    Field('journal_voucher_header_id','reference Journal_Voucher_Header', ondelete = 'NO ACTION', writable = False),    
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_debit_code','string',length=20),# to pv and jv 
    Field('account_credit_code','string',length=20),# to pv and jv 
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal        
    Field('amount','decimal(20,2)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), 
    Field('department','integer'), 
    Field('invoice_no','string',length=30),
    Field('location','integer'), 
    Field('cost_center_category_id','reference Cost_Center_Category',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_category_code','string',length=20), 
    Field('cost_center_id','reference Cost_Center',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'))), # ex:
    Field('cost_center_code','string',length=20), 
    Field('journal_voucher_request_no','integer', default=0), # auto generate
    Field('journal_voucher_no','string',length=20), # voucher serial no    
    Field('gl_id','integer',default=0,writable=False,readable=False), 
    Field('gl_entry_ref','string',writable=False,readable=False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Journal_Voucher_Header_Request', 
    Field('journal_voucher_no','string',length=20), # voucher serial no
    Field('journal_voucher_date','date'), 
    Field('journal_voucher_request_no','integer', default=0), # auto generate
    Field('account_reference','string',length=15), # ex. invoice name or any references
    Field('journal_voucher_type_id','string',length=10, requires = IS_EMPTY_OR(IS_IN_SET([('A','Adjustment'),('P','Payment'),('S','Sales')], zero = 'Choose Adjustment Type'))), # ex: Adjustment, Payment, Sales
    Field('transaction_reference_date','date',default=request.now), # dynamic/input from user
    Field('account_voucher_transaction_type','integer',default=0), # need to remove ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV    
    Field('total_amount','decimal(20,2)',default=0),
    Field('entry_date','date',default=request.now, writable=False, readable=False), # entry date / transaction _date, actual date of transaction
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'JV-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('remarks','text'),       
    Field('gl_entry_ref','string',writable=False,readable=False),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('requested_by', db.auth_user, ondelete = 'NO ACTION', writable = False, readable = False),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Journal_Voucher_Transaction_Request',    
    Field('journal_voucher_header_request_id','reference Journal_Voucher_Header_Request', ondelete = 'NO ACTION', writable = False),    
    Field('account_voucher_transaction_type','integer',default=0), # ex. 20,21     
    Field('account_voucher_transaction_code','string',length=10), # ex. RV,PV,JV        
    Field('account_code','string',length=20), # from master account bank code
    Field('account_debit_code','string',length=20),# to pv and jv 
    Field('account_credit_code','string',length=20),# to pv and jv 
    Field('dept_code_id','reference General_Department_Cost_Center',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.General_Department_Cost_Center.id,'%(department_code)s - %(department_name)s',zero='Choose Department'))),                
    Field('department_code', 'string', length = 10), # department normal        
    Field('amount','decimal(20,2)',default=0),
    Field('description','string',length=50),
    Field('account_reference','string',length=15), 
    Field('department','integer'), 
    Field('invoice_no','string',length=30),
    Field('location','integer'), 
    Field('cost_center_category_id','reference Cost_Center_Category',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center_Category.id,'%(cost_center_category_name)s, %(cost_center_category_code)s',zero='Choose Payment Type'),null=None)), # ex:
    Field('cost_center_category_code','string',length=20), 
    Field('cost_center_id','reference Cost_Center',ondelete = 'NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Cost_Center.id,'%(cost_center_name)s, %(cost_center_code)s',zero='Choose Payment Type'),null=None)), # ex:
    Field('cost_center_code','string',length=20), 
    Field('journal_voucher_request_no','integer', default=0), # auto generate
    Field('journal_voucher_no','string',length=20), # voucher serial no    
    Field('gl_id','integer',default=0,writable=False,readable=False), 
    Field('gl_entry_ref','string',writable=False,readable=False),    
    Field('ticket_no_id','string',length=20,writable=False,readable=False),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))



# ----------  journal voucher confirmation -----------

# ----------   reconciliation transaction  -----------
db.define_table('Account_Reconciliation_Header',
    Field('reconciliation_transaction_no','integer'), # automated serial from reconciliation table
    Field('reconciliation_date','date'), # automated serial from reconciliation table
    Field('voucher_no','string',length=20), # rv no from Receipt_Voucher_Header
    Field('rv_amount','decimal(20,6)',default=0), # selected from rv
    Field('total_reconciled_amount','decimal(20,6)',default=0), # compounted from transactions
    Field('rv_balanced_amount','decimal(20,6)',default=0), # ex: rv_balanced_amount = rv_amount - total_reconciled_amount    
    Field('reconciled_amount_entry','decimal(20,6)',default=0), # realtime calculation of reconciled amount
    Field('requested_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'AR-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Reconciliation_Transaction',
    Field('account_reconciliation_header_id','reference Account_Reconciliation_Header', ondelete = 'NO ACTION', writable = False),
    # Field('reconciliation_transaction_no','integer'), # automated serial from reconciliation table
    # Field('reconciliation_date','date'), # automated serial from reconciliation table
    Field('transaction_type','integer'), # from consolidated merch stock header, specific tranx type of inventory and accounting transaction
    Field('transaction_date','date',default=request.now), # grv date/ purchase receipt date
    Field('entry_date','date'), # actual transaction date of entry to ledger
    Field('transaction_prefix_id', 'reference GL_Transaction_Serial', ondelete = 'NO ACTION',writable = False),   # TRNX            
    Field('transaction_no','integer',default=0,writable = False), # transaction ref => serial ex: 
    Field('transaction_type_ref', 'string', length = 10), # from library
    Field('location', 'integer'),   # from location master
    Field('department','integer'), # from consolidated merch stock header        
    Field('type','integer'),  # 1-ACCOUNT TRNX / 2-INVENTORY TRANX => GROUP TYPE OF TRANX ex: ACCT,INVT
    Field('reference_no','string',length=30), # prefix + voucher no
    Field('account_reference_no','string',length=30), # ex: no prefix, only voucher no 
    Field('account_code','string',length=15), # general account suppler, customer, etc
    Field('description','string'), 
    Field('credit','decimal(20,6)',default=0), # computed credit  amount
    Field('debit','decimal(20,6)',default=0), # computed debit amount 
    Field('rv_payment_reference','string',length=30), # rv payment
    Field('balanced_amount','decimal(20,6)',default=0),# actual balanced amount
    Field('amount_paid','decimal(20,6)',default=0),# actual paid, accumulate
    Field('new_amount_paid','decimal(20,6)',default=0),# new/current payment
    Field('paid','boolean',default = False), # rv confirmation and account reconcillation
    Field('acct_code2','string',length=8),    
    Field('status','boolean',default = False), # cancelled / deleted, for admin purpose
    Field('posted','boolean',default = False), # flag_post            
    Field('gl_entry_ref','string'),    
    Field('requested_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('status_id','integer', default = 0, writable = False, requires = IS_EMPTY_OR(IS_IN_SET([('1','Deleted'),('2','Requested'),('3','Approved'),('4','Confirmed'),('5','Posted')]))), 
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Reconciliation_Header_Request',
    Field('reconciliation_transaction_no','integer'), # automated serial from reconciliation table
    Field('reconciliation_date','date'), # automated serial from reconciliation table
    Field('voucher_no','string',length=20), # rv no from Receipt_Voucher_Header
    Field('rv_amount','decimal(20,6)',default=0), # selected from rv
    Field('total_reconciled_amount','decimal(20,6)',default=0), # compounded from transactions
    Field('rv_balanced_amount','decimal(20,6)',default=0), # ex: rv_balanced_amount = rv_amount - total_reconciled_amount    
    Field('reconciled_amount_entry','decimal(20,6)',default=0), # realtime calculation of reconciled amount
    Field('requested_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('status_id','reference Accounts_Workflow_Status',ondelete = 'NO ACTION',requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'AR-TASK1'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')),   
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Reconciliation_Transaction_Request',
    Field('account_reconciliation_header_request_id','reference Account_Reconciliation_Header_Request', ondelete = 'NO ACTION', writable = False),
    Field('transaction_type','integer'), # from consolidated merch stock header, specific tranx type of inventory and accounting transaction
    Field('transaction_date','date',default=request.now), # grv date/ purchase receipt date
    Field('entry_date','date'), # actual transaction date of entry to ledger
    Field('transaction_prefix_id', 'reference GL_Transaction_Serial', ondelete = 'NO ACTION',writable = False),   # TRNX            
    Field('transaction_no','integer',default=0,writable = False), # transaction ref => serial ex: 
    Field('transaction_type_ref', 'string', length = 10), # from library
    Field('location', 'integer'),   # from location master
    Field('department','integer'), # from consolidated merch stock header        
    Field('type','integer'),  # 1-ACCOUNT TRNX / 2-INVENTORY TRANX => GROUP TYPE OF TRANX ex: ACCT,INVT
    Field('reference_no','string',length=30), # prefix + voucher no
    Field('account_reference_no','string',length=30), # ex: no prefix, only voucher no 
    Field('account_code','string',length=15), # general account suppler, customer, etc
    Field('description','string'), 
    Field('credit','decimal(20,6)',default=0), # computed credit  amount
    Field('debit','decimal(20,6)',default=0), # computed debit amount 
    Field('rv_payment_reference','string',length=30), # rv payment
    Field('amount_paid','decimal(20,6)',default=0),# actual paid, last actual payment
    Field('balanced_amount','decimal(20,6)',default=0),# actual balanced amount        
    Field('new_amount_paid','decimal(20,6)',default=0),# new/current payment
    Field('paid','boolean',default = False), # rv confirmation and account reconcillation
    Field('acct_code2','string',length=8),    
    Field('status','boolean',default = False), # cancelled / deleted, for admin purpose
    Field('posted','boolean',default = False), # flag_post            
    Field('gl_entry_ref','string'),
    Field('requested_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('requested_on', 'datetime', default=request.now, writable = False, readable = False),    
    Field('mark','boolean',default = False), # marking for reconciliation
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

# d2.define_table('General_Location_Cost_Center',    
#     Field('location_code','string', length = 5),
#     Field('location_name','string', length = 50),    
#     Field('cost_center','string',length = 15))

# d2.define_table('Cost_Center_Category',
#     Field('cost_center_category_group_id', 'integer'),
#     Field('cost_center_category_code', 'string', length=15),
#     Field('cost_center_category_name', 'string', length=50))

# d2.define_table('Cost_Center',
#     Field('cost_center_category_group_id', 'integer',default =0),
#     Field('cost_center_code', 'string', length=15),
#     Field('cost_center_name', 'string', length=50),
#     Field('dept_code_id','integer',default=0),                
#     Field('location_cost_center_id','integer',default=0))

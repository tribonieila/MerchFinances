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

db.define_table('Account_Transaction_Type', # receipt voucher, payment voucher, journal voucher
    Field('account_transaction_code','string',length=10),
    Field('account_transaction_name','string',length=50),
    Field('created_on','datetime', default=request.now, writable = False, readable = False),
    Field('created_by',db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on','datetime', update=request.now, writable = False, readable = False),
    Field('updated_by',db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(account_transaction_code)s')

db.define_table('Account_Payment_Mode', # cash, cash cheque, post-dated-cheque
    Field('payment_code','string',length=5),
    Field('payment_name','string',length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(payment_code)s')

db.define_table('Department',    
    Field('department_code','string', length = 5, label ='Department Code', requires = IS_NOT_IN_DB(db, 'Department.department_code')),
    Field('department_name','string', length = 50, label = 'Department Name', requires = [IS_UPPER(), IS_NOT_IN_DB(db, 'Department.department_name')]),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(department_code)s')

db.define_table('Department_Head_Assignment',
    Field('users_id', db.auth_user, ondelete = 'NO ACTION'),    
    Field('department_id','reference Department',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Department.id,'%(department_code)s - %(department_name)s',zero='Choose Department')),    
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Account_Voucher', #ondelete = 'NO ACTION', requires = IS_IN_DB(db, db.Department.id, '%(department_code)s - %(department_name)s', zero = 'Choose Department')),
    Field('account_transaction_code_id','reference Account_Transaction_Type',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Account_Transaction_Type.id,'%(account_transaction_code)',zero='Choose Account Code')),
    Field('reference_date','date',default=request.now),
    Field('reference_no','integer'),
    Field('account_payment_mode_id','reference Account_Payment_Mode',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Account_Payment_Mode.id,'%(payment_code)', zero='Choose Payment Code')),
    Field('total_amount','decimal(10,2)',default=0),
    Field('account_code_id','string',length=10),
    Field('bank_name','string',length=50),
    Field('cheque_no','string',length=15),
    Field('cheque_date','date',default=request.now),
    Field('purpose','integer'),
    Field('post_ref_no','string',length=10),
    Field('person','string',length=20),
    Field('entry_date','date',default=request.now),
    Field('cost_center','string',length=15),
    Field('location_center','string',length=5),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(reference_no)s')

db.define_table('Account_Transaction',
    Field('account_voucher_id','reference Account_Voucher'),
    Field('account_transaction_type_id','string'),
    Field('department_id','reference Department',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Department.id,'%(department_code)',zero='Choose Department')),    
    Field('voucher_reference','string',length=10),
    Field('amount_paid','decimal(10,2)',default=0),
    Field('description','string',length=50),
    Field('account_credit_code','string',length=10),
    Field('account_debit_code','string',length=10),
    Field('account_type','integer',length=1),
    Field('account_reference','integer',length=10),
    Field('account_date','date',default=request.now),
    Field('bank_code','string',length=10),
    Field('person','string',length=50),
    Field('entry_date','date',default=request.now),
    Field('user','string',length=10),
    Field('cost_center','string',length=15),
    Field('location_center','string',length=5),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Business_Unit',
    Field('business_name','string',length=50),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format='%(business_name)s')

db.define_table('Record_Status',
    Field('status','string',length=20, requires = [IS_LENGTH(20),IS_UPPER(), IS_NOT_IN_DB(db, 'Record_Status.status')]),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False),format = '%(status)s')

db.define_table('Note_Status',
    Field('status', 'string', length = 10),
    Field('action_required','string', length = 50),
    Field('description', 'string', length = 50),         
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION',default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION',update=auth.user_id, writable = False, readable = False), format = 'mnemonic')

db.define_table('Currency',
    Field('mnemonic', 'string', length = 10, requires = [IS_LENGTH(10), IS_UPPER()]),
    Field('description', 'string', length = 50, requires = [IS_LENGTH(50), IS_UPPER()]), 
    Field('status_id','reference Record_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Record_Status.id,'%(status)s', zero = 'Choose status')), 
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

db.define_table('Debit_Credit',
    Field('serial_note','string',length=15),
    Field('department_id','reference Department',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Department.id,'%(department_code)s - %(department_name)s',zero='Choose Department')),    
    Field('business_unit','reference Business_Unit',ondelete='NO ACTION',requires=IS_IN_DB(db,db.Business_Unit.id,'%(business_name)s', zero='Choose Business Unit')),
    Field('transaction_date','date',request.now),
    Field('transaction_type','string',length=25,requires = IS_IN_SET(['Debit Note','Credit Note'], zero = 'Transaction Type')),
    Field('note_type','string',length=25,requires=IS_IN_SET(['Normal','Stand Rent'],zero='Type of Note')),
    Field('currency_id', 'reference Currency', requires = IS_IN_DB(db, db.Currency.id, '%(mnemonic)s - %(description)s', zero = 'Choose Currency')),
    Field('brand_code_id','reference Stand_Rent_Brand',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Stand_Rent_Brand.id,'%(brand_code)s - %(brand_name)s',zero='Choose Brand Name'))),
    Field('total_amount','decimal(10,2)',default=0),
    Field('remarks','string'),
    Field('account_remarks','string'),
    Field('department_remarks','string'),
    Field('management_remakrs','string'),
    Field('status_id','reference Note_Status', ondelete = 'NO ACTION', label = 'Status', default = 1, requires = IS_IN_DB(db, db.Note_Status.id,'%(status)s', zero = 'Choose status')), 
    Field('cancelled','boolean',default=False),
    Field('ticket_no', 'string', length = 10),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Debit_Credit_Transaction',
    Field('serial_note_id','reference Debit_Credit',ondelete='NO ACTION',writable=False,readable=False),
    Field('transaction_no','string',length=20),
    Field('account_code'),
    Field('description_1','string'),
    Field('description_2','string'),
    Field('date_from','date'),
    Field('date_to','date'),
    Field('amount','decimal(10,2)'),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False))

db.define_table('Debit_Credit_Transaction_Temporary',    
    Field('account_code'),
    Field('description_1','string'),
    Field('description_2','string'),
    Field('date_from','date'),
    Field('date_to','date'),
    Field('amount','decimal(10,2)'),
    Field('ticket_no_id', 'string', length = 10))
    
db.define_table('acctvou',
    Field('type','integer'),
    Field('refdte','date',default=request.now),
    Field('refno','integer'),
    Field('modeofpay','integer'),
    Field('totalamount','decimal(10,2)',default=0),
    Field('acctcode','string',length=10),
    Field('bankname','string',length=50),
    Field('chequeno','string',length=15),
    Field('dated','date',default=request.now),
    Field('purpose','integer'),
    Field('postrefno','string',length=10),
    Field('person','string',length=20),
    Field('entrydate','date',default=request.now),
    Field('ccent','string',length=15),
    Field('loccent','string',length=5),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(sector)s')

db.define_table('accttrn',
    Field('department','integer'),
    Field('voutype','integer'),
    Field('vouref','string',length=10),
    Field('amntpaid','decimal(10,2)',default=0),
    Field('descript','string',length=50),
    Field('acctcrcode','string',length=10),
    Field('acctdbcode','string',length=10),
    Field('accstype','integer',length=1),
    Field('accsref','integer',length=10),
    Field('accsdte','date',default=request.now),
    Field('bankcode','string',length=10),
    Field('person','string',length=50),
    Field('entrydte','date',default=request.now),
    Field('user','string',length=10),
    Field('ccent','string',length=15),
    Field('loccent','string',length=5),
    Field('created_on', 'datetime', default=request.now, writable = False, readable = False),
    Field('created_by', db.auth_user, ondelete = 'NO ACTION', default=auth.user_id, writable = False, readable = False),
    Field('updated_on', 'datetime', update=request.now, writable = False, readable = False),
    Field('updated_by', db.auth_user, ondelete = 'NO ACTION', update=auth.user_id, writable = False, readable = False), format = '%(sector)s')

from datetime import datetime, date
import locale
import datetime
import random
import string
# import date
locale.setlocale(locale.LC_ALL, '')
_arr = []

def put_batch_posting_sequence_id():
    # _id = db(db.Batch_Posting_Sequence.prefix_seq == request.args(0)).select().first()
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq

def get_item_description():
    # _gl = db(db.General_Ledger.reference_no == request.vars.account_reference).select().first()
    _ah = db(db.Receipt_Voucher_Header.account_reference == request.vars.account_reference).select().first()
    if _ah:
        _text_description = db(db.GL_Description_Library.id == 11).select().first()
        _field_description = _description = str(_text_description.common_text) + ' ' + str(request.vars.account_reference)
        _total_amount = float(_ah.total_amount or 0) - float(_ah.amount_paid or 0)
        if (int(_ah.account_payment_mode_id) == 3) or (int(_ah.account_payment_mode_id) == 2):            
            _field_description = str(_text_description.common_text2) + str(_ah.bank_name_id.bank_name.upper()) + ' CHQ #' +str(_ah.cheque_no)
            response.js = "$('#Receipt_Voucher_Transaction_Confirmation_Request_amount_paid').prop('readonly', true);$('#Receipt_Voucher_Transaction_Confirmation_Request_account_code').val('%s');$('#Receipt_Voucher_Transaction_Confirmation_Request_description').val('%s');$('#Receipt_Voucher_Transaction_Confirmation_Request_amount_paid').val('%s');" %(_ah.account_code, _field_description, locale.format('%.2F',_total_amount or 0))
        elif int(_ah.account_payment_mode_id) == 1:
            _field_description = str(_text_description.common_text) + ' ' + str(request.vars.account_reference)
            response.js = "$('#Receipt_Voucher_Transaction_Confirmation_Request_account_code').val('%s');$('#Receipt_Voucher_Transaction_Confirmation_Request_description').val('%s');$('#Receipt_Voucher_Transaction_Confirmation_Request_amount_paid').val('%s');" %(_ah.account_code, _field_description, locale.format('%.2F',_total_amount or 0))
        return DIV(SPAN(I(_class='fas fa-info-circle'),_class='info-box-icon bg-aqua'),DIV(SPAN('Account Reference',_class='info-box-text'),SPAN(str(_description),_class='info-box-number'),_class='info-box-content'),_class='info-box')
    elif not _ah:
        response.js = "$('#Receipt_Voucher_Transaction_Confirmation_Request_account_code').val('');$('#Receipt_Voucher_Transaction_Confirmation_Request_description').val('');$('#Receipt_Voucher_Transaction_Confirmation_Request_amount_paid').val('0');" 
        return DIV(SPAN(I(_class='fas fa-times-circle'),_class='info-box-icon bg-red'),DIV(SPAN('Account Reference',_class='info-box-text'),SPAN('Not Found!',_class='info-box-number'),_class='info-box-content'),_class='info-box')

def patch_receipt_voucher():
    if int(request.args(0)) == 1: # RV Conf. Type
        _voucher_type = 0
        if request.vars.receipt_voucher_confirmation_type_id == 'A':
            _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC1').select().first()
            _voucher_type = _voucher_type.voucher_serial_no + 1
        elif request.vars.receipt_voucher_confirmation_type_id == 'B':
            _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC2').select().first()
            _voucher_type = _voucher_type.voucher_serial_no + 1
        response.js = "$('#no_table_voucher_no').val('%s');" % (_voucher_type)
    elif int(request.args(0)) == 2: # Deposited To Bank Account Code
        _ba = db((db.Merch_Bank_Master.account_code == request.vars.account_code) & (db.Merch_Bank_Master.status_id == 1)).select().first()
        if _ba:
            response.js = "$('#bank_name').val('%s');" % (_ba.bank_name)
        elif not _ba:
            print('false')
    elif int(request.args(0)) == 3: # submit/save button        
        _trnx = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id).count()
        if int(_trnx or 0) <= 0:
            response.js = "alertify.notify('Empty account reference not allowed.','warning')"
        elif int(_trnx or 0) > 0:
            _voucher_type = 0
            if request.vars.receipt_voucher_confirmation_type_id == 'A': # cash 02 account code
                _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC1').select().first()
                _voucher_type.voucher_serial_no += 1
                _voucher_type.update_record()
            elif request.vars.receipt_voucher_confirmation_type_id == 'B': # pdc 08 account code
                _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC2').select().first()
                _voucher_type.voucher_serial_no += 1
                _voucher_type.update_record()
            _bank_name_id = db(db.Merch_Bank_Master.id == request.vars.bank_name_id).select().first()
            _bank_name_code = ''
            if _bank_name_id:
                _bank_name_code = _bank_name_id.account_code
            db.Receipt_Voucher_Confirmation.insert(
                voucher_no = _voucher_type.voucher_serial_no,
                transaction_reference_date = request.vars.transaction_reference_date,
                account_voucher_transaction_type = _voucher_type.account_voucher_transaction_type,
                account_voucher_transaction_code = _voucher_type.account_voucher_transaction_code,
                receipt_voucher_confirmation_type_id = request.vars.receipt_voucher_confirmation_type_id,
                account_code = _bank_name_code,
                account_reference = str(_voucher_type.account_voucher_transaction_code) + str(_voucher_type.voucher_serial_no),
                remarks = request.vars.remarks.upper(),
                status_id = 11)
            _head = db(db.Receipt_Voucher_Confirmation.voucher_no == _voucher_type.voucher_serial_no).select().first()
            _total_amount = db.Receipt_Voucher_Transaction_Confirmation_Request.amount_paid.sum().coalesce_zero()
            _total_amount = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id).select(_total_amount).first()[_total_amount]            
            
            _account_ref = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id).select().first()
            
            for n in db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id).select():

                # ------ update request/receipt header transaction --------------------
                _amount_paid = 0
                _req = db(db.Receipt_Voucher_Request.account_reference == str(n.account_reference)).select().first() # request header table
                _rec = db((db.Receipt_Voucher_Header.account_reference == str(n.account_reference)) & (db.Receipt_Voucher_Header.account_code == n.account_code)).select().first() # receipt header table

                _ref = _head.account_reference
                _amount_paid = float(n.amount_paid or 0)
                _status_id = 10
                if float(_rec.amount_paid or 0) > 0.0:                    
                    _ref = str(_rec.rv_confirmation_reference) + ' | ' + str(_head.account_reference)
                    _amount_paid = float(_rec.amount_paid or 0) + float(n.amount_paid or 0)
                    if (float(_amount_paid or 0) == float(_rec.total_amount or 0)):
                        _status_id = 11    
                elif (float(n.amount_paid or 0) == float(_rec.total_amount or 0)) or (float(_amount_paid or 0) == float(_rec.total_amount or 0)):
                    _status_id = 11                
                _req.update_record(status_id = _status_id)
                _rec.update_record(status_id = _status_id, rv_confirmation_reference = _ref, amount_paid = _amount_paid)
                for x in db(db.Receipt_Voucher_Transaction.receipt_voucher_header_id == _rec.id).select():
                    x.update_record(rv_confirmation_reference = _rec.account_reference)                
                # ------ update request/receipt header transaction --------------------

                # ------ transaction table insertion --------------------------------

                db.Receipt_Voucher_Transaction_Confirmation.insert(
                    receipt_voucher_confirmation_id = _head.id,
                    account_voucher_transaction_type = _head.account_voucher_transaction_type,
                    account_voucher_transaction_code = _head.account_voucher_transaction_code,
                    account_code = n.account_code,
                    account_reference = n.account_reference,
                    account_credit_code = n.account_credit_code,
                    account_debit_code = n.account_debit_code,
                    dept_code_id = n.dept_code_id,
                    department_code = n.department_code,
                    location_cost_center_id = n.location_cost_center_id,
                    location_code = n.location_code,
                    transaction_payment_type_id = n.transaction_payment_type_id,
                    amount_paid = n.amount_paid,
                    description = n.description,
                    voucher_no = _head.voucher_no,
                    gl_entry_ref = n.gl_entry_ref,
                    department = n.department, 
                    invoice_no = n.invoice_no,
                    bank_name_id = n.bank_name_id,
                    cheque_no = n.cheque_no,
                    cheque_date = n.cheque_dated,
                    location = n.location)
                # ------ transaction table insertion --------------------------------

            _head.update_record(total_amount = _total_amount, account_code2 = _account_ref.account_code, requested_by = _rec.requested_by, requested_on = _rec.requested_on) # update confirmation header
            _account_ref.delete_record() # remove/delete confirmation transaction request

            # --------------- general ledger insertion --------------------------            
            # --------------- header debit entry/bank account code --------------
            _seq = put_batch_posting_sequence_id()    
            _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
            _row = db(db.GL_Transaction_Serial.id == 2).select().first() 
            _ga = db(db.General_Account.id == 1).select().first()
            _gl = db(db.GL_Description_Library.transaction_type == 21).select().first()
            _ser.serial_number += 1
            _row.serial_number += 1
            _voucher_no_serial1 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_head.account_code) + '/' + str(_row.serial_number)    
            _bank_name = 'None'
            if _head.bank_name_id:
                _bank_name = _head.bank_name_id.bank_name
            db.General_Ledger.insert(
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _head.transaction_reference_date,
                transaction_type = _head.account_voucher_transaction_type,
                location = 99, # general
                transaction_type_ref = _head.account_voucher_transaction_code,
                transaction_date_entered = request.now,
                department = 99, # general
                type = _head.account_voucher_transaction_type,
                reference_no = _head.account_reference,
                account_reference_no = _head.voucher_no,
                account_code = _head.account_code,
                description = str(_gl.common_text) + ' ' + str(_head.account_reference),
                entrydate = request.now,
                credit = 0,
                debit = _head.total_amount,
                amount_paid = 0,
                gl_entry_ref = _voucher_no_serial1,
                batch_posting_seq = _seq,
                bank_code = _head.account_code,
                # cheque_no = _head.cheque_no,
                # cheque_bank_name = _bank_name
            )
            _row.update_record()
            # HEADER CREDIT ENTRY/ PDC/CASH + CASH CHEQUE (02-20 , 08-02)
            # _ser.serial_number += 1
            _row.serial_number += 1
            _voucher_no_serial2 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_head.account_code) + '/' + str(_row.serial_number)    
            db.General_Ledger.insert(
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _head.transaction_reference_date,
                transaction_type = _head.account_voucher_transaction_type,
                location = 99, # general
                transaction_type_ref = _head.account_voucher_transaction_code,
                transaction_date_entered = request.now,
                department = 99, # general
                type = _head.account_voucher_transaction_type,
                reference_no = _head.account_reference,
                account_reference_no = _head.voucher_no,
                account_code = _head.account_code2,
                description = str(_gl.common_text) + ' ' + str(_head.account_reference),
                entrydate = request.now,
                credit = _head.total_amount,
                debit = 0,
                amount_paid = 0,
                gl_entry_ref = _voucher_no_serial2,
                batch_posting_seq = _seq,
                bank_code = _head.account_code2,
                # cheque_no = _head.cheque_no,
                # cheque_bank_name = _bank_name
            )
            _row.update_record()
            # RV CONFIRMATION TRANSACTION - REFERENCE RV NUMBER ENTERED ON RVC TRANSACTION, AMOUNT PAID UPDATE OF 02 AND 08 ACCOUNT
            for n in db(db.Receipt_Voucher_Transaction_Confirmation.receipt_voucher_confirmation_id == _head.id).select():
                # update record here gen_led_ref
                n.update_record(gl_entry_ref = str(_voucher_no_serial1) + ' | ' + str(_voucher_no_serial2))
                _gen_led = db((db.General_Ledger.account_code == n.account_code) & (db.General_Ledger.reference_no == n.account_reference)).select().first()
                _amount_paid = float(_gen_led.amount_paid or 0) + float(n.amount_paid or 0)
                _paid = False
                _cheque_no = _bank_name = 'None'
                if float(_gen_led.debit or 0) == float(_amount_paid or 0):
                    _paid = True
                if _head.receipt_voucher_confirmation_type_id == 'B':
                    _bank_name = n.bank_name_id.bank_code.upper()
                    _cheque_no = n.cheque_no
                    if _gen_led.amount_paid > 0.0:
                        _bank_name = str(_gen_led.cheque_bank_name) + ' | ' + str(n.bank_name_id.bank_code.upper())
                        _cheque_no = str(_gen_led.cheque_no) + ' | ' + str(n.cheque_no)
                _gen_led.update_record(amount_paid = _amount_paid, paid = _paid, bank_code = _head.account_code, rv_payment_reference = _head.account_reference, cheque_no = _cheque_no, cheque_bank_name = _bank_name)
            # GENERAL LEDGER INSERTION --------------------------------
                     
            # --------------- general ledger insertion --------------------------               
            for n in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
                _mb = db(db.Master_Account_Balance_Current_Year.account_code == n.account_code).select().first()
                _ma = dc(dc.Master_Account.account_code == n.account_code).select().first()
                if _mb: # existing entry
                    if n.credit == 0:            
                        _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) + float(n.debit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) + float(n.debit or 0))
                    else:
                        _mb.update_record(closing_balance_99 = float(_mb.closing_balance_99 or 0) - float(n.credit or 0), total_closing_balance = float(_mb.total_closing_balance or 0) - float(n.credit or 0))
                elif not _mb: # new entry
                    if n.credit == 0:
                        db.Master_Account_Balance_Current_Year.insert(
                            financial_year = request.now, 
                            account_code = n.account_code,
                            account_name = _ma.account_name,
                            closing_balance_99 = float(n.debit or 0),
                            total_closing_balance = float(n.debit or 0))                
                    else:
                        x = 0                
                        db.Master_Account_Balance_Current_Year.insert(
                            financial_year = request.now, 
                            account_code = n.account_code,
                            account_name = _ma.account_name,
                            closing_balance_99 = float(-n.credit or 0),
                            total_closing_balance = float(-n.credit or 0))                
            _ser.update_record()   
            response.js = "window.location.replace('%s')" % URL('workflow_rv_confirmation','get_rv_confirmation_grid')
    elif int(request.args(0)) == 4: # Exit button
        db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id).delete()                    
        response.js = "window.location.replace('%s')" % URL('workflow_rv_confirmation','get_rv_confirmation_grid')

def patch_rv_confirmation_session():
    session.receipt_voucher_confirmation_type_id = request.vars.receipt_voucher_confirmation_type_id
    session.bank_name_id = request.vars.bank_name_id
    # print('patch:'), session.receipt_voucher_confirmation_type_id, session.bank_name_id


# --------------------------------B E G I N ----------------------------------
# --------------------   RV  C O N F I R M A T I O N   -----------------------
# ----------------------------------------------------------------------------

def get_rv_confirmation_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('VOU.No.'),TD('Type'),TD('Code'),TD('Total Amount'),TD('Status'),TD('Required Action'),TD()),_class='bg-red')
    for n in db(db.Receipt_Voucher_Header.status_id != 11).select(): # check the status id after confirmation
        ctr += 1
        work_lnk = A(I(_class='fas fa-user-plus'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle' , _href=URL('account_transaction','post_receipt_voucher',args = n.id, extension = False))
        prin_lnk = A(I(_class='fas fa-print'), _title='View/Update/Cancel', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_id',args = n.id, extension = False))
        btn_lnk = DIV(prin_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(_vn.account_voucher_transaction_code,n.voucher_no),
            TD(_vn.account_voucher_transaction_type),
            TD(_vn.account_voucher_transaction_code),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(n.status_id.description),
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table')
    return dict(table = table)

def validate_post_receipt_voucher(form):        
    if request.vars.receipt_voucher_confirmation_type_id == 'A':
        _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC1').select().first()
        _voucher_type.voucher_serial_no += 1
        _voucher_type.update_record()
        # if cash a rv must 02
    elif request.vars.receipt_voucher_confirmation_type_id == 'B':
        _voucher_type = db(db.Account_Voucher_Type.transaction_prefix == 'RVC2').select().first()
        _voucher_type.voucher_serial_no += 1
        _voucher_type.update_record()
        # if pdc rv must 08 account code
    # no duplicate rv entry
    # total amount value
    _bank_name_id = db(db.Merch_Bank_Master.id == request.vars.bank_name_id).select().first()
    _bank_name_code = ""
    if _bank_name_id:
        _bank_name_code = _bank_name_id.account_code

    form.vars.voucher_no = _voucher_type.voucher_serial_no
    form.vars.status_id = 10
    form.vars.remarks = request.vars.remarks.upper()
    form.vars.account_code = _bank_name_code
    form.vars.account_voucher_transaction_code = _voucher_type.account_voucher_transaction_code
    form.vars.account_voucher_transaction_type = _voucher_type.account_voucher_transaction_type
    
    # , bank_name_id = _rcpt_hdr.bank_name_id, cheque_no = _rcpt_hdr.cheque_no, cheque_date = _rcpt_hdr.cheque_date

@auth.requires_login()
def post_receipt_voucher_confirmation():
    _total_amount = 0
    ticket_no_id = id_generator()
    session.ticket_no_id = ticket_no_id
    # db.Receipt_Voucher_Transaction_Confirmation_Request.voucher_no.default = 0
    # db.Receipt_Voucher_Transaction_Confirmation_Request.status_id.default = 9
    form = SQLFORM.factory(
        Field('voucher_no','string',length=20), 
        Field('transaction_reference_date','date',default=request.now), 
        Field('receipt_voucher_confirmation_type_id','string',length=10,requires = IS_EMPTY_OR(IS_IN_SET([('A','CASH/CASH CHEQUE'),('B','POST DATED CHEQUE')], zero = 'Choose Confirmation Type'))),
        Field('bank_name_id','reference Merch_Bank_Master',ondelete='NO ACTION',requires=IS_EMPTY_OR(IS_IN_DB(db,db.Merch_Bank_Master.id,'%(account_code)s : %(bank_name)s',zero='Choose Bank'))),    
        Field('remarks','text'))    
    if form.process(onvalidation = validate_post_receipt_voucher).accepted:
        response.flash = 'RECORD SAVE'                
        # insert to main table --------------------------------
        _total_amount = 0
        db.Receipt_Voucher_Confirmation.insert(
            voucher_no = form.vars.voucher_no,
            transaction_reference_date = form.vars.transaction_reference_date,
            account_voucher_transaction_type = form.vars.account_voucher_transaction_type,
            account_voucher_transaction_code = form.vars.account_voucher_transaction_code,
            receipt_voucher_confirmation_type_id = form.vars.receipt_voucher_confirmation_type_id,
            account_code = form.vars.account_code,            
            remarks = form.vars.remarks.upper(),
            account_reference = str(form.vars.account_voucher_transaction_code) + str(form.vars.voucher_no),
            status_id = 11)
        _head = db(db.Receipt_Voucher_Confirmation.voucher_no == form.vars.voucher_no).select().first()
        _total_amount = db.Receipt_Voucher_Transaction_Confirmation_Request.amount_paid.sum().coalesce_zero()
        _total_amount = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == request.vars.ticket_no_id).select(_total_amount).first()[_total_amount]            
        
        _account_ref = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == request.vars.ticket_no_id).select().first()
        
        for n in db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == request.vars.ticket_no_id).select():
            # if fully paid change status 
            # concatenate rv_confirmation_reference
            db(db.Receipt_Voucher_Request.account_reference == str(n.account_reference)).update(status_id = 11)            
            db(db.Receipt_Voucher_Header.account_reference == str(n.account_reference)).update(status_id = 11,rv_confirmation_reference = _head.account_reference)
            _rcpt_hdr = db(db.Receipt_Voucher_Header.account_reference == str(n.account_reference)).select().first()
            for x in db(db.Receipt_Voucher_Transaction.receipt_voucher_header_id == _rcpt_hdr.id).select():
                x.update_record(rv_confirmation_reference = _head.account_reference)
            
            db.Receipt_Voucher_Transaction_Confirmation.insert(
                receipt_voucher_confirmation_id = _head.id,
                account_voucher_transaction_type = _head.account_voucher_transaction_type,
                account_voucher_transaction_code = _head.account_voucher_transaction_code,
                account_code = n.account_code,
                account_reference = n.account_reference,
                account_credit_code = n.account_credit_code,
                account_debit_code = n.account_debit_code,
                dept_code_id = n.dept_code_id,
                department_code = n.department_code,
                location_cost_center_id = n.location_cost_center_id,
                location_code = n.location_code,
                transaction_payment_type_id = n.transaction_payment_type_id,
                amount_paid = n.amount_paid,
                description = n.description,
                voucher_no = _head.voucher_no,
                gl_entry_ref = n.gl_entry_ref,
                department = n.department, 
                invoice_no = n.invoice_no,
                bank_name_id = n.bank_name_id,
                cheque_no = n.cheque_no,
                cheque_date = n.cheque_dated,
                location = n.location)
        _head.update_record(total_amount = _total_amount, account_code2 = _account_ref.account_code)               
        _account_ref.delete_record()

        # insert to main table --------------------------------

        # GENERAL LEDGER INSERTION --------------------------------
        # HEADER DEBIT ENTRY/BANK ACCOUNT CODE
        _seq = put_batch_posting_sequence_id()    
        _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
        _row = db(db.GL_Transaction_Serial.id == 2).select().first() 
        _ga = db(db.General_Account.id == 1).select().first()
        _gl = db(db.GL_Description_Library.transaction_type == 21).select().first()
        _ser.serial_number += 1
        _row.serial_number += 1
        _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_head.account_code) + '/' + str(_row.serial_number)    
        _bank_name = 'None'
        if _head.bank_name_id:
            _bank_name = _head.bank_name_id.bank_name
        db.General_Ledger.insert(
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _head.transaction_reference_date,
            transaction_type = _head.account_voucher_transaction_type,
            location = 99, # general
            transaction_type_ref = _head.account_voucher_transaction_code,
            transaction_date_entered = request.now,
            department = 99, # general
            type = _head.account_voucher_transaction_type,
            reference_no = _head.account_reference,
            account_reference_no = _head.voucher_no,
            account_code = _head.account_code,
            description = str(_gl.common_text) + ' ' + str(_head.account_reference),
            entrydate = request.now,
            credit = 0,
            debit = _head.total_amount,
            amount_paid = 0,
            gl_entry_ref = _voucher_no_serial,
            batch_posting_seq = _seq,
            bank_code = _head.account_code,
            cheque_no = _head.cheque_no,
            cheque_bank_name = _bank_name
        )
        _row.update_record()
        # HEADER CREDIT ENTRY/ PDC/CASH + CASH CHEQUE (02-20 , 08-02)
        _ser.serial_number += 1
        _row.serial_number += 1
        _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_head.account_code) + '/' + str(_row.serial_number)    
        db.General_Ledger.insert(
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _head.transaction_reference_date,
            transaction_type = _head.account_voucher_transaction_type,
            location = 99, # general
            transaction_type_ref = _head.account_voucher_transaction_code,
            transaction_date_entered = request.now,
            department = 99, # general
            type = _head.account_voucher_transaction_type,
            reference_no = _head.account_reference,
            account_reference_no = _head.voucher_no,
            account_code = _head.account_code2,
            description = str(_gl.common_text) + ' ' + str(_head.account_reference),
            entrydate = request.now,
            credit = _head.total_amount,
            debit = 0,
            amount_paid = 0,
            gl_entry_ref = _voucher_no_serial,
            batch_posting_seq = _seq,
            bank_code = _head.account_code2,
            cheque_no = _head.cheque_no,
            cheque_bank_name = _bank_name
        )
        _row.update_record()
        # RV CONFIRMATION TRANSACTION - REFERENCE RV NUMBER ENTERED ON RVC TRANSACTION, AMOUNT PAID UPDATE OF 02 AND 08 ACCOUNT
        for n in db(db.Receipt_Voucher_Transaction_Confirmation.receipt_voucher_confirmation_id == _head.id).select():
            _gen_led = db((db.General_Ledger.account_code == n.account_code) & (db.General_Ledger.reference_no == n.account_reference)).select().first()
            _amount_paid = float(_gen_led.amount_paid or 0) + float(n.amount_paid or 0)
            _paid = False
            _cheque_no = _bank_name = 'None'
            if float(_gen_led.debit or 0) == float(_amount_paid or 0):
                _paid = True
            if _head.receipt_voucher_confirmation_type_id == 'B':
                if n.bank_name_id:
                    _bank_name = str(_gen_led.cheque_bank_name) + ' | ' + str(n.bank_name_id.bank_code.upper())
                    _cheque_no = str(_gen_led.cheque_no) + ' | ' + str(n.cheque_no)
            _gen_led.update_record(amount_paid = _amount_paid, paid = _paid, bank_code = _head.account_code, rv_payment_reference = _head.account_reference, cheque_no = n.cheque_no, cheque_bank_name = _bank_name)
        # GENERAL LEDGER INSERTION --------------------------------
        _ser.update_record()

        redirect(URL('workflow_rv_confirmation','get_rv_confirmation_grid'))
    elif form.errors:
        response.flash = 'FORM HAS ERROR'
    return dict(form = form, ticket_no_id = ticket_no_id)

# rv confirmation 
# if pdc date is greater than the current date
#  pdc check of this rv is not yet due for deposit

def validate_post_receipt_voucher_confirmation_transaction(form):
    _id = db(db.Receipt_Voucher_Header.account_reference == request.vars.account_reference).select().first()
    if not _id:
        form.errors.account_reference = 'Account reference not found.'
        response.js = "alertify.error('Account reference not found.');"
    elif request.vars.account_reference == '' or request.vars.account_reference == None:
        form.errors.account_reference = 'Account reference is empty.'
        response.js = "alertify.error('Account reference is empty.');"
    elif db((db.Receipt_Voucher_Transaction_Confirmation_Request.account_reference == request.vars.account_reference) & (db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id)).select().first():
        form.errors.account_reference = 'RV already added.'        
    elif _id: 
        _ga = db(db.General_Account.id == 1).select().first()
        if _id.status_id == 11:
            form.errors.account_reference = 'RV already confirmed.'
        elif _id.account_payment_mode_id != 1 and _id.cheque_dated >= request.now.date():
            form.errors.description = 'PDC Due date of this RV is not yet due.'
        elif str(_id.account_code) == str(_ga.pdc_receipt_voucher_account) and str(session.receipt_voucher_confirmation_type_id) != 'B':
            form.errors.account_reference = 'RV No. belongs to PDC (08-02).'
        elif str(_id.account_code) == str(_ga.receipt_voucher_account) and str(session.receipt_voucher_confirmation_type_id) != 'A':
            form.errors.account_reference = 'RV No. belongs to cash and cash cheque (02-20).'
        form.vars.account_voucher_transaction_type = 21
        form.vars.account_voucher_transaction_code = 'RV'
        form.vars.bank_name_id = _id.bank_name_id
        form.vars.cheque_no = _id.cheque_no
        form.vars.cheque_dated = _id.cheque_dated
        # print(':'), _id.account_code == '08-02' and request.vars.no_table_receipt_voucher_confirmation_type_id == 'B'        

@auth.requires_login()
def post_receipt_voucher_confirmation_transaction():
    db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id.default = session.ticket_no_id
    _ticket_no_ref = session.ticket_no_id
    form = SQLFORM(db.Receipt_Voucher_Transaction_Confirmation_Request)
    if form.process(onvalidation = validate_post_receipt_voucher_confirmation_transaction).accepted:
        # if request.args(0):
        #     _av = db(db.Account_Voucher_Request.id == int(request.args(0))).select().first()
        #     _total_amount = db.Receipt_Voucher_Transaction_Confirmation_Request.amount_paid.sum().coalesce_zero()
        #     _total_amount = db(db.Receipt_Voucher_Transaction_Confirmation_Request.receipt_voucher_confirmation_request_id == request.args(0)).select(_total_amount).first()[_total_amount]
        #     _av.update_record(total_amount = _total_amount)
        response.js = "$('#AVTtbl').get(0).reload();$('#btnadd').attr('disabled',false);$('#btnSubmit').prop('disabled',false)"
    elif form.errors:
        response.flash = None        
        response.js = "alertify.error('%s')" %(form.errors)        
    ctr = _total_amount = 0
    row = []    
    head = THEAD(TR(TD('#'),TD('RV No.'),TD('Account Code'),TD('Description'),TD('Amount'),TD('')),_class='bg-red')
    _query = db(db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == _ticket_no_ref).select()    
    for n in _query:
        ctr += 1
        dele_lnk = A(I(_class='fas fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle delete' , callback=URL('workflow_rv_confirmation','delete_account_transaction_id',args = n.id, extension = False))
        btn_lnk = DIV(dele_lnk)
        _total_amount += float(n.amount_paid or 0)
        row.append(TR(
            TD(ctr),            
            TD(n.account_reference),
            TD(n.account_code),
            TD(n.description),
            TD(locale.format('%.2F', n.amount_paid or 0, grouping = True), _align='right'),
            TD(btn_lnk)))
    body = TBODY(*row)
    foot = TFOOT(TR(
        TD(),TD(),TD(),TD('Total Amount: ',_align='right'),TD(locale.format('%.2F', _total_amount or 0, grouping = True), _align ='right'),TD()))
    table = TABLE([head, body, foot], _class='table',_id='AVTtbl')
    return dict(form = form, table = table)

def delete_account_transaction_id():
    response.js = "alertify.confirm('Receipt Voucher Confirmation', 'Are you sure you want to delete?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('workflow_rv_confirmation','delete_transaction_id',args = request.args(0))

def delete_transaction_id():
    _trnx = db(db.Receipt_Voucher_Transaction_Confirmation_Request.id == request.args(0)).select().first()
    _trnx.delete_record()
    response.js = "$('#AVTtbl').get(0).reload();alertify.error('Record Deleted.');"

def get_receipt_voucher_header_grid():
    ctr = _balanced = 0
    row = []
    _ga = db(db.General_Account.id == 1).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Account Code'),TD('Account Mode'),TD('Acct.Ref.'),TD('Total Amount'),TD('Amount Paid'),TD('Balanced'),TD()),_class='bg-red')
    _query = db((db.Receipt_Voucher_Header.account_code == _ga.receipt_voucher_account) & (db.Receipt_Voucher_Header.status_id == 10)).select()
    if session.receipt_voucher_confirmation_type_id == 'B':
        _query = db((db.Receipt_Voucher_Header.account_code == _ga.pdc_receipt_voucher_account) & (db.Receipt_Voucher_Header.status_id == 10)).select()
    for n in _query:
        ctr += 1        
        _balanced = float(n.total_amount or 0) - float(n.amount_paid or 0)
        _btnSelect = INPUT(_type='checkbox', _name='btnSelect',_onclick="ajax('%s',['btnSelect'])" % URL('workflow_rv_confirmation','patch_rv_confirmation_id', args = [n.id, _balanced])) 
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_code),
            TD(n.account_payment_mode_id.account_voucher_payment_code,' - ',n.account_payment_mode_id.account_voucher_payment_name ),
            TD(n.account_reference),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F', n.amount_paid or 0, grouping = True),_align='right'),
            TD(locale.format('%.2F', _balanced or 0, grouping = True),_align='right'),
            TD(_btnSelect)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table', _id='tblConf')
    response.js = "$('#btnSelect').prop('checked', false);alertify.alert().set({'startMaximized':true, 'title':'Receipt Voucher Request','message':'%s'}).show();alertify.alert().set('onok', function(closeEvent){  alertify.success('Success!')})" %(XML(table, sanitize = True))   #$('#AVTtbl').get(0).reload();

def patch_rv_confirmation_id():
    _id = db(db.Receipt_Voucher_Header.id == request.args(0)).select().first()
    _text_description = db(db.GL_Description_Library.id == 11).select().first()
    if request.vars.btnSelect: # selected        
        if db((db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id) & (db.Receipt_Voucher_Transaction_Confirmation_Request.account_reference == _id.account_reference)).select().first():
            response.js = "alertify.error('Account Reference already exist.')"
        elif _id.account_payment_mode_id != 1 and _id.cheque_dated >= request.now.date():
            response.js = "alertify.error('PDC Due date of this RV is not yet due.')"
        elif not db((db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id) & (db.Receipt_Voucher_Transaction_Confirmation_Request.account_reference == _id.account_reference)).select().first():
            _field_description = str(_text_description.common_text) + ' ' + str(_id.account_reference)
            if _id.account_payment_mode_id == 3:
                _field_description = str(_text_description.common_text2) + str(_id.bank_name_id.bank_name.upper()) + ' CHQ #' +str(_id.cheque_no)
            db.Receipt_Voucher_Transaction_Confirmation_Request.insert(
                account_voucher_transaction_type = _id.account_voucher_transaction_type,
                account_voucher_transaction_code = _id.account_voucher_transaction_code,
                account_code = _id.account_code,
                amount_paid = float(request.args(1) or 0),
                description = _field_description,
                account_reference = _id.account_reference,
                cheque_no = _id.cheque_no,
                cheque_dated = _id.cheque_dated,
                bank_name_id = _id.bank_name_id,
                ticket_no_id = session.ticket_no_id,
            )
            response.js = "$('#AVTtbl').get(0).reload();"
    elif not request.vars.btnSelect: # deleted
        _trnx = db((db.Receipt_Voucher_Transaction_Confirmation_Request.ticket_no_id == session.ticket_no_id) & (db.Receipt_Voucher_Transaction_Confirmation_Request.account_reference == _id.account_reference)).select().first()
        if _trnx:
            _trnx.delete_record()        
        response.js = "$('#AVTtbl').get(0).reload();"
 
# --------------------------------   E N D  ----------------------------------
# --------------------   RV  C O N F I R M A T I O N   -----------------------
# ----------------------------------------------------------------------------

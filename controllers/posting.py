def patch_obsolescence_id():    # audited 
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 9).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 9) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0                    

            _credit1 = n.average_cost_pcs * n.quantity
            _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 9) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no # by default

            if not _voucher_no_pur: # gl entry for obsolescne purhase account
                _row.serial_number += 1       
                _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                db.General_Ledger.insert(
                    voucher_no_id = _id.id, 
                    transaction_type_ref = str(_gl.order_no_text),
                    account_reference_no = _voucher_no_ref,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = n.transaction_date,
                    transaction_type = n.transaction_type,
                    location = n.location,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    type = n.transaction_type,
                    department = n.dept_code,
                    account_code = _sm.supplier_purchase_account, # purchase account
                    due_date = _id.transaction_date + datetime.timedelta(days=60),
                    credit = _credit1,
                    debit = 0,
                    description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                    batch_posting_seq = _seq,
                    gl_entry_ref = _voucher_no_pur_serial)                                
                _serial = str(_voucher_no_pur_serial)
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                _row.update_record()                
            elif _voucher_no_pur: # if exist
                _voucher_no_pur.credit += _credit1
                _voucher_no_pur.update_record()
                n.gl_entry_ref = str(_voucher_no_pur.gl_entry_ref)
                n.update_record()
        
                            
        # header obs account debit entry @ total adjustment amount
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.order_no_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit =  0,
            debit = float(_id.total_amount_after_discount or 0) - float(_id.total_selective_tax or 0),
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header obs account account debit entry total  amount @ tax rate
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _id.account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit =  0,
                debit = float(_id.total_selective_tax or 0), 
                description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry @ total selective tax amount
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = float(_id.total_selective_tax or 0), 
                debit = 0,
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()     
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
 
def patch_adjustment_plus_id():    # audited 
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 7).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 7) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0                    

            _credit1 = n.average_cost_pcs * n.quantity            
            _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 7) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no # by default

            if not _voucher_no_pur: # gl entry for purchase account
                _row.serial_number += 1       
                _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                db.General_Ledger.insert(
                    voucher_no_id = _id.id, 
                    transaction_type_ref = str(_gl.order_no_text),
                    account_reference_no = _voucher_no_ref,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = n.transaction_date,
                    transaction_type = n.transaction_type,
                    location = n.location,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    type = n.transaction_type,
                    department = n.dept_code,
                    account_code = _sm.supplier_purchase_account, # purchase account
                    due_date = _id.transaction_date + datetime.timedelta(days=60),
                    credit = 0,
                    debit = _credit1,
                    description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                    batch_posting_seq = _seq,
                    gl_entry_ref = _voucher_no_pur_serial)                                
                _serial = str(_voucher_no_pur_serial)
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                _row.update_record()                
            elif _voucher_no_pur: # if exist
                _voucher_no_pur.debit += _credit1
                _voucher_no_pur.update_record()
                n.gl_entry_ref = str(_voucher_no_pur.gl_entry_ref)
                n.update_record()
        
                            
        # header adjustment account/purchase return account debit entry @ total adjustment amount - selective tax
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.order_no_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit =  float(_id.total_amount_after_discount or 0) - float(_id.total_selective_tax or 0),
            debit = 0,
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header adjustment account credit entry  @ total selective tax
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _id.account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = float(_id.total_selective_tax or 0),
                debit = 0, 
                description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax debit entry @ selective tax account
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = 0, 
                debit = float(_id.total_selective_tax or 0),
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()     
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
 
def patch_adjustment_minus_id():    # audited 
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 6).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 6) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0                    

            _credit1 = n.average_cost_pcs * n.quantity            
            _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 6) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no # by default

            if not _voucher_no_pur: # gl entry for purchase account
                _row.serial_number += 1       
                _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                db.General_Ledger.insert(
                    voucher_no_id = _id.id, 
                    transaction_type_ref = str(_gl.order_no_text),
                    account_reference_no = _voucher_no_ref,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = n.transaction_date,
                    transaction_type = n.transaction_type,
                    location = n.location,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    type = n.transaction_type,
                    department = n.dept_code,
                    account_code = _sm.supplier_purchase_account, # purchase account
                    due_date = _id.transaction_date + datetime.timedelta(days=60),
                    credit = _credit1,
                    debit = 0,
                    description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                    batch_posting_seq = _seq,
                    gl_entry_ref = _voucher_no_pur_serial)                                
                _serial = str(_voucher_no_pur_serial)
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                _row.update_record()                
            elif _voucher_no_pur: # if exist
                _voucher_no_pur.credit += _credit1
                _voucher_no_pur.update_record()
                n.gl_entry_ref = str(_voucher_no_pur.gl_entry_ref)
                n.update_record()
        
                            
        # header adjustment account/purchase return account debit entry @ total adjustment amount - selective tax
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.order_no_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit =  0,
            debit = float(_id.total_amount_after_discount or 0) - float(_id.total_selective_tax or 0),
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header adjustment account/purchase return account debit entry @ total adjustment amount tax rate
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _id.account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit =  0,
                debit = float(_id.total_selective_tax or 0), 
                description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry @ selective tax account
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = float(_id.total_selective_tax or 0), 
                debit = 0,
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()     
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
 
def patch_sales_return_id():    # audited
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 4).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 4) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_sales_account, account_name = str('SALES ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_ib_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_ib_account, account_name = str('IB ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0
            if n.category_id == 'N':
                _credit = n.sale_cost_notax_pcs * n.quantity
                _debit = 0

            elif n.category_id == 'P':            
                _credit1 = n.average_cost_pcs * n.quantity
                _debit = 0
                _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
            _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no

            if int(n.location) != 1:
                _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
                _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 4) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_ref = n.voucher_no2                                

            if not _voucher_no: # not exist / gl entry for sales account with category n
                # transaction sales return account credit entry            
                if n.category_id == 'N':                                         
                    _row.serial_number += 1       
                    _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_sales_account,
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit,
                        description = str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref) + str(' CUSTOMER SRS REF. ') + str(_id.customer_return_reference),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_serial)                                
                    _row.update_record()
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_serial)
            elif _voucher_no: # if exist
                _voucher_no.debit += _credit
                _voucher_no.update_record()
                n.gl_entry_ref = _voucher_no.gl_entry_ref
                n.update_record()
                            
            if not _voucher_no_ib: # gl entry for ib account with category P for items with no selective tax
                if n.category_id == 'P' and (n.selective_tax_price == 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_zero_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit1,
                        debit = 0,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_zero_serial)                                
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_zero_serial)
                    _row.update_record()
                
            elif _voucher_no_ib: # if exist
                if (n.category_id == 'P') and (n.selective_tax_price == 0):                    
                    _voucher_no_ib.credit += _credit1
                    _voucher_no_ib.update_record()        
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()

            if not _voucher_no_ib: # gl entry for ib account with category P for items with selective tax

                if (n.category_id == 'P') and (n.selective_tax_price > 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_not_zero_serial_2 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)

                    db.General_Ledger.insert( # ib account entry at tax price
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit2,
                        debit = 0,
                        description = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    session.gl_entry_ref2 = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref)
                    # n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)

                    db.General_Ledger.insert(# ib account entry at average cost
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit1,
                        debit = 0,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)    
                    session.gl_entry_ref1 = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref)                    
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    _row.update_record()
            elif _voucher_no_ib: # if exist                
                if (n.category_id == 'P') and (n.selective_tax_price > 0):                    
                    _gl_entry_ref2 = db(db.General_Ledger.description == session.gl_entry_ref2).select().first() # chacnge to description 
                    _gl_entry_ref2.credit += _credit2                    
                    _gl_entry_ref2.update_record()                
                    # n.gl_entry_ref = str(session.gl_entry_ref2) + '/' + str(_row.serial_number)
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
                
                    _gl_entry_ref1 = db(db.General_Ledger.description == session.gl_entry_ref1).select().first()                    
                    _gl_entry_ref1.credit += _credit1
                    _gl_entry_ref1.update_record()  
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
            
            if not _voucher_no_pur: # gl entry for purchase account with category P
                if n.category_id == 'P':
                    # _row.serial_number += 1       
                    _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_purchase_account, # purchase account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit1,
                        description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_pur_serial)                                
                    _serial = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur_serial)
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                    # _row.update_record()                
            elif _voucher_no_pur: # if exist
                if n.category_id == 'P':
                    _voucher_no_pur.debit += _credit1
                    _voucher_no_pur.update_record()
                    n.gl_entry_ref = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur.gl_entry_ref)
                    n.update_record()
                            
        # header customer debit entry    
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.transaction_prefix_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit = float(_id.total_amount_after_discount or 0) + float(_id.delivery_charges or 0), 
            debit = 0,
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref) + str(' CUSTOMER SRS REF. ') + str(_id.customer_return_reference),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # debit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.provision_delivery_income,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = 0,
                debit = _id.delivery_charges or 0,
                description = str(_gl.common_text2) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = 0, 
                debit = _id.total_selective_tax,
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref) + str(' CUSTOMER SRS REF. ') + str(_id.customer_return_reference),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # if selective tax foc > 0:
        # insert 
        if _id.total_selective_tax_foc > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = 0, 
                debit = _id.total_selective_tax_foc or 0,
                description = 'FOC ' + str(_gl.excise_tax_text) + str(_gl.transaction_prefix_text) + str(_voucher_no_ref) + str(' CUSTOMER SRS REF. ') + str(_id.customer_return_reference),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()     
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
  
def patch_cash_sales_id():    # audited
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 3).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 3) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_sales_account, account_name = str('SALES ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_ib_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_ib_account, account_name = str('IB ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0
            if n.category_id == 'N':
                _credit = n.sale_cost_notax_pcs * n.quantity
                _debit = 0

            elif n.category_id == 'P':            
                _credit1 = n.average_cost_pcs * n.quantity
                _debit = 0
                _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
            _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no

            if int(n.location) != 1:
                _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
                _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 3) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_ref = n.voucher_no2

            if not _voucher_no: # not exist / gl entry for sales account with category n
                # transaction cash sales account credit entry               
                if n.category_id == 'N':                                         
                    _row.serial_number += 1       
                    _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_sales_account,
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit,
                        debit = 0,
                        description = str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_serial)                                
                    _row.update_record()
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_serial)
            elif _voucher_no: # if exist
                _voucher_no.credit += _credit
                _voucher_no.update_record()
                n.gl_entry_ref = _voucher_no.gl_entry_ref
                n.update_record()
                            
            if not _voucher_no_ib: # gl entry for ib account with category P for items with no selective tax
                if n.category_id == 'P' and (n.selective_tax_price == 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_zero_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit1,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_zero_serial)                                
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_zero_serial)
                    _row.update_record()
                
            elif _voucher_no_ib: # if exist
                if (n.category_id == 'P') and (n.selective_tax_price == 0):                    
                    _voucher_no_ib.debit += _credit1
                    _voucher_no_ib.update_record()        
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()

            if not _voucher_no_ib: # gl entry for ib account with category P for items with selective tax

                if (n.category_id == 'P') and (n.selective_tax_price > 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_not_zero_serial_2 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)

                    db.General_Ledger.insert( # ib account entry at tax price
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit2,
                        description = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    session.gl_entry_ref2 = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref)
                    # n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)

                    db.General_Ledger.insert(# ib account entry at average cost
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit1,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)    
                    session.gl_entry_ref1 = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref)                    
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    _row.update_record()
            elif _voucher_no_ib: # if exist                
                if (n.category_id == 'P') and (n.selective_tax_price > 0):                    
                    _gl_entry_ref2 = db(db.General_Ledger.description == session.gl_entry_ref2).select().first() # chacnge to description 
                    _gl_entry_ref2.debit += _credit2                    
                    _gl_entry_ref2.update_record()                
                    # n.gl_entry_ref = str(session.gl_entry_ref2) + '/' + str(_row.serial_number)
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
                
                    _gl_entry_ref1 = db(db.General_Ledger.description == session.gl_entry_ref1).select().first()                    
                    _gl_entry_ref1.debit += _credit1
                    _gl_entry_ref1.update_record()  
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
            
            if not _voucher_no_pur: # gl entry for purchase account with category P
                if n.category_id == 'P':
                    # _row.serial_number += 1       
                    _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_purchase_account, # purchase account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit1,
                        debit = 0,
                        description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_pur_serial)                                
                    _serial = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur_serial)
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                    # _row.update_record()                
            elif _voucher_no_pur: # if exist
                if n.category_id == 'P':
                    _voucher_no_pur.credit += _credit1
                    _voucher_no_pur.update_record()
                    n.gl_entry_ref = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur.gl_entry_ref)
                    n.update_record()
                            
        # header customer debit entry    
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.transaction_prefix_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit = 0, 
            debit = float(_id.total_amount_after_discount or 0) + float(_id.delivery_charges or 0),
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # credit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.provision_delivery_income,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.delivery_charges or 0,
                debit = 0,
                description = str(_gl.common_text2) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' +  str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.total_selective_tax, 
                debit = 0,
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' +  str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # if selective tax foc > 0:
        # insert 
        if _id.total_selective_tax_foc > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.total_selective_tax_foc, 
                debit = 0,
                description = 'FOC ' + str(_gl.excise_tax_text) + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' +  str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()     
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
 
def patch_sales_invoice_id(): # audited
    import datetime
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _ga = db(db.General_Account.id == 1).select().first()
    _ma = dc(dc.Master_Account.account_code == _id.account).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 2).select().first()
    if not _ma: # if account code not exist
        response.js = "alertify.alert('Account Code', 'Account code does not exist in master account file!');"
    elif _ma: # if account code exist
        _ser.serial_number += 1
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.transaction_type == 2) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()        
            _sma = dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_sales_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_sales_account, account_name = str('SALES ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_ib_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_ib_account, account_name = str('IB ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _id.account).select().first():
                dc.Master_Account.insert(account_code = _id.account, account_name = str('UPDATE ACCOUNT NAME'), master_account_type_id = 'G')

            _credit = _debit = _credit1 = _credit2 = 0
            if n.category_id == 'N':
                _credit = n.sale_cost_notax_pcs * n.quantity
                _debit = 0

            elif n.category_id == 'P':            
                _credit1 = n.average_cost_pcs * n.quantity
                _debit = 0
                _credit2 = (n.selective_tax_price / n.uom) * n.quantity            
            
            _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
            _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_ref = n.voucher_no

            if int(n.location) != 1:
                _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
                _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no2) & (db.General_Ledger.transaction_type == 2) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
                _voucher_no_ref = n.voucher_no2                                

            if not _voucher_no: # not exist / gl entry for sales account with category n
                # transaction invoice sales account credit entry            
                if n.category_id == 'N':                                         
                    _row.serial_number += 1       
                    _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_sales_account,
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit,
                        debit = 0,
                        description = str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_serial)                                
                    _row.update_record()
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_serial)
            elif _voucher_no: # if exist
                _voucher_no.credit += _credit
                _voucher_no.update_record()
                n.gl_entry_ref = _voucher_no.gl_entry_ref
                n.update_record()
                            
            if not _voucher_no_ib: # gl entry for ib account with category P for items with no selective tax
                if n.category_id == 'P' and (n.selective_tax_price == 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_zero_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit1,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_zero_serial)                                
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_zero_serial)
                    _row.update_record()
                
            elif _voucher_no_ib: # if exist
                if (n.category_id == 'P') and (n.selective_tax_price == 0):                    
                    _voucher_no_ib.debit += _credit1
                    _voucher_no_ib.update_record()        
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()

            if not _voucher_no_ib: # gl entry for ib account with category P for items with selective tax

                if (n.category_id == 'P') and (n.selective_tax_price > 0):
                    _row.serial_number += 1       
                    _voucher_no_ib_p_not_zero_serial_2 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)

                    db.General_Ledger.insert( # ib account entry at tax price
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit2,
                        description = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    session.gl_entry_ref2 = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) +  str(_voucher_no_ref)
                    # n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)

                    db.General_Ledger.insert(# ib account entry at average cost
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_ib_account, # ib account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = 0,
                        debit = _credit1,
                        description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)    
                    session.gl_entry_ref1 = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref)                    
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _voucher_no_ib_p_not_zero_serial_2)
                    _row.update_record()
            elif _voucher_no_ib: # if exist                
                if (n.category_id == 'P') and (n.selective_tax_price > 0):                    
                    _gl_entry_ref2 = db(db.General_Ledger.description == session.gl_entry_ref2).select().first() # chacnge to description 
                    _gl_entry_ref2.debit += _credit2                    
                    _gl_entry_ref2.update_record()                
                    # n.gl_entry_ref = str(session.gl_entry_ref2) + '/' + str(_row.serial_number)
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
                
                    _gl_entry_ref1 = db(db.General_Ledger.description == session.gl_entry_ref1).select().first()                    
                    _gl_entry_ref1.debit += _credit1
                    _gl_entry_ref1.update_record()  
                    n.gl_entry_ref = _voucher_no_ib.gl_entry_ref
                    n.update_record()
            
            if not _voucher_no_pur: # gl entry for purchase account with category P
                if n.category_id == 'P':
                    # _row.serial_number += 1       
                    _voucher_no_pur_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) 

                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _voucher_no_ref,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = n.transaction_date,
                        transaction_type = n.transaction_type,
                        location = n.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = n.transaction_type,
                        department = n.dept_code,
                        account_code = _sm.supplier_purchase_account, # purchase account
                        due_date = _id.transaction_date + datetime.timedelta(days=60),
                        credit = _credit1,
                        debit = 0,
                        description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                        batch_posting_seq = _seq,
                        gl_entry_ref = _voucher_no_pur_serial)                                
                    _serial = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur_serial)
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq,gl_entry_ref = _serial)
                    # _row.update_record()                
            elif _voucher_no_pur: # if exist
                if n.category_id == 'P':
                    _voucher_no_pur.credit += _credit1
                    _voucher_no_pur.update_record()
                    n.gl_entry_ref = str(n.gl_entry_ref) + '|' + str(_voucher_no_pur.gl_entry_ref)
                    n.update_record()
                            
        # header customer debit entry    
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id,
            transaction_type_ref = str(_gl.transaction_prefix_text),
            account_reference_no = _voucher_no_ref,
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            transaction_date_entered = request.now,
            entrydate = request.now,
            type = _id.transaction_type,
            department = _id.dept_code,
            account_code = _id.account,
            due_date = _id.transaction_date + datetime.timedelta(days=60),
            credit = 0, 
            debit = float(_id.total_amount_after_discount or 0) + float(_id.delivery_charges or 0),
            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
            batch_posting_seq = _seq,
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # credit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.provision_delivery_income,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.delivery_charges or 0,
                debit = 0,
                description = str(_gl.common_text2) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.total_selective_tax, 
                debit = 0,
                description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # if selective tax foc > 0:
        # insert 
        if _id.total_selective_tax_foc > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = _voucher_no_ref,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = _id.transaction_type,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                due_date = _id.transaction_date + datetime.timedelta(days=60),
                credit = _id.total_selective_tax_foc, 
                debit = 0,
                description = 'FOC ' + str(_gl.excise_tax_text) + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        # # all entries from transactions posted in gen ledger update on mas account        
        for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
            _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
            if _ma:   
                if int(x.department) == 1:
                    _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_1 or 0 
                elif int(x.department) == 2:
                    _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_2 or 0 
                elif int(x.department) == 3:                
                    _ma.credit_balance_3 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_3 or 0
                elif int(x.department) == 4:
                    _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_4 or 0 
                elif int(x.department) == 5:
                    _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_5 or 0 
                elif int(x.department) == 6:
                    _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_6 or 0 
                elif int(x.department) == 9:
                    _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
                    _ma.closing_balance += _ma.credit_balance_9 or 0 
                _ma.update_record()
 
        _ser.update_record()
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        

def patch_purchase_receipt_id(): # audited
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    _chk = db((db.General_Ledger.account_reference_no == _id.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.location == _id.location) & (db.General_Ledger.department == _id.dept_code)).select().first()              
    _ma = dc((dc.Master_Account.account_code == str(_id.account)) & (dc.Master_Account.status == False)).select().first()
    if _chk:
        response.js = "alertify.warning('Voucher already posted. Please contact the system administrator.');" 
        return True
    if str(_id.account[:2]) != '16' and str(_id.account[:2]) != '17' and str(_id.account[:2]) != '25' and str(_id.account[:2]) != '28':
        response.js = "alertify.warning('Please contact the system administrator.');" 
        return True
    if not _ma:
        response.js = "alertify.warning('Account code %s not found. Please contact the system administrator.');" %(_id.account)               
        return True 
    _seq = put_batch_posting_sequence_id()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first()
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    
    _ga = db(db.General_Account.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 1).select().first()        
    _supplier_invoice = ''
    if _id.supplier_invoice:
        _supplier_invoice = '-INV' + str(_id.supplier_invoice)
    _description = str(_gl.order_no_text) + str(_id.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(_id.voucher_no)
    _excise_tax_description = str(_gl.excise_tax_text) + str(_id.voucher_no)
    _account_ref = str(_gl.transaction_prefix_text) + str(_id.voucher_no)
    _TXN_ref = str(_gl.transaction_prefix_text)                 
    _purchase_description = str(_gl.order_no_text) + str(_id.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(_id.voucher_no)                
    _short_description = str(_gl.short_supply_text) + str(_supplier_invoice)
    _order_transaction_description = str(_gl.order_no_text) + str(_id.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(_id.voucher_no)
    _damaged_description = str(_gl.damaged_supply_text) + str(_id.order_account)
    if _ma:
        _ser.serial_number += 1
        _total_amount = (float(_id.total_amount_after_discount or 0) + float(_id.other_charges or 0)) * float(_id.exchange_rate or 0) 
        _trnx_amount = 0
        
        for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == int(_id.id)) & (dc.Merch_Stock_Transaction.delete == False)).select():            
            _im = dc(dc.Item_Master.item_code == n.item_code).select().first()
            _sm = dc(dc.Supplier_Master.id == _im.supplier_code_id).select().first()
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = str('PURCHASE ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')
            if not dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first():
                dc.Master_Account.insert(account_code = _ga.selective_tax_receivable_account, account_name = str('SELECTIVE TAX ACCOUNT - ') + str(_sm.supp_name), master_account_type_id = 'G')

            _voucher_no = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.account_code == _sm.supp_sub_code) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()              
            _voucher_no_ib = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _voucher_no_pur = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            _order_account = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.account_code == _id.order_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()            
            _claim_receivable_account = db((db.General_Ledger.account_reference_no == n.voucher_no) & (db.General_Ledger.transaction_type == 1) & (db.General_Ledger.account_code == _ga.claim_receivable_account) & (db.General_Ledger.location == n.location) & (db.General_Ledger.department == n.dept_code)).select().first()
            
            _voucher_no_ref = n.voucher_no                        

            _trnx_amount = (n.price_cost_after_discount * n.quantity) * _id.landed_cost
            if n.category_id == 'N': # normal
                # begin debit purchase account --------------------------------                    
                if not _voucher_no_pur: # 18 - purchase account              
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        account_reference_no = _id.voucher_no,
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,
                        transaction_date = _id.transaction_date,
                        transaction_type = _id.transaction_type,
                        location = _id.location,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        type = _id.transaction_type,
                        department = _id.dept_code,
                        account_code = _sm.supplier_purchase_account,
                        credit = 0,
                        debit = float(_trnx_amount or 0),
                        description = _purchase_description,
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq)                               
                    session.purchase_serial = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number)
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) )        
                    _row.update_record()                    
                elif _voucher_no_pur: # if exist
                    session.purchase_serial = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number)
                    _voucher_no_pur.debit += _trnx_amount                    
                    _voucher_no_pur.update_record()      
                    n.gl_entry_ref = _voucher_no_pur.gl_entry_ref
                    n.update_record()       
                    
                
                # end debit purchase account --------------------------------                            
            
            # begin credit order account ---------------------------              
            # print('-----------')         
            if not _order_account: # 10 - order account                     
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = _id.id, 
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,                
                    transaction_date = _id.transaction_date,
                    transaction_type = _id.transaction_type, 
                    location = _id.location,
                    type = _id.transaction_type,               
                    department = _id.dept_code,
                    account_code = _id.order_account, 
                    credit = float(_trnx_amount or 0), 
                    debit = 0,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    account_reference_no = _id.voucher_no, 
                    description = _order_transaction_description, 
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.order_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) 
                _serial = str(n.gl_entry_ref) + ' | ' + str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.order_account) + '/' + str(_row.serial_number)
                # print('order serial'), _serial
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = _serial)        
                _row.update_record()
            elif _order_account:
                _order_account.credit += _trnx_amount
                _order_account.update_record()
                if n.category_id == 'N': # normal
                    n.gl_entry_ref = str(session.purchase_serial) + ' | ' +  str(_order_account.gl_entry_ref)
                elif n.category_id == 'S': # short
                    n.gl_entry_ref = str(_order_account.gl_entry_ref)
                elif n.category_id == 'D': # damaged
                    # print('_order_account: D')
                    n.gl_entry_ref = str(_order_account.gl_entry_ref)

                n.update_record()
                # print('existing order serial'), n.gl_entry_ref

            # end credit order account ---------------------------                       

            # begin debit entry supplier account from transaction with short category  ---------------------------            
            if n.category_id == 'S': # 16 - supplier account short  
                if not _voucher_no:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = _id.transaction_date,
                        transaction_type = _id.transaction_type,
                        location = _id.location,
                        type = _id.transaction_type,
                        department = _id.dept_code,
                        account_code = _id.account, 
                        credit = 0,
                        debit = float(_trnx_amount or 0),
                        transaction_date_entered = request.now, 
                        entrydate = request.now,                    
                        account_reference_no = _id.voucher_no, 
                        description = _short_description, 
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 16 - supplier account short                                              
                    _row.update_record()                    
                    _serial = str(n.gl_entry_ref) + ' | ' +  str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number)
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = _serial)                            
                    
                elif _voucher_no: 
                    _voucher_no.debit += _trnx_amount
                    _voucher_no.update_record()
                    n.gl_entry_ref = str(n.gl_entry_ref) + ' | ' + str(_voucher_no.gl_entry_ref)
                    n.update_record()
            # end debit entry supplier account from transaction with short category  ---------------------------                       

            # begin debit entry damaged claim revs account rev from transaction with damaged category  ---------------------------                       
            if n.category_id == 'D': # damaged                
                if not _claim_receivable_account:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = _id.transaction_date,
                        transaction_type = _id.transaction_type,
                        location = _id.location,
                        type = _id.transaction_type,
                        department = _id.dept_code,
                        account_code = _ga.claim_receivable_account, 
                        credit = 0,
                        debit = float(_trnx_amount or 0),
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        account_reference_no = _id.voucher_no, 
                        description = _damaged_description, 
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.claim_receivable_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 08-04 - damaged claim account                
                    _row.update_record()
                    n.gl_entry_ref = str(n.gl_entry_ref) + ' | ' + str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.claim_receivable_account) + '/' + str(_row.serial_number)
                    n.update_record()                    
                    # print('not _claim_receivable_account: D')
                elif _claim_receivable_account: # if exist
                    _claim_receivable_account.debit += _trnx_amount
                    _claim_receivable_account.update_record()
                # end debit entry damaged claim revs account rev from transaction with damaged category  ---------------------------                       

            
        
        # update from header table
        if _id.total_selective_tax > 0.0:                 
            _row.serial_number += 1
            db.General_Ledger.insert( # credit selective tax
                voucher_no_id = _id.id, 
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,                    
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                department = _id.dept_code,
                account_code = _ga.selective_tax_payable_account,
                credit = _id.total_selective_tax, 
                debit = 0,
                transaction_date_entered = request.now, 
                entrydate = request.now , 
                account_reference_no = _id.voucher_no,  
                description = _excise_tax_description, 
                transaction_type_ref = str(_gl.transaction_prefix_text),
                gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number),
                batch_posting_seq = _seq)    
            _row.update_record()
            _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number) )        
            
            
            _row.serial_number += 1
            db.General_Ledger.insert( # debit selective tax
                voucher_no_id = _id.id, 
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,                    
                transaction_date = _id.transaction_date,
                transaction_type = _id.transaction_type,
                location = _id.location,
                department = _id.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                credit = 0, 
                debit = _id.total_selective_tax,
                transaction_date_entered = request.now, 
                entrydate = request.now, 
                account_reference_no = _id.voucher_no,  
                description = _excise_tax_description, 
                transaction_type_ref = str(_gl.transaction_prefix_text),
                gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number),
                batch_posting_seq = _seq)    
            _row.update_record()
            _serial_id = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number)
            _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = _serial_id )        
        
        # begin credit supplier account ------------------------
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id, 
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,                
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            department = _id.dept_code,
            account_code = _id.account,
            credit = _total_amount, # _total_amount + other charges
            debit = 0,
            transaction_date_entered = request.now, 
            entrydate = request.now, 
            description = _description,  
            account_reference_no = _id.voucher_no,  
            transaction_type_ref = str(_gl.transaction_prefix_text),
            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number),
            batch_posting_seq = _seq) # 16
        _row.update_record()
        _serial_id = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number)
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = _serial_id)        
        # end credit supplier account ------------------------
        
        # begin debit order account ------------------------
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = _id.id, 
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,                
            transaction_date = _id.transaction_date,
            transaction_type = _id.transaction_type,
            location = _id.location,
            department = _id.dept_code,
            account_code = _id.order_account,
            credit = 0,
            debit = _total_amount, # _total_amount + other charges
            transaction_date_entered = request.now,
            entrydate = request.now, 
            description = _description,  
            account_reference_no = _id.voucher_no,  
            transaction_type_ref = str(_gl.transaction_prefix_text),
            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.order_account) + '/' + str(_row.serial_number),
            batch_posting_seq = _seq ) # 10
        _row.update_record()
        _serial_id = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_id.order_account) + '/' + str(_row.serial_number)
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = _serial_id)        
        # end debit order account ------------------------
        _ser.update_record()
    # >> begin update master_account table ---------------------------
    for x in db(db.General_Ledger.transaction_no == _ser.serial_number).select():
        _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
        if _ma:
            if int(x.department) == 1:
                _ma.credit_balance_1 += x.debit or 0 - x.credit or 0
            elif int(x.department) == 2:
                _ma.credit_balance_2 += x.debit or 0 - x.credit or 0
            elif int(x.department) == 3:                
                _ma.credit_balance_3 += x.debit or 0 - x.credit or 0                        
            elif int(x.department) == 4:
                _ma.credit_balance_4 += x.debit or 0 - x.credit or 0
            elif int(x.department) == 5:
                _ma.credit_balance_5 += x.debit or 0 - x.credit or 0
            elif int(x.department) == 6:
                _ma.credit_balance_6 += x.debit or 0 - x.credit or 0
            elif int(x.department) == 9:
                _ma.credit_balance_9 += x.debit or 0 - x.credit or 0
            _ma.update_record()             
    # << end update master_account table ---------------------------
    # print(': {:15} {:15} {:15}'.format(x.account_code, x.debit, x.credit))

    response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!');"                

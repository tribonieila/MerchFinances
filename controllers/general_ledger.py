from datetime import datetime, date
import locale
import datetime
# import date
locale.setlocale(locale.LC_ALL, '')
_arr = []


@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_general_ledger_account_posting_grid():
    # session.active = 0
    _trnx_title = ''
    session.month = request.now.month
    if int(request.args(0)) == 1:
        title = 'Purchase Receipt Form'
        _trnx_title = 'Purchase Receipt Transaction Grid'
    elif int(request.args(0)) == 2:
        title = 'Sales Invoice Form'
        _trnx_title = 'Sales Invoice Transaction Grid'
    elif int(request.args(0)) == 3:
        title = 'Cash Sales Form'
        _trnx_title = 'Cash Sales Transaction Grid'
    elif int(request.args(0)) == 4:
        title = 'Sales Return Form'
        _trnx_title = 'Sales Return Transaction Grid'
    elif int(request.args(0)) == 5:
        title = 'Stock Transfer Form'
        _trnx_title = 'Stock Transfer Transaction Grid'
    elif int(request.args(0)) == 6:
        title = 'Stock Adjustment Form'
        _trnx_title = 'Purchase Return/Stock Adjustment Minus(-) Transaction Grid'
    elif int(request.args(0)) == 7:
        title = 'Stock Adjustment Form'
        _trnx_title = 'Stock Adjustment Plus(+) Transaction Grid'

    elif int(request.args(0)) == 9:
        title = 'Obsolescence Form'    
        _trnx_title = 'Obsolescence Transaction Grid'
    form = SQLFORM.factory(Field('month','string',length=25,requires = IS_IN_SET([('01', 'January'), ('02', 'February'), ('03', 'March'),('04','April'),('05','May'),('06','June'),('07', 'July'),('08', 'August'), ('09', 'September'),('10','October'),('11','November'),('12','December')],zero='Choose Month')))    
    return dict(form = form, title = title, _trnx_title = _trnx_title)

def month_session():
    # session.active = 0        
    if request.vars.month:    
        # session.active = 1        
        session.month = request.vars.month
        response.js = "$('#tblMSH').get(0).reload();$('#btnPost').removeAttr('disabled');" 

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def load_general_ledger_account_posting_grid():    
    
    if int(request.args(0)) == 1:
        
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('Voucher No'),TD('Account Code'),TD('Order Account'),TD('Amount After Discount'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & (dc.Merch_Stock_Header.cancelled == False) & (dc.Merch_Stock_Header.gl_batch_posting == False)).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),TD(n.transaction_date),TD(n.voucher_no),TD(n.account),TD(n.order_account),TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  
    elif int(request.args(0)) == 2:
        print('2')
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Dept.'),TD('Loc.'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  

    elif int(request.args(0)) == 3:
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Dept.'),TD('Loc.'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  
    elif int(request.args(0)) == 4:
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Department'),TD('Location'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  
    elif int(request.args(0)) == 5:
        table = DIV(H4('Stock Transfer Transaction Grid'),P('In progress...'),_class='callout callout-info')
    elif int(request.args(0)) == 6:
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Department'),TD('Location'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  
    elif int(request.args(0)) == 7:
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Department'),TD('Location'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  

    elif int(request.args(0)) == 9:
        ctr = 0
        row = []    
        head = THEAD(TR(TD('#'),TD('Date'),TD('VOU No.'),TD('POS/VOU No.'),TD('Department'),TD('Location'),TD('Account Code'),TD('Net Amount'),TD('Selective Tax'),TD('Selective Tax FOC'),TD()),_class='bg-red')    
        _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None)) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None))).select()                
        for n in _query:
            ctr += 1                
            post_lnk = A(I(_class='fas fa-edit'), _title='Post Row', _type='button ', _role='button', _class='btn btn-icon-toggle', callback=URL('general_ledger','get_ledger_account_id', args = [request.args(0),n.id], extension = False))
            trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
            btn_lnk = DIV(post_lnk, trax_lnk)
            row.append(TR(
                TD(ctr,INPUT(_type='integer',_value=n.id,_name='_id',_hidden=True)),
                TD(n.transaction_date),
                TD(n.voucher_no),
                TD(n.voucher_no2),
                TD(n.dept_code),
                TD(n.location),
                TD(n.account),                
                TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax or 0, grouping = True),_align='right'),
                TD(locale.format('%.3F',n.total_selective_tax_foc or 0, grouping = True),_align='right'),
            TD(btn_lnk)))        
        body = TBODY(*row)
        table = TABLE(*[head,body],_class='table', _id = 'tblMSH')  

    return dict(table = table) 

def get_ledger_account_grid():
    response.js = "alertify.confirm('Ledger', 'Are you sure you want to post?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('general_ledger','patch_ledger_account_grid',args = request.args(0))

def patch_ledger_account_grid():
    _id = dc(dc.Merch_Stock_Header.id == request.args(0)).select().first()
    if int(request.args(0)) == 1: # purchase receipt
        print('1:'), request.args(0)        
        patch_purchase_receipt_grid()
    elif int(request.args(0)) == 2: # sales invoice        
        patch_sales_invoice_grid()
    elif int(request.args(0)) == 3: # cash sales
        print('3:'), request.args(0)
        patch_cash_sales_grid()
    elif int(request.args(0)) == 4: # sales return
        print('4:'), request.args(0)
        patch_sales_return_grid()
    elif int(request.args(0)) == 5: # stock transfer
        print('5:'), request.args(0)
        patch_stock_transfer_grid()
    elif int(request.args(0)) == 6: # stock adjustment
        print('6:'), request.args(0)
        patch_stock_adjustment_grid()
    elif int(request.args(0)) == 9: # obsolescence
        print('9:'), request.args(0)
        patch_obsolescence_grid()
    response.js = "$('#tblMSH').get(0).reload()"

def xpatch_purchase_receipt_grid():
    print('------------')
    ctr = 0
    for m in dc(((dc.Merch_Stock_Header.account[:2] == '16') | (dc.Merch_Stock_Header.account[:2] == '17') | (dc.Merch_Stock_Header.account[:2] == '25') | (dc.Merch_Stock_Header.account[:2] == '28')) & (dc.Merch_Stock_Header.transaction_type == 1) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None)) & (dc.Merch_Stock_Header.cancelled == False)).select():        
        ctr += 1
        _account = m.account 
        if str(m.account[:2]) == '28':
            _trnx = dc((dc.Merch_Stock_Transaction.merch_stock_header_id == int(m.id)) & (dc.Merch_Stock_Transaction.delete == False)).select().first()
            _account = _trnx.aged_supplier_code
        print(':'), ctr,  m.account, ' > ', _account

def patch_purchase_receipt_grid():    
    _seq = put_batch_posting_sequence_id()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first() # TXN
    _row = db(db.GL_Transaction_Serial.id == 2).select().first()    # ROW
    _ga = db(db.General_Account.id == 1).select().first()
    _gl = db(db.GL_Description_Library.transaction_type == 1).select().first()    
    for m in dc(((dc.Merch_Stock_Header.account[:2] == '16') | (dc.Merch_Stock_Header.account[:2] == '17') | (dc.Merch_Stock_Header.account[:2] == '25') | (dc.Merch_Stock_Header.account[:2] == '28')) & (dc.Merch_Stock_Header.transaction_type == 1) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None)) & (dc.Merch_Stock_Header.cancelled == False)).select():        
        _ser.serial_number += 1
        _supplier_invoice = ''
        if m.supplier_invoice:
            _supplier_invoice = '-INV' + str(m.supplier_invoice)
        _description = str(_gl.order_no_text) + str(m.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(m.voucher_no)
        _ma = dc(dc.Master_Account.account_code == str(m.account)).select().first()     
        _account = m.account
        if str(m.account[:2]) == '25':
            _account = '16' + str(m.account[2:])      
        if str(m.account[:2]) == '28':
            _trnx = dc((dc.Merch_Stock_Transaction.merch_stock_header_id == int(m.id)) & (dc.Merch_Stock_Transaction.delete == False)).select().first()
            _account = _trnx.aged_supplier_code          
        _sm = dc(dc.Supplier_Master.supp_sub_code == str(_account)).select().first() # get purchase_code if account code ib account to check
        _purchase_description = str(_gl.order_no_text) + str(m.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(m.voucher_no)         
        _short_description = str(_gl.short_supply_text) + str(_supplier_invoice)    
        _order_transaction_description = str(_gl.order_no_text) + str(m.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(m.voucher_no)      
        _damaged_description = str(_gl.damaged_supply_text) + str(m.order_account)                
        _excise_tax_description = str(_gl.excise_tax_text) + str(m.voucher_no)
        if _ma: 
            _trnx_amount = _nrm_total_amount = _shr_total_amount = _dam_total_amount = _order_amount = 0           
            if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = _sm.supp_name, master_account_type_id = 'S')
            if not dc(dc.Master_Account.account_code == _sm.supplier_ib_account).select().first():
                dc.Master_Account.insert(account_code = _sm.supplier_ib_account, account_name = _sm.supp_name, master_account_type_id = 'S')
            if not dc(dc.Master_Account.account_code == m.order_account).select().first():                        
                dc.Master_Account.insert(account_code = m.order_account, account_name = _sm.supp_name, master_account_type_id = 'S')
                _total_amount = float(m.total_amount_after_discount or 0)  * float(m.exchange_rate or 0)            
                for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == m.id) & ((dc.Merch_Stock_Transaction.delete == False) | (dc.Merch_Stock_Transaction.cancelled == False))).select():
                    _trnx_amount = float(n.price_cost_after_discount or 0) * n.quantity
                    if n.category_id == 'N': # normal
                        _nrm_total_amount += round(_trnx_amount, 3)
                    elif n.category_id == 'S': # short
                        _shr_total_amount += round(_trnx_amount, 3)
                    elif n.category_id == 'D': # damaged
                        _dam_total_amount += round(_trnx_amount, 3)
                _nrm_total_amount = float(_nrm_total_amount or 0) * float(m.landed_cost or 0)
                _shr_total_amount = float(_shr_total_amount or 0) * float(m.landed_cost or 0)
                _dam_total_amount = float(_dam_total_amount or 0) * float(m.landed_cost or 0)
                _purchase_amount  = float(_nrm_total_amount or 0)
                _order_amount = float(_nrm_total_amount or 0) + float(_shr_total_amount or 0) + float(_dam_total_amount or 0) 
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    account_reference_no = m.voucher_no,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type,
                    location = m.location,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    type = m.transaction_type,
                    department = m.dept_code,
                    account_code = _sm.supplier_purchase_account,
                    credit = 0,
                    debit = _purchase_amount,
                    description = _purchase_description,
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) # 18 - purchase account    
                _row.update_record()
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number) )

                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,                
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type, 
                    location = m.location,
                    type = m.transaction_type,               
                    department = m.dept_code,
                    account_code = m.order_account, 
                    credit = _order_amount, 
                    debit = 0,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    account_reference_no = m.voucher_no, 
                    description = _order_transaction_description, 
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.order_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) # 10 - order account   
                _row.update_record()       
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.order_account) + '/' + str(_row.serial_number))
                # debit supp account short receipt  
                if _shr_total_amount > 0:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        type = m.transaction_type,
                        department = m.dept_code,
                        account_code = m.account, 
                        credit = 0,
                        debit = _shr_total_amount,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,                    
                        account_reference_no = m.voucher_no, 
                        description = _short_description, 
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 16 - supplier account short
                    _row.update_record()      
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.account) + '/' + str(_row.serial_number))          


                    # print(': {:5} {:10} {:10}'.format(n.id, n.voucher_no, n.account))
                if _dam_total_amount > 0:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        type = m.transaction_type,
                        department = m.dept_code,
                        account_code = _ga.claim_receivable_account, 
                        credit = 0,
                        debit = _dam_total_amount,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        account_reference_no = m.voucher_no, 
                        description = _damaged_description, 
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.claim_receivable_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 0804 - damaged claim account
                    _row.update_record()    
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.claim_receivable_account) + '/' + str(_row.serial_number))            

                if m.total_selective_tax > 0.0:
                    # credit selective tax
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        department = m.dept_code,
                        account_code = _ga.selective_tax_payable_account,
                        credit = m.total_selective_tax, 
                        debit = 0,
                        transaction_date_entered = request.now, 
                        entrydate = request.now , 
                        account_reference_no = m.voucher_no,  
                        description = _excise_tax_description, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq)    
                    _row.update_record()  
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number))
                    # debit selective tax
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        department = m.dept_code,
                        account_code = _ga.selective_tax_receivable_account,
                        credit = 0, 
                        debit = m.total_selective_tax,
                        transaction_date_entered = request.now, 
                        entrydate = request.now, 
                        account_reference_no = m.voucher_no,  
                        description = _excise_tax_description, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq)    
                    _row.update_record()
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))
                # credit supplier account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,                
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type,
                    location = m.location,
                    department = m.dept_code,
                    account_code = m.account,
                    credit = _total_amount,
                    debit = 0,
                    transaction_date_entered = request.now, 
                    entrydate = request.now, 
                    description = _description,  
                    account_reference_no = m.voucher_no,  
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) # 16
                _row.update_record()
                
                # debit order account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,                
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type,
                    location = m.location,
                    department = m.dept_code,
                    account_code = m.order_account,
                    credit = 0,
                    debit = _total_amount,
                    transaction_date_entered = request.now,
                    entrydate = request.now, 
                    description = _description,  
                    account_reference_no = m.voucher_no,  
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.order_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq ) # 10
                _row.update_record()
            else:
                _total_amount = _nrm_total_amount = _shr_total_amount = _dam_total_amount = _purchase_amount = _trnx_amount = _order_amount = 0
                _total_amount = (float(m.total_amount_after_discount or 0) + float(m.other_charges or 0)) * float(m.exchange_rate or 0)
                for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == m.id) & ((dc.Merch_Stock_Transaction.delete == False) | (dc.Merch_Stock_Transaction.cancelled == False))).select():
                    _trnx_amount = float(n.price_cost_after_discount or 0) * int(n.quantity or 0)
                    if n.category_id == 'N': # normal
                        _nrm_total_amount += round(_trnx_amount, 3)
                    elif n.category_id == 'S': # short
                        _shr_total_amount += round(_trnx_amount, 3)
                    elif n.category_id == 'D': # damaged
                        _dam_total_amount += round(_trnx_amount, 3)   
                _nrm_total_amount = float(_nrm_total_amount or 0) * float(m.landed_cost or 0)
                _shr_total_amount = float(_shr_total_amount or 0) * float(m.landed_cost or 0)
                _dam_total_amount = float(_dam_total_amount or 0) * float(m.landed_cost or 0)
                _purchase_amount = float(_nrm_total_amount or 0) #+ float(_dam_total_amount or 0) 
                _order_amount = float(_nrm_total_amount or 0) + float(_shr_total_amount or 0) + float(_dam_total_amount or 0)             
                # transaction
                # debit purchase account                  
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type,
                    location = m.location,
                    department = m.dept_code,
                    account_code = _sm.supplier_purchase_account,
                    credit = 0,
                    debit = _purchase_amount,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,                
                    description = _purchase_description, 
                    account_reference_no = m.voucher_no,  
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) # 18 - purchase account                        
                _row.update_record()
                # credit order account                                         
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = m.id, 
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,                
                    transaction_date = m.transaction_date,
                    transaction_type = m.transaction_type,
                    location = m.location,
                    department = m.dept_code,
                    account_code =  m.order_account, 
                    credit = _order_amount, 
                    debit = 0,
                    transaction_date_entered = request.now, 
                    entrydate = request.now,
                    account_reference_no =  m.voucher_no, 
                    description = _order_transaction_description, 
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.order_account) + '/' + str(_row.serial_number),
                    batch_posting_seq = _seq) # 10 - order account
                _row.update_record()      
                # debit supp account short receipt
                if _shr_total_amount > 0:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        department = m.dept_code,
                        account_code = m.account, 
                        credit = 0,
                        debit = _shr_total_amount,
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        account_reference_no = m.voucher_no, 
                        description = _short_description, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 16 - supplier account short
                    _row.update_record()
                if _dam_total_amount > 0:
                    _row.serial_number += 1
                    db.General_Ledger.insert(
                        voucher_no_id = m.id, 
                        transaction_prefix_id = _ser.id,
                        transaction_no = _ser.serial_number,                    
                        transaction_date = m.transaction_date,
                        transaction_type = m.transaction_type,
                        location = m.location,
                        department = m.dept_code,
                        account_code = _ga.claim_receivable_account, 
                        credit = 0,
                        debit = _dam_total_amount, 
                        transaction_date_entered = request.now, 
                        entrydate = request.now,
                        account_reference_no = m.voucher_no, 
                        description = _damaged_description, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.claim_receivable_account) + '/' + str(_row.serial_number),
                        batch_posting_seq = _seq) # 0804 - damaged claim account
                    _row.update_record() 
        # header 
        if m.total_selective_tax > 0.0:                                            
            # credit selective tax
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = m.id, 
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,                    
                transaction_date = m.transaction_date,
                transaction_type = m.transaction_type,
                location = m.location,
                department = m.dept_code,
                account_code = _ga.selective_tax_payable_account,
                credit = m.total_selective_tax, 
                debit = 0,
                transaction_date_entered = request.now, 
                entrydate = request.now, 
                account_reference_no = m.voucher_no, 
                description = _excise_tax_description, 
                transaction_type_ref = str(_gl.transaction_prefix_text),
                gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number),
                batch_posting_seq = _seq)    
            _row.update_record()
            # debit selective tax
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = m.id, 
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,                    
                transaction_date = m.transaction_date,
                transaction_type = m.transaction_type,
                location = m.location,
                department = m.dept_code,
                account_code = _ga.selective_tax_receivable_account,
                credit = 0, 
                debit = m.total_selective_tax,
                transaction_date_entered = request.now, 
                entrydate = request.now, 
                account_reference_no = m.voucher_no, 
                description = _excise_tax_description, 
                transaction_type_ref = str(_gl.transaction_prefix_text),
                gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number),
                batch_posting_seq = _seq)    
            _row.update_record()
        # credit supplier account
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = m.id, 
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,                
            transaction_date = m.transaction_date,
            transaction_type = m.transaction_type,
            location = m.location,
            department = m.dept_code,
            account_code = m.account,
            credit = _total_amount,
            debit = 0,
            transaction_date_entered = request.now, 
            entrydate = request.now, 
            description = _description,  
            account_reference_no = m.voucher_no, 
            transaction_type_ref = str(_gl.transaction_prefix_text), 
            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.account) + '/' + str(_row.serial_number),
            batch_posting_seq = _seq) # 16
        _row.update_record()
        # debit order account
        _row.serial_number += 1
        db.General_Ledger.insert(
            voucher_no_id = m.id, 
            transaction_prefix_id = _ser.id,
            transaction_no = _ser.serial_number,                
            transaction_date = m.transaction_date,
            transaction_type = m.transaction_type,
            location = m.location,
            department = m.dept_code,
            account_code = m.order_account,
            credit = 0,
            debit = _total_amount,
            transaction_date_entered = request.now, 
            entrydate = request.now, 
            description = _description,  
            account_reference_no = m.voucher_no, 
            transaction_type_ref = str(_gl.transaction_prefix_text),
            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(m.order_account) + '/' + str(_row.serial_number),
            batch_posting_seq = _seq) # 10                                        
        _row.update_record()
        m.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq)
        _ser.update_record()
    for n in db(db.General_Ledger.batch_posting_seq == _seq).select():            
        _ma = dc(dc.Master_Account.account_code == n.account_code).select().first()
        if _ma:
            if int(n.department) == 1:
                _ma.credit_balance_1 += n.debit or 0 - n.credit or 0
            elif int(n.department) == 2:
                _ma.credit_balance_2 += n.debit or 0 - n.credit or 0
            elif int(n.department) == 3:                
                _ma.credit_balance_3 += n.debit or 0 - n.credit or 0                        
            elif int(n.department) == 4:
                _ma.credit_balance_4 += n.debit or 0 - n.credit or 0
            elif int(n.department) == 5:
                _ma.credit_balance_5 += n.debit or 0 - n.credit or 0
            elif int(n.department) == 6:
                _ma.credit_balance_6 += n.debit or 0 - n.credit or 0
            elif int(n.department) == 9:
                _ma.credit_balance_9 += n.debit or 0 - n.credit or 0
        _ma.update_record()             

def patch_sales_invoice_grid():    
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first() # TXN
    _row = db(db.GL_Transaction_Serial.id == 2).select().first() # ROW
    _gl = db(db.GL_Description_Library.transaction_type == 2).select().first()    
    for n in dc((dc.Merch_Stock_Header.transaction_type == 2) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None)) & (dc.Merch_Stock_Header.cancelled == False)).select(limitby=(0,10)):        
        _ma = dc((dc.Master_Account.account_code == n.account) & (dc.Master_Account.status == 0)).select().first()
        if _ma:
            _ga = db(db.General_Account.id == 1).select().first()
            _ser.serial_number += 1
            # _ma = dc(dc.Master_Account.account_code == n.account).select().first()
            for x in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == n.id) & (dc.Merch_Stock_Transaction.transaction_type == 2) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():        
                _im = dc(dc.Item_Master.item_code == x.item_code).select().first()
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
                if not dc(dc.Master_Account.account_code == n.account).select().first():
                    dc.Master_Account.insert(account_code = n.account, account_name = str('UPDATE ACCOUNT NAME - '), master_account_type_id = 'G')

                _credit = _debit = _credit1 = _credit2 = 0 
                if x.category_id == 'N':
                    _credit = x.sale_cost_notax_pcs * x.quantity
                    _debit = 0
                elif x.category_id == 'P':
                    _credit1 = x.average_cost_pcs * x.quantity
                    _credit2 = x.selective_tax_price / x.uom * x.quantity
                    _debit = 0
                
                # _voucher_no = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_sales_account)).select().first() 
                # _voucher_no_ib = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_ib_account)).select().first()                
                # _voucher_no_pur = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_purchase_account)).select().first()
            
                _voucher_no = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                _voucher_no_ib = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                _voucher_no_pur = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                _voucher_no_ref = n.voucher_no
                if int(x.location) != 1:
                    _voucher_no = db((db.General_Ledger.account_reference_no == x.voucher_no2) & (db.General_Ledger.account_code == _sm.supplier_sales_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                    _voucher_no_ib = db((db.General_Ledger.account_reference_no == x.voucher_no2) & (db.General_Ledger.account_code == _sm.supplier_ib_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                    _voucher_no_pur = db((db.General_Ledger.account_reference_no == x.voucher_no2) & (db.General_Ledger.account_code == _sm.supplier_purchase_account) & (db.General_Ledger.location == x.location) & (db.General_Ledger.department == x.dept_code)).select().first()
                    _voucher_no_ref = n.voucher_no2


                if not _voucher_no: # not exist / gl entry for sales account with category n
                    # transaction invoice sales account credit entry
                    if x.category_id == 'N':
                        _row.serial_number += 1       
                        db.General_Ledger.insert(
                            voucher_no_id = n.id,
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = _voucher_no_ref,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now,
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_sales_account,
                            credit = _credit, 
                            debit = 0,
                            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number))
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number))
                elif _voucher_no: # if exist
                    _voucher_no.credit += _credit
                    _voucher_no.update_record()     
                    x.gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number)
                    x.update_record()
                
                if not _voucher_no_ib: # gl entry for ib account with category P for items with no selective tax
                    if x.category_id == 'P' and (x.selective_tax_price == 0):
                        _row.serial_number += 1 
                        db.General_Ledger.insert(
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = _voucher_no_ref,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_ib_account, # ib account
                            due_date = n.transaction_date + datetime.timedelta(days=60),
                            credit = 0,
                            debit = _credit1,
                            description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))   
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))
                elif _voucher_no_ib: # if exist
                    if (x.category_id == 'P') and (x.selective_tax_price == 0):
                        _voucher_no_ib.debit += _credit1
                        _voucher_no_ib.update_record()
                        x.gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)
                        x.update_record()                    
                
                if not _voucher_no_ib: # gl entry for ib account with category P for items with selective tax
                    if (x.category_id == 'P') and (x.selective_tax_price >= 0):
                        _row.serial_number += 1       
                        db.General_Ledger.insert( # ib account entry at tax price
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = _voucher_no_ref,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = n.dept_code,
                            account_code = _sm.supplier_ib_account, # ib account
                            due_date = n.transaction_date + datetime.timedelta(days=60),
                            credit = 0,
                            debit = _credit2,
                            description = 'PROMO ' + str(_gl.ib_text) + ' AT TAX RATE ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))        
                        session.gl_entry_ref2 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)    
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))

                        _row.serial_number += 1       
                        db.General_Ledger.insert( # ib account entry at tax price
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = _voucher_no_ref,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = n.dept_code,
                            account_code = _sm.supplier_ib_account, # ib account
                            due_date = n.transaction_date + datetime.timedelta(days=60),
                            credit = 0,
                            debit = _credit1,
                            description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))    
                        session.gl_entry_ref1 = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number)        
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))

                elif _voucher_no_ib: # if exist
                    if (x.category_id == 'P') and (x.selective_tax_price >= 0):
                        _gl_entry_ref2 = db(db.General_Ledger.gl_entry_ref == session.gl_entry_ref2).select().first()
                        _gl_entry_ref2.debit += _credit2
                        _gl_entry_ref2.update_record()
                        x.gl_entry_ref = str(session.gl_entry_ref2)
                        x.update_record()

                        _gl_entry_ref1 = db(db.General_Ledger.gl_entry_ref == session.gl_entry_ref1).select().first()
                        _gl_entry_ref1.debit += _credit2
                        _gl_entry_ref1.update_record()
                        x.gl_entry_ref = str(session.gl_entry_ref1)
                        x.update_record()
                                        
                if not _voucher_no_pur: # gl entry for purchase account with category P
                    if x.category_id == 'P':
                        _row.serial_number += 1       
                        db.General_Ledger.insert(
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = _voucher_no_ref,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_purchase_account, # purchase account
                            due_date = x.transaction_date + datetime.timedelta(days=60),
                            credit = _credit1,
                            debit = 0,
                            description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number))
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number))
                elif _voucher_no_pur: # if exist
                    _voucher_no_pur.credit += _credit1
                    _voucher_no_pur.update_record()
                    x.gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number)
                    x.update_record()
            
            # header customer debit entry        
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = n.id,
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
                account_code = n.account,
                due_date = n.transaction_date + datetime.timedelta(days=60),
                credit = 0, 
                debit = n.total_amount_after_discount or 0,
                description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))            

            # header selective tax credit entry
            if n.total_selective_tax > 0:         # if selective tax > 0: insert selective tax in credit entry and selective tax payable account -> general account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = n.id,
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
                    account_code = _ga.selective_tax_payable_account,
                    credit = n.total_selective_tax, 
                    debit = 0,
                    description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                    gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
                _row.update_record()
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))

            if n.total_selective_tax_foc > 0:         # if selective tax > 0: insert selective tax in credit entry and selective tax payable account -> general account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = n.id,
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
                    account_code = _ga.selective_tax_payable_account,
                    due_date = _id.transaction_date + datetime.timedelta(days=60),
                    credit = n.total_selective_tax_foc, 
                    debit = 0,
                    description = 'FOC ' +  str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
                    gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ser.serial_number))
                _row.update_record()
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))                              

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

def patch_cash_sales_grid():    
    _seq = put_batch_posting_sequence_id()
    _ctr = db(db.General_Ledger.id).count()
    _ser = db(db.GL_Transaction_Serial.id == 1).select().first() # TXN
    _row = db(db.GL_Transaction_Serial.id == 2).select().first() # ROW
    _gl = db(db.GL_Description_Library.transaction_type == 3).select().first()    
    for n in dc((dc.Merch_Stock_Header.transaction_type == 3) & (dc.Merch_Stock_Header.transaction_date.month() == session.month) & ((dc.Merch_Stock_Header.gl_batch_posting == False) | (dc.Merch_Stock_Header.gl_batch_posting == None)) & (dc.Merch_Stock_Header.cancelled == False)).select(limitby=(0,10)):        
        _ma = dc((dc.Master_Account.account_code == n.account) & (dc.Master_Account.status == 0)).select().first()
        if _ma:
            _ga = db(db.General_Account.id == 1).select().first()
            _ser.serial_number += 1
            # _ma = dc(dc.Master_Account.account_code == n.account).select().first()
            for x in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == n.id) & (dc.Merch_Stock_Transaction.transaction_type == 3) & (dc.Merch_Stock_Transaction.transaction_date.month() == session.month) & ((dc.Merch_Stock_Transaction.gl_batch_posting == False) | (dc.Merch_Stock_Transaction.gl_batch_posting == None)) & (dc.Merch_Stock_Transaction.delete == False)).select():        
                _im = dc(dc.Item_Master.item_code == x.item_code).select().first()
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
                if not dc(dc.Master_Account.account_code == n.account).select().first():
                    dc.Master_Account.insert(account_code = n.account, account_name = str('UPDATE ACCOUNT NAME - '), master_account_type_id = 'G')

                _credit = _debit = _credit1 = _credit2 = 0 
                if x.category_id == 'N':
                    _credit = x.sale_cost_notax_pcs * x.quantity
                    _debit = 0
                elif x.category_id == 'P':
                    _credit1 = x.average_cost_pcs * x.quantity
                    _credit2 = x.selective_tax_price / x.uom * x.quantity
                    _debit = 0
                
                _voucher_no = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_sales_account)).select().first() 

                _voucher_no_ib = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_ib_account)).select().first()
                
                _voucher_no_pur = db((db.General_Ledger.account_reference_no == x.voucher_no) & (db.General_Ledger.account_code == _sm.supplier_purchase_account)).select().first()

                if not _voucher_no: # not exist / gl entry for sales account with category n
                    # transaction invoice sales account credit entry
                    if x.category_id == 'N':
                        _row.serial_number += 1       
                        db.General_Ledger.insert(
                            voucher_no_id = n.id,
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = x.voucher_no,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now,
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_sales_account,
                            credit = _credit, 
                            debit = 0,
                            description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(n.voucher_no),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number))
                        _row.update_record()
                        x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number))
                elif _voucher_no: # if exist
                    _voucher_no.credit += _credit
                    _voucher_no.update_record()     
                
                if not _voucher_no_ib: # gl entry for ib account with category P for items with no selective tax
                    if x.category_id == 'P':
                        _row.serial_number += 1 
                        db.General_Ledger.insert(
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = x.voucher_no,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_ib_account, # ib account
                            due_date = n.transaction_date + datetime.timedelta(days=60),
                            credit = 0,
                            debit = _credit1,
                            description = 'CGS ' + str(_gl.ib_text) + ' ' + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(n.voucher_no),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))   
                        _row.update_record()
                    x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))
                elif _voucher_no_ib: # if exist
                    _voucher_no_ib.debit += _credit1
                    _voucher_no_ib.update_record()
                
                if not _voucher_no_ib: # gl entry for ib account with category P for items with selective tax
                    if (x.category_id == 'P') and (x.selective_tax_price >= 0):
                        _row.serial_number += 1       
                        db.General_Ledger.insert(
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = x.voucher_no,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = n.dept_code,
                            account_code = _sm.supplier_ib_account, # ib account
                            due_date = n.transaction_date + datetime.timedelta(days=60),
                            credit = 0,
                            debit = _credit2,
                            description = 'PROMO ' + str(_gl.ib_text) + str(_gl.common_text) + ' ' + str(_gl.transaction_prefix_text) + str(n.voucher_no),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))            
                        _row.update_record()
                    x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_ib_account) + '/' + str(_row.serial_number))
                elif _voucher_no_ib: # if exist
                    _voucher_no_ib.debit += _credit2
                    _voucher_no_ib.update_record()
                
                if not _voucher_no_pur: # gl entry for purchase account with category P
                    if x.category_id == 'P':
                        _row.serial_number += 1       
                        db.General_Ledger.insert(
                            voucher_no_id = n.id, 
                            transaction_type_ref = str(_gl.transaction_prefix_text),
                            account_reference_no = x.voucher_no,
                            transaction_prefix_id = _ser.id,
                            transaction_no = _ser.serial_number,
                            transaction_date = x.transaction_date,
                            transaction_type = x.transaction_type,
                            location = x.location,
                            transaction_date_entered = request.now, 
                            entrydate = request.now,
                            type = x.transaction_type,
                            department = x.dept_code,
                            account_code = _sm.supplier_purchase_account, # purchase account
                            due_date = x.transaction_date + datetime.timedelta(days=60),
                            credit = _credit1,
                            debit = 0,
                            description = str(_gl.purchase_receipt_no_text) + ' ' + str(_gl.transaction_prefix_text) + str(x.voucher_no),
                            batch_posting_seq = _seq,
                            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number))
                        _row.update_record()
                    x.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_purchase_account) + '/' + str(_row.serial_number))
                elif _voucher_no_pur: # if exist
                    _voucher_no_pur.credit += _credit1
                    _voucher_no_pur.update_record()
            
            # header customer debit entry        
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = n.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                account_reference_no = n.voucher_no,
                transaction_prefix_id = _ser.id,
                transaction_no = _ser.serial_number,
                transaction_date = n.transaction_date,
                transaction_type = n.transaction_type,
                location = n.location,
                transaction_date_entered = request.now,
                entrydate = request.now,
                type = n.transaction_type,
                department = n.dept_code,
                account_code = n.account,
                due_date = n.transaction_date + datetime.timedelta(days=60),
                credit = 0, 
                debit = n.total_amount_after_discount or 0,
                description = str(_gl.common_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(n.voucher_no),
                batch_posting_seq = _seq,
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
            _row.update_record()
            n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))
            
            #update master account by account code and dept
            if int(request.args(0)) == 1:
                _ma.credit_balance_1 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_1 or 0
                _ma.update_record()
            elif int(request.args(0)) == 2:
                _ma.credit_balance_2 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_2 or 0
                _ma.update_record()
            elif int(request.args(0)) == 3:
                _ma.credit_balance_3 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_3 or 0
                _ma.update_record()
            elif int(request.args(0)) == 4:
                _ma.credit_balance_4 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_4 or 0
                _ma.update_record()
            elif int(request.args(0)) == 5:
                _ma.credit_balance_5 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_5 or 0
                _ma.update_record()
            elif int(request.args(0)) == 6:
                _ma.credit_balance_6 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_6 or 0
                _ma.update_record()
            elif int(request.args(0)) == 9:
                _ma.credit_balance_9 += n.total_amount_after_discount or 0
                _ma.closing_balance += _ma.credit_balance_9 or 0
                _ma.update_record()

            # header selective tax credit entry
            if n.total_selective_tax > 0:         # if selective tax > 0: insert selective tax in credit entry and selective tax payable account -> general account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = n.id,
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    account_reference_no = n.voucher_no,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = n.transaction_date,
                    transaction_type = n.transaction_type,
                    location = n.location,
                    transaction_date_entered = request.now,
                    entrydate = request.now,
                    type = n.transaction_type,
                    department = n.dept_code,
                    account_code = _ga.selective_tax_payable_account,
                    credit = n.total_selective_tax, 
                    debit = 0,
                    description = str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(n.voucher_no),
                    gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number))
                _row.update_record()
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))

                _sel = dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first()     
                if int(request.args(0)) == 1:
                    _sel.credit_balance_1 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 2:
                    _sel.credit_balance_2 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 3:
                    _sel.credit_balance_3 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 4:
                    _sel.credit_balance_4 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 5:
                    _sel.credit_balance_5 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 6:
                    _sel.credit_balance_6 += n.total_amount_after_discount or 0
                    _sel.update_record()
                elif int(request.args(0)) == 9:
                    _sel.credit_balance_9 += n.total_amount_after_discount or 0
                    _sel.update_record()


            if n.total_selective_tax_foc > 0:         # if selective tax > 0: insert selective tax in credit entry and selective tax payable account -> general account
                _row.serial_number += 1
                db.General_Ledger.insert(
                    voucher_no_id = n.id,
                    transaction_type_ref = str(_gl.transaction_prefix_text),
                    account_reference_no = n.voucher_no,
                    transaction_prefix_id = _ser.id,
                    transaction_no = _ser.serial_number,
                    transaction_date = n.transaction_date,
                    transaction_type = n.transaction_type,
                    location = n.location,
                    transaction_date_entered = request.now,
                    entrydate = request.now,
                    type = n.transaction_type,
                    department = n.dept_code,
                    account_code = _ga.selective_tax_payable_account,
                    due_date = _id.transaction_date + datetime.timedelta(days=60),
                    credit = n.total_selective_tax_foc, 
                    debit = 0,
                    description = 'FOC ' +  str(_gl.excise_tax_text) +  ' ' +  str(_gl.transaction_prefix_text) + str(n.voucher_no),
                    gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ser.serial_number))
                _row.update_record()
                n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number))
                
                _foc = dc(dc.Master_Account.account_code == _ga.selective_tax_receivable_account).select().first()        
                if int(request.args(0)) == 1:
                    _foc.credit_balance_1 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 2:
                    _foc.credit_balance_2 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 3:
                    _foc.credit_balance_3 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 4:
                    _foc.credit_balance_4 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 5:
                    _foc.credit_balance_5 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 6:
                    _foc.credit_balance_6 += n.total_selective_tax_foc or 0
                    _foc.update_record()
                elif int(request.args(0)) == 9:
                    _foc.credit_balance_9 += n.total_selective_tax_foc or 0
                    _foc.update_record()                

            _ser.update_record()    
            response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"

def patch_sales_return_grid():
    print('sales return')

def patch_stock_transfer_grid():
    print('stock transfer')

def patch_stock_adjustment_grid():
    print('stock adjustment')

def patch_obsolescence_grid():
    print('obsolescence')


def get_ledger_account_id():    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    response.js = "alertify.confirm('Ledger', 'Are you sure you want to post?', function(){ ajax('%s') }, function(){ alertify.error('Cancel')});" % URL('general_ledger','patch_ledger_account_id',args = [request.args(0),request.args(1)])
    if _id.gl_batch_posting:
        response.js = "$('#tblMSH').get(0).reload();alertify.notify('Already posted.','warning')"                   

def patch_ledger_account_id():    
    if int(request.args(0)) == 1: # purchase receipt
        patch_purchase_receipt_id()
    elif int(request.args(0)) == 2: # sales invoice
        patch_sales_invoice_id()
    elif int(request.args(0)) == 3: # cash sales
        patch_cash_sales_id()
    elif int(request.args(0)) == 4: # sales return
        patch_sales_return_id()
    elif int(request.args(0)) == 6: # stock adjustment minus
        patch_adjustment_minus_id()
    elif int(request.args(0)) == 7: # stock adjustment plus
        patch_adjustment_plus_id()
    elif int(request.args(0)) == 9: # obsolescence
        patch_obsolescence_id()

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
                    reference_no = str(_gl.transaction_prefix_text)+str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header obs account account debit entry total  amount @ tax rate
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/'+  str(_id.account)  + '/'+ str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry @ total selective tax amount
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record()             
            
        _ser.update_record()     
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))             
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
                    reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header adjustment account credit entry  @ total selective tax
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax debit entry @ selective tax account
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
                    
        _ser.update_record()    
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))              
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
                    reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 

        # header adjustment account/purchase return account debit entry @ total adjustment amount tax rate
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry @ selective tax account
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.order_no_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record()             
 
        _ser.update_record()     
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))             
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
            if n.category_id == 'N' or n.category_id == 'D':
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

            if not _voucher_no: # not exist / gl entry for supplier sales account with category n
                # transaction sales return account credit entry for supplier sales account           
                if n.category_id == 'N' or n.category_id == 'D':                                         
                    _row.serial_number += 1       
                    _voucher_no_serial = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_sm.supplier_sales_account) + '/' + str(_row.serial_number)
                    db.General_Ledger.insert(
                        voucher_no_id = _id.id, 
                        transaction_type_ref = str(_gl.transaction_prefix_text),
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        account_code = _sm.supplier_sales_account, # for supplier sales account
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # debit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.provision_delivery_income) + '/' + str(_row.serial_number))
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 

        # header selective tax credit entry
        if _id.total_selective_tax > 0:
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))                                                          
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
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            _id.gl_entry_ref = str(_id.gl_entry_ref)+ ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        _ser.update_record()     
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))               
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' + str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # credit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.provision_delivery_income) + '/' + str(_row.serial_number))
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
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))
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
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)  + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))                                                          
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' +  str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
            
        _ser.update_record()     
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))            
        response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!')"        
 
def patch_sales_invoice_id(): # audited
    import datetime
    _voucher_no_ref = 'None'
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
            gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_id.account) + '/' +str(_row.serial_number))
        _row.update_record()
        _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number)+ '/' +str(_row.serial_number)) 
        
        if float(_id.delivery_charges or 0) > 0: # credit entries for delivery charges
            _row.serial_number += 1
            db.General_Ledger.insert(
                voucher_no_id = _id.id,
                transaction_type_ref = str(_gl.transaction_prefix_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.provision_delivery_income) +'/' + str(_row.serial_number))
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
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account)+ '/' + str(_row.serial_number))
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
                reference_no = str(_gl.transaction_prefix_text) + str(_voucher_no_ref),
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
                gl_entry_ref = str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_ga.selective_tax_receivable_account) + '/' + str(_row.serial_number))
            _row.update_record()
            # _id.gl_entry_ref = str(_id.gl_entry_ref)+ '/' + str(_row.serial_number)
            _id.gl_entry_ref = str(_id.gl_entry_ref) + ' | ' + str(_ser.prefix)+str(_ser.serial_number) + '/' + str(_row.serial_number)
            _id.update_record() 
             
        _ser.update_record()
        # >>------------ Master_Account_Balance_Current_Year <<---------------------
        calculate_master_account(int(_ser.serial_number))       

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
    if _id.order_account != _ma.account_code:
        dc.Master_Account.insert(
            account_code = _id.order_account,
            account_name = 'ORDER ACCOUNT - ' + str(_id.account),
            account_sub_group_id = 15,
            chart_of_account_group_code = '10',
            master_account_type_id = 'S'            
        )
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
                    reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
                        reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
                transaction_type_ref = str(_gl.transaction_prefix_text),
                reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
                gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number),
                batch_posting_seq = _seq)    
            _row.update_record()
            _id.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now, gl_batch_posting_seq = _seq, gl_entry_ref = str(_ser.prefix) + str(_ser.serial_number) + '/' + str(_ga.selective_tax_payable_account) + '/' + str(_row.serial_number) )        
            
            
            _row.serial_number += 1
            db.General_Ledger.insert( # debit selective tax
                voucher_no_id = _id.id, 
                transaction_prefix_id = _ser.id,
                reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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
            reference_no = str(_gl.transaction_prefix_text) + str(_id.voucher_no),
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

    # >>------------ Master_Account_Balance_Current_Year <<---------------------
    calculate_master_account(int(_ser.serial_number))       

    response.js = "$('#tblMSH').get(0).reload();alertify.success('Success!');"                
    # print(': {:15} {:15} {:15}'.format(x.account_code, x.debit, x.credit))

def get_general_ledger_account_table():    
    ctr = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Date'),TD('Voucher No'),TD('Account Code'),TD('Order Account'),TD('Amount After Discount')),_class='bg-red')
    _query = dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.gl_batch_posting == False) & (dc.Merch_Stock_Header.cancelled == False) & (dc.Merch_Stock_Header.transaction_date.month() == int(request.vars.month))).select()
    for n in _query:
        ctr += 1                
        row.append(TR(TD(ctr),TD(n.transaction_date),TD(n.voucher_no),TD(n.account),TD(n.order_account),TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right')))        
    body = TBODY(*row)
    table = TABLE(*[head,body],_class='table', _id = 'tblMSH')   
    return table

def put_batch_posting_sequence_id():
    # _id = db(db.Batch_Posting_Sequence.prefix_seq == request.args(0)).select().first()
    _id = db(db.Batch_Posting_Sequence.prefix_seq == 1).select().first()
    _seq = int(_id.sequence_no) + 1
    _id.update_record(sequence_no = _seq)
    return _seq
    
@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def post_in_general_ledger():   # validate cancelled False
    _seq = put_batch_posting_sequence_id()
    if request.vars.month == "":                
        response.js = "alertify.warning('Selected month not found or empty.');"
    else:        
        if int(request.args(0)) == 1:                       
            _ga = db(db.General_Account.id == 1).select().first()
            _gl = db(db.GL_Description_Library.transaction_type == 1).select().first()
            _query = dc((dc.Merch_Stock_Header.transaction_type == int(request.args(0))) & (dc.Merch_Stock_Header.gl_batch_posting == False) & (dc.Merch_Stock_Header.cancelled == False) & (dc.Merch_Stock_Header.transaction_date.month() == int(request.vars.month))).select(orderby = dc.Merch_Stock_Header.id)
            for n in _query:                                                
                _id = dc(dc.Master_Account.account_code == str(n.account)).select().first()
                if n.supplier_invoice ==  None:
                    _empty = '-PRNT' + str(n.voucher_no)
                else:
                    _empty = '-INV' + str(n.supplier_invoice)                                
                _description = str(_gl.order_no_text)+ str(n.order_account) + ' '  + str(_gl.purchase_receipt_no_text) + str(n.voucher_no)
                _excise_tax_description = str(_gl.excise_tax_text) + str(n.voucher_no)
                _account_ref = str(_gl.transaction_prefix_text) + str(n.voucher_no)
                _trnx_ref = str(_gl.transaction_prefix_text)                 
                _purchase_description = str(_gl.order_no_text) + str(n.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(n.voucher_no)                
                _short_description = str(_gl.short_supply_text) + str(_empty)
                _order_transaction_description = str(_gl.order_no_text) + str(n.order_account) + ' ' + str(_gl.purchase_receipt_no_text) + str(n.voucher_no)
                _damaged_description = str(_gl.damaged_supply_text) + str(n.order_account)                
                if _id:
                    _sm = dc(dc.Supplier_Master.supp_sub_code == str(n.account)).select().first() # get purchase_code
                    if not dc(dc.Master_Account.account_code == _sm.supplier_purchase_account).select().first():
                        dc.Master_Account.insert(account_code = _sm.supplier_purchase_account, account_name = _sm.supp_name, master_account_type_id = 'S')
                    if not dc(dc.Master_Account.account_code == _sm.supplier_ib_account).select().first():
                        dc.Master_Account.insert(account_code = _sm.supplier_ib_account, account_name = _sm.supp_name, master_account_type_id = 'S')
                    if not dc(dc.Master_Account.account_code == n.order_account).select().first():                        
                        dc.Master_Account.insert(account_code = n.order_account, account_name = _sm.supp_name, master_account_type_id = 'S')
                        _total_amount = (float(n.total_amount_after_discount or 0) + float(_id.other_charges or 0)) * float(n.exchange_rate or 0)                        
                        _nrm_total_amount = _shr_total_amount = _dam_total_amount = _purchase_amount = _trnx_amount = _order_amount = 0
                        for x in dc(dc.Merch_Stock_Transaction.merch_stock_header_id == int(_id.id)).select():
                            _trnx_amount = float(x.price_cost_after_discount or 0) * int(x.quantity or 0)# * float(n.landed_cost or 0)                                                        
                            if x.category_id == 'N': # normal
                                _nrm_total_amount += _trnx_amount
                            elif x.category_id == 'S': # short
                                _shr_total_amount += _trnx_amount
                            elif x.category_id == 'D': # damaged
                                _dam_total_amount += _trnx_amount
                        _nrm_total_amount = float(_nrm_total_amount or 0) * float(n.landed_cost or 0)
                        _shr_total_amount = float(_shr_total_amount or 0) * float(n.landed_cost or 0)
                        _dam_total_amount = float(_dam_total_amount or 0) * float(n.landed_cost or 0)
                        _purchase_amount = float(_nrm_total_amount or 0) #+ float(_dam_total_amount or 0) 
                        _order_amount = float(_nrm_total_amount or 0) + float(_shr_total_amount or 0) + float(_dam_total_amount or 0) 
                        # debit                        
                        db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _sm.supplier_purchase_account,credit = 0,debit = _purchase_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _purchase_description,batch_posting_seq = _seq) # 18 - purchase account                        
                        # credit                                                        
                        db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code =  n.order_account, credit = _order_amount, debit = 0,entrydate = request.now,account_reference_no =  n.voucher_no, description = _order_transaction_description, batch_posting_seq = _seq) # 10 - order account
                        # debit supp account
                        if _shr_total_amount > 0:
                            db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.account, credit = 0,debit = _shr_total_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _short_description, batch_posting_seq = _seq) # 16 - supplier account short
                        if _dam_total_amount > 0:
                            db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.claim_receivable_account, credit = 0,debit = _dam_total_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _damaged_description, batch_posting_seq = _seq) # 0804 - damaged claim account
                        # header                                             
                        if n.total_selective_tax > 0.0:
                            # print 'insert'
                            # credit
                            db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.selective_tax_payable_account,credit = n.total_selective_tax, debit = 0,entrydate = request.now , account_reference_no = _account_ref, description = _excise_tax_description, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq)    
                            # debit
                            db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.selective_tax_receivable_account,credit = 0, debit = n.total_selective_tax,entrydate = request.now, account_reference_no = _account_ref, description = _excise_tax_description, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq)    
                        # credit
                        db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.account,credit = _total_amount,debit = 0,entrydate = request.now, description = _description,  account_reference_no = _account_ref, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq) # 16
                        # debit
                        db.General_Ledger.insert(voucher_no_id = _id.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.order_account,credit = 0,debit = _total_amount,entrydate = request.now, description = _description,  account_reference_no = _account_ref, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq ) # 10
                    else:                        
                        _sm = dc(dc.Supplier_Master.supp_sub_code == str(n.account)).select().first()
                        _total_amount = float(n.total_amount_after_discount or 0) * float(n.exchange_rate or 0)
                        # transaction                        
                        _nrm_total_amount = _shr_total_amount = _dam_total_amount = _purchase_amount = _trnx_amount = _order_amount = 0
                        
                        for x in dc(dc.Merch_Stock_Transaction.merch_stock_header_id == int(n.id)).select():                            
                            _trnx_amount = float(x.price_cost_after_discount or 0) * int(x.quantity or 0)# * float(n.landed_cost or 0)                                                        
                            if x.category_id == 'N': # normal
                                _nrm_total_amount += _trnx_amount
                            elif x.category_id == 'S': # short
                                _shr_total_amount += _trnx_amount
                            elif x.category_id == 'D': # damaged
                                _dam_total_amount += _trnx_amount                            
                        _nrm_total_amount = float(_nrm_total_amount or 0) * float(n.landed_cost or 0)
                        _shr_total_amount = float(_shr_total_amount or 0) * float(n.landed_cost or 0)
                        _dam_total_amount = float(_dam_total_amount or 0) * float(n.landed_cost or 0)
                        _purchase_amount = float(_nrm_total_amount or 0) #+ float(_dam_total_amount or 0) 
                        _order_amount = float(_nrm_total_amount or 0) + float(_shr_total_amount or 0) + float(_dam_total_amount or 0) 
                        
                        # debit                        
                        db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _sm.supplier_purchase_account,credit = 0,debit = _purchase_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _purchase_description, batch_posting_seq = _seq) # 18 - purchase account                        
                        # credit                                                        
                        db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code =  n.order_account, credit = _order_amount, debit = 0,entrydate = request.now,account_reference_no =  n.voucher_no, description = _order_transaction_description, batch_posting_seq = _seq) # 10 - order account
                        # debit supp account
                        if _shr_total_amount > 0:
                            db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.account, credit = 0,debit = _shr_total_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _short_description, batch_posting_seq = _seq) # 16 - supplier account short
                        if _dam_total_amount > 0:
                            db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.claim_receivable_account, credit = 0,debit = _dam_total_amount,entrydate = request.now,account_reference_no = n.voucher_no, description = _damaged_description, batch_posting_seq = _seq) # 0804 - damaged claim account
                        # header 
                        if n.total_selective_tax > 0.0:                            
                            # print 'update'
                            # credit
                            db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.selective_tax_payable_account,credit = n.total_selective_tax, debit = 0,entrydate = request.now, account_reference_no = _account_ref, description = _excise_tax_description, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq)    
                            # debit
                            db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = _ga.selective_tax_receivable_account,credit = 0, debit = n.total_selective_tax,entrydate = request.now, account_reference_no = _account_ref, description = _excise_tax_description, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq)    
                        # credit
                        db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.account,credit = _total_amount,debit = 0,entrydate = request.now, description = _description,  account_reference_no = _account_ref, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq) # 16
                        # debit
                        db.General_Ledger.insert(voucher_no_id = n.id, transaction_date = n.transaction_date,transaction_type = n.transaction_type,department = n.dept_code,account_code = n.order_account,credit = 0,debit = _total_amount,entrydate = request.now, description = _description,  account_reference_no = _account_ref, transaction_type_ref = _trnx_ref, batch_posting_seq = _seq) # 10                                        
                    n.update_record(gl_batch_posting = True, gl_batch_posting_date = request.now,gl_batch_posting_seq = _seq)
                    response.js = "Pace.restart(); alertify.success('Account code validated.');"                
                else:                                    
                    response.js = "Pace.restart(); alertify.warning('Account code %s not found.');" %(n.account)            
        elif int(request.args(0)) == 2:
            _bs = db(db.Batch_Posting_Sequence.prefix_seq == 2).select().first()
            _query = dc((dc.Merch_Stock_Header.transaction_type == int(request.args(0))) & (dc.Merch_Stock_Header.gl_batch_posting == False) & (dc.Merch_Stock_Header.cancelled == False) & (dc.Merch_Stock_Header.transaction_date.month() == int(request.vars.month))).select(orderby = dc.Merch_Stock_Header.id)
            for n in _query:
                _id = dc(dc.Master_Account.account_code == str(n.account)).select().first()
                if _id:                
                    response.js = "alertify.success('Account code validated.');"
                else:                
                    response.js = "alertify.warning('Account code %s not found.');" %(n.account)                
        elif int(request.args(0)) == 3:
            _bs = db(db.Batch_Posting_Sequence.prefix_seq == 3).select().first()
            response.js = "alertify.success('Cash Sales posted.');"
        elif int(request.args(0)) == 4:
            _bs = db(db.Batch_Posting_Sequence.prefix_seq == 4).select().first()
            response.js = "alertify.success('Sales Return posted.');"
        elif int(request.args(0)) == 5:
            _bs = db(db.Batch_Posting_Sequence == 5).select().first()
            response.js = "alertify.success('Stock Transfer posted.');"
        elif int(request.args(0)) == 6:
            _bs = db(db.Batch_Posting_Sequence == 6).select().first()
            response.js = "alertify.success('Stock Adjustment posted.');"
        elif int(request.args(0)) == 9:
            _bs = db(db.Batch_Posting_Sequence == 9).select().first()
            response.js = "alertify.success('Obsolescences posted.');"
        put_master_account_list(_seq)

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_general_ledger_grid():
    form = SQLFORM.factory(
        Field('start_date','date', default = request.now),
        Field('end_date','date', default = request.now),
        Field('transaction_group_type','integer', requires = IS_IN_SET([('1', '1 - Account Transaction'), ('2', '2 - Inventory Transaction')],zero='Choose Group Type')))    
    return dict(form = form)

def post_general_ledger_session(): 
    print(':'), request.vars.start_date, request.vars.end_date, request.vars.transaction_group_type

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def load_general_ledger_grid():
    row = []
    ctr = _total_debit_amount = _total_credit_amount = 0
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction No.'),TD('Trnx Type'),TD('Loc.'),TD('Dept.'),TD('Ref.No'),TD('Voucher No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Amount Paid'),TD('A/C Paymnt Ref.'),TD('Description'),TD('GL Entry Ref.')),_class='bg-red')
    for n in db().select(orderby = db.General_Ledger.id):
        ctr += 1
        _total_debit_amount += n.debit
        _total_credit_amount += n.credit        
        _trnx = A(n.transaction_prefix_id.prefix,n.transaction_no, _title='Entry Date', _type='button', _role='button', callback=URL('general_ledger','get_posted_by', args = n.id, extension = False))        
        _trnx_type = A(n.account_reference_no, _title='Details', _type='button', _role='button', callback=URL('consolidated','get_consolidated_transactions_id', args = [n.transaction_type, n.voucher_no_id], extension = False))
        if n.type == 21 or n.type == 22:
            _trnx = A(n.transaction_prefix_id.prefix,n.transaction_no, _title='Entry Date', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [1, n.transaction_type, n.id], extension = False))        
            _trnx_type = A(n.account_reference_no, _title='Details', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [2, n.transaction_type, n.id], extension = False))
        elif n.type == 23:
            _trnx = A(n.transaction_prefix_id.prefix,n.transaction_no, _title='Entry Date', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [1, n.transaction_type, n.id], extension = False))        
            _trnx_type = A(n.account_reference_no, _title='Details', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [2, n.transaction_type, n.id], extension = False))
        elif n.type == 24:
            _trnx = A(n.transaction_prefix_id.prefix,n.transaction_no, _title='Entry Date', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [1, n.transaction_type, n.id], extension = False))        
            _trnx_type = A(n.account_reference_no, _title='Details', _type='button', _role='button', callback=URL('account_transaction_general_ledger','get_account_transaction_general_ledger_id', args = [2, n.transaction_type, n.id], extension = False))

        row.append(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD(_trnx),
            TD(n.transaction_type_ref),
            TD(n.location),
            TD(n.department),
            TD(n.reference_no),
            TD(_trnx_type),
            TD(n.account_code),
            TD(locale.format('%.2F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.amount_paid or 0, grouping = True), _align='right'),
            TD(n.rv_payment_reference),
            TD(n.description),
            TD(n.gl_entry_ref)))
    _bg_class = 'bg-green color-palette'
    if _total_debit_amount != _total_credit_amount:
        _bg_class = 'bg-red color-palette'
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD(),TD(),TD('Total Amount:',_colspan='2',_align='right'),TD(locale.format('%.2F',_total_debit_amount or 0, grouping = True), _align='right',_class=_bg_class),TD(locale.format('%.2F',_total_credit_amount or 0, grouping = True), _align='right',_class=_bg_class),TD(),TD(),TD(),TD()))
    table = TABLE(*[head, body,foot],_class='table table-hover')
    return dict(table = table)

def get_posted_by():    
    _id = db(db.General_Ledger.id == request.args(0)).select().first()
    table = TABLE(
        TR(TD('Entry Date'),TD('Posted By')),
        TR(TD(_id.entrydate),TD(_id.created_by.first_name, ' ', _id.created_by.last_name)),_class='table')

    row = []
    ctr = _total_debit_amount = _total_credit_amount = 0
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction Type'),TD('Transaction No'),TD('Account Ref No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Description'),TD('Reff.')),_class='bg-red')
    for n in db(db.General_Ledger.voucher_no_id == _id.voucher_no_id).select(orderby = db.General_Ledger.id):
        ctr += 1
        _total_debit_amount += n.debit
        _total_credit_amount += n.credit
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD(n.transaction_type),            
            TD(n.transaction_prefix_id.prefix,n.transaction_no),
            TD(n.account_reference_no),
            TD(n.account_code),
            TD(locale.format('%.3F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.3F',n.credit or 0, grouping = True), _align='right'),
            TD(n.description),TD(n.gl_entry_ref)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount:'),TD(locale.format('%.3F',_total_debit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(locale.format('%.3F',_total_credit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(),TD()))
    table += TABLE(*[head, body, foot],_class='table')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Entry Date','message':'%s'}).show();" %(XML(table, sanitize = True))    

def put_master_account_list(x):
    # print '---- ',x 
    # _query = dc((dc.Merch_Stock_Header.transaction_type == 1) & (dc.Merch_Stock_Header.gl_batch_posting == False) & (dc.Merch_Stock_Header.cancelled == False) & (dc.Merch_Stock_Header.transaction_date.month() == int(1))).select(orderby = dc.Merch_Stock_Header.id)
    _cre = 0
    _query = db((db.General_Ledger.batch_posting_seq == x) & (db.General_Ledger.transaction_type == request.args(0))).select()
    for n in _query:                
        _id = dc(dc.Master_Account.account_code == n.account_code).select().first()
        if int(request.args(0)) == 1:
            if float(n.credit) > 0:
                # print 'credit 1:- ', n.id, n.account_code, _id.account_code
                _cre = float(_id.credit_balance_1 or 0) - float(n.credit or 0)                
                _id.update_record(credit_balance_1 = float(_cre or 0))
            else:                
                # print 'debit  1:+ ', n.id, n.account_code, _id.account_code
                _cre = float(_id.credit_balance_1 or 0) + float(n.debit or 0)                
                _id.update_record(credit_balance_1 = float(_cre or 0))
        elif int(request.args(0)) == 2:
            if float(n.credit) > 0:
                print 'credit 2:- ', n.id, n.credit
            else:
                print 'debit  2:+ ', n.id, n.debit
        elif int(request.args(0)) == 3:
            if float(n.credit) > 0:
                print 'credit 3:- ', n.id, n.credit
            else:
                print 'debit  3:+ ', n.id, n.debit
        elif int(request.args(0)) == 4:
            if float(n.credit) > 0:
                print 'credit 4:- ', n.id, n.credit
            else:
                print 'debit  4:+ ', n.id, n.debit
        elif int(request.args(0)) == 5:
            if float(n.credit) > 0:
                print 'credit 5:- ', n.id, n.credit
            else:
                print 'debit  5:+ ', n.id, n.debit
        elif int(request.args(0)) == 6:
            if float(n.credit) > 0:
                print 'credit 6:- ', n.id, n.credit
            else:
                print 'debit  6:+ ', n.id, n.debit
        elif int(request.args(0)) == 9:
            if float(n.credit) > 0:
                print 'credit 9:- ', n.id, n.credit
            else:
                print 'debit  9:+ ', n.id, n.debit

def testing():
    print('--------------------------------')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == int(675)) & (dc.Merch_Stock_Transaction.category_id != 'P') & (dc.Merch_Stock_Transaction.category_id != 'S') & (dc.Merch_Stock_Transaction.category_id != 'D') & (dc.Merch_Stock_Transaction.delete == False)).select():    
        print(':'), n.id


    return dict()

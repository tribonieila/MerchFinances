# ----------------------------------------------------------------------------------------------
# >>------     A C C O U N T S  R E C O N C I L L A T I O N  T R A N S A C T I O N S    ------<<
# ----------------------------------------------------------------------------------------------
from datetime import datetime, date
import locale
import datetime
import random
import string
locale.setlocale(locale.LC_ALL, '')
x = datetime.datetime.now() # auth generate

def patch_receipt_voucher_transaction_id():
    _rc_amt = _ba_amt = 0
    _req = db(db.Account_Reconciliation_Header_Request.id == request.args(1)).select().first()
    _rv = db(db.Receipt_Voucher_Header.voucher_no == _req.voucher_no).select().first()
    _reconciled_amount_entry = float(_req.reconciled_amount_entry or 0) # switch to zero in rv header, delete after and add to total_reconciled_amount submit
    _trnx = db(db.Account_Reconciliation_Transaction_Request.id == request.args(2)).select().first()       
    if int(request.args(0)) == 1: # mark row    
        _trnx.update_record(mark = True, new_amount_paid = _trnx.balanced_amount or 0)
    elif int(request.args(0)) == 2: # unmark row
        _trnx.update_record(mark = False, new_amount_paid = 0)
    elif int(request.args(0)) == 3: # add new account code 
        for n in db((db.General_Ledger.account_code == str(request.vars.account_code_ref)) & (db.General_Ledger.paid == False) & ((db.General_Ledger.transaction_type != 21) & (db.General_Ledger.transaction_type != 23))).select():
            _ar = db((db.Account_Reconciliation_Transaction.account_code == n.account_code) & (db.Account_Reconciliation_Transaction.department == n.department) & (db.Account_Reconciliation_Transaction.account_reference_no == n.account_reference_no) & (db.Account_Reconciliation_Transaction.status_id == 5)).select().first()
            if not _ar:
                _balanced_amount = (float(n.debit or 0) - float(n.credit or 0)) - float(n.amount_paid or 0)
                db.Account_Reconciliation_Transaction_Request.insert(
                    account_reconciliation_header_request_id = request.args(1),
                    transaction_type = n.transaction_type,
                    transaction_date = n.transaction_date,
                    entry_date = n.entrydate,
                    transaction_prefix_id = n.transaction_prefix_id,
                    transaction_no = n.transaction_no,
                    transaction_type_ref = n.transaction_type_ref,
                    location = n.location,
                    department = n.department,
                    type = n.type,
                    reference_no = n.reference_no,
                    account_reference_no = n.account_reference_no,
                    account_code = n.account_code,                                                
                    description = n.description,
                    debit = n.debit,
                    credit = n.credit,
                    rv_payment_reference = n.rv_payment_reference,                
                    balanced_amount = _balanced_amount,
                    amount_paid = n.amount_paid,
                    requested_by = _rv.requested_by,
                    requested_on = _rv.requested_on)
    elif int(request.args(0)) == 4: # add new account group
        for n in dc(dc.Customer.customer_group_code_id == request.vars.customer_group_code_id).select():
            for x in db((db.General_Ledger.account_code == n.customer_account_no) & (db.General_Ledger.paid == False) & ((db.General_Ledger.transaction_type != 21) & (db.General_Ledger.transaction_type != 23))).select():
                _ar = db((db.Account_Reconciliation_Transaction.account_code == x.account_code) & (db.Account_Reconciliation_Transaction.department == x.department) & (db.Account_Reconciliation_Transaction.account_reference_no == x.account_reference_no) & (db.Account_Reconciliation_Transaction.status_id == 5)).select().first()                
                if not _ar:
                    _balanced_amount = (float(x.debit or 0) - float(x.credit or 0)) - float(x.amount_paid or 0)
                    db.Account_Reconciliation_Transaction_Request.insert(
                        account_reconciliation_header_request_id = request.args(1),
                        transaction_type = x.transaction_type,
                        transaction_date = x.transaction_date,
                        entry_date = x.entrydate,
                        transaction_prefix_id = x.transaction_prefix_id,
                        transaction_no = x.transaction_no,
                        transaction_type_ref = x.transaction_type_ref,
                        location = x.location,
                        department = x.department,
                        type = x.type,
                        reference_no = x.reference_no,
                        account_reference_no = x.account_reference_no,
                        account_code = x.account_code,                                                
                        description = x.description,
                        debit = x.debit,
                        credit = x.credit,
                        rv_payment_reference = x.rv_payment_reference,                
                        balanced_amount = _balanced_amount,
                        amount_paid = x.amount_paid,
                        requested_by = _rv.requested_by,
                        requested_on = _rv.requested_on)
    _total_reconciled_amount = patch_transaction_id()    
    _ba_amt = float(_rv.total_amount) - float(_rv.last_reconciled_amount or 0) - float(_total_reconciled_amount or 0)
    
    if _ba_amt < 0:
        _trnx.update_record(mark = False, new_amount_paid = 0)
        response.js = "$('#ARTtbl').get(0).reload();alert('Err;')"
        return 
    _req.update_record(total_reconciled_amount = float(_total_reconciled_amount or 0), rv_balanced_amount = float(_ba_amt or 0))
    response.js = "$('#ARTtbl').get(0).reload();$('#Account_Reconciliation_Header_total_reconciled_amount').val('%s');$('#Account_Reconciliation_Header_rv_balanced_amount').val('%s');" %(locale.format('%.2F',_total_reconciled_amount or 0, grouping = True), locale.format('%.2F',_ba_amt or 0, grouping = True))

def patch_transaction_id():
    _new_amount_paid = db.Account_Reconciliation_Transaction_Request.new_amount_paid.sum().coalesce_zero()
    _new_amount_paid = db(db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(1)).select(_new_amount_paid).first()[_new_amount_paid]
    return _new_amount_paid

def post_account_reconciliation_header(): # submit
    _id = db(db.Account_Reconciliation_Header_Request.id == request.args(0)).select().first()
    _ser_no = db(db.Account_Voucher_Type.account_voucher_transaction_type == 25).select().first()        
    _trnx_no = int(_ser_no.voucher_serial_no or 0) + 1
    _rv = db(db.Receipt_Voucher_Header.voucher_no == request.vars.voucher_no).select().first()
    _rv.update_record(reconciliation_request = True)    
    _ser_no.update_record(voucher_serial_no = _trnx_no)
    db.Account_Reconciliation_Header.insert(
        reconciliation_transaction_no = _trnx_no,
        reconciliation_date = request.vars.reconciliation_date,
        voucher_no = request.vars.voucher_no,
        rv_amount = float(_rv.total_amount or 0),
        total_reconciled_amount = request.vars.total_reconciled_amount.replace(',',''),
        rv_balanced_amount = request.vars.rv_balanced_amount.replace(',',''),
        reconciled_amount_entry = request.vars.total_reconciled_amount.replace(',',''),
        requested_by = _id.requested_by, 
        requested_on = _id.requested_on, 
        status_id = 20)
    _header = db(db.Account_Reconciliation_Header.reconciliation_transaction_no == _trnx_no).select().first()
    for n in db((db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(0)) & (db.Account_Reconciliation_Transaction_Request.mark == True)).select():
        db.Account_Reconciliation_Transaction.insert(
            account_reconciliation_header_id = _header.id,
            transaction_type = n.transaction_type,
            transaction_date = n.transaction_date,
            entry_date = n.entry_date,
            transaction_prefix_id = n.transaction_prefix_id,
            transation_no = n.transaction_no,
            transaction_type_ref = n.transaction_type_ref,
            location = n.location,
            department = n.department,
            type = n.type, 
            reference_no = n.reference_no,
            account_reference_no = n.account_reference_no,
            account_code = n.account_code,
            description = n.description,
            credit = n.credit,
            debit = n.debit,
            rv_payment_reference = n.rv_payment_reference,
            amount_paid = n.amount_paid,
            balanced_amount = n.balanced_amount,
            new_amount_paid = n.new_amount_paid,
            requested_by = n.requested_by,
            requested_on = n.requested_on,
            status_id = 2
        )        
    
    db(db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(0)).delete() # remove transaction after submited
    db(db.Account_Reconciliation_Header_Request.id == request.args(0)).delete() # remove header after submited
    response.js = "alertify.success('Success!');window.location.replace('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')   

def patch_account_reconcilation_transactions_id():
    if int(request.args(0)) == 1: # exit from post_account_reconciliation and clear the pending transactions
        db(db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(1)).delete()
        db(db.Account_Reconciliation_Header_Request.id == request.args(1)).delete()
        response.js = "window.location.replace('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')        
    elif int(request.args(0)) == 2: # update  Account_Reconciliation_Transaction_Request table amount_paid        
        response.js = "alertify.prompt( 'Account Reconciliation', 'Amount Paid', '%s', function(evt, value) { ajax('%s' + '/' +  value) }, function() { alertify.error('Cancel') });" %(request.args(2), URL('workflow_accounts_recon','patch_amount_paid_id', args = request.args(1)))
        
def patch_amount_paid_id():
    _trnx = db(db.Account_Reconciliation_Transaction_Request.id == request.args(0)).select().first()
    _req = db(db.Account_Reconciliation_Header_Request.id == _trnx.account_reconciliation_header_request_id).select().first()
    if (float(request.args(1).replace(',','') or 0) < 0) & (float(_trnx.balanced_amount or 0) > float(request.args(1).replace(',','') or 0)):
            response.js = "alertify.alert('Account Reconciliation', 'New payment must not less than to closing balance.');"
    elif (float(request.args(1).replace(',','') or 0) > 0) & (float(_trnx.balanced_amount or 0) < float(request.args(1).replace(',','') or 0)):
            response.js = "alertify.alert('Account Reconciliation', 'New payment must not greater than to closing balance.');"
    else:

        # _total_reconciled_amount = patch_transaction_id()    
        # _ba_amt = float(_rv.total_amount) - float(_rv.last_reconciled_amount or 0) - float(_total_reconciled_amount or 0)

        _trnx.update_record(new_amount_paid = request.args(1).replace(',',''))
        _new_amount_paid = db.Account_Reconciliation_Transaction_Request.new_amount_paid.sum().coalesce_zero()
        _new_amount_paid = db(db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == _trnx.account_reconciliation_header_request_id).select(_new_amount_paid).first()[_new_amount_paid]
        _ba_amt = float(_trnx.balanced_amount or 0) - float(_new_amount_paid or 0)
        _req.update_record(total_reconciled_amount = float(_new_amount_paid or 0), rv_balanced_amount = float(_ba_amt or 0))        
        response.js = "$('#ARTtbl').get(0).reload();$('#Account_Reconciliation_Header_total_reconciled_amount').val('%s');$('#Account_Reconciliation_Header_rv_balanced_amount').val('%s');" %(locale.format('%.2F',_new_amount_paid or 0, grouping = True), locale.format('%.2F',_ba_amt or 0, grouping = True))

# ---------------------------------------------------------------------
@auth.requires_login()
def post_receipt_voucher_header_id():        
    _id = db(db.Receipt_Voucher_Header.id == request.args(0)).select().first()
    if db(db.Account_Reconciliation_Header_Request.voucher_no == _id.voucher_no).select().first():
        _id = db(db.Account_Reconciliation_Header_Request.voucher_no == _id.voucher_no).select().first()
        response.js = "window.location.replace('%s')" % URL('workflow_accounts_recon','post_account_reconciliation', args = _id.id)        
    else:
        db.Account_Reconciliation_Header_Request.insert(
                voucher_no = _id.voucher_no,
                rv_amount = _id.total_amount,          
                requested_by = _id.requested_by,
                requested_on = _id.requested_on,
                status_id =  20)
        _header = db(db.Account_Reconciliation_Header_Request.voucher_no == _id.voucher_no).select().first()
        for n in db(db.Receipt_Voucher_Transaction.receipt_voucher_header_id == request.args(0)).select():
            for y in db((db.General_Ledger.account_code == str(n.account_credit_code)) & (db.General_Ledger.paid == False) & ((db.General_Ledger.transaction_type != 21) & (db.General_Ledger.transaction_type != 23))).select():                
                _ar = db((db.Account_Reconciliation_Transaction.account_code == y.account_code) & (db.Account_Reconciliation_Transaction.department == y.department) & (db.Account_Reconciliation_Transaction.account_reference_no == y.account_reference_no) & (db.Account_Reconciliation_Transaction.status_id == 5)).select().first()
                if not _ar:                    
                    _balanced_amount = (float(y.debit or 0) - float(y.credit or 0)) - float(y.amount_paid or 0)
                    db.Account_Reconciliation_Transaction_Request.insert(
                        account_reconciliation_header_request_id = _header.id,
                        transaction_type = y.transaction_type,
                        transaction_date = y.transaction_date,
                        entry_date = y.entrydate,
                        transaction_prefix_id = y.transaction_prefix_id,
                        transaction_no = y.transaction_no,
                        transaction_type_ref = y.transaction_type_ref,
                        location = y.location,
                        department = y.department,
                        type = y.type,
                        reference_no = y.reference_no,
                        account_reference_no = y.account_reference_no,
                        account_code = y.account_code,                                                
                        description = y.description,
                        debit = y.debit,
                        credit = y.credit,
                        rv_payment_reference = y.rv_payment_reference,                
                        balanced_amount = _balanced_amount,
                        amount_paid = y.amount_paid,
                        requested_by = _header.requested_by,
                        requested_on = _header.requested_on)
        
        response.js = "window.location.replace('%s')" % URL('workflow_accounts_recon','post_account_reconciliation', args = _header.id)        

@auth.requires_login()    
def delete_account_reconciliation_request_id():
    db(db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(0)).delete()
    db(db.Account_Reconciliation_Header_Request.id == request.args(0)).delete()
    response.js = "window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')

@auth.requires_login()    
def post_account_reconciliation():
    _trnx_no = db(db.Account_Voucher_Type.account_voucher_transaction_type == 25).select().first()        

    _id = db(db.Account_Reconciliation_Header_Request.id == request.args(0)).select().first()
    _rv = db(db.Receipt_Voucher_Header.voucher_no == _id.voucher_no).select().first()
    _rv_amount = _rv.total_amount - _rv.last_reconciled_amount 
    db.Account_Reconciliation_Header.reconciliation_transaction_no.default = int(_trnx_no.voucher_serial_no or 0) + 1
    db.Account_Reconciliation_Header.voucher_no.default = _id.voucher_no    
    db.Account_Reconciliation_Header.rv_amount.default = locale.format('%.2F' ,_rv_amount or 0, grouping = True)        
    db.Account_Reconciliation_Header.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.id == 20), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
    db.Account_Reconciliation_Header.status_id.default = 20

    form = SQLFORM(db.Account_Reconciliation_Header)
    form2 = SQLFORM.factory(
        Field('customer_group_code_id', 'reference Customer_Group_Code', ondelete = 'NO ACTION', requires = IS_EMPTY_OR(IS_IN_DB(dc, dc.Customer_Group_Code.id,'%(description)s', zero = 'Choose Group Code')))
    )
    # print _id.rv_amount, _id.status_id
    return dict(form = form, _id=_id, form2 = form2)

def post_account_reconciliation_transaction():
    ctr = _total_amount = _total_debit = _total_credit = _total_credit_amount = _total_debit_amount = 0
    row = []

    _total_amount = db.Account_Reconciliation_Transaction_Request.new_amount_paid.sum().coalesce_zero()
    _total_amount = db((db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(0)) & (db.Account_Reconciliation_Transaction_Request.mark == True)).select(_total_amount).first()[_total_amount]

    head = THEAD(TR(TD('#'),TD('Date'),TD('Account Code'),TD('Voucher No.'),TD('Type'),TD('Dept.'),TD('Description'),TD('Debit'),TD('Credit'),TD('Last Payment'),TD('Balance'),TD('New Payment'),TD()),_class='bg-red')
    for n in db((db.Account_Reconciliation_Transaction_Request.account_reconciliation_header_request_id == request.args(0)) & (db.Account_Reconciliation_Transaction_Request.paid == False)).select():
        ctr += 1        
        _mark = INPUT(_type='checkbox', _class='marking',_role='button', _name='mark',_id = 'mark', value=n.mark)
        appr_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Amount Paid', _role='button', _class='btn btn-icon-toggle disabled')
        if (n.new_amount_paid or 0) != 0.0:        
            appr_lnk = A(I(_class='fas fa-pencil-alt'), _title='Edit Amount Paid', _role='button', _class='btn btn-icon-toggle', callback=URL('workflow_accounts_recon','patch_account_reconcilation_transactions_id',args = [2, n.id,n.new_amount_paid], extension = False))

        row.append(TR(
            TD(ctr, INPUT(_type='number', _name='_id', _value = n.id, _hidden=True)),
            TD(n.transaction_date),
            TD(n.account_code),
            TD(n.account_reference_no),
            TD(n.transaction_type),
            TD(n.department),
            TD(n.description),
            TD(locale.format('%.2F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.amount_paid or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.balanced_amount or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.new_amount_paid or 0, grouping = True), _align='right'),
            TD(appr_lnk,' ', _mark,_align='right')))
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD('Total Amount:',_colspan='11', _align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True), _align='right'),TD()))
    table = TABLE(*[head, body, foot], _class='table',_id='ARTtbl')
    return dict(table = table)

@auth.requires_login()
def get_pending_rv_reconciliation_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Trnx No'),TD('Voucher No'),TD('Total Amount'),TD('Requestd By'),TD('Status'),TD()),_class='bg-red')    
    _query = db((db.Account_Reconciliation_Header.created_by == auth.user_id) & (db.Account_Reconciliation_Header.status_id != 22)).select()
    if auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'ROOT'):
        _query = db(db.Account_Reconciliation_Header.status_id != 22).select()
    for n in _query:
        ctr += 1
        view_lnk = A(I(_class='fas fa-search'), _title='Reconcile RV', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_receipt_voucher_id',args = n.id, extension = False))
        _acc_ref = A(I(_class='fas fa-handshake'), _title='Reconcile RV', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(view_lnk)
        if auth.has_membership(role = 'ACCOUNTS MANAGER') | auth.has_membership(role = 'ROOT'):
            view_lnk = A(I(_class='fas fa-search'), _title='View/Approved', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_account_reconciliation_id',args = n.id, extension = False))
            appr_lnk = A(I(_class='fas fa-user-check'), _title='Approved', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('workflow_accounts_recon','patch_account_reconcilation_id',args = [4,n.id], extension = False))
            reje_lnk = A(I(_class='fas fa-user-times'), _title='Reject', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('workflow_accounts_recon','patch_account_reconcilation_id',args = [5,n.id], extension = False))
            btn_lnk = DIV(view_lnk, appr_lnk, reje_lnk)
        if auth.has_membership(role = 'ACCOUNTS') and n.status_id == 21:
            view_lnk = A(I(_class='fas fa-search'), _title='View/Confirmation', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_account_reconciliation_id',args = n.id, extension = False))
            btn_lnk = DIV(view_lnk)
        elif auth.has_membership(role = 'ACCOUNTS') and n.status_id == 1:
            view_lnk = A(I(_class='fas fa-search'), _title='View', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_account_reconciliation_id',args = n.id, extension = False))
            btn_lnk = DIV(view_lnk)

        row.append(TR(
            TD(ctr),
            TD(n.reconciliation_date),
            TD('AR',n.reconciliation_transaction_no),            
            TD('RV',n.voucher_no),            
            TD(locale.format('%.2F', n.rv_amount or 0, grouping = True),_align='right'),                                               
            TD(n.requested_by.first_name,' ',n.requested_by.last_name[0],'.'),            
            TD(n.status_id.required_action),
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table table-hover',_id='TBLAct')
    return dict(table = table)

@auth.requires_login()
def get_account_recon_grid():
    ctr = 0
    row = []
    _vn = db(db.Account_Voucher_Type.account_voucher_transaction_type == 21).select().first()
    head = THEAD(TR(TD('#'),TD('Date'),TD('Type'),TD('Code'),TD('Account Code'),TD('Account Reference'),TD('RVC Ref.'),TD('RVC Type'),TD('Total Amount'),TD('Reconciled Amount'),TD('Reconciliation Txn Ref'),TD()),_class='bg-red')    
    for n in db((db.Receipt_Voucher_Header.reconciled == False) & (db.Receipt_Voucher_Header.reconciliation_request == False)).select():
        ctr += 1
        sear_lnk = A(I(_class='fas fa-search'), _title='Open RV', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('workflow_accounts_recon','get_receipt_voucher_id',args = n.id, extension = False))
        # _acc_ref = A(I(_class='fas fa-handshake'), _title='Open RV', _type='button  ', _role='button', _class='btn btn-icon-toggle', _target='blank', _href=URL('account_transaction_reports','get_account_voucher_request_id',args = n.id, extension = False))
        btn_lnk = DIV(sear_lnk)
        row.append(TR(
            TD(ctr),
            TD(n.transaction_reference_date),
            TD(n.account_voucher_transaction_type),
            TD(n.account_voucher_transaction_code),            
            TD(n.account_code),            
            TD(n.account_reference),
            TD(n.rv_confirmation_reference),
            TD(n.receipt_voucher_confirmation_type_id),
            TD(locale.format('%.2F', n.total_amount or 0, grouping = True),_align='right'),            
            TD(locale.format('%.2F', n.reconciled_amount or 0, grouping = True),_align='right'),            
            TD(n.reconciliation_transaction_ref),                        
            TD(btn_lnk)))
    body = TBODY(*[row])
    table = TABLE([head, body],_class='table table-hover',_id='TBLAct')
    return dict(table = table)

@auth.requires_login()
def get_receipt_voucher_id():
    _header = db(db.Receipt_Voucher_Header.id == request.args(0)).select().first()

    db.Account_Reconciliation_Header_Request.voucher_no.default = str(_header.account_voucher_transaction_code) + str(_header.voucher_no)
    db.Account_Reconciliation_Header_Request.rv_amount.default = locale.format('%.2F',_header.total_amount or 0, grouping = True)
    # db.Account_Reconciliation_Header_Request.reconciliation_date = _header.transaction_reference_date
    form = SQLFORM(db.Account_Reconciliation_Header_Request)
    return dict(form = form, _id = _header)

def get_receipt_voucher_transaction_id():
    ctr = _total_amount = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Account Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount')),_class='bg-red')
    for n in db(db.Receipt_Voucher_Transaction.receipt_voucher_header_id == request.args(0)).select(): #                        
        ctr += 1
        _am = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
        row.append(TR(
            TD(ctr),
            TD(n.account_credit_code),
            TD(_am.account_name),
            TD(n.department_code),
            TD(n.description),
            TD(locale.format('%.2F',n.amount_paid or 0, grouping = True),_align='right')))
    body = TBODY(*row)
    foot = TFOOT(TR(TD('Total Amount Reconcile: ',_colspan='5',_align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True), _align='right')))
    table = TABLE(*[head, body], _class='table', _id='RVTtbl')
    return dict(table = table)

# >> -------------------- ACCOUNT MANAGER view/approval -------------------

def patch_account_reconcilation_id():
    if int(request.args(0)) == 1: # account reconcilation approval -> account/finance manager
        _id = db(db.Account_Reconciliation_Header.id == request.args(1)).select().first()
        _id.update_record(status_id = 21)
        for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(1)).select():
            n.update_record(status_id = 3)
        response.js = "alertify.success('Approved!');window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')

    elif int(request.args(0)) == 2: # account confirmation
        # gl table
        # gl.amount_paid ===
        # validate _gl.amount_paid == _ar_transaction.amount_paid
        # if true:
        # _gl.paid = True        
        # rv_payment_reference == _act_recon: voucher_no ex: RVXXXXX
        
        # rv table >>>>
        # 
        # Receipt_Voucher_Header.reconciled_amount == Account_Reconciliation_Header.total_reconciled_amount
        # if Receipt_Voucher_Header.total_amount == Account_Reconciliation_Header.total_reconciled_amount:
            # reconciled = True
        # Receipt_Voucher_Header.amount_paid += Account_Reconciliation_Header.total_reconciled_amount 
        # Receipt_Voucher_Header.reconciled_amount += Account_Reconciliation_Header.total_reconciled_amount 
        # Receipt_Voucher_Header.reconciliation_transaction_ref == ARXXXXXXXX

        # Receipt_Voucher_Header.reconciliation_request == False
        
        _id = db(db.Account_Reconciliation_Header.id == request.args(1)).select().first()        
        _rv = db(db.Receipt_Voucher_Header.voucher_no == _id.voucher_no).select().first()
        
        # use _rv.last_reconciled_amount instead _rv.amount_paid
        _rv_reconciled_amount = float(_rv.reconciled_amount or 0) + float(_id.total_reconciled_amount or 0)
        _last_reconciled_amount = float(_rv.last_reconciled_amount or 0) + float(_id.total_reconciled_amount or 0)
        # _rv_amount_paid = float(_rv.amount_paid or 0) + float(_id.total_reconciled_amount or 0)
        _rv_reconciliation_transaction_no = str(_rv.reconciliation_transaction_ref) + ' / AR' + str(_id.reconciliation_transaction_no)
        _rv.update_record(reconciled_amount = float(_rv_reconciled_amount or 0), last_reconciled_amount = float(_last_reconciled_amount or 0))
        
        if _rv.total_amount == float(_last_reconciled_amount or 0):
            _rv.update_record(reconciled =  True)
        if _rv.reconciliation_transaction_ref == None:
            _rv_reconciliation_transaction_no = 'AR' + str(_id.reconciliation_transaction_no)
        _rv.update_record(reconciliation_transaction_ref = _rv_reconciliation_transaction_no, reconciliation_request = False)       

        for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(1)).select():
            _status_id = 4
            n.update_record(amount_paid = n.new_amount_paid)            
            if n.amount_paid == n.balanced_amount:
                _status_id = 5            
            n.update_record(status_id = _status_id)            
            _gl = db((db.General_Ledger.account_code == n.account_code) & (db.General_Ledger.account_reference_no == n.account_reference_no) & (db.General_Ledger.transaction_type == n.type) & (db.General_Ledger.department == n.department)).select().first()
            if _gl:
                _amount_paid = float(_gl.amount_paid or 0) + float(n.new_amount_paid or 0)
                _account_reference_no = str(_gl.rv_payment_reference) + '/RV' + str(_id.voucher_no)
                _reconciliation_transaction_no = str(_gl.reconciliation_transaction_no) + ', ' + str(_id.reconciliation_transaction_no)
                if _gl.rv_payment_reference == None:
                    _account_reference_no = 'RV' + str(_id.voucher_no)
                if _gl.reconciliation_transaction_no == None:
                    _reconciliation_transaction_no = _id.reconciliation_transaction_no
                _gl.update_record(amount_paid = _amount_paid)
                if (float(_gl.debit or 0) - float(_gl.credit or 0)) == float(_amount_paid or 0):
                    _gl.update_record(paid = True)
                _gl.update_record(rv_payment_reference = _account_reference_no, reconciliation_transaction_no = _reconciliation_transaction_no)
        
        _total_reconciled_amount = float(_rv.reconciled_amount or 0)# + float(_id.reconciled_amount_entry or 0)
        _total_reconciled_balance = float(_rv.total_amount or 0) - float(_total_reconciled_amount or 0)        
        
        _id.update_record(total_reconciled_amount = float(_total_reconciled_amount or 0),rv_balanced_amount = _total_reconciled_balance, status_id = 22)    
        response.js = "alertify.success('Confirmed!');window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')
            
    elif int(request.args(0)) == 3:
        print('reject')
    # if rejected:
    # status_id = rejected
    # rv.reconciliation_request = False
        response.js = "alertify.warning('Rejected!');window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')
    elif int(request.args(0)) == 4: # short-cut approved        
        _req = db(db.Account_Reconciliation_Header.id == request.args(1)).select().first()        
        _req.update_record(status_id = 21)
        for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(1)).select():
            n.update_record(status_id = 3)        
        response.js = "alertify.success('Approved!');window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')        
    elif int(request.args(0)) == 5: # short-cut reject        
        _req = db(db.Account_Reconciliation_Header.id == request.args(1)).select().first()
        _req.update_record(status_id = 1)
        for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(1)).select():
            n.update_record(status_id = 0)        

        response.js = "alertify.warning('Rejected!');window.location.href=('%s')" % URL('workflow_accounts_recon','get_pending_rv_reconciliation_grid')
        


        

@auth.requires_login()
def get_account_reconciliation_id():
    _id = db(db.Account_Reconciliation_Header.id == request.args(0)).select().first()
    
    if auth.has_membership(role = 'ACCOUNTS MANAGER') and db(db.Account_Reconciliation_Header.status_id == 21).select().first(): 
        db.Account_Reconciliation_Header.status_id.requires = IS_IN_DB(db(db.Accounts_Workflow_Status.mnemonic == 'AR-TASK2'), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
        db.Account_Reconciliation_Header.status_id.default = 21
    elif auth.has_membership(role = 'ACCOUNTS') and db(db.Account_Reconciliation_Header.status_id == 11).select().first(): 
        db.Account_Reconciliation_Header.status_id.requires = IS_IN_DB(db((db.Accounts_Workflow_Status.id == 1) | (db.Accounts_Workflow_Status.mnemonic == 'AR-TASK2')), db.Accounts_Workflow_Status.id, '%(description)s', zero = 'Choose Status')
        db.Account_Reconciliation_Header.status_id.default = 1

    form = SQLFORM(db.Account_Reconciliation_Header, request.args(0))
    return dict(form = form, _id = _id)

@auth.requires_login()
def get_account_reconciliation_transaction_id():
    ctr = 0
    row = []    
    head = THEAD(TR(TD('#'),TD('Date'),TD('Account Code'),TD('Voucher No.'),TD('Type'),TD('Dept.'),TD('Description'),TD('Debit'),TD('Credit'),TD('Last Payment'),TD('Balance'),TD('New Payment'),TD()),_class='bg-red')
    for n in db(db.Account_Reconciliation_Transaction.account_reconciliation_header_id == request.args(0)).select():
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.transaction_date),
            TD(n.account_code),
            TD(n.account_reference_no),
            TD(n.transaction_type),
            TD(n.department),
            TD(n.description),
            TD(locale.format('%.2F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.amount_paid or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.balanced_amount or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.new_amount_paid or 0, grouping = True), _align='right'),
            TD()))
    body = TBODY(*row)
    table = TABLE(*[head, body], _class='table', _id='ARTtbl')
    return dict(table = table)

# << -------------------- ACCOUNT MANAGER view/approval -------------------
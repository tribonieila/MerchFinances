from datetime import datetime, date
import locale
import datetime
# import date
locale.setlocale(locale.LC_ALL, '')
_arr = []

def get_account_transaction_general_ledger_id():
    if int(request.args(0)) == 1:
        _id = db(db.General_Ledger.id == request.args(2)).select().first()         
        row = []
        ctr = _total_debit_amount = _total_credit_amount = 0
        head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction Type'),TD('Transaction No'),TD('Account Ref No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Description'),TD('Reff.')),_class='bg-red')
        for n in db(db.General_Ledger.transaction_no == _id.transaction_no).select(orderby = db.General_Ledger.id):
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
                TD(n.description),
                TD(n.gl_entry_ref)))
        body = TBODY(*row)
        foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount:'),TD(locale.format('%.3F',_total_debit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(locale.format('%.3F',_total_credit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(),TD()))
        table = TABLE(*[head, body, foot],_class='table')
        response.js = "alertify.alert().set({'startMaximized':true, 'title':'Entry Date','message':'%s'}).show();" %(XML(table, sanitize = True))    

    elif int(request.args(0)) == 2 and int(request.args(1)) == 21: # rv grid        
        _gl = db(db.General_Ledger.id == request.args(2)).select().first()
        _rv = db(db.Receipt_Voucher_Header.voucher_no == _gl.account_reference_no).select().first()
        if _rv:
            _bank_name = 'None'
            if _rv.bank_name_id:
                _bank_name = _rv.bank_name_id.bank_code,' - ',_rv.bank_name_id.bank_name
            table = TABLE(
                TR(TD('Date'),TD('Account Reference'),TD('Type'),TD('Code'),TD('Payment Mode'),TD('Account Code'),TD('Cheque No'),TD('Bank Name'),TD('Cheque Dated')),
                TR(
                    TD(_rv.transaction_reference_date),
                    TD(_rv.account_reference),
                    TD(_rv.account_voucher_transaction_type),
                    TD(_rv.account_voucher_transaction_code),
                    TD(_rv.account_payment_mode_id.account_voucher_payment_code,' - ',_rv.account_payment_mode_id.account_voucher_payment_name),
                    TD(_rv.account_code),
                    TD(_rv.cheque_no),
                    TD(_bank_name),
                    TD(_rv.cheque_dated)),_class='table table-bordered table-condensed')

            table += TABLE(
                TR(TD('Total Amount'),TD('Amount Paid'),TD('Received From'),TD('Collected By'),TD('Manual RV#'),TD('Remarks')),
                TR(
                    TD(locale.format('%.2F',_rv.total_amount or 0, grouping = True),_align='right'),
                    TD(locale.format('%.2F',_rv.amount_paid or 0, grouping = True),_align='right'),
                    TD(_rv.received_from),
                    TD(_rv.collected_by),
                    TD(_rv.manual_rv_no),
                    TD(_rv.remarks)),_class='table table-bordered table-condensed')
            row = []
            ctr = _total_amount = 0
            head = THEAD(TR(TD('#'),TD('Account Credit Code'),TD('Account Name'),TD('Dept.'),TD('Description'),TD('Amount'),TD('Reff.')),_class='bg-red')
            for n in db(db.Receipt_Voucher_Transaction.receipt_voucher_header_id == _rv.id).select():
                ctr += 1                
                _total_amount += float(n.amount_paid or 0)
                _ma = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
                row.append(TR(
                    TD(ctr),
                    TD(n.account_credit_code),
                    TD(_ma.account_name),
                    TD(n.department_code),
                    TD(n.description),
                    TD(locale.format('%.2F', n.amount_paid or 0, grouping = True), _align='right'),
                    TD(n.gl_entry_ref)))
            body = TBODY(*row)
            foot = TFOOT(TR(TD('Total Amount: ',_colspan='5',_align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align='right')))
            table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed')
            response.js = "alertify.alert().set({'startMaximized':true, 'title':'Receipt Voucher Transaction','message':'%s'}).show();" %(XML(table, sanitize = True))    
        elif not _rv:
            response.js = "alertify.notify('Account Ref. not found','warning')"

    elif int(request.args(0)) == 2 and int(request.args(1)) == 22: # rvc grid        
        _gl = db(db.General_Ledger.id == request.args(2)).select().first()
        _rvc = db(db.Receipt_Voucher_Confirmation.voucher_no == _gl.account_reference_no).select().first()
        if _rvc:
            _type = 'CASH/CHEQUE'
            if _rvc.receipt_voucher_confirmation_type_id == 'B':
                _type = 'POST DATED CHEQUE'
            table = TABLE(
                TR(TD('Date'),TD('Account Reference'),TD('RV Confirmation Type'),TD('Account Code'),TD('Remarks')),
                TR(
                    TD(_rvc.transaction_reference_date),
                    TD(_rvc.account_reference),
                    TD(_type),
                    TD(_rvc.account_code),
                    TD(_rvc.remarks)),_class='table table-bordered table-condensed')

            row = []
            ctr = _total_amount = 0
            head = THEAD(TR(TD('#'),TD('Account Reference'),TD('Account Credit Code'),TD('Description'),TD('Amount'),TD('Ref.')),_class='bg-red')
            for n in db(db.Receipt_Voucher_Transaction_Confirmation.receipt_voucher_confirmation_id == _rvc.id).select():
                ctr += 1                
                _total_amount += float(n.amount_paid or 0)
                # _ma = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
                row.append(TR(
                    TD(ctr),
                    TD(n.account_reference),
                    TD(n.account_credit_code),                    
                    TD(n.description),
                    TD(locale.format('%.2F', n.amount_paid or 0, grouping = True), _align='right'),
                    TD(n.gl_entry_ref)))
            body = TBODY(*row)
            foot = TFOOT(TR(TD('Total Amount: ',_colspan='4',_align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align='right')))
            table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed')
            response.js = "alertify.alert().set({'startMaximized':true, 'title':'Receipt Voucher Confirmation Transaction','message':'%s'}).show();" %(XML(table, sanitize = True))    
        elif not _rvc:
            response.js = "alertify.notify('Account Ref. not found','warning')"
    
    elif int(request.args(0)) == 2 and int(request.args(1)) == 23: # pv grid        
        _gl = db(db.General_Ledger.id == request.args(2)).select().first()
        _pv = db(db.Payment_Voucher_Header.payment_voucher_no == _gl.account_reference_no).select().first()
        if _pv:
            _type = 'CASH/CHEQUE'
            if _pv.account_payment_mode_id == 3:
                _type = 'POST DATED CHEQUE'
            table = TABLE(
                TR(TD('Date'),TD('Account Reference'),TD('PV Type'),TD('Account Code'),TD('Remarks'),_class='bg-red'),
                TR(
                    TD(_pv.transaction_reference_date),
                    TD(_pv.account_reference),
                    TD(_type),
                    TD(_pv.account_code),
                    TD(_pv.remarks)),_class='table table-bordered table-condensed')

            row = []
            ctr = _total_amount = 0
            head = THEAD(TR(TD('#'),TD('Account Reference'),TD('Account Debit Code'),TD('Description'),TD('Category'),TD('Cost Center'),TD('Amount'),TD('Ref.')),_class='bg-primary')
            for n in db(db.Payment_Voucher_Transaction.payment_voucher_header_id == _pv.id).select():
                ctr += 1                
                _total_amount += float(n.amount or 0)
                # _ma = dc(dc.Master_Account.account_code == n.account_credit_code).select().first()
                row.append(TR(
                    TD(ctr),
                    TD(n.account_reference),
                    TD(n.account_debit_code),
                    TD(n.description),
                    TD(n.cost_center_category_id.cost_center_category_name),
                    TD(n.cost_center_code),
                    TD(locale.format('%.2F', n.amount or 0, grouping = True), _align='right'),
                    TD(n.gl_entry_ref)))
            body = TBODY(*row)
            foot = TFOOT(TR(TD('Total Amount: ',_colspan='6',_align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True),_align='right')))
            table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed')
            response.js = "alertify.alert().set({'startMaximized':true, 'title':'Payment Voucher Transaction','message':'%s'}).show();" %(XML(table, sanitize = True))    
        elif not _pv:
            response.js = "alertify.notify('Account Ref. not found','warning')"    
    
    elif int(request.args(0)) == 2 and int(request.args(1)) == 24: # jv grid
        _gl = db(db.General_Ledger.id == request.args(2)).select().first()
        _jv = db(db.Journal_Voucher_Header.journal_voucher_no == _gl.account_reference_no).select().first()        
        if _jv:
            table = TABLE(
                TR(TD('Date'),TD('Account Reference'),TD('Type'),TD('Code'),TD('JV Type'),TD('Remarks')),
                TR(TD(_jv.journal_voucher_date),TD(_jv.account_reference),TD(_jv.account_voucher_transaction_type),TD(_jv.account_voucher_transaction_code),TD(_jv.journal_voucher_type_id),TD(_jv.remarks)),_class='table table-bordered table-condensed'
            )
            row = []
            ctr = _total_amount = 0
            head = THEAD(TR(TD('#'),TD('A.Reff.'),TD('AD Code'),TD('AC Code'),TD('Description'),TD('Amount'),TD('Reff.')),_class='bg-red')
            for n in db(db.Journal_Voucher_Transaction.journal_voucher_header_id == _jv.id).select():
                ctr += 1
                _total_amount += n.amount
                row.append(TR(
                    TD(ctr),
                    TD(n.account_reference),
                    TD(n.account_debit_code),
                    TD(n.account_credit_code),
                    TD(n.description),
                    TD(locale.format('%.2F', n.amount or 0, grouping = True), _align='right'),
                    TD(n.gl_entry_ref),
                ))
            body = TBODY(*[row])
            foot = TFOOT(TR(TD('Total Amount : ',_colspan='5', _align='right'),TD(locale.format('%.2F',_total_amount or 0, grouping = True), _align='right')))
            table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed')
            
            response.js = "alertify.alert().set({'startMaximized':true, 'title':'Journal Voucher Transaction','message':'%s'}).show();" %(XML(table, sanitize = True))    
        elif not _jv:
            response.js = "alertify.notify('Account Ref. not found','warning')"    


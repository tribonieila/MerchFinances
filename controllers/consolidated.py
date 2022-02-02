import locale

def add_general_ledger_id():
    row = []
    ctr = _total_debit_amount = _total_credit_amount = 0
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction Type'),TD('Transaction No'),TD('Account Ref No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Description'),TD('Reff.')),_class='bg-red')
    for n in db(db.General_Ledger.voucher_no_id == request.args(0)).select(orderby = db.General_Ledger.id):
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
            TD(locale.format('%.2F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True), _align='right'),
            TD(n.description),TD(n.gl_entry_ref)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount:'),TD(locale.format('%.2F',_total_debit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(locale.format('%.2F',_total_credit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(),TD()))
    table = TABLE(*[head, body, foot],_class='table')

@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))        
def get_general_ledger_id():
    row = []
    ctr = _total_debit_amount = _total_credit_amount = 0
    head = THEAD(TR(TD('#'),TD('Date'),TD('Transaction Type'),TD('Transaction No'),TD('Account Ref No.'),TD('Account Code'),TD('Debit Amount'),TD('Credit Amount'),TD('Description'),TD('Reff.')),_class='bg-red')
    for n in db(db.General_Ledger.voucher_no_id == request.args(0)).select(orderby = db.General_Ledger.id):
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
            TD(locale.format('%.2F',n.debit or 0, grouping = True), _align='right'),
            TD(locale.format('%.2F',n.credit or 0, grouping = True), _align='right'),
            TD(n.description),TD(n.gl_entry_ref)))
    body = TBODY(*row)
    foot = TFOOT(TR(TD(),TD(),TD(),TD(),TD(),TD('Total Amount:'),TD(locale.format('%.2F',_total_debit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(locale.format('%.2F',_total_credit_amount or 0, grouping = True), _align='right',_class='bg-gray-active color-palette'),TD(),TD()))
    table = TABLE(*[head, body, foot],_class='table')
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'General Ledger','message':'%s'}).show();" %(XML(table, sanitize = True))    
    # response.js = "alertify.alert().set({'resizable',true,'HELLO'}).resizeTo('100%',250);" 
    # response.js = "alertify.confirm('%s').set('resizable',true).resizeTo('100%',250); " %(XML(table))

def patch_session_consolidated():    
    session.cons_dept_code_id = request.vars.dept_code_id
    session.cons_year = request.vars.year
    session.cons_month = request.vars.month
    response.js = "$('#CONtbl').get(0).reload();alertify.notify('loading...');"


@auth.requires(lambda: auth.has_membership('ACCOUNTS') |  auth.has_membership('ACCOUNTS MANAGER') | auth.has_membership(role = 'MANAGEMENT') | auth.has_membership('ROOT'))
def get_consolidated_transactions_grid():
    from datetime import date
    session.cons_month = request.now.month
    if int(request.args(0)) == 1:
        title = 'Purchase Receipt'                    
    elif int(request.args(0)) == 2:
        title = 'Sales Invoice'
    elif int(request.args(0)) == 3:
        title = 'Cash Sales'
    elif int(request.args(0)) == 4:
        title = 'Sales Return'
    elif int(request.args(0)) == 5:
        title = 'Stock Transfer'
    elif int(request.args(0)) == 6:
        title = 'Stock Adjustment'
    elif int(request.args(0)) == 9:
        title = 'Obsolescence'    
    _year = date.today().year
    _year1 = _year - 1
    _year2 = _year - 2        
    form = SQLFORM.factory(
        Field('dept_code_id','reference Department', ondelete = 'NO ACTION',label = 'Dept Code',requires = IS_IN_DB(dc, dc.Department.id,'%(dept_code)s - %(dept_name)s', zero = 'Choose Department')),
        Field('year','string',length = 4, default=_year, requires = IS_IN_SET([(_year,_year),(_year1, _year1),(_year2,_year2)],zero = 'Choose Year')),
        Field('month','string',length=25,requires = IS_IN_SET([('01', 'January'), ('02', 'February'), ('03', 'March'),('04','April'),('05','May'),('06','June'),('07', 'July'),('08', 'August'), ('09', 'September'),('10','October'),('11','November'),('12','December')],zero='Choose Month')))    
    return dict(form = form, title = title)

def load_consolidated_transactions_grid():
    row = []
    ctr = 0
    head = THEAD(TR(TD('#'),TD('Transaction Date'),TD('Voucher No'), TD('POS Voucher'),TD('Location'),TD('Type'),TD('Account'),TD('Order No.'),TD('Amount'),TD('Action')),_class='bg-red')    
    # for n in dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.cancelled == False)).select(orderby = dc.Merch_Stock_Header.id):
    for n in dc((dc.Merch_Stock_Header.transaction_type == request.args(0)) & (dc.Merch_Stock_Header.dept_code == session.cons_dept_code_id) & (dc.Merch_Stock_Header.transaction_date.year() == session.cons_year) & (dc.Merch_Stock_Header.transaction_date.month() == session.cons_month) & ((dc.Merch_Stock_Header.cancelled == False) | (dc.Merch_Stock_Header.cancelled == None))).select(orderby = dc.Merch_Stock_Header.id):
        ctr += 1
        view_lnk = A(I(_class='fa fa-search'), _title='View Row', _type=' button', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_general_ledger_id', args = n.id))
        trax_lnk = A(I(_class='fa fa-file-invoice'), _title='View Trnx', _type='button  ', _role='button', _class='btn btn-icon-toggle', callback=URL('consolidated','get_consolidated_transactions_id', args = [request.args(0),n.id], extension = False))
        dele_lnk = A(I(_class='fa fa-trash'), _title='Delete Row', _type='button  ', _role='button', _class='btn btn-icon-toggle disabled')
        _loc = dc(dc.Location.id == n.location).select().first()
        btn_lnk = DIV(view_lnk, trax_lnk, dele_lnk)
        row.append(TR(TD(ctr),TD(n.transaction_date),TD(n.voucher_no),TD(n.voucher_no2),TD(_loc.location_code, ' - ',_loc.location_name),TD(n.transaction_type),TD(n.account),TD(n.order_account),TD(locale.format('%.3F',n.total_amount_after_discount or 0, grouping = True),_align='right'),TD(btn_lnk)))
    body = TBODY(*row)
    table = TABLE(*[head, body],_class='table',_id='CONtbl')
    return dict(table = table)


def get_consolidated_transactions_id():    
    if int(request.args(0)) == 1:
        title = 'Purchase Receipt Transaction'
        table = get_purchase_receipt_id()
        table += get_purchase_receipt_transaction_id()
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 2:
        title = 'Sales Invoice Transaction'
        table = get_sales_invoice_id()        
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 3:
        title = 'Cash Sales Transaction'
        table = get_sales_invoice_id()
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 4:
        title = 'Sales Return Transaction'
        table = get_sales_invoice_id()
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 5:
        print('5'), request.args(0), request.args(1)
    elif int(request.args(0)) == 6:        
        title = 'Purchase Return/Stock Adjustment Minus(-) Transaction'
        table = get_adjustment_minus()
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 7:   
        title = 'Stock Adjustment Plus(+) Transaction'     
        table = get_adjustment_plus()
        table += get_gl_entry_ref()
    elif int(request.args(0)) == 9:
        title = 'Obsolescence Transaction'     
        table = get_obsolescence_id()
        table += get_gl_entry_ref()
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'%s','message':'%s'}).show();" %(title, table)    

def get_purchase_receipt_id():    
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    table = TABLE(
        TR(TD('Transaction Date'),TD('Voucher No.'),TD('Voucher No. Ref.'),TD('Account'),TD('Order Account'),TD('Department'),TD('Location'),TD('Transaction Type')),
        TR(TD(_id.transaction_date),TD(_id.voucher_no),TD(_id.voucher_no_reference),TD(_id.account),TD(_id.order_account),TD(_id.dept_code),TD(_id.location),TD(_id.transaction_type))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Supplier Ref. Order'),TD('Supplier Invoice No'),TD('Customer Return Ref.'),TD('Trade Terms'),TD('Stock Destination'),TD('Sales Man'),TD('Sales Man on Behalf')),
        TR(TD(_id.supplier_reference_order),TD(_id.supplier_invoice),TD(_id.customer_return_reference),TD(_id.trade_terms_id),TD(_id.stock_destination),TD(_id.sales_man_code),TD(_id.sales_man_on_behalf))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Exchange Rate'),TD('Landed Cost'),TD('Custom Duty Charges'),TD('Other Charges')),
        TR(TD(locale.format('%.3F',_id.exchange_rate or 0, grouping = True)),TD(locale.format('%.3F',_id.landed_cost or 0, grouping = True)),TD(locale.format('%.3F',_id.custom_duty_charges or 0, grouping = True)),TD(locale.format('%.3F', _id.other_charges or 0, grouping = True)))
    ,_class='table table-bordered table-condensed')
    return table
def get_gl_entry_ref():
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    gl_entry_ref = TABLE(TR(
        TD('Header GL Entry Ref '),TD(' : '),TD(_id.gl_entry_ref)))
    return gl_entry_ref


def get_purchase_receipt_transaction_id():
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    row = []
    ctr = _grand_total = _net_amount = _selective_tax = 0
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('UOM'),TD('Category'),TD('Quantity'),TD('Average Cost'),TD('Sel.Tax.'),TD('Wholesale'),TD('Supplier Price (FC)'),TD('Discount %'),TD('Net Price'),TD('Total Amount'),TD('Reff.')),_class='bg-red')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.delete == False)).select():
        ctr += 1                
        _unit_price = float(n.price_cost_pcs or 0)  * int(n.uom)
        _net_price = (float(_unit_price or 0)  * (100 - float(n.discount or 0))) / 100
        _total_amount = float(n.price_cost_pcs or 0)  * int(n.quantity)
        _i = dc(dc.Item_Master.item_code == n.item_code).select().first()
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_i.item_description),   
            TD(n.uom),
            TD(n.category_id),
            TD(card(n.quantity, n.uom),_align ='right'),
            TD(locale.format('%.3F', n.average_cost or 0, grouping = True), _align = 'right'),    
            TD(locale.format('%.3F', n.selective_tax_price or 0, grouping = True), _align = 'right'),  
            TD(locale.format('%.3F', n.wholesale_price or 0, grouping = True), _align = 'right'),  
            TD(locale.format('%.3F', _unit_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.2F', n.discount or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.3F', _net_price or 0, grouping = True), _align = 'right'),
            TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right'),
            TD(n.gl_entry_ref)))
        
        _grand_total += n.price_cost_pcs  * n.quantity
    _purchase_value = _id.total_amount * _id.landed_cost 
    _others = PRE(
        TABLE(
            TR(TD('Exchange Rate'),TD(':'),TD(locale.format('%.3F',_id.exchange_rate or 0, grouping = True), _align = 'right')),
            TR(TD('Lnd Cost Rate'),TD(':'),TD(locale.format('%.3F',_id.landed_cost or 0, grouping = True), _align = 'right')),
            TR(TD('Custom Duty Ch.'),TD(':'),TD('  QR ', locale.format('%.3F',_id.custom_duty_charges or 0, grouping = True), _align = 'right')),
            TR(TD('Selective Tax'),TD(':'),TD('  QR ',locale.format('%.3F',_id.total_selective_tax or 0, grouping = True), _align = 'right')),
            TR(TD('Purchase Value'),TD(':'),TD('  QR ',locale.format('%.3F',_purchase_value or 0, grouping = True), _align = 'right')),            
            ))
    _net_amount = (float(_id.total_amount or 0) - float(_id.discount_added)) + float(_id.other_charges or 0)
    _net_amount_qr = float(_net_amount or 0) * float(_id.exchange_rate or 0)
    foot = TFOOT(
        TR(TD(_others,_colspan = '11',_rowspan='5'),TD('Total Amount: ',_align ='right'),TD(locale.format('%.3F',_id.total_amount or 0, grouping = True), _align = 'right')),
        TR(TD('Added Discount Amount',_align ='right'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Other Charges',_align ='right'),TD(locale.format('%.3F',_id.other_charges or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount',_align ='right'),TD(locale.format('%.3F',_net_amount or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount (QR)',_align ='right'),TD(locale.format('%.3F',_net_amount_qr or 0, grouping = True), _align = 'right')),
        
        )
    # foot += TFOOT(
    #     TR(TD('Header GL Entry Ref'),TD(':'),TD(_id.gl_entry_ref)),
    # )
    body = TBODY(*row)
    table = TABLE(*[head, body, foot], _class='table table-bordered table-condensed table-hover')
    return table

def get_sales_invoice_id():
    _total_selective_tax = _total_selective_tax_foc = ''
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    table = TABLE(
        TR(TD('Transaction Date'),TD('Voucher No.'),TD('POS/Voucher No.'),TD('Voucher No. Ref.'),TD('Account'),TD('Order Account'),TD('Department'),TD('Location'),TD('Transaction Type')),
        TR(TD(_id.transaction_date),TD(_id.voucher_no),TD(_id.voucher_no2),TD(_id.voucher_no_reference),TD(_id.account),TD(_id.order_account),TD(_id.dept_code),TD(_id.location),TD(_id.transaction_type))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Supplier Ref. Order'),TD('Supplier Invoice No'),TD('Customer Return Ref.'),TD('Trade Terms'),TD('Stock Destination'),TD('Sales Man'),TD('Sales Man on Behalf')),
        TR(TD(_id.supplier_reference_order),TD(_id.supplier_invoice),TD(_id.customer_return_reference),TD(_id.trade_terms_id),TD(_id.stock_destination),TD(_id.sales_man_code),TD(_id.sales_man_on_behalf))
    ,_class='table table-bordered table-condensed')
    ctr = _delivery_charges = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('UOM'),TD('Category'),TD('Supp.Code'),TD('Quantity'),TD('Average Cost'),TD('SEL.Tax'),TD('Wholesale'),TD('Price/Sel.Tax'),TD('Discount %'),TD('Net Price'),TD('Total Amount'),TD('Reff.')),_class='bg-red')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.delete == False)).select():
        ctr += 1                
        _unit_price = float(n.price_cost_pcs or 0)  * int(n.uom) + float(n.selective_tax_price or 0)
        _net_price = (float(_unit_price or 0)  * (100 - float(n.discount or 0))) / 100 
        _net_price = locale.format('%.3F', _net_price or 0, grouping = True)
        _total_amount = float(_net_price or 0) / n.uom * int(n.quantity) 
        _i = dc(dc.Item_Master.item_code == n.item_code).select().first()
        if n.category_id == 'P':
            _net_price = 'FOC-Price'
            _total_amount = 0.0
        
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_i.item_description),   
            TD(n.uom),
            TD(n.category_id),            
            TD(_i.supplier_code_id.supp_sub_code),
            TD(card(n.quantity, n.uom),_align ='right'),
            TD(locale.format('%.3F', n.average_cost or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.selective_tax_price or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.wholesale_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', _unit_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', n.discount or 0, grouping = True), _align = 'right'),
            TD(_net_price, _align = 'right'),
            TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right'),
            TD(n.gl_entry_ref)))
    
    if _id.total_selective_tax > 0.0:
        _total_selective_tax = 'Total Selective Tax: ' + str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
    if _id.total_selective_tax_foc > 0.0:
        _total_selective_tax_foc = 'Total Selective Tax FOC: ' + str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _tax_remarks = PRE(_total_selective_tax + '\n' + ' ' + _total_selective_tax_foc)
    _delivery_charges = _id.delivery_charges or 0 + _id.total_amount_after_discount or 0
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='11',_rowspan='4'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _id.total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Delivery Charges:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.delivery_charges or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_delivery_charges or 0, grouping = True), _align = 'right')))                                

    table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed table-hover')
    return table

def get_adjustment_minus():
    _total_selective_tax = _total_selective_tax_foc = ''
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    table = TABLE(
        TR(TD('Transaction Date'),TD('Voucher No.'),TD('POS/Voucher No.'),TD('Voucher No. Ref.'),TD('Account'),TD('Order Account'),TD('Department'),TD('Location'),TD('Transaction Type')),
        TR(TD(_id.transaction_date),TD(_id.voucher_no),TD(_id.voucher_no2),TD(_id.voucher_no_reference),TD(_id.account),TD(_id.order_account),TD(_id.dept_code),TD(_id.location),TD(_id.transaction_type))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Supplier Ref. Order'),TD('Supplier Invoice No'),TD('Customer Return Ref.'),TD('Trade Terms'),TD('Stock Destination'),TD('Sales Man'),TD('Sales Man on Behalf')),
        TR(TD(_id.supplier_reference_order),TD(_id.supplier_invoice),TD(_id.customer_return_reference),TD(_id.trade_terms_id),TD(_id.stock_destination),TD(_id.sales_man_code),TD(_id.sales_man_on_behalf))
    ,_class='table table-bordered table-condensed')
    ctr = _delivery_charges = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('UOM'),TD('Category'),TD('Supp.Code'),TD('Quantity'),TD('Average Cost'),TD('SEL.Tax'),TD('Wholesale'),TD('Price/Sel.Tax'),TD('Discount %'),TD('Net Price'),TD('Total Amount'),TD('Reff.')),_class='bg-red')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.delete == False)).select():
        ctr += 1                
        _unit_price = float(n.price_cost_pcs or 0)  * int(n.uom) + float(n.selective_tax_price or 0)
        _net_price = (float(_unit_price or 0)  * (100 - float(n.discount or 0))) / 100         
        _total_amount = float(_net_price or 0) / n.uom * int(n.quantity or 0) 
        _net_price = locale.format('%.3F', _net_price or 0, grouping = True)
        _i = dc(dc.Item_Master.item_code == n.item_code).select().first()
        if n.category_id == 'P':
            _net_price = 'FOC-Price'
            _total_amount = 0.0
        
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_i.item_description),   
            TD(n.uom),
            TD(n.category_id),            
            TD(_i.supplier_code_id.supp_sub_code),
            TD(card(n.quantity, n.uom),_align ='right'),
            TD(locale.format('%.3F', n.average_cost or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.selective_tax_price or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.wholesale_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', _unit_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', n.discount or 0, grouping = True), _align = 'right'),
            TD(_net_price, _align = 'right'),
            TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right'),
            TD(n.gl_entry_ref)))
    
    if _id.total_selective_tax > 0.0:
        _total_selective_tax = 'Total Selective Tax: ' + str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
    if _id.total_selective_tax_foc > 0.0:
        _total_selective_tax_foc = 'Total Selective Tax FOC: ' + str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _tax_remarks = PRE(_total_selective_tax + '\n' + ' ' + _total_selective_tax_foc)
    _delivery_charges = _id.delivery_charges or 0 + _id.total_amount_after_discount or 0
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='11',_rowspan='4'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _id.total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Delivery Charges:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.delivery_charges or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_delivery_charges or 0, grouping = True), _align = 'right')))                                

    table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed table-hover')
    return table

def get_adjustment_plus():
    _total_selective_tax = _total_selective_tax_foc = ''
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    table = TABLE(
        TR(TD('Transaction Date'),TD('Voucher No.'),TD('POS/Voucher No.'),TD('Voucher No. Ref.'),TD('Account'),TD('Order Account'),TD('Department'),TD('Location'),TD('Transaction Type')),
        TR(TD(_id.transaction_date),TD(_id.voucher_no),TD(_id.voucher_no2),TD(_id.voucher_no_reference),TD(_id.account),TD(_id.order_account),TD(_id.dept_code),TD(_id.location),TD(_id.transaction_type))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Supplier Ref. Order'),TD('Supplier Invoice No'),TD('Customer Return Ref.'),TD('Trade Terms'),TD('Stock Destination'),TD('Sales Man'),TD('Sales Man on Behalf')),
        TR(TD(_id.supplier_reference_order),TD(_id.supplier_invoice),TD(_id.customer_return_reference),TD(_id.trade_terms_id),TD(_id.stock_destination),TD(_id.sales_man_code),TD(_id.sales_man_on_behalf))
    ,_class='table table-bordered table-condensed')
    ctr = _delivery_charges = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('UOM'),TD('Category'),TD('Supp.Code'),TD('Quantity'),TD('Average Cost'),TD('SEL.Tax'),TD('Wholesale'),TD('Price/Sel.Tax'),TD('Discount %'),TD('Net Price'),TD('Total Amount'),TD('Reff.')),_class='bg-red')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.delete == False)).select():
        ctr += 1                
        _unit_price = float(n.price_cost_pcs or 0)  * int(n.uom) + float(n.selective_tax_price or 0)
        _net_price = (float(_unit_price or 0)  * (100 - float(n.discount or 0))) / 100         
        _total_amount = float(_net_price or 0) / n.uom * int(n.quantity or 0) 
        _net_price = locale.format('%.3F', _net_price or 0, grouping = True)
        _i = dc(dc.Item_Master.item_code == n.item_code).select().first()
        if n.category_id == 'P':
            _net_price = 'FOC-Price'
            _total_amount = 0.0
        
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_i.item_description),   
            TD(n.uom),
            TD(n.category_id),            
            TD(_i.supplier_code_id.supp_sub_code),
            TD(card(n.quantity, n.uom),_align ='right'),
            TD(locale.format('%.3F', n.average_cost or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.selective_tax_price or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.wholesale_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', _unit_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', n.discount or 0, grouping = True), _align = 'right'),
            TD(_net_price, _align = 'right'),
            TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right'),
            TD(n.gl_entry_ref)))
    
    if _id.total_selective_tax > 0.0:
        _total_selective_tax = 'Total Selective Tax: ' + str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
    if _id.total_selective_tax_foc > 0.0:
        _total_selective_tax_foc = 'Total Selective Tax FOC: ' + str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _tax_remarks = PRE(_total_selective_tax + '\n' + ' ' + _total_selective_tax_foc)
    _delivery_charges = _id.delivery_charges or 0 + _id.total_amount_after_discount or 0
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='11',_rowspan='4'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _id.total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Delivery Charges:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.delivery_charges or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_delivery_charges or 0, grouping = True), _align = 'right')))                                

    table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed table-hover')
    return table

def get_obsolescence_id():
    _total_selective_tax = _total_selective_tax_foc = ''
    _id = dc(dc.Merch_Stock_Header.id == request.args(1)).select().first()
    table = TABLE(
        TR(TD('Transaction Date'),TD('Voucher No.'),TD('POS/Voucher No.'),TD('Voucher No. Ref.'),TD('Account'),TD('Order Account'),TD('Department'),TD('Location'),TD('Transaction Type')),
        TR(TD(_id.transaction_date),TD(_id.voucher_no),TD(_id.voucher_no2),TD(_id.voucher_no_reference),TD(_id.account),TD(_id.order_account),TD(_id.dept_code),TD(_id.location),TD(_id.transaction_type))
    ,_class='table table-bordered table-condensed')

    table += TABLE(
        TR(TD('Supplier Ref. Order'),TD('Supplier Invoice No'),TD('Customer Return Ref.'),TD('Trade Terms'),TD('Stock Destination'),TD('Sales Man'),TD('Sales Man on Behalf')),
        TR(TD(_id.supplier_reference_order),TD(_id.supplier_invoice),TD(_id.customer_return_reference),TD(_id.trade_terms_id),TD(_id.stock_destination),TD(_id.sales_man_code),TD(_id.sales_man_on_behalf))
    ,_class='table table-bordered table-condensed')
    ctr = _delivery_charges = 0
    row = []
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Description'),TD('UOM'),TD('Category'),TD('Supp.Code'),TD('Quantity'),TD('Average Cost'),TD('SEL.Tax'),TD('Wholesale'),TD('Price/Sel.Tax'),TD('Discount %'),TD('Net Price'),TD('Total Amount'),TD('Reff.')),_class='bg-red')
    for n in dc((dc.Merch_Stock_Transaction.merch_stock_header_id == request.args(1)) & (dc.Merch_Stock_Transaction.delete == False)).select():
        ctr += 1                
        _unit_price = float(n.price_cost_pcs or 0)  * int(n.uom) + float(n.selective_tax_price or 0)
        _net_price = (float(_unit_price or 0)  * (100 - float(n.discount or 0))) / 100         
        _total_amount = float(_net_price or 0) / n.uom * int(n.quantity or 0) 
        _net_price = locale.format('%.3F', _net_price or 0, grouping = True)
        _i = dc(dc.Item_Master.item_code == n.item_code).select().first()
        if n.category_id == 'P':
            _net_price = 'FOC-Price'
            _total_amount = 0.0
        
        row.append(TR(
            TD(ctr),
            TD(n.item_code),
            TD(_i.item_description),   
            TD(n.uom),
            TD(n.category_id),            
            TD(_i.supplier_code_id.supp_sub_code),
            TD(card(n.quantity, n.uom),_align ='right'),
            TD(locale.format('%.3F', n.average_cost or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.selective_tax_price or 0, grouping = True), _align = 'right'),     
            TD(locale.format('%.3F', n.wholesale_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', _unit_price or 0, grouping = True), _align = 'right'),            
            TD(locale.format('%.3F', n.discount or 0, grouping = True), _align = 'right'),
            TD(_net_price, _align = 'right'),
            TD(locale.format('%.3F', _total_amount or 0, grouping = True), _align = 'right'),
            TD(n.gl_entry_ref)))
    
    if _id.total_selective_tax > 0.0:
        _total_selective_tax = 'Total Selective Tax: ' + str(locale.format('%.2F',_id.total_selective_tax or 0, grouping = True))
    if _id.total_selective_tax_foc > 0.0:
        _total_selective_tax_foc = 'Total Selective Tax FOC: ' + str(locale.format('%.2F',_id.total_selective_tax_foc or 0, grouping = True))
    _tax_remarks = PRE(_total_selective_tax + '\n' + ' ' + _total_selective_tax_foc)
    _delivery_charges = _id.delivery_charges or 0 + _id.total_amount_after_discount or 0
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD(_tax_remarks,_colspan='11',_rowspan='4'),TD('Total Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F', _id.total_amount or 0, grouping = True), _align = 'right')),    
        TR(TD('Added Discount Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.discount_added or 0, grouping = True), _align = 'right')),
        TR(TD('Delivery Charges:',_align='right',_colspan='2'),TD(locale.format('%.3F',_id.delivery_charges or 0, grouping = True), _align = 'right')),
        TR(TD('Net Amount:',_align='right',_colspan='2'),TD(locale.format('%.3F',_delivery_charges or 0, grouping = True), _align = 'right')))                                

    table += TABLE(*[head, body, foot], _class='table table-bordered table-condensed table-hover')
    return table

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

@auth.requires_login()
def card(quantity, uom_value):
    if uom_value == 1:
        return quantity
    else:
        return str(int(quantity) / int(uom_value)) + ' - ' + str(int(quantity) - int(quantity) / int(uom_value) * int(uom_value))  + '/' + str(int(uom_value))        

def get_direct_purchase_receipt_view_id():
    _id = dc(dc.Direct_Purchase_Receipt.purchase_receipt_no == request.args(0)).select().first()
    if _id.purchase_receipt_no_prefix_id == None:
        _purchase_receipt_no = _purchase_receipt_date = ''
    else:
        _purchase_receipt_no = _id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no
        _purchase_receipt_date = _id.purchase_receipt_date
    table = TABLE(
        TR(TD('Purchase Receipt No'),TD('Purchase Receipt Date'),TD('Purchase Order No'),TD('Transaction No'),TD('Transaction Date')),
        TR(TD(_purchase_receipt_no),TD(_purchase_receipt_date),TD(_id.purchase_order_no),TD(_id.transaction_no),TD(_id.transaction_date)),_class='table table-bordered table-condensed')
    table += TABLE(
        TR(TD('Department'),TD('Location'),TD('Supplier Ref Order'),TD('Trade Terms'),TD('Mode of Shipment'),TD('Supplier Account Code'),TD('Supplier Account Description'),TD('Status')),
        TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),
        TD(_id.location_code_id.location_code,' - ',_id.location_code_id.location_name),
        TD(_id.supplier_reference_order),        
        TD(_id.trade_terms_id.trade_terms),
        TD(_id.mode_of_shipment),
        TD(_id.supplier_account_code),
        TD(_id.supplier_account_code_description),
        TD(_id.status_id.description)),_class='table table-bordered table-condensed')
    table += TABLE(
        TR(TD('Currency'),TD('Exchange Rate'),TD('Landed Cost (QR)'),TD('Custom Duty Charge (QR)'),TD('Selective Tax (QR)'),TD('Other Charges (FC)')),
        TR(
            TD(_id.currency_id.mnemonic),
            TD(locale.format('%.4F',_id.exchange_rate or 0, grouping = True)),
            TD(locale.format('%.4F',_id.landed_cost or 0, grouping = True)),
            TD(locale.format('%.4F',_id.custom_duty_charges or 0, grouping = True)),
            TD(locale.format('%.4F',_id.selective_tax or 0, grouping = True)),
            TD(locale.format('%.4F',_id.other_charges or 0, grouping = True))),
            _class='table table-bordered table-condensed')
    table += get_direct_purchase_receipt_transaction_id()
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Direct Purchase Receipt','message':'%s'}).show();" %(XML(table, sanitize = True))    

def get_direct_purchase_receipt_transaction_id():
    _id = dc(dc.Direct_Purchase_Receipt.purchase_receipt_no == request.args(0)).select().first()
    ctr = _total_amount = _net_amount = _net_amount_qr = _purchase_value_qr = 0
    row = []
    head = THEAD(TR(TH('#'),TH('Item Code'),TH('Item Description'),TH('UOM'),TH('Category'),TH('Quantity'),TH('Supplier Price (FC)'),TH('Discount %'),TH('Net Price'),TH('Total Amount'),_class='bg-primary'))
    for n in dc((dc.Direct_Purchase_Receipt_Transaction.purchase_receipt_no_id == _id.id) & (dc.Direct_Purchase_Receipt_Transaction.delete == False)).select(orderby = dc.Direct_Purchase_Receipt_Transaction.id):
        ctr += 1
        _total_amount += n.total_amount
        _net_amount = float(_total_amount or 0) - float(_id.added_discount_amount or 0) + float(_id.other_charges)
        _net_amount_qr = float(_net_amount or 0) * float(_id.exchange_rate or 0)
        _purchase_value_qr = float(_total_amount or 0)  * float(_id.landed_cost or 0)
        # _purchase_value_qr = (float(_total_amount or 0) - float(_id.other_charges or 0)) * float(_id.landed_cost or 0)
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),
            TD(card(n.quantity, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right')))
    body = TBODY(*row)
    foot = TFOOT(
        TR(TD(_colspan = '8', _rowspan='5'),TD('Total Amount:',_align = 'right'),TD(locale.format('%.3F',_total_amount or 0, grouping = True),_align='right')),
        TR(TD('Added Discount Amount:',_align = 'right'),TD(locale.format('%.3F',_id.added_discount_amount or 0, grouping = True),_align='right')),
        TR(TD('Net Amount:',_align = 'right'),TD(locale.format('%.3F',_net_amount or 0, grouping = True),_align='right')),
        TR(TD('Net Amount (QR):',_align = 'right'),TD(locale.format('%.3F',_net_amount_qr or 0, grouping = True),_align='right')),
        TR(TD('Purchase Value (QR):',_align = 'right'),TD(locale.format('%.3F',_purchase_value_qr or 0, grouping = True),_align='right')))
    table = TABLE(*[head, body, foot],_class='table table-hover table-bordered table-condensed')
    table += TABLE(TR(TD('Remarks:'),TD(_id.remarks)))
    return table

def get_purchase_receipt_view_id(): # audited
    _id = dc(dc.Purchase_Receipt.purchase_receipt_no == request.args(0)).select().first()
    if _id.purchase_receipt_no_prefix_id:
        _purchase_receipt = _id.purchase_receipt_no_prefix_id.prefix,_id.purchase_receipt_no
        _purchase_receipt_date = _id.purchase_receipt_date
    else:
        _purchase_receipt = _purchase_receipt_date = ''

    if _id.purchase_order_no_prefix_id:        
        _purchase_order = _id.purchase_order_no_prefix_id.prefix,_id.purchase_order_no
        _purchase_date = _id.purchase_order_date
    else:        
        _purchase_order = _purchase_date = ''
    table = TABLE(TR(TD('Purchase Request Date'),TD('Purchase Request No.'),TD('Purchase Order Date'),TD('Purchase Order No.'),TD('Purchase Receipt Date'),TD('Purchase Receipt No.')),
        TR(TD(_id.purchase_request_date),TD(_id.purchase_request_no_prefix_id.prefix,_id.purchase_request_no),TD(_purchase_date),TD(_purchase_order),TD(_purchase_receipt_date),TD(_purchase_receipt)),_class='table table-bordered table-condensed')
    table += TABLE(TR(TD('Department'),TD('Supplier Name'),TD('Mode Of Shipment'),TD('Trade Terms'),TD('Location'),TD('Supplier Proforma Invoice'),TD('Currency'),TD('ETA'),TD('Status')),
        TR(TD(_id.dept_code_id.dept_code,' - ',_id.dept_code_id.dept_name),TD(_id.supplier_code_id.supp_code, ' - ', _id.supplier_code_id.supp_name,', ', SPAN(_id.supplier_code_id.supp_sub_code,_class='text-muted')),TD(_id.mode_of_shipment),TD(_id.trade_terms_id.trade_terms),TD(_id.location_code_id.location_code,' - ',_id.location_code_id.location_name),TD(_id.supplier_reference_order),TD(_id.currency_id.mnemonic,' ', _id.exchange_rate),TD(_id.estimated_time_of_arrival),TD(_id.status_id.description)),_class='table table-bordered table-condensed')
    row = []
    ctr = _total_amount = _net_amount_fr = _net_amount_qr =  0
    head = THEAD(TR(TD('#'),TD('Item Code'),TD('Item Description'),TD('UOM'),TD('Category'),TD('Qty.'),TD('Unit Price'),TD('Discount %'),TD('Net Price'),TD('Total Amount')),_class='bg-primary')
    for n in dc((dc.Purchase_Receipt_Transaction.purchase_receipt_no_id == _id.id) & (dc.Purchase_Receipt_Transaction.delete == False)).select():        
        
        ctr += 1
        row.append(TR(
            TD(ctr),
            TD(n.item_code_id.item_code),
            TD(n.item_code_id.item_description),
            TD(n.uom),
            TD(n.category_id.mnemonic),
            TD(card(n.quantity_invoiced, n.uom)),
            TD(locale.format('%.3F',n.price_cost or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.discount_percentage or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.net_price or 0, grouping = True),_align='right'),
            TD(locale.format('%.3F',n.total_amount or 0, grouping = True),_align='right')))
        _total_amount += n.total_amount
    _net_amount_fr = float(_total_amount or 0)  - float(_id.added_discount_amount or 0)
    _net_amount_qr = float(_net_amount_fr or 0) * float(_id.exchange_rate or 0)
    body = TBODY(*row)    
    foot = TFOOT(TR(TD(_colspan='8',_rowspan='4'),TD('Total Amount: ',_align = 'right'),TD(_id.currency_id.mnemonic, ' ', locale.format('%.3F',_total_amount or 0, grouping = True), _align = 'right')),
    TR(TD('Added Discount Amount: ',_align = 'right'),TD(locale.format('%.3F',_id.added_discount_amount or 0, grouping = True), _align = 'right')),
    TR(TD('Net Amount: ',_align = 'right'),TD(_id.currency_id.mnemonic, ' ',locale.format('%.3F',_net_amount_fr or 0, grouping = True), _align = 'right')),
    TR(TD('Net Amount (QR): ',_align = 'right'),TD(B(locale.format('%.3F',_net_amount_qr or 0, grouping = True)), _align = 'right')))
    table += TABLE(*[head, body, foot], _class='table table-bordered table-hover table-condensed')
    table += TABLE(TR(TD('Remarks: ', _id.remarks)))
    response.js = "alertify.alert().set({'startMaximized':true, 'title':'Purchase Receipt','message':'%s'}).show();" %(XML(table, sanitize = True))    

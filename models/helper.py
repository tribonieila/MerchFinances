def id_generator():    
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def calculate_master_account(trnx_no):    # from gl account posting
    for x in db(db.General_Ledger.transaction_no == trnx_no).select():
        _cy = db((db.Master_Account_Balance_Current_Year.account_code == x.account_code) & (db.Master_Account_Balance_Current_Year.financial_year.year() == x.transaction_date.year)).select().first()
        _ma = dc(dc.Master_Account.account_code == x.account_code).select().first()
        if _cy: # update if exist
            if int(x.department) == 1:
                _cy.closing_balance_1 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 2:
                _cy.closing_balance_2 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 3:                
                _cy.closing_balance_3 += x.debit or 0 - x.credit or 0                        
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 4:
                _cy.closing_balance_4 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 5:
                _cy.closing_balance_5 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 6:
                _cy.closing_balance_6 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 7:
                _cy.closing_balance_7 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            elif int(x.department) == 99:
                _cy.closing_balance_99 += x.debit or 0 - x.credit or 0
                _cy.total_closing_balance += x.debit or 0 - x.credit or 0
            _cy.update_record()             
        elif not _cy: # otherwise insert 
            _bal = float(x.debit or 0) - float(x.credit or 0)
            if int(x.department) == 1:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_1 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 2:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_2 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 3:                
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_3 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 4:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_4 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 5:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_5 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 6:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_6 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 7:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_7 = float(_bal or 0),total_closing_balance = float(_bal or 0))
            elif int(x.department) == 99:
                db.Master_Account_Balance_Current_Year.insert(financial_year = x.transaction_date,account_code = x.account_code, account_name = _ma.account_name,closing_balance_99 = float(_bal or 0),total_closing_balance = float(_bal or 0))            

def total_closing_balance(year, acc):
    try:
        _total_closing_balance = 0
        _id = db((db.Master_Account_Balance_Current_Year.account_code == acc) & (db.Master_Account_Balance_Current_Year.financial_year.year() == year)).select().first()
        _total_closing_balance = float(_id.total_closing_balance or 0)
        if int(year) != int(request.now.year):
            _id = db((db.Master_Account_Balance.account_code == acc) & (db.Master_Account_Balance.financial_year.year() == year)).select().first()        
            _total_closing_balance = float(_id.total_closing_balance or 0)        
        return _total_closing_balance
    except:
        response.js = "alertify.error('Ops! Total Closing Balance. Something went wrong.')"

def total_opening_balance(year, acc):
    try:
        _total_opening_balance = 0
        _id = db((db.Master_Account_Balance_Current_Year.account_code == acc) & (db.Master_Account_Balance_Current_Year.financial_year.year() == year)).select().first()
        _total_opening_balance = float(_id.total_opening_balance or 0)
        if int(year) != int(request.now.year):
            _id = db((db.Master_Account_Balance.account_code == acc) & (db.Master_Account_Balance.financial_year.year() == year)).select().first()        
            _total_opening_balance = float(_id.total_opening_balance or 0)        
        return _total_opening_balance
    except:
        response.js = "alertify.error('Ops! Total Opening Balance. Something went wrong.')"

def total_credit_terms(acc):
    return total_terms

def total_credit_limit(acc):
    return total_limit

def closing_balance(year, acc, dep):        
    try:
        _closing_balance = 0
        _id = db(db.Master_Account_Balance_Current_Year.account_code == acc).select().first()
        if int(year) != int(request.now.year):            
            _id = db((db.Master_Account_Balance.financial_year.year() == year) & (db.Master_Account_Balance.account_code == acc)).select().first()
        if _id:
            if int(dep or 0) == 1:
                _closing_balance = _id.closing_balance_1
            elif int(dep or 0) == 2:
                _closing_balance = _id.closing_balance_2
            elif int(dep or 0) == 3:
                _closing_balance = _id.closing_balance_3
            elif int(dep or 0) == 4:
                _closing_balance = _id.closing_balance_4
            elif int(dep or 0) == 5:
                _closing_balance = _id.closing_balance_5
            elif int(dep or 0) == 6:
                _closing_balance = _id.closing_balance_6
            elif int(dep or 0) == 9:
                _closing_balance = _id.closing_balance_9        
            elif int(dep or 0) == 99:
                _closing_balance = _id.closing_balance_99
        return _closing_balance
    except:
        response.js = "alertify.error('Ops! Closing Balance. Something went wrong.')"
        
def opening_balance(year, acc, dep):
    try:
        _opening_balance = 0
        _id = db(db.Master_Account_Balance_Current_Year.account_code == acc).select().first()
        if int(year) != int(request.now.year):            
            _id = db((db.Master_Account_Balance.financial_year.year() == year) & (db.Master_Account_Balance.account_code == acc)).select().first()            
        if _id:
            if int(dep or 0) == 1:
                _opening_balance = _id.opening_balance_1
            elif int(dep or 0) == 2:
                _opening_balance = _id.opening_balance_2
            elif int(dep or 0) == 3:
                _opening_balance = _id.opening_balance_3
            elif int(dep or 0) == 4:
                _opening_balance = _id.opening_balance_4
            elif int(dep or 0) == 5:
                _opening_balance = _id.opening_balance_5
            elif int(dep or 0) == 6:
                _opening_balance = _id.opening_balance_6
            elif int(dep or 0) == 9:
                _opening_balance = _id.opening_balance_9
            elif int(dep or 0) == 99:
                _opening_balance = _id.opening_balance_99        
            return _opening_balance
    except:
        response.js = "alertify.error('Ops! Opening Balance. Something went wrong.')"

def credit_terms(year, acc, dep):
    _credit_terms = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()    
    if int(dep or 0) == 1:
        _credit_terms = _id.credit_terms_1
    elif int(dep or 0) == 2:
        _credit_terms = _id.credit_terms_2
    elif int(dep or 0) == 3:
        _credit_terms = _id.credit_terms_3
    elif int(dep or 0) == 4:
        _credit_terms = _id.credit_terms_4
    elif int(dep or 0) == 5:
        _credit_terms = _id.credit_terms_5
    elif int(dep or 0) == 6:
        _credit_terms = _id.credit_terms_6
    elif int(dep or 0) == 9:
        _credit_terms = _id.credit_terms_9        
    return _credit_terms

def credit_limit(year, acc, dep):
    _credit_limit = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()    
    if int(dep or 0) == 1:
        _credit_limit = _id.credit_limit_1
    elif int(dep or 0) == 2:
        _credit_limit = _id.credit_limit_2
    elif int(dep or 0) == 3:
        _credit_limit = _id.credit_limit_3
    elif int(dep or 0) == 4:
        _credit_limit = _id.credit_limit_4
    elif int(dep or 0) == 5:
        _credit_limit = _id.credit_limit_5
    elif int(dep or 0) == 6:
        _credit_limit = _id.credit_limit_6
    elif int(dep or 0) == 9:
        _credit_limit = _id.credit_limit_9        
    return _credit_limit
    # _credit_balance = 'dc.Master_Account' + '.' + 'credit_balance_' + str(session.dept_code_id)
    # _ma = dc((dc.Master_Account.account_code == session.account_code) & (_credit_balance == _credit_balance)).select().first()     
def total_credit_balance(acc):
    total_balance = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()   
    if _id: 
        total_balance = float(_id.credit_balance_1 or 0) + float(_id.credit_balance_2 or 0) + float(_id.credit_balance_3 or 0) + float(_id.credit_balance_4 or 0) + float(_id.credit_balance_5 or 0) + float(_id.credit_balance_6 or 0) + float(_id.credit_balance_9 or 0)
    return total_balance

def total_opening_balance(acc):
    total_balance = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()   
    if _id: 
        total_balance = float(_id.opening_balance_1 or 0) + float(_id.opening_balance_2 or 0) + float(_id.opening_balance_3 or 0) + float(_id.opening_balance_4 or 0) + float(_id.opening_balance_5 or 0) + float(_id.opening_balance_6 or 0) + float(_id.opening_balance_9 or 0)
    return total_balance

def total_credit_terms(acc):
    return total_terms

def total_credit_limit(acc):
    return total_limit

def credit_balance(acc, dep):        
    _credit_balance = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()    
    if int(dep or 0) == 1:
        _credit_balance = _id.credit_balance_1
    elif int(dep or 0) == 2:
        _credit_balance = _id.credit_balance_2
    elif int(dep or 0) == 3:
        _credit_balance = _id.credit_balance_3
    elif int(dep or 0) == 4:
        _credit_balance = _id.credit_balance_4
    elif int(dep or 0) == 5:
        _credit_balance = _id.credit_balance_5
    elif int(dep or 0) == 6:
        _credit_balance = _id.credit_balance_6
    elif int(dep or 0) == 9:
        _credit_balance = _id.credit_balance_9        
    return _credit_balance

def opening_balance(acc, dep):
    _opening_balance = 0
    _id = dc(dc.Master_Account.account_code == acc).select().first()    
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
    return _opening_balance

def credit_terms(acc, dep):
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

def credit_limit(acc, dep):
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
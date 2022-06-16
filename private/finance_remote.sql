
-- UPDATE [m3rch_finances_db].[dbo].[General_Ledger] SET [amount_paid] = 0, [rv_payment_reference] = Null, [paid] = 0, [reconciliation_transaction_no] = Null
-- UPDATE [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] SET [amount_paid] = 0, [reconciled_amount] = 0, [reconciled] = 0, [reconciliation_transaction_ref] = Null, [reconciliation_request] = 0
SELECT * FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] 
-- ajax("{{=URL('workflow_accounts_recon','delete_account_reconciliation_request_id', args = request.args(0))}}");
SELECT * FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction] WHERE [account_code] = '07-325-2'
-- SELECT * FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header] 
-- SELECT * FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction]  
-- SELECT * FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction] where [receipt_voucher_header_id] = 44
-- SELECT * FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Confirmation] ORDER BY [id]
-- SELECT * FROM [m3rch_finances_db].[dbo].[Master_Account_Balance_Current_Year] WHERE [account_code] = '02-06' ORDER BY [id]
-- UPDATE [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] SET [reconciliation_request] = 0
-- UPDATE [m3rch_finances_db].[dbo].[Payment_Voucher_Request] SET [status_id] = 12 WHERE [id] = 8

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction_Request]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header_Request]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Header_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Payment_Voucher_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Header]
-- DBCC CHECKIDENT ('[Payment_Voucher_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Transaction_Request]
-- DBCC CHECKIDENT ('[Payment_Voucher_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Request]
-- DBCC CHECKIDENT ('[Payment_Voucher_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Header]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Confirmation_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Confirmation_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Confirmation]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Confirmation]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Confirmation]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Confirmation]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Journal_Voucher_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Header_Request]
-- DBCC CHECKIDENT ('[Journal_Voucher_Header_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Transaction_Request]
-- DBCC CHECKIDENT ('[Journal_Voucher_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Header_Request]
-- DBCC CHECKIDENT ('[Journal_Voucher_Header_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Master_Account_Balance_Current_Year]
-- DBCC CHECKIDENT ('[Master_Account_Balance_Current_Year]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[General_Ledger]
-- DBCC CHECKIDENT ('[General_Ledger]', RESEED, 0);


-- 21300804
-- 22300574
-- UPDATE [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] SET [reconciliation_request] = 0
-- SELECT * FROM [m3rch_inv_db].[dbo].[Purchase_Receipt] WHERE [supplier_account_code] IS NULL


-- SELECT [id],[reconciled_amount],[amount_paid], [reconciled], [reconciliation_transaction_ref], [reconciliation_request] FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] WHERE [id] = 2
-- SELECT * FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction] ORDER BY [id] DESC

SELECT * FROM [m3rch_finances_db].[dbo].[General_Ledger] 
SELECT * FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] WHERE [id] = 2
SELECT * FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header] ORDER BY [id] DESC
SELECT * FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction] ORDER BY [id] 

-- UPDATE [m3rch_finances_db].[dbo].[General_Ledger] SET [amount_paid] = 0, [rv_payment_reference] = Null, [paid] = 0, [reconciliation_transaction_no] = Null
-- UPDATE [m3rch_finances_db].[dbo].[Receipt_Voucher_Header] SET [last_reconciled_amount] = 0, [reconciled_amount] = 0, [reconciled] = 0, [reconciliation_transaction_ref] = Null, [reconciliation_request] = 0

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction_Request]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header_Request]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Header_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Transaction]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Account_Reconciliation_Header]
-- DBCC CHECKIDENT ('[Account_Reconciliation_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Master_Account_Balance_Current_Year]
-- DBCC CHECKIDENT ('[Master_Account_Balance_Current_Year]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[General_Ledger]
-- DBCC CHECKIDENT ('[General_Ledger]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Confirmation_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Confirmation_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Confirmation]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Confirmation]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Header]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Transaction_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Receipt_Voucher_Request]
-- DBCC CHECKIDENT ('[Receipt_Voucher_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Transaction_Request]
-- DBCC CHECKIDENT ('[Journal_Voucher_Transaction_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Header_Request]
-- DBCC CHECKIDENT ('[Journal_Voucher_Header_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Journal_Voucher_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Journal_Voucher_Header]
-- DBCC CHECKIDENT ('[Journal_Voucher_Header]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Request]
-- DBCC CHECKIDENT ('[Payment_Voucher_Request]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Transaction]
-- DBCC CHECKIDENT ('[Payment_Voucher_Transaction]', RESEED, 0);

-- DELETE FROM [m3rch_finances_db].[dbo].[Payment_Voucher_Header]
-- DBCC CHECKIDENT ('[Payment_Voucher_Header]', RESEED, 0);


-- DELETE FROM [m3rch_finances_db].[dbo].[Cost_Center]
-- DBCC CHECKIDENT ('[Cost_Center]', RESEED, 0);



-- DROP TABLE [dbo].[Account_Reconciliation_Transaction_Request];
-- DROP TABLE [dbo].[Account_Reconciliation_Header_Request];
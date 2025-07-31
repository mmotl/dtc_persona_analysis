-- Docs: https://docs.mage.ai/guides/sql-blocks
select * from customer_features_test
where extract(month from date) = 3 --{{ current_month }}
-- Docs: https://docs.mage.ai/guides/sql-blocks
select * from customer_features
where extract(month from date) = 1;
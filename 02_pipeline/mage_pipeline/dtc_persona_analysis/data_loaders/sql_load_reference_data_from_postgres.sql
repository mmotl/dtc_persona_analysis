-- Docs: https://docs.mage.ai/guides/sql-blocks
select * from ing_test
where extract(month from date) = 1 --{{ reference_month }};
-- ============================================================
-- seed.sql
-- ------------------------------------------------------------
-- Demo data for ANPR Project (MySQL)
--
-- What this script does:
-- - Inserts a demo owner
-- - Inserts a demo vehicle mapped to that owner
--
-- Notes:
-- - Run this AFTER schema.sql
-- - You can add more owners/vehicles for testing
-- ============================================================

USE anpr_db;

-- ------------------------------------------------------------
-- 1) Insert demo owner
-- ------------------------------------------------------------
INSERT INTO owners (name, email, phone, address)
VALUES ('Demo Owner', 'demo.owner@email.com', '9999999999', 'Demo Address');

-- ------------------------------------------------------------
-- 2) Insert demo vehicle (mapped to the latest inserted owner)
-- ------------------------------------------------------------
INSERT INTO vehicles (plate_number, owner_id, vehicle_type)
VALUES ('22BH6517A', LAST_INSERT_ID(), 'Car');


-- 1. Upsert (insert или update)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;


-- 2. Массовая вставка с проверкой
CREATE OR REPLACE PROCEDURE insert_many_users(names TEXT[], phones TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        -- проверка телефона (только цифры и длина >= 10)
        IF phones[i] ~ '^[0-9]{10,}$' THEN
            CALL upsert_contact(names[i], phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: % for user: %', phones[i], names[i];
        END IF;

    END LOOP;
END;
$$;


-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value OR phone = p_value;
END;
$$;
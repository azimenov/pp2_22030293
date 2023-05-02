
CREATE PROCEDURE Insert_data(text, text)
LANGUAGE 'plpgsql'

AS $$

BEGIN

INSERT INTO public.phone_book("PersonName", "PhoneNumber") values ($1, $2);
COMMIT;

END;
$$;


CREATE PROCEDURE Update_data (
    IN ContactName TEXT,
    IN NewPhone TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS (SELECT * FROM public.phone_book WHERE "PersonName" = ContactName) THEN
  
        UPDATE public.phone_book SET "PhoneNumber" = NewPhone WHERE "PersonName" = ContactName;
        RAISE INFO 'Phone number updated for contact %', ContactName;
    ELSE
        RAISE EXCEPTION 'Contact % does not exist', ContactName;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_list_of_users(
  IN users TEXT[][]
)

LANGUAGE 'plpgsql'

AS $$

DECLARE
  i TEXT[];

BEGIN 

  Foreach i slice 1 in array users
  LOOP
    INSERT INTO public.phone_book ("PersonName", "PhoneNumber") VALUES (i[1], i[2]);
  END LOOP;

END;
$$;

CREATE OR REPLACE FUNCTION paginating(a integer, b integer)
RETURNS SETOF public.phone_book
AS $$
    SELECT * FROM public.phone_book 
  ORDER BY id
  LIMIT a OFFSET b;
$$
language sql;


CREATE OR REPLACE PROCEDURE delete_data_by_username_or_phone(
    IN delete_by text,
    IN delete_value text
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF delete_by = 'username' THEN
        DELETE FROM public.phone_book WHERE "PersonName" = delete_value;
    ELSIF delete_by = 'phone' THEN
        DELETE FROM public.phone_book WHERE "PhoneNumber" = delete_value;
    ELSE
        RAISE EXCEPTION 'Invalid delete_by parameter: %', delete_by;
    END IF;
END;
$$;
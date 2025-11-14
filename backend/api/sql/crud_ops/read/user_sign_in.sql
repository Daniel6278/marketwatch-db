SELECT user_id
FROM User
WHERE email = %(email_address)s AND password_hash = %(user_id)s;
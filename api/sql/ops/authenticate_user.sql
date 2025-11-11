SELECT EXISTS(
    SELECT username
    FROM User
    WHERE user_id = %(user_id)s AND password_hash = %(user_id)s
) AS 'user_exists'
FROM User;
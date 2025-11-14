def sql_code_return_wrapper(callback, return_sql_code: bool = False):
    response, sql_code = callback()
    return (response | {"sql": sql_code}) if return_sql_code else response

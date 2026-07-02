def is_safe_sql(sql):

    blocked = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    sql_upper = sql.upper()

    for word in blocked:
        if word in sql_upper:
            return False

    return True
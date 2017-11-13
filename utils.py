def insert_into_redis(conn, details):
    conn.set(details.get_city, 'hahah')
    print('task done buoyyzz')
    print('jilebi pakodi', conn.get(details.get_city))
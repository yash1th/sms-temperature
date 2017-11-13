def insert_into_redis(conn, details):
    conn.set(details.get_city, 'hahah')
    print('task done buoyyzz')
    print('jilebi pakodi', r.get(details.get_city))
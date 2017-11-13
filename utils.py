def insert_into_redis(details):
    r.set(details.get_city, 'hahah')
    print('task done buoyyzz')
    print('jilebi pakodi', r.get(details.get_city))
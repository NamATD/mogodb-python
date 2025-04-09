def get_latest_data(collection):
    latest_data = list(collection.find().sort("datetime", -1).limit(10))
    for item in latest_data:
        item['_id'] = str(item['_id'])
    return latest_data

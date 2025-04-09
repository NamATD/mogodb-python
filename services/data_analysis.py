from datetime import datetime, timedelta
from collections import defaultdict

def get_weekly_stats(collection):
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    cursor = collection.find({"datetime": {"$gte": one_week_ago}})

    hourly_stats = defaultdict(int)
    count_per_hour = defaultdict(int)

    for doc in cursor:
        hour = doc["datetime"].hour
        hourly_stats[hour] += doc["total_vehicles"]
        count_per_hour[hour] += 1

    result = []
    for hour in range(24):
        avg = 0
        if count_per_hour[hour] > 0:
            avg = hourly_stats[hour] / count_per_hour[hour]
        result.append({"hour": hour, "average_vehicles": round(avg, 2)})

    return result

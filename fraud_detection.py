from database import collection
from datetime import datetime, timedelta

def check_duplicate(tx_id):
    existing = collection.find_one({"transaction_id": tx_id})
    return existing is not None


def check_frequency(sender):
    one_min_ago = datetime.now() - timedelta(minutes=1)

    count = collection.count_documents({
        "sender": sender,
        "timestamp": {"$gte": one_min_ago}
    })

    return count >= 3
import hashlib
from typing import Dict
import requests as r
import os
from backend.config import HASURA_URL


def hash_query(query):
    print(''.join(query.split()))
    return hashlib.md5(''.join(query.split()).encode('utf-8')).hexdigest()


def api_call(payload: Dict):
    response = r.post(
        f"{HASURA_URL}/v1/metadata",
        json=payload,
        headers={
            "X-Hasura-Role": "admin",
            "X-Hasura-Admin-Secret": os.getenv('HASURA_ADMIN_SECRET'),
        }
    )

    return response
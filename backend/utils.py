import hashlib
from typing import Dict
import requests as r
import os

from backend.config import HASURA_URL


def hash_query(query):
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


def get_collections():
    response = api_call({"args": {}, "type": "export_metadata", "version": 2})
    metadata = response.json()['metadata']

    collections = {}
    collections_on_allow_list = [i['collection'] for i in metadata['allowlist']]
    for collection in metadata['query_collections']:
        collections[collection['name']] = []
        for query in collection['definition']['queries']:
            collections[collection['name']].append(
                {
                    "name": query['name'],
                    "query": query['query'],
                    "hash": hash_query(query['query'])
                }
            )

    return {'collections': collections, 'on_allow': collections_on_allow_list}

import hashlib
from json import JSONDecodeError
from typing import Dict
import requests as r
import os
import docker
import json
from flask_cors import CORS

from flask import Flask, jsonify, request

from backend.config import HASURA_URL
from backend.utils import api_call, hash_query

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    },
})
QUERY_CACHE: Dict = {}



@app.route("/add-collection", methods=["POST"])
def add_collection():
    req = request.json

    response = api_call(
        {
            "type": "create_query_collection",
            "args": {
                "name": req['collection_name'],
                "comment": req['comment'],
            }
        }
    )
    return jsonify(response.json())


@app.route("/add-query", methods=["POST"])
def add_query():
    req = request.json

    response = api_call(
        {
            "type": "add_query_to_collection",
            "args": {
                "collection_name": req['collectionName'],
                "query_name": req['name'],
                "query": req['query']
            }
        }
    )
    return jsonify(response.json())


@app.route("/delete-query", methods=["POST"])
def delete_query():
    req = request.json

    response = api_call(
        {
            "type": "drop_query_from_collection",
            "args": {
                "collection_name": "allowed-queries",
                "query_name": req['name']
            }
        }
    )
    return f"{response.status_code}"


@app.route("/update-query", methods=["POST"])
def update_query():
    status_code = delete_query()
    status_code_2 = add_query()

    return f"{status_code}, {status_code_2}"


@app.route("/")
def refresh_queries():
    client = docker.from_env()

    container = client.containers.get(os.getenv('HASURA_CONTAINER_NAME'))
    for line in container.logs().decode().split("\n"):
        try:
            logObject = json.loads(line)
        except JSONDecodeError:
            continue
        if "type" in logObject and logObject['type'] == 'http-log':
            hasuraQuery = logObject['detail']['operation'].get('query')
            if hasuraQuery is not None and "query" in hasuraQuery:
                query = hasuraQuery['query']
                queryName = hasuraQuery.get("operationName",
                                            None) if hasuraQuery.get("operationName", None) is not None else 'No name'
                # print("#" * 20, "START", "#" * 20)
                # print(query)
                # print(queryName)
                user_role = logObject['detail']['operation']['user_vars']['x-hasura-role']
                queryName = f"{user_role}_{queryName}"
                if queryName not in QUERY_CACHE:
                    QUERY_CACHE[queryName] = {"raw": query, "hash": hash_query(query)}
                else:
                    QUERY_CACHE[queryName] = {"raw": query, "hash": hash_query(query)}
    return jsonify(QUERY_CACHE)


@app.route("/allow-list")
def allow_list():
    response = r.post(
        f"{HASURA_URL}/v1/metadata",
        json={
            "args": {},
            "type": "export_metadata",
            "version": 2
        },
        headers={
            "X-Hasura-Role": "admin",
            "X-Hasura-Admin-Secret": os.getenv('HASURA_ADMIN_SECRET'),
        }
    )

    metadata = response.json()['metadata']

    queries = {}
    hashes = []
    hash_to_query_name_map = {}
    for collection in metadata['query_collections']:
        for query in collection['definition']['queries']:
            queries[query['name']] = query['query']
            _hash = hash_query(query['query'])
            hashes.append(_hash)
            hash_to_query_name_map[_hash] = query['name']

    return jsonify({'queries': queries, 'hashes': hashes, 'hash_to_query_name_map': hash_to_query_name_map})

from backend.blueprints.collections import collections as b_collections
from backend.blueprints.queries import queries as b_queries

if __name__ == "__main__":
    app.register_blueprint(b_collections)
    app.register_blueprint(b_queries)
    app.run(debug=True, port=5151, host="0.0.0.0")

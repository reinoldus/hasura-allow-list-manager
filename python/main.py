import hashlib
from json import JSONDecodeError
from typing import Dict
import requests as r
import os
import docker
import json
from flask_cors import CORS

from flask import Flask, jsonify, request

app = Flask(__name__)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    },
})
QUERY_CACHE: Dict = {}


def hashQuery(query):
    return hashlib.md5(''.join(query.split()).encode('utf-8')).hexdigest()


@app.route("/add-to-hasura", methods=["POST"])
def add_to_hasura():
    req = request.json
    response = r.post(
        "http://localhost:8080/v1/metadata",
        json={
            "type": "add_query_to_collection",
            "args": {
                "collection_name": "allowed-queries",
                "query_name": req['name'],
                "query": req['query']
            }
        },
        headers={
            "X-Hasura-Role": "admin",
            "X-Hasura-Admin-Secret": os.getenv('HASURA_ADMIN_SECRET'),
        }
    )

    return jsonify(QUERY_CACHE)


@app.route("/")
def refresh_queries():
    client = docker.from_env()

    container = client.containers.get(os.getenv('HASURA_CONTAINER_NAME'))
    for line in container.logs().decode().split("\n"):
        try:
            logObject = json.loads(line)
        except JSONDecodeError:
            continue
        if logObject['type'] == 'http-log':
            hasuraQuery = logObject['detail']['operation'].get('query')
            if hasuraQuery is not None and "query" in hasuraQuery:
                query = hasuraQuery['query']
                queryName = hasuraQuery.get("operationName",
                                            None) if hasuraQuery.get("operationName", None) is not None else 'No name'
                # print("#" * 20, "START", "#" * 20)
                # print(query)
                # print(queryName)
                # pprint(logObject['detail']['operation']['user_vars'])
                if queryName not in QUERY_CACHE:
                    print(query.split())
                    QUERY_CACHE[queryName] = {"raw": query, "hash": hashQuery(query)}
                else:
                    print(queryName, hashQuery(query))

    return jsonify(QUERY_CACHE)


@app.route("/allow-list")
def allow_list():
    response = r.post(
        "http://localhost:8080/v1/metadata",
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
    for collection in metadata['query_collections']:
        for query in collection['definition']['queries']:
            queries[query['name']] = query['query']
            print(query['name'], hashQuery(query['query']), "from h")
            hashes.append(hashQuery(query['query']))

    return jsonify({'queries': queries, 'hashes': hashes})


if __name__ == "__main__":
    app.run(debug=True, port=5151, host="0.0.0.0")

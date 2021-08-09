from collections import defaultdict
from pprint import pprint
import docker, os, json
from typing import Dict, Union

from flask import Blueprint, jsonify

from flask import Flask, jsonify, request
from backend.utils import api_call, hash_query, get_collections

queries = Blueprint('queries', __name__, url_prefix='/queries')

QUERY_CACHE: Dict = {}


@queries.route('/list')
def list_queries():
    response = api_call({"args": {}, "type": "export_metadata", "version": 2})
    metadata = response.json()['metadata']

    queries: Dict[str, Dict[str, Union[list, str]]] = defaultdict(lambda: defaultdict(list))
    for collection in metadata['query_collections']:
        for query in collection['definition']['queries']:
            query_hash = hash_query(query['query'])
            queries[query_hash]['names'].append(query['name'])
            queries[query_hash]['collections'].append(collection['name'])
            queries[query_hash]['query'] = query['query']

    return jsonify(queries)


@queries.route('/delete', methods=['POST'])
def delete():
    req = request.json
    print(req)
    response = api_call(
        {
            "type": "drop_query_from_collection",
            "args": {
                "query_name": req['name'],
                "collection_name": req['collection_name']
            }
        }
    )

    return jsonify(response.json())


@queries.route('/add', methods=['POST'])
def add_to_collection():
    req = request.json
    response = api_call(
        {
            "type": "add_query_to_collection",
            "args": {
                "collection_name": req['collection_name'],
                "query_name": req['name'],
                "query": req['query']
            }
        }
    )

    return jsonify(response.json())

@queries.route('/update', methods=['POST'])
def update_query():
    req = request.json

    delete()
    add_to_collection()

    return "Success", 200


@queries.route('/session/list')
def list_session_queries():
    client = docker.from_env()

    container = client.containers.get(os.getenv('HASURA_CONTAINER_NAME'))
    session_queries = defaultdict(lambda: defaultdict(list))

    # We use this set to track queries that have been overwritten in this session
    # If we do not do it we get all the different for one query that we might be developing right now
    already_added_set = set()
    colls = get_collections()['collections']
    hash_to_collection = defaultdict(list)
    name_to_collection = defaultdict(list)
    for collection_name, queries in colls.items():
        for query in queries:
            hash_to_collection[query['hash']].append(collection_name)
            name_to_collection[query['name']].append(collection_name)

    # We have read the logs bottom to top to get the latest query if a query changes
    for line in reversed(container.logs().decode().split("\n")):
        try:
            logObject = json.loads(line)
        except json.JSONDecodeError:
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
                print(queryName)
                query_hash = hash_query(query)
                user_role = logObject['detail']['operation']['user_vars']['x-hasura-role']
                if (queryName, user_role) in already_added_set:
                    continue
                already_added_set.add((queryName, user_role))

                if query_hash in hash_to_collection:
                    session_queries[query_hash]["collections_by_hash"].extend(hash_to_collection[query_hash])
                if queryName in name_to_collection:
                    session_queries[query_hash]["collections_by_name"].extend(name_to_collection[queryName])
                # Make sure the keys are present
                if query_hash not in hash_to_collection or queryName not in name_to_collection:
                    if len(session_queries[query_hash]["collections_by_hash"]) == 0:
                        session_queries[query_hash]["collections_by_hash"] = []
                    if len(session_queries[query_hash]["collections_by_name"]) == 0:
                        session_queries[query_hash]["collections_by_name"] = []

                session_queries[query_hash]["name"] = queryName
                session_queries[query_hash]["query"] = query
                session_queries[query_hash]["hash"] = query_hash
                session_queries[query_hash]["role"].append(user_role)
                session_queries[query_hash]["role"] = list(set(session_queries[query_hash]["role"]))

    print(session_queries)

    return jsonify(session_queries)

# @queries.route('/add', methods=['POST'])
# def add():
#     req = request.json
#     response = api_call(
#         {
#             "type": "create_query_collection",
#             "args":
#                 {
#                     "name": req['name'],
#                     "comment": req['comment'],
#                     "definition": {
#                         'queries':[]
#                     }
#                 }
#         }
#     )
#
#     return jsonify(response.json())
#
# @queries.route('/add-to-allow-list', methods=['POST'])
# def add_to_allow_list():
#     req = request.json
#     response = api_call(
#         {
#             "type": "add_collection_to_allowlist",
#             "args":
#                 {
#                     "collection": req['name']
#                 }
#         }
#     )
#
#     return jsonify(response.json())

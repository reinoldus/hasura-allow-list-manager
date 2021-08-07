from flask import Blueprint, jsonify

from flask import Flask, jsonify, request
from backend.utils import api_call, hash_query

collections = Blueprint('collections', __name__, url_prefix='/collections')


@collections.route('/list')
def list():
    response = api_call({"args": {}, "type": "export_metadata", "version": 2})
    metadata = response.json()['metadata']

    collections = {}
    for collection in metadata['query_collections']:
        print(collection)
        collections[collection['name']] = []
        for query in collection['definition']['queries']:
            collections[collection['name']].append({
                "name": query['name'],
                "query": query['query'],
                "hash": hash_query(query['query'])
            })

    return jsonify({'collections': collections})


@collections.route('/add', methods=['POST'])
def add():
    req = request.json
    response = api_call(
        {
            "type": "create_query_collection",
            "args":
                {
                    "name": req['name'],
                    "comment": req['comment'],
                    "definition": {
                        'queries':[]
                    }
                }
        }
    )

    return jsonify(response.json())

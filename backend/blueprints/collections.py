from pprint import pprint

from flask import Blueprint, jsonify

from flask import Flask, jsonify, request
from backend.utils import api_call, hash_query, get_collections

collections = Blueprint('collections', __name__, url_prefix='/collections')


@collections.route('/list')
def list():
    res = get_collections()
    return jsonify(res)


@collections.route('/delete', methods=['POST'])
def delete():
    req = request.json
    print(req)
    response = api_call(
        {
            "type": "drop_query_collection",
            "args": {
                "collection": req['name'],
                "cascade": True
            }
        }
    )

    return jsonify(response.json())


@collections.route('/add', methods=['POST'])
def add():
    req = request.json
    response = api_call(
        {
            "type": "create_query_collection",
            "args": {
                "name": req['name'],
                "comment": req['comment'],
                "definition": {
                    'queries': []
                }
            }
        }
    )

    return jsonify(response.json())


@collections.route('/add-to-allow-list', methods=['POST'])
def add_to_allow_list():
    req = request.json
    response = api_call({"type": "add_collection_to_allowlist", "args": {"collection": req['name']}})

    return jsonify(response.json())

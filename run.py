#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

import pymongo
from bson import ObjectId
from eve import Eve
from eve.auth import BasicAuth
from flask import current_app, jsonify
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError


class AuthForNewItem(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        # check for user exists. Only for new item from potential user.
        if method == 'POST' and resource == 'items':
            users = current_app.data.driver.db['users']
            user = users.find_one({
                'username': username,
            })

            if user:
                return pbkdf2_sha256.verify(password, user['password'])

            return False
        # another collections.
        return True


def before_insert(resource, documents):
    if resource == 'users':
        for document in documents:
            document['password'] = pbkdf2_sha256.hash(document['password'])
    else:
        categories = current_app.data.driver.db['categories']
        new_bulk = []

        for document in documents:
            _id = ObjectId(document.get('parent_category'))
            category = categories['categories'].find({
                '_id': _id
            })
            if category:
                if resource == 'items':
                    new_bulk.append(UpdateOne(
                        {'_id': _id},
                        {'$inc': {'items': 1}}
                    ))

                elif resource == 'categories':
                    if resource == 'items':
                        new_bulk.append(UpdateOne(
                            {'_id': _id},
                            {'$inc': {'child_categories': 1}}
                        ))

        try:
            categories.bulk_write(new_bulk)
        except BulkWriteError as bwe:
            pprint(bwe.details)
        except pymongo.errors.InvalidOperation:
            pass


def after_get(resource, response):
    if resource == 'items':
        items = current_app.data.driver.db['items']
        if response['_items']:
            new_bulk = []

            for item in response['_items']:
                new_bulk.append(UpdateOne(
                    {'_id': item['_id']},
                    {'$inc': {'views': 1}}
                ))

            try:
                items.bulk_write(new_bulk)
            except BulkWriteError as bwe:
                pprint(bwe.details)

    elif resource == 'categories':
        engine = current_app.data.driver.db
        for category in response['_items']:
            _id = category['_id']
            sub_categories = engine['categories'].find({
                'parent_category': _id
            })
            items = engine['items'].find({
                'parent_category': category['_id']
            })
            category['sub_categories'] = len(list(sub_categories))
            category['items'] = len(list(items))


app = Eve()
app.on_insert += before_insert
app.on_fetched_resource += after_get


@app.route(f"{app.api_prefix}/over-all", methods=['GET'])
def get_overall_info():
    engine = current_app.data.driver.db
    categories = list(engine['categories'].find({}))
    items = list(engine['items'].find({}))

    for category in categories:
        category['_id'] = str(category['_id'])
        try:
            category['parent_category'] = str(category['parent_category'])
        except KeyError:
            category['parent_category'] = 'I have no father...'

    for item in items:
        item['_id'] = str(item['_id'])
        item['parent_category'] = str(item['parent_category'])

    result = {
        'categories': categories,
        'items': items
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=False)

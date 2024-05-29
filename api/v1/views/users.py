#!/usr/bin/python3
"""
Creates users view routes
"""

from flask import jsonify, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    user_list = []
    for value in storage.all(User).items():
        user_list.append(value.to_dict())

    return jsonify(user_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id):
    """Retrieves a User"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)
    
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a User"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify(()), 200
    else:
        return abort(404)
    
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    if not request.get_json():
        return abort(400, 'Not a JSON')

    data = request.get_json()
    if 'email' not in data:
        return abort(400, 'Missing email')
    if 'password' not in data:
        return abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    user = storage.get(User, user_id)
    if user:
        if request.content_type != 'application/json':
            return abort(400, 'Not a JSON')

        if not request.get_json():
            return abort(400, 'Not a JSON')

        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
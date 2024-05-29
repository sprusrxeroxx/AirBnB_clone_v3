#!/usr/bin/python3
"""
Creates users view routes
"""

from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views

@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_all_places_by_city(city_id):
    """Retrieves the list of all Place objects by City"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)

@app_views.route('/places/<place_id>', strict_slashes=False)
def get_places(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)

    if place:
        return jsonify(place.to_dict())
    else:
        return abort(404)
    
@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify(()), 200
    else:
        return abort(404)
    
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    
    if not request.get_json():
        return abort(400, 'Not a JSON')
    
    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing name')
    if 'user_id' not in data:
        return abort(400, 'Missing user_id')
    
    data['city_id'] = city_id

    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place:
        if request.content_type != 'application/json':
            return abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        return abort(404)
    
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    places = storage.all(Place).values()
    if 'states' in data:
        places = [place for place in places if place.city.state_id in data['states']]
    if 'cities' in data:
        places = [place for place in places if place.city_id in data['cities']]
    if 'amenities' in data:
        places = [place for place in places if all(amenity.id in place.amenities for amenity in data['amenities'])]
    return jsonify([place.to_dict() for place in places])

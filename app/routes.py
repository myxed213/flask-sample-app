from app import app
from flask import request, jsonify

# In-memory item list
items = []

@app.route('/')
def hello():
    return "Hello, Flask!"

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

# Get a specific item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    if 0 <= item_id < len(items):
        return jsonify({'item': items[item_id]})
    return jsonify({'error': 'Item not found'}), 404

# Add a new item
@app.route('/items', methods=['POST'])
def add_item():
    item = request.get_json()
    if not item:
        return jsonify({'error': 'No data provided'}), 400
    items.append(item)
    return jsonify({'message': 'Item added successfully', 'item': item}), 201

# Update an existing item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    if 0 <= item_id < len(items):
        updated_data = request.get_json()
        if not updated_data:
            return jsonify({'error': 'No data provided'}), 400
        items[item_id] = updated_data
        return jsonify({'message': 'Item updated successfully', 'item': updated_data})
    return jsonify({'error': 'Item not found'}), 404

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return jsonify({'message': 'Item deleted successfully', 'item': removed_item})
    return jsonify({'error': 'Item not found'}), 404

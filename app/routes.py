from app import app
from flask import request, jsonify, render_template_string

# In-memory item list with initial data for testing
items = [
    {"id": 0, "name": "Sample Item 1", "price": 10.99},
    {"id": 1, "name": "Sample Item 2", "price": 20.99}
]

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Flask CRUD Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                button { margin: 5px; }
                .form-group { margin: 10px 0; }
            </style>
        </head>
        <body>
            <h1>Flask CRUD Demo</h1>
            
            <h2>Add New Item</h2>
            <form id="addForm">
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" id="name" required>
                </div>
                <div class="form-group">
                    <label>Price:</label>
                    <input type="number" step="0.01" id="price" required>
                </div>
                <button type="button" onclick="addItem()">Add Item</button>
            </form>

            <h2>Items List</h2>
            <table id="itemsTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in items %}
                    <tr id="row-{{ item.id }}">
                        <td>{{ item.id }}</td>
                        <td>{{ item.name }}</td>
                        <td>${{ item.price }}</td>
                        <td>
                            <button onclick="deleteItem({{ item.id }})">Delete</button>
                            <button onclick="editItem({{ item.id }})">Edit</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <script>
                function refreshItems() {
                    fetch('/items')
                        .then(response => response.json())
                        .then(data => {
                            let tableBody = document.querySelector('#itemsTable tbody');
                            tableBody.innerHTML = data.items.map(item => `
                                <tr id="row-${item.id}">
                                    <td>${item.id}</td>
                                    <td>${item.name}</td>
                                    <td>$${item.price}</td>
                                    <td>
                                        <button onclick="deleteItem(${item.id})">Delete</button>
                                        <button onclick="editItem(${item.id})">Edit</button>
                                    </td>
                                </tr>
                            `).join('');
                        });
                }

                function addItem() {
                    const name = document.getElementById('name').value;
                    const price = document.getElementById('price').value;
                    
                    fetch('/items', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name, price })
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        document.getElementById('addForm').reset();
                        refreshItems();
                    });
                }

                function deleteItem(id) {
                    if (confirm('Are you sure you want to delete this item?')) {
                        fetch(`/items/${id}`, { method: 'DELETE' })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                refreshItems();
                            });
                    }
                }

                function editItem(id) {
                    const newName = prompt('Enter new name:');
                    if (newName === null) return;
                    
                    const newPrice = prompt('Enter new price:');
                    if (newPrice === null) return;

                    fetch(`/items/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ name: newName, price: newPrice })
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        refreshItems();
                    });
                }
            </script>
        </body>
        </html>
    ''', items=items)

# REST API Endpoints (same as before)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify({'item': item})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_item = {
        "id": len(items),
        "name": data['name'],
        "price": data.get('price', 0.0)
    }
    items.append(new_item)
    return jsonify({'message': 'Item added successfully', 'item': new_item}), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    item['name'] = data.get('name', item['name'])
    item['price'] = data.get('price', item['price'])
    return jsonify({'message': 'Item updated successfully', 'item': item})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    item = next((item for item in items if item['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    items = [item for item in items if item['id'] != item_id]
    return jsonify({'message': 'Item deleted successfully', 'item': item})
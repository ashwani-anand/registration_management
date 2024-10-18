from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8544@localhost/registration_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Registration model
class Registration(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=False)
    PhoneNumber = db.Column(db.String(15))
    RegistrationDate = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database table
@app.before_request
def create_tables():
    db.create_all()  # This will create tables before every request

# Create a new registration (POST request)
@app.route('/registration', methods=['POST'])
def create_registration():
    data = request.json
    if not data or 'Name' not in data or 'Email' not in data or 'DateOfBirth' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Check if email already exists
    if Registration.query.filter_by(Email=data['Email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    try:
        new_registration = Registration(
            Name=data['Name'],
            Email=data['Email'],
            DateOfBirth=datetime.strptime(data['DateOfBirth'], '%Y-%m-%d'),
            PhoneNumber=data.get('PhoneNumber')
        )
        db.session.add(new_registration)
        db.session.commit()
        return jsonify({'message': 'Registration created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Retrieve all registrations (GET request)
@app.route('/registration', methods=['GET'])
def get_registrations():
    registrations = Registration.query.all()
    result = []
    for reg in registrations:
        result.append({
            'ID': reg.ID,
            'Name': reg.Name,
            'Email': reg.Email,
            'DateOfBirth': reg.DateOfBirth.strftime('%Y-%m-%d'),
            'PhoneNumber': reg.PhoneNumber,
            'RegistrationDate': reg.RegistrationDate.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(result)

# Update a registration by ID (PUT request)
@app.route('/registration/<int:id>', methods=['PUT'])
def update_registration(id):
    registration = Registration.query.get_or_404(id)
    data = request.json
    try:
        if 'Name' in data:
            registration.Name = data['Name']
        if 'Email' in data:
            registration.Email = data['Email']
        if 'DateOfBirth' in data:
            registration.DateOfBirth = datetime.strptime(data['DateOfBirth'], '%Y-%m-%d')
        if 'PhoneNumber' in data:
            registration.PhoneNumber = data['PhoneNumber']
        
        db.session.commit()
        return jsonify({'message': 'Registration updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a registration by ID (DELETE request)
@app.route('/registration/<int:id>', methods=['DELETE'])
def delete_registration(id):
    registration = Registration.query.get_or_404(id)
    try:
        db.session.delete(registration)
        db.session.commit()
        return jsonify({'message': 'Registration deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

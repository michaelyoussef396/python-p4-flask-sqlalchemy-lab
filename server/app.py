from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    return jsonify(
        id=animal.id,
        name=animal.name,
        species=animal.species,
        zookeeper=animal.zookeeper.name if animal.zookeeper else None,
        enclosure=animal.enclosure.environment if animal.enclosure else None
    )

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    return jsonify(
        id=zookeeper.id,
        name=zookeeper.name,
        birthday=zookeeper.birthday,
        animals=[animal.name for animal in zookeeper.animals]
    )

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    return jsonify(
        id=enclosure.id,
        environment=enclosure.environment,
        open_to_visitors=enclosure.open_to_visitors,
        animals=[animal.name for animal in enclosure.animals]
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)

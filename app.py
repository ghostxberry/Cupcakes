"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake, DEFAULT_IMAGE

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "super-secret"

connect_db(app)


@app.route("/")
def root():
    """Render homepage."""
    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    """Return all cupcakes in the system in JSON form like: {cupcakes: [{id, flavor, rating, size, image}, ...]}"""

    with app.app_context():
        cupcakes = [cupcake.serialized() for cupcake in Cupcake.query.all()]
        return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    try:
        data = request.json
        new_cupcake = Cupcake(
            flavor=data['flavor'],
            size=data['size'],
            rating=data['rating'],
            image=data['image']
        )

        with app.app_context():
            db.session.add(new_cupcake)
            db.session.commit()

        return jsonify({'message': 'Cupcake created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/cupcakes/<int:id>")
def show_cupcake(id):
    with app.app_context():
        cupcake = Cupcake.query.get_or_404(id)
        return jsonify(cupcake=cupcake.serialized())
    
@app.route("/api/cupcakes/<int:id>", methods = ["PATCH"])
def update_cupcake(id):
    data = request.json
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

    
@app.route('/api/cupcakes/<int:id>', methods=['GET', 'DELETE'])
def delete_cupcake(id):
    with app.app_context():
        cupcake = Cupcake.query.get_or_404(id)
        db.session.delete(cupcake)
        db.session.commit()
        return jsonify(message="Cupcake deleted successfully"), 200


if __name__ == '__main__':
    app.run(debug=True)

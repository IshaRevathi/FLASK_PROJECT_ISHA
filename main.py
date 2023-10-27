import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #location_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False) 
    company = db.Column(db.String(100), nullable=False) 
    quantity = db.Column(db.Integer)
    stored_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    movement_id = db.Column(db.String(200), nullable=False)
    from_location = db.Column(db.String(200), nullable=False)
    to_location = db.Column(db.String(200), nullable=False)
    #bio = db.Column(db.Text)

    def _repr_(self):
        return f'<Products {self.product_name}>'



@app.route('/')
def index():
    products = Products.query.all()
    return render_template('index.html', products=products)

# ...

@app.route('/<int:product_id>/')
def product(product_id):
    product = Products.query.get_or_404(product_id)
    return render_template('product.html', product=product)

# ...


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        #location_id = int(request.form['location_id'])
        product_name= request.form['product_name']
        company = request.form['company']
        quantity = int(request.form['quantity'])
        movement_id = request.form['movement_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product = Products(product_name=product_name,
                          company=company,
                          quantity=quantity)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

# ...


@app.route('/<int:product_id>/edit/', methods=('GET', 'POST'))
def edit(product_id):
    product = Products.query.get_or_404(product_id)

    if request.method == 'POST':
        #location_id = int(request.form['location_id'])
        product_name = request.form['product_name']
        company = request.form['company']
        quantity = int(request.form['quantity'])
        movement_id = request.form['movement_id']
        from_location = request.form['from_location']
        to_location = request.form['to_location']

        product.product_name = product_name
        product.company = company
        product.quantity = quantity
        product.from_location = from_location
        product.to_location = to_location

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

    # ...

@app.post('/<int:product_id>/delete/')
def delete(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/about/', methods=('GET', 'POST'))
def about():
    return render_template('about.html')
from math import prod
from flask import redirect, render_template, request, flash, url_for
from flask_market.models import Product
from flask_market.forms import ProductForm
from flask_market import app
from PIL import Image
import os
import secrets

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (600, 600)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/')
@app.route('/home')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.filter_by(id=id).first()
    image = url_for('static', filename=f'profile_pics/{product.image}')
    return render_template('product.html', product=product, image=image,title='Product')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            status = False
            if form.status.data == 'Active':
                status = True
            image = save_picture(form.image.data)
            product = Product(name=form.name.data, sku=form.sku.data, short_description=form.short_description.data,
                                 description=form.description.data, price=form.price.data, status=status, image=image)
            product.save()
            flash('Product added', 'success')
            return redirect(url_for('home'))
    return render_template('add_product.html', title='Add Product', form=form)

@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.filter_by(id=id).first()
    form = ProductForm()
    if request.method == 'GET':
        form.name.data = product.name
        form.sku.data = product.sku
        form.short_description.data = product.short_description
        form.description.data = product.description
        form.price.data = product.price
        if product.status:
            form.status.data = 'Active'
        else:
            form.status.data = 'Inactive'
    elif request.method == 'POST':
        product.name = form.name.data
        product.sku = form.sku.data
        product.short_description = form.short_description.data
        product.description = form.description.data
        product.price = form.price.data
        product.status = False
        product.image = save_picture(form.image.data)
        if form.status.data == 'Active':
            product.status = True
        product.save_changes()
        flash('Product updated', 'success')
        return redirect(url_for('home'))
    image = url_for('static', filename=f'profile_pics/{product.image}')
    return render_template('update.html', form=form, image=image,title='Update Product')

@app.route('/delete_product/<int:id>')
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    product.delete()
    flash('Product deleted', 'success')
    return redirect(url_for('home'))
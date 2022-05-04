from flask_market import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String(12), unique=True, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='product.jpg')
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'{self.name} - {self.price}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def save_changes(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

db.create_all()
db.session.commit()
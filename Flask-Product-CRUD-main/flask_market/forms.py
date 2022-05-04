from wtforms.fields import StringField, TextAreaField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_market.models import Product

class ProductForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    sku = StringField(label='SKU', validators=[DataRequired(), Length(min=8, max=12)])
    short_description = TextAreaField(label='Short Description', validators=[DataRequired()])
    image = FileField(label='Product Image', validators=[FileAllowed(['jpeg', 'png', 'jpg']), DataRequired()])
    description = TextAreaField(label='Description', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    status = RadioField(label='Status', choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    submit = SubmitField('Add')

    def validate_sku(self, sku):
        product = Product.query.filter_by(sku=sku.data).first()
        if product:
            raise ValidationError('A product with that SKU already exists')
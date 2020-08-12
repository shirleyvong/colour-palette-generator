from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Palette(db.Model, SerializerMixin):
  __tablename__ = 'palettes'
  id = db.Column(db.Integer, primary_key=True)
  colours = db.Column(db.ARRAY(db.String(6)), nullable=False)

  def __repr__(self):
    return '[' + ', '.join(self.colours) + ']'
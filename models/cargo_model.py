from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cargo(db.Model):
    __tablename__ = 'cargo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    stowage_location = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Cargo {self.name} - {self.weight}kg to {self.destination}>'

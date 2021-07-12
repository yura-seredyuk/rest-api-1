from app import db, session, Base

class Info(Base):
    __tablename__ = 'information'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)

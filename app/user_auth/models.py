from app import db
from sqlalchemy.orm import relationship, backref
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.communities.models import Issue, Comment, \
  CommentVoteUserJoin, Community, ActionPlanVoteUserJoin, admin_community_association

  
class User(db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), nullable=False, unique=True, index=True)
  is_admin = db.Column(db.Boolean)
  password_hash = db.Column(db.String)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  postal_code = db.Column(db.String)

  admin_of_community = db.relationship("Community",
                            secondary=admin_community_association,
                            backref=db.backref('users'),
    )

  issue_id = db.relationship('Issue', backref='users', lazy='dynamic')
  comment_id = db.relationship('Comment', backref='users', lazy='dynamic')
  comment_vote_user_joins_id = db.relationship("CommentVoteUserJoin", backref='users', lazy='dynamic')
  action_plan_vote_user_joins_id = db.relationship("ActionPlanVoteUserJoin", backref='users', lazy='dynamic')
 
  def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

  def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

  def serialize(self):
    return {
      'id': self.id,
      'first_name' : self.first_name,
      'last_name' : self.last_name,
      'email' : self.email,
      'postal_code' : self.postal_code,
    }

  def __init__(self, first_name, last_name, email, postal_code):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.postal_code = postal_code

  def __repr__(self):
    return '<User %r>' % self.email

  def generate_auth_token(self, expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': self.id})

  @staticmethod
  def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except SignatureExpired:
      return None    # valid token, but expired
    except BadSignature:
      return None    # invalid token
    user = User.query.get(data['id'])
    return user

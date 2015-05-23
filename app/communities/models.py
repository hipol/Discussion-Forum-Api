from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.user_auth.models import User
from datetime import datetime


admin_community_association = db.Table('admin_community_association', db.Model.metadata,
     db.Column('admin_id', db.Integer, db.ForeignKey('users.id')),
     db.Column('community_id', db.Integer, db.ForeignKey('communities.id'))
     )

class Community(db.Model):
	__tablename__ = "communities"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	kind = db.Column(db.Integer) #city = 0, state = 1, country = 2

	admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	issue_id = relationship("Issue", backref="communities")

	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'kind': self.kind
		}
	 
	def __init__(self, name, kind):
		self.name = name
		self.kind = kind

	def __repr__(self):
		return '<User %r>' % self.name


class Issue(db.Model):
	__tablename__ = "issues"
	id = db.Column(db.Integer, primary_key=True)
	views = db.Column(db.Integer)
	importance_count = db.Column(db.Integer)
	title = db.Column(db.String)
	picture = db.Column(db.String)
	#how to store photos?!? - - - - - - - - - - - - - - - - - - - - - - - --- - - - - - - - -
	info = db.Column(db.String)
	pub_date = db.Column(db.DateTime)

	community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	action_plan_id = relationship("ActionPlan", backref="issues", lazy='dynamic')
	event_id = relationship("Event", backref="issues", lazy='dynamic')
	
	def serialize(self):

		return {
			'id': self.id,
			'views': self.views,
			'importance_count': self.importance_count,
			'title': self.title,
			'info': self.info,
			'picture' : self.picture,
			'community_id': self.community_id,
			'author': User.query.get(self.author_id).first_name + " " + User.query.get(self.author_id).last_name,
			'author_id': self.author_id,
			'pub_date' : self.pub_date,
			'action_plan_id': [x.serialize() for x in self.action_plan_id],
			'time_since': timesince(self.pub_date)
			#figure out the x.plan


#jsonify({"community" : [community.serialize() for community in communitieslist]})


			}

	def __init__(self, title, info, author_id, picture):
	#def __init__(self, title, info, author_id):
		self.views = 0
		self.importance_count = 0
		self.title = title
		self.info = info
		self.author_id = author_id
		self.picture = picture
		self.pub_date = datetime.utcnow()
		

	def __repr__(self):
		return '<Issue: %r, # %s>' %(self.title, self.id)

class ActionPlan(db.Model):
	__tablename__ = "actionplans"
	id = db.Column(db.Integer, primary_key=True)
	votes = db.Column(db.Integer)
	plan = db.Column(db.String)
	article = db.Column(db.String)
	pub_date = db.Column(db.DateTime)

	issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	action_plan_vote_user_joins_id = db.relationship("ActionPlanVoteUserJoin", backref='actionplans', lazy='dynamic')
	comment_id = db.relationship("Comment", backref='actionplans', lazy='dynamic')
	event_id = relationship("Event", backref="actionplans", lazy='dynamic')

	def serialize(self):
		return {
			'id': self.id,
			'votes': self.votes,
			'plan': self.plan,
			'article': self.article,
			'author': User.query.get(self.author_id).first_name + " " + User.query.get(self.author_id).last_name,
			'author_id': self.author_id,
			'issue_id': self.issue_id,
			'pub_date' : self.pub_date,
			'time_since': timesince(self.pub_date),
    		'comments' : [x.serialize() for x in self.comment_id]
		}

	def __init__(self, plan, article, author_id, issue_id):
		self.votes = 0
		self.plan = plan
		self.article = article
		self.author_id = author_id
		self.issue_id = issue_id
		self.pub_date = datetime.utcnow()
		

	def __repr__(self):
		return '<ActionPlan %r %s>' %(self.plan, self.id)

class ActionPlanVoteUserJoin(db.Model):
	__tablename__ = "actionplanvoteuserjoins"
	id = db.Column(db.Integer, primary_key=True)
	pub_date = db.Column(db.DateTime)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	voter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	event_id = relationship("Event", backref="actionplanvoteuserjoins", lazy='dynamic')

	def serialize(self):
		return {
			'id': self.id,
			'voter_id': self.voter_id,
			'action_plan_id': self.action_plan_id,
			'pub_date': self.pub_date,
			'time_since': timesince(self.pub_date)
		}

	def __init__(self, action_plan_id, voter_id):
		self.action_plan_id = action_plan_id
		self.voter_id = voter_id
		self.pub_date = datetime.utcnow()
		

	def __repr__(self):
		return '<ActionPlan: %s, User: %s>' %(action_plan_id, voter_id)

class Comment(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer, primary_key=True)
	upvotes = db.Column(db.Integer)
	downvotes = db.Column(db.Integer)
	text = db.Column(db.String)
	pub_date = db.Column(db.DateTime)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	event_id = relationship("Event", backref="comments", lazy='dynamic')
	comment_vote_user_joins_id = db.relationship("CommentVoteUserJoin", backref='comments', lazy='dynamic')

	def serialize(self):
		return {
			'id': self.id,
			'text': self.text,
			'upvotes': self.upvotes,
			'downvotes': self.downvotes,
			'author_id': User.query.get(self.author_id).first_name + " " + User.query.get(self.author_id).last_name,
			'action_plan_id': self.action_plan_id,
			'pub_date': self.pub_date,
			'time_since': timesince(self.pub_date)
		}

	def __init__(self, text, action_plan_id, author_id):
		self.text = text
		self.upvotes = 0
		self.downvotes = 0
		self.author_id = author_id
		self.action_plan_id = action_plan_id
		self.pub_date = datetime.utcnow()
		

	def __repr__(self):
		return '<Comment: %s>' % id

# FIGURE OUT THESE JOINS... ALSO FOR PROS AND CONS

class CommentVoteUserJoin(db.Model):
	__tablename__ = "commentvoteuserjoins"
	id = db.Column(db.Integer, primary_key=True)
	main_value = db.Column(db.Integer)
	pub_date = db.Column(db.DateTime)

	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	voter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	event_id = relationship("Event", backref="commentvoteuserjoins", lazy='dynamic')

	def __init__(self, comment_id, voter_id, main_value):
		self.comment_id = comment_id
		self.voter_id = voter_id
		self.main_value = main_value
		self.pub_date = datetime.utcnow()

	def serialize(self):
		return {
			'id': self.id,
			'voter_id': self.voter_id,
			'comment_id': self.comment_id,
			'main_value': self.main_value,
			'pub_date': self.pub_date,
			'time_since': timesince(self.pub_date)
		}

		

	def __repr__(self):
		return '<Comment: %s, User: %s>' %(comment_id, voter_id)

class Event(db.Model):
	__tablename__ = "event"
	id = db.Column(db.Integer, primary_key=True)
	event_type = db.Column(db.Integer) #1=issue #2=action_plan #3comment #4vote #5commentvote
	pub_date = db.Column(db.DateTime)

	issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))
	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	actionplanvoteuserjoins_id = db.Column(db.Integer, db.ForeignKey('actionplanvoteuserjoins.id'))
	commentvoteuserjoins_id = db.Column(db.Integer, db.ForeignKey('commentvoteuserjoins.id'))

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, event_type, user_id):
		self.user_id = user_id
		self.event_type = event_type
		self.pub_date = datetime.utcnow()

	def serialize(self):
		return {
			'id': self.id,
			'event_type': self.event_type,
			'pub_date': self.pub_date,
			'time_since': timesince(self.pub_date)
		}

	def __repr__(self):
		return '<Comment: %s, User: %s>' %(comment_id, voter_id)


from datetime import datetime
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default





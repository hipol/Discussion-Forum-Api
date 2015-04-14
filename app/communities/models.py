from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


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
	#picture = db.Column(db.String)
	#how to store photos?!? - - - - - - - - - - - - - - - - - - - - - - - --- - - - - - - - -
	info = db.Column(db.String)

	community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	action_plan_id = relationship("ActionPlan", backref="issues", lazy='dynamic')
	
	def serialize(self):

		return {
			'id': self.id,
			'views': self.views,
			'importance_count': self.importance_count,
			'title': self.title,
			'info': self.info,
			#'picture' : self.picture,
			'community_id': self.community_id,
			'author_id': User.query.get(self.author_id).first_name + " " + User.query.get(self.author_id).last_name,

			'action_plan_id': [x.serialize() for x in self.action_plan_id] 
			#figure out the x.plan


#jsonify({"community" : [community.serialize() for community in communitieslist]})


			}

	#def __init__(self, title, info, community_id, author_id, picture):
	def __init__(self, title, info, author_id):
		self.views = 0
		self.importance_count = 0
		self.title = title
		self.info = info
		self.author_id = author_id
		#self.picture = picture

	def __repr__(self):
		return '<Issue: %r, # %s>' %(self.title, self.id)

class ActionPlan(db.Model):
	__tablename__ = "actionplans"
	id = db.Column(db.Integer, primary_key=True)
	votes = db.Column(db.Integer)
	plan = db.Column(db.String)
	article = db.Column(db.String)

	issue_id = db.Column(db.Integer, db.ForeignKey('issues.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	action_plan_vote_user_joins_id = db.relationship("ActionPlanVoteUserJoin", backref='actionplans', lazy='dynamic')
	comment_id = db.relationship("Comment", backref='articles', lazy='dynamic')
	pros = db.relationship("Pros", backref='articles', lazy='dynamic')
	cons = db.relationship("Cons", backref='articles', lazy='dynamic')

	def serialize(self):
		return {
			'id': self.id,
			'votes': self.votes,
			'plan': self.plan,
			'article': self.article,
			'pros': [x for x in self.pros],
			'cons': [x for x in self.cons],
			'author_id': self.author_id,
			'issue_id': self.issue_id
		}

	def __init__(self, plan, article, author_id, issue_id):
		self.votes = 0
		self.plan = plan
		self.article = article
		self.author_id = author_id
		self.issue_id = issue_id

	def __repr__(self):
		return '<ActionPlan %r %s>' %(self.plan, self.id)

class ActionPlanVoteUserJoin(db.Model):
	__tablename__ = "actionplanvoteuserjoins"
	id = db.Column(db.Integer, primary_key=True)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	voter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, action_plan_id, user_id):
		self.action_plan_id = action_plan_id
		self.user_id = user_id

	def __repr__(self):
		return '<ActionPlan: %s, User: %s>' %(action_plan_id, voter_id)

class Pros(db.Model):
	__tablename__ = "pros"
	id = db.Column(db.Integer, primary_key=True)
	upvotes = db.Column(db.Integer)
	downvotes = db.Column(db.Integer)
	text = db.Column(db.String)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#	comment_vote_user_joins_id = db.relationship("Pros", backref='comments', lazy='dynamic')

	def __init__(self, text, issue_id, article_id, user_id):
		self.text = text
		self.upvotes = 0
		self.downvotes = 0
		self.user_id = user_id
		self.issue_id = issue_id
		self.article_id = article_id

	def __repr__(self):
		return '<Pros: %s>' % id

class Cons(db.Model):
	__tablename__ = "cons"
	id = db.Column(db.Integer, primary_key=True)
	upvotes = db.Column(db.Integer)
	downvotes = db.Column(db.Integer)
	text = db.Column(db.String)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#	comment_vote_user_joins_id = db.relationship("Pros", backref='comments', lazy='dynamic')

	def __init__(self, text, issue_id, article_id, user_id):
		self.text = text
		self.upvotes = 0
		self.downvotes = 0
		self.user_id = user_id
		self.issue_id = issue_id
		self.article_id = article_id

	def __repr__(self):
		return '<Pros: %s>' % id

class Comment(db.Model):
	__tablename__ = "comments"
	id = db.Column(db.Integer, primary_key=True)
	upvotes = db.Column(db.Integer)
	downvotes = db.Column(db.Integer)
	text = db.Column(db.String)

	action_plan_id = db.Column(db.Integer, db.ForeignKey('actionplans.id'))
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	comment_vote_user_joins_id = db.relationship("CommentVoteUserJoin", backref='comments', lazy='dynamic')

	def __init__(self, text, issue_id, article_id, user_id):
		self.text = text
		self.upvotes = 0
		self.downvotes = 0
		self.user_id = user_id
		self.issue_id = issue_id
		self.article_id = article_id

	def __repr__(self):
		return '<Comment: %s>' % id

# FIGURE OUT THESE JOINS... ALSO FOR PROS AND CONS

class CommentVoteUserJoin(db.Model):
	__tablename__ = "commentvoteuserjoins"
	id = db.Column(db.Integer, primary_key=True)
	main_id = db.Column(db.Integer)

	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	voter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, comment_id, user_id):
		self.comment_id = comment_id
		self.user_id = user_id
		self.vote = 0

	def __repr__(self):
		return '<Comment: %s, User: %s>' %(comment_id, voter_id)

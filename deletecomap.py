

from app import db
from app.communities.models import Comment
com = Comment.query.all()
for i in com:
	db.session.delete(i)

from app.communities.models import ActionPlan
com = ActionPlan.query.all()
for i in com:
	db.session.delete(i)


db.session.commit()
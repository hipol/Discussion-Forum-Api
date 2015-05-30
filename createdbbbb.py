

from app import db
from app.communities.models import Issue

iss = Issue.query.filter_by(id=8).first()
iss.picture = "https://res.cloudinary.com/demo/image/fetch/http://www.cbc.ca/polopoly_fs/1.1551009.1381653461!/httpImage/image.jpg_gen/derivatives/16x9_620/hi-dollar-01324872.jpg"
iss2 = Issue.query.filter_by(id=9).first()
iss2.picture = "https://res.cloudinary.com/demo/image/fetch/http://www.kdnuggets.com/wp-content/uploads/privacy-lock.jpg"
iss3 = Issue.query.filter_by(id=10).first()
iss3.picture = "https://res.cloudinary.com/demo/image/fetch/http://thepolitic.org/wp-content/uploads/2012/04/politics1.jpg"
iss4 = Issue.query.filter_by(id=11).first()
iss4.picture = "https://res.cloudinary.com/demo/image/fetch/http://citycaucus.com/wp-content/uploads/2012/05/800_cp_montreal_student_protest_120223.jpg"
iss5 = Issue.query.filter_by(id=12).first()
iss5.picture = "https://res.cloudinary.com/demo/image/fetch/http://images.wisegeek.com/man-in-suit-speaking-to-audience-in-front-of-him.jpg"

db.session.commit()

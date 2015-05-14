from app import db
db.create_all()

from app import Issue
iss = Issue("title", "info", 1, "lala")
db.session.add(iss)
db.session.commit()
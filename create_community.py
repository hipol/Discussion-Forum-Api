
from app import db
from app.communities.models import Community
londy = Community("London", 0)
db.session.add(londy)
db.session.commit()
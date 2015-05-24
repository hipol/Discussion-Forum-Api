

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


Both governments and citizens desire a higher level of 'engagement', which is seemingly the ultimate goal when it comes to political affairs. What does ‘engagement’ mean to you? And what could your government do to make it easier for you as a citizen to engage in debate and decision making?


 "<p>When it comes to the Canadian economy, what should be the focus? Our knowledge economy? Natural Resource sector? Or something else entirely?</p><p>Canadians are divided on the issue of natural resource development and the relationship our economy has with our natural landscape. As we move into an important federal election, what direction would you like to see Canada’s economy go? Should we capitalize on our nation’s bountiful natural resources as the focus? Or should we put additional resources into shifting the focus to more of a knowledge sector based economy, capitalizing on university research and advances in technology? Any good economy of course must have many facets, but what should be the focus of Canada’s future economic development? What do we want Canada’s economy to be known for internationally? </p>"
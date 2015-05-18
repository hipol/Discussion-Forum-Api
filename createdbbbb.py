from app import db
db.create_all()

from app import Issue
iss = Issue("The Canadian Economy", "When it comes to the Canadian economy, what should be the focus? Our knowledge economy? Natural Resource sector? Or something else entirely?", 1, "http://static1.squarespace.com/static/540d1865e4b091e569d68f16/t/54165ec7e4b08db1809356ec/1410752200433/Monetary_Policy_and_Economics.jpg?format=2500w")
db.session.add(iss)
iss = Issue("Bill C-51", "As a citizen, what balance would you like to see between the importance of national security with your need for privacy (C-51)?", 1, "http://www.kdnuggets.com/wp-content/uploads/privacy-lock.jpg")
db.session.add(iss)
iss = Issue("Party Politics", "Do you think anything could be done to improve the current party politics system?", 1, "http://thepolitic.org/wp-content/uploads/2012/04/politics1.jpg")
db.session.add(iss)
iss = Issue("The Cost of Education", "Is the cost of quality education too high? If so, what can be done to improve the system?", 1, "http://citycaucus.com/wp-content/uploads/2012/05/800_cp_montreal_student_protest_120223.jpg")
db.session.add(iss)
iss = Issue("Citizen Engagement", "What are the most tangible ways in which your government could assist you and others to become 'engaged' citizens?", 1, "http://images.wisegeek.com/man-in-suit-speaking-to-audience-in-front-of-him.jpg")
db.session.add(iss)

db.session.commit()



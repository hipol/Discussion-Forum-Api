
# Statement for enabling the development environment
DEBUG = True

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'postgresql://townsquaren36:townsquaren36password@townsquaren36.cpsi9ozyfzbi.us-east-1.rds.amazonaws.com:5432/townsquaren36'
SQLALCHEMY_DATABASE_URI = 'postgres://wllktomrcevqwj:Bjlml2bAxSHb2iIiWe6bZJKamp@ec2-23-23-81-189.compute-1.amazonaws.com:5432/der28r25heo67u'
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')




#SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
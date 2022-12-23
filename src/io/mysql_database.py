import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# creating a connection to the database
mysql_url = os.environ.get("MYSQL_HOST")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
database_name = os.environ.get("MYSQL_DATABASE")

# recreating the URL connection
connection_url = "mysql://{user}:{password}@{url}/{database}".format(
    user=mysql_user, password=mysql_password, url=mysql_url, database=database_name
)
# creating the connection
engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

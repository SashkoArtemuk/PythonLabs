from models import User
from models import Session
from dbfun import create_model
user = User("test", "Test@gmai.com", "1234567")

create_model(user)
# pip install sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///example.db')

# 객체 정의
Base = declarative_base()

# 테이블 정의
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 테이블 생성
Base.metadata.create_all(engine)

# 데이터 삽입
Session = sessionmaker(bind=engine)
session = Session() # like cursor in sqlite3

new_user = User(name="홍길동", age=25)
session.add(new_user)

new_user = User(name="고길동", age=34)
session.add(new_user)

session.commit()

# 데이터 조회
users = session.query(User).all()
for user in users:
    print(user.name, user.age)
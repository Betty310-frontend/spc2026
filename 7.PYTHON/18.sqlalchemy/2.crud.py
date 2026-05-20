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

# CRUD 수행할 함수 구현
def create_user(session, name, age):
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()
    return new_user

def list_users(session):
    users = session.query(User).all()
    return users

def get_user_by_id(session, user_id):
    # 원래 사용하던 sqlalchemy 방식
    user = session.query(User).filter_by(id=user_id).first()

    # session.get() 방식 (sqlalchemy 2.0에서 권장)
    # user = session.get(User, user_id) 
    return user

def update_user_age(session, user_id, new_age):
    user = session.get(User, user_id)
    if not user:
        return False
    user.age = new_age
    session.commit()

    return True

def delete_user_by_id(session, user_id):
    user = session.get(User, user_id)
    if not user:
        return 0
    session.delete(user)
    session.commit()

    return len(users)

def delete_user_by_name(session, name):
    users = session.query(User).filter_by(name=name).all()
    if not users:
        return 0
    
    for user in users:
        session.delete(user)
    session.commit()
    return len(users)

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    with Session() as session:
        # 1) 사용자 생성
        create_user(session, "홍길동", 25)
        create_user(session, "홍길동", 40)
        create_user(session, "고길동", 34)
        create_user(session, "고길동", 21)

        # 2) 사용자 목록 조회
        users = list_users(session)
        print("\nlist_users:")
        for user in users:
            print(user.id, user.name, user.age)

        # 3) 사용자 ID로 조회
        user = get_user_by_id(session, 2)
        print("\nget_user_by_id:")
        if user:
            print(user.id, user.name, user.age)

        # 4) 사용자 정보 업데이트
        update_user_age(session, 2, 30)
        user = get_user_by_id(session, 2)
        print("\nupdate_user_age:")
        if user:
            print(user.id, user.name, user.age)

        # 5) 사용자 삭제
        rest_users = delete_user_by_id(session, 2)
        users = list_users(session)
        print("\ndelete_user_by_id:")
        print(rest_users)
        for user in users:
            print(user.id, user.name, user.age)

        # 6) 이름으로 사용자 삭제
        rest_users = delete_user_by_name(session, '고길동')
        users = list_users(session)
        print("\ndelete_user_by_name:")
        print(rest_users)   
        for user in users:
            print(user.id, user.name, user.age)


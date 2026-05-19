import database.my_crud_lib as db
from drop_table import drop_table

def main():
    drop_table()
    db.create_table()

    db.insert_user('Alice', 30)
    db.insert_user('Bob', 25)
    db.insert_user('Charlie', 35)

    print("\nAll users:")
    users = db.get_all_users()
    for user in users:
        print(user)

    print("\nUpdate user:")
    db.update_user(2, age=26)
    user = db.get_user_by_id(2)
    print(user)

    print("\nDelete user: id=1")
    db.delete_user_by_id(1)

    print("\nAll users after deletion:")
    users = db.get_all_users()
    for user in users:
        print(user)

if __name__ == "__main__":
    main()
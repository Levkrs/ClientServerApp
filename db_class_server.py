from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime
import os
PATH_TO_FILE = os.path.dirname(__file__)
print('----')
PATH_TO_SQL = f'sqlite:///{PATH_TO_FILE}/db_sqlite.db3'
print(PATH_TO_SQL)
# print(SQL_PATH)
print('----')


class ServerStorage:
    class User:
        def __init__(self, username):
            self.name = username
            self.register_date = datetime.datetime.now()
            self.id = None

    class ActiveUser:
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip = ip_address
            self.port = port
            self.login_time = login_time

    class StoryClient:
        def __init__(self, name, ip_address, login_time, port):
            self.name = name
            self.date_time = login_time
            self.ip = ip_address
            self.port = port
            self.id = None

    class UserContact:
        def __init__(self, user_id, contact_id):
            self.id = None
            self.user_id = user_id
            self.contact_id = contact_id

    def __init__(self):
        print('--- INIT --')
        # self.database_engine = create_engine('sqlite:///db_sqlite.db3', echo=True)
        self.database_engine = create_engine(PATH_TO_SQL, echo=False)
        print('Database_engine', self.database_engine)
        self.metadata = MetaData()

        user_table = Table('User', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String),
                           Column('register_date', DateTime),
                           )

        active_user_table = Table('ActiveUser', self.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('user', ForeignKey('User.id'), unique=True),
                                  Column('ip', String),
                                  Column('port', String),
                                  Column('login_time', DateTime)
                                  )

        story_table = Table('StoryTable', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', ForeignKey('User.name')),
                            Column('date_time', DateTime),
                            Column('ip', String),
                            Column('port', String)
                            )

        user_contact_table = Table('UserContact', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user_id', ForeignKey('User.id')),
                                   Column('contact_id', ForeignKey('User.id'))
                                   )

        self.metadata.create_all(self.database_engine)

        mapper(self.User, user_table)
        mapper(self.StoryClient, story_table)
        mapper(self.ActiveUser, active_user_table)
        mapper(self.UserContact, user_contact_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.session.query(self.ActiveUser).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port):
        print(f'Login info {username}, {ip_address}, {port}')
        rez = self.session.query(self.User).filter_by(name=username)
        print(rez)
        if rez.count():
            user = rez.first()
            user.register_date = datetime.datetime.now()
        else:
            user = self.User(username)
            self.session.add(user)
            self.session.commit()

        # new_user = self.ActiveUser(user.id, ip_address, port, datetime.datetime.now())
        new_user = self.ActiveUser(user_id=user.id, ip_address=ip_address, port=port,
                                   login_time=datetime.datetime.now())
        self.session.add(new_user)
        histroy = self.StoryClient(name=user.name, login_time=datetime.datetime.now(), ip_address=ip_address, port=port)
        self.session.add(histroy)

        self.session.commit()
        print('New_user_add ')

    def user_logout(self, username):
        user = self.session.query(self.User).filter_by(name=username).first()
        self.session.query(self.ActiveUser).filter_by(user=user.id).delete()
        self.session.commit()
        print('Delete active user')


    def active_user(self):
        query = self.session.query(
            self.User.name,
            self.ActiveUser.ip,
            self.ActiveUser.port,
            self.ActiveUser.login_time
        ).join(self.User)
        return query.all()

    def login_history(self, username=None):
        query = self.session.query(self.User.name,
                                   self.StoryClient.date_time,
                                   self.StoryClient.ip,
                                   self.StoryClient.port,
                                   ).join(self.User)
        if username:
            query = query.filter(self.User.name == username)
            # query=self.session.query(self.User.name == username)
        return query.all()

    def add_contact(self, user, contact):
        user = self.session.query(self.User).filter_by(name=user).first()
        contact = self.session.query(self.User).filter_by(name=contact).first()

        if not contact or self.session.query(self.UserContact).filter_by(user_id=user.id, contact_id=contact.id).count():
            return

        contact_row = self.UserContact(user_id=user.id, contact_id=contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        user = self.session.query(self.User).filter_by(name=user).first()
        contact = self.session.query(self.User).filter_by(name=contact).first()
        remove_row = self.session.query(self.UserContact).filter(
            self.UserContact.user_id == user.id, self.UserContact.contact_id == contact.id).delete()
        print('DeleteUser')
        self.session.commit()

    #Проверить
    def contact_list(self, user):
        user = self.session.query(self.User).filter_by(name=user).first()
        contact_list = self.session.query(self.UserContact, self.User.name). \
            filter_by(user_id=user.id). \
            join(self.User, self.UserContact.contact_id == self.User.id)
        # contact_list = self.session.query(self.UserContact).filter(
        #     self.UserContact.user_id == user.id).all()
        contact_list_nick = []

        self.session.commit()
        print(contact_list.__dict__)
        return [item[1] for item in contact_list.all()]
        # for item in contact_list:
        #     print(item[1])

        # return contact_list
        # Здесь функция на удаление контакта





if __name__ == '__main__':
    # pass
    print('_____MAIN_____')
    test_db = ServerStorage()
    test_db.contact_list('nik6')
    # test_db.contact_list('nik5')

    # test_db.user_login('Serg', '192.168.0.0', 750)
    # test_db.user_login('Kiril', '192.168.1.1', 650)
    # test_db.add_contact('Serg', 'Kiril')
    # test_db.remove_contact('Serg', 'Kiril')
    # test_db.user_logout('Serg')
    # print(test_db.active_user())
    # print('----')
    # login_h = test_db.login_history('Serg')
    # print('Login history')
    # print(login_h)
    print('----')
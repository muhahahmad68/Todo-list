# Write your code here
from sqlalchemy import create_engine, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

today = datetime.today()

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # create the database
Base = declarative_base()
session = sessionmaker(bind=engine)()


#  Create a table in form of classes where your task are stored
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=today.date())

    def __repr__(self):

        return str(self.task), self.deadline


Base.metadata.create_all(engine)


def today_task():
    print(f'Today {today.day} {today.strftime("%b")}')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    if len(rows) == 0:
        print("Nothing to do!\n")
    else:
        print(row for row in rows)
        print()


def add_task():
    action = input('Enter task\n')
    dead = input('Enter deadline\n')
    print("The task has been added!")
    new_row = Table(task=action, deadline=datetime.strptime(dead, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()


def week_task():
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in range(7):
        rows = session.query(Table).filter(Table.deadline ==
                                           (today + timedelta(days=i)).date()).order_by(Table.deadline).all()
        print(weekdays[(today + timedelta(i)).weekday()],
              (today + timedelta(i)).day, (today + timedelta(i)).strftime('%b'))
        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            print('{}\n'.format(rows[0].task))


def all_task():
    al = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    count = 1
    for row in al:
        if row.task:
            print('{}. {}. {}\n'.format(count, row.task, row.deadline.strftime("%#d %b")))
            count += 1


def missed_task():
    past = session.query(Table).filter(Table.deadline < today.date()).all()
    print("Missed tasks:")
    count = 1
    if len(past) == 0:
        print('Nothing is missed!')
    else:
        for i in past:
            if i.task:
                print('{}. {}. {}'.format(count, i.task, i.deadline.strftime("%d %b")))
                count += 1


def delete_task():
    print("Choose the number of the task you want to delete:")
    al = session.query(Table).order_by(Table.deadline).all()
    count = 1
    for row in al:
        if row.task:
            print('{}. {}. {}\n'.format(count, row.task, row.deadline.strftime("%#d %b")))
            count += 1
    no = int(input())
    specific_row = al[no - 1]
    session.delete(specific_row)
    session.commit()
    print("The task has been deleted")


def main():
    while True:

        option = input("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                       "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
        if option == '1':
            today_task()
        elif option == '2':
            week_task()
        elif option == '3':
            all_task()
        elif option == '4':
            missed_task()
        elif option == '5':
            add_task()
        elif option == '6':
            delete_task()
        elif option == '0':
            print('\nBye')
            break
        else:
            print('Invalid input')


if __name__ == '__main__':

    main()

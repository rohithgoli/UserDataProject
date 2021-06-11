from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import cast
from sqlalchemy import and_, or_, not_


engine = create_engine('sqlite:///sample.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(50), index=True)
    student_gender = Column(String(20))
    student_residence = Column(String(50))
    student_rank = Column(Integer())
    student_attendance = Column(Numeric(4, 2))


Base.metadata.create_all(engine)
"""                                                                    Create Operation in Database
student1 = Student(
                student_name='Afroz',
                student_gender='M',
                student_residence='Hyderabad',
                student_rank=10,
                student_attendance=90.50)

session.add(student1)
session.commit()

print(student1.student_id)
"""


"""                                                                  Create Multiple objects operation in Database
s1 = Student(
                student_name='Vishvesh',
                student_gender='M',
                student_residence='Chennai',
                student_rank=1,
                student_attendance=75.50)

s2 = Student(
                student_name='Chandan Singh Rajput',
                student_gender='M',
                student_residence='Gaya',
                student_rank=5,
                student_attendance=85.50)

session.bulk_save_objects([s1, s2])
session.commit()

"""
"""                                                                             Read Operation on Database
results = session.query(Student).all()
for result in results:
    print(result.student_name, result.student_rank)

print(session.query(Student.student_name, Student.student_attendance).first())
"""

"""#                                                                             Read Operation using order_by
for student in session.query(Student).order_by(Student.student_name):
    print(f'{student.student_name} from {student.student_residence} secured rank {student.student_rank}')
"""

"""                                                                             order_by DESC in Read Operation 
for student in session.query(Student).order_by(desc(Student.student_name)):
    print(student.student_name, student.student_rank)
"""

"""                                                                             Pagination of results
query = session.query(Student).order_by(desc(Student.student_rank)).limit(2)
print([result.student_name for result in query])
"""

"""                                                                              SUM function
attendance_sum = session.query(func.sum(Student.student_attendance)).scalar()
print(attendance_sum)
"""

"""                                                                               COUNT function
student_count = session.query(func.count(Student.student_id)).first()
print(student_count)
"""

"""                                                                                     Labeling
rec_count = session.query(func.count(Student.student_id).label('Total_students')).first()

print(rec_count.keys())
print(rec_count.Total_students)
"""


"""                                                                                     filter_by
result = session.query(Student).filter_by(student_rank=1).first()
print(result.student_name)
"""


"""                                                                                      filter
result = session.query(Student).filter(Student.student_name == 'Afroz').first()
print(result.student_rank)
"""

"""                                                                                       clause elements -> LIKE
result = session.query(Student).filter(Student.student_name.like('%Rajput%'))
for record in result:
    print(record.student_name, record.student_attendance)
"""

"""                                                                                Conjunctions --> and_ or_ not_
query = session.query(Student).filter(
                or_(
                    Student.student_name.contains('Rajput'),
                    Student.student_rank.between(1, 5)
                )
            )
for result in query:
    print(result.student_name, result.student_rank)
"""


"""                                                                                             Update operation
req_result = session.query(Student).filter(Student.student_rank == 1).first()
req_result.student_attendance = req_result.student_attendance + 5
session.commit()

print(req_result.student_attendance)
"""

"""                                                                                              Delete Operation
query = session.query(Student)
query = query.filter(Student.student_rank == 10)

del_result = query.one()
session.delete(del_result)
session.commit()

del_result = query.first()
print(del_result)

"""
"""Server ORM"""
from app import db
from app.models import utility


class User(db.Model):
    """Models a user that plays our game"""
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telegram_handle = db.Column(db.String(64), nullable=True, unique=True)
    telegram_start_token = db.Column(db.String(64), nullable=False, unique=False,
                                     default=utility.create_telegram_start_token)
    current_story_point = db.Column(db.String(64), nullable=True, unique=False)
    # TODO: This should be some sort of array, which sqllite does not support
    requested_data_types = db.relationship("RequestedDatatype")
    # TODO: Placeholder, has no real function/use in code
    current_story_point = db.Column(db.String(64))
    task_assigments = db.relationship("TaskAssignment")

    def as_dict(self):
        """As sqlalchemy obj cant be parsed to json we build a custom converter"""
        return utility.dict_keys_to_camel_case(
            {c.name: getattr(self, c.name) for c in self.__table__.columns})

    def __repr__(self):
        return "<User {}.{}>".format(self.user_id, self.telegram_handle)

class Task(db.Model):
    """Models a task to be completed by a user"""
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(64), nullable=False)
    datatype_id = db.Column(db.Integer, db.ForeignKey("spydatatype.spydatatype_id"))
    task_assigments = db.relationship("TaskAssignment")
    # TODO: validation_function
    # How to reference a function that can check whether available data suffices to complete a task?
    # Maybe hardcode "needed data" with placeholders/wildcards?

    def __repr__(self):
        return "<Task{}>".format(self.description[:12] + "...")

class TaskAssignment(db.Model):
    """Models an assigned (and maybe already completed) task to a user"""
    __tablename__ = "task_assignment"
    task_assignment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    task_id = db.Column(db.Integer, db.ForeignKey("task.task_id"))
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<TaskAssignment user:{} task:{}".format(self.user_id, self.task_id)
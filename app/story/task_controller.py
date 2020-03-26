"""Method collection to handle task assignment and completion"""
import app.story.story as story_code
from app import db
from app.firebase_interaction import FirebaseInteraction
from app.models.game_models import TaskAssignment
from app.models.game_models import User
from app.story.story import tasks


def assign_tasks(user_id, task_names):
    """Assigns all tasks of a story point to a user
    Triggers app update with new tasks"""

    for task_name in task_names:
        task_assignment = TaskAssignment()
        task_assignment.user_id = user_id
        task_assignment.task_name = task_name
        db.session.add(task_assignment)
        db.session.commit()

    new_tasks = [task_name_to_dict_for_app(task_name) for task_name in task_names]
    FirebaseInteraction.update_tasks(user_id, new_tasks)

def reset_tasks(user_id):
    """removes all tasks for a user"""
    for assignment in TaskAssignment.query.filter_by(user_id=user_id):
        db.session.delete(assignment)
    db.session.commit()

def task_name_to_dict_for_app(task_name):
    """returns the task dictionary for the app for a task name"""
    task = tasks[task_name]
    app_task = {key: task[key] for key in ["description", "datatype"]}
    app_task.update([
        ("name", task_name),
        ("permissionExplanation", task.get(
            "permission_explanation",
            "Zur Überprüfung des Tasks brauchen wir die folgende Berechtigung"
            )
        )
    ])
    return app_task

def get_incomplete_tasks(user_id):
    """Returns a list of incomplete tasks of a certain user"""
    user = User.get_user(user_id)
    return [task.task_name for task in user.task_assigments if not task.finished]

def task_validation_method(task_name):
    """Gets the python validation method symbol for a sepcific task"""
    validation_method = tasks[task_name]["validation_method"]
    return getattr(story_code, validation_method, None)
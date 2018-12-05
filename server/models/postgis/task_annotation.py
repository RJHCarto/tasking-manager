from server.models.postgis.utils import InvalidData, InvalidGeoJson, timestamp, NotFound
from server import db


class TaskAnnotation(db.Model):
    """ Describes Task annotaions like derived ML attributes """
    __tablename__ = "task_annotations"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'),  index=True)
    task_id = db.Column(db.Integer, nullable=False)
    annotation_type = db.Column(db.String, nullable=False)
    annotation_source = db.Column(db.String)
    updated_timestamp = db.Column(db.DateTime, nullable=False, default=timestamp)
    properties = db.Column(db.JSON, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint([task_id, project_id], ['tasks.id', 'tasks.project_id'], name='fk_task_annotations'), db.Index('idx_task_annotations_composite', 'task_id', 'project_id'), {})

    def __init__(self, task_id, project_id, annotation_type, annotation_source, properties):
        self.task_id = task_id
        self.project_id = project_id
        self.annotation_type = annotation_type
        self.annotation_source = annotation_source
        self.properties = properties

    def create(self):
        """ Creates and saves the current model to the DB """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Updates the DB with the current state of the Task Annotations """
        db.session.commit()

    def delete(self):
        """ Deletes the current model from the DB """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_task_annotation(task_id, project_id, annotation_type):
        """ Get annotations for a task with supplied type """
        return TaskAnnotation.query.filter_by(
            project_id=project_id, task_id=task_id, annotation_type=annotation_type).one_or_none()

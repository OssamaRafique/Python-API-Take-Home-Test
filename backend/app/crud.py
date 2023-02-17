from sqlalchemy.orm import Session
from . import models, schemas


def get_metrics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Metric).offset(skip).limit(limit).all()


def get_metric_by_code(db: Session, metric_code: str):
    return db.query(models.Metric).filter(models.Metric.metric_code == metric_code).first()


def create_metric(db: Session, metric: schemas.MetricCreate):
    db_metric = models.Metric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric
  
def get_values_by_metric_code(db: Session, metric_code: str, skip: int = 0, limit: int = 100):
    return db.query(models.ValueDefinition).filter(models.ValueDefinition.metric_code == metric_code).offset(skip).limit(limit).all()

def delete_metric(db: Session, metric_code: str):
    metric = db.query(models.Metric).filter(models.Metric.metric_code == metric_code).first()
    if metric:
        value_definitions = db.query(models.ValueDefinition).filter(models.ValueDefinition.metric_code == metric_code).all()
        for value_definition in value_definitions:
            db.delete(value_definition)
        db.delete(metric)
        db.commit()
    return metric

def get_value_definition(db: Session, value_definition_id: int):
    return db.query(models.ValueDefinition).filter(models.ValueDefinition.id == value_definition_id).first()

def get_value_definition_by_label(db: Session, label: str):
    return db.query(models.ValueDefinition).filter(models.ValueDefinition.value_label == label).first()

def get_value_definitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ValueDefinition).offset(skip).limit(limit).all()


def create_value_definition(db: Session, value_definition: schemas.ValueDefinitionCreate):
    db_value_definition = models.ValueDefinition(**value_definition.dict())
    db.add(db_value_definition)
    db.commit()
    db.refresh(db_value_definition)
    return db_value_definition


def update_value_definition(db: Session, value_definition_id: int, value_definition: schemas.ValueDefinitionUpdate):
    db_value_definition = db.query(models.ValueDefinition).filter(models.ValueDefinition.id == value_definition_id).first()
    if db_value_definition:
        for field, value in value_definition:
            setattr(db_value_definition, field, value) if value else None
        db.commit()
        db.refresh(db_value_definition)
    return db_value_definition


def delete_value_definition(db: Session, value_definition_id: int):
    db_value_definition = db.query(models.ValueDefinition).filter(models.ValueDefinition.id == value_definition_id).first()
    if db_value_definition:
        db.delete(db_value_definition)
        db.commit()
    return db_value_definition



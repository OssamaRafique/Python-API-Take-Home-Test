import csv
from pathlib import Path
from typing import List

from db import Base, SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas

# Define the FastAPI app
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Define the function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_csv_to_database(csv_path: str, db: Session):
    metrics = {}
    path = Path(__file__).parent/csv_path
    with path.open() as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            metric_code = row['metric_code']
            metric_description = row['metric_description']
            
            # check if metric already exists
            db_metric = crud.get_metric_by_code(db, metric_code=metric_code)
            if db_metric is None:
                # create new metric
                metric = schemas.MetricCreate(metric_code=metric_code, metric_description=metric_description)
                db_metric = crud.create_metric(db, metric=metric)
            
            metrics[metric_code] = db_metric
            
            # create value definition
            value_definition = schemas.ValueDefinitionCreate(value_label=row['value_label'], value_type=row['value_type'], metric_code=db_metric.metric_code)
            db_value_definition = crud.get_value_definition_by_label(db, label=value_definition.value_label)
            if db_value_definition is None:
                crud.create_value_definition(db, value_definition=value_definition)

load_csv_to_database("../resources/metrics.csv", SessionLocal())


@app.post("/metrics/", response_model=schemas.Metric)
def create_metric(metric: schemas.MetricCreate, db: Session = Depends(get_db)):
    db_metric = crud.get_metric_by_code(db, metric_code=metric.metric_code)
    if db_metric:
        raise HTTPException(status_code=400, detail="Metric code already registered")
    return crud.create_metric(db=db, metric=metric)

@app.get("/metrics/", response_model=List[schemas.Metric])
def read_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metrics = crud.get_metrics(db, skip=skip, limit=limit)
    return metrics

@app.get("/metrics/{metric_code}", response_model=schemas.Metric)
def read_metric(metric_code: str, db: Session = Depends(get_db)):
    db_metric = crud.get_metric_by_code(db, metric_code=metric_code)
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return db_metric

@app.get("/metrics/{metric_code}/values", response_model=List[schemas.ValueDefinition])
def get_values_by_metric_code(metric_code: str, db: Session = Depends(get_db)):
    db_metric = crud.get_metric_by_code(db, metric_code=metric_code)
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    db_values = crud.get_values_by_metric_code(db, metric_code=db_metric.metric_code)
    return db_values
  
@app.delete("/metrics/{metric_code}", response_model=schemas.Metric)
def delete_metric_by_code(metric_code: str, db: Session = Depends(get_db)):
    db_metric = crud.get_metric_by_code(db, metric_code=metric_code)
    if db_metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    crud.delete_metric(db, metric_code=db_metric.metric_code)
    return db_metric

@app.post("/value-definitions/", response_model=schemas.ValueDefinition)
def create_value_definition(value_definition: schemas.ValueDefinitionCreate, db: Session = Depends(get_db)):
    db_value_definition = crud.get_value_definition_by_label(db, label=value_definition.value_label)
    if db_value_definition:
        raise HTTPException(status_code=400, detail="Value definition already exists")
    return crud.create_value_definition(db=db, value_definition=value_definition)

@app.get("/value-definitions/", response_model=List[schemas.ValueDefinition])
def read_value_definitions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    value_definitions = crud.get_value_definitions(db, skip=skip, limit=limit)
    return value_definitions

@app.get("/value-definitions/{value_definition_id}", response_model=schemas.ValueDefinition)
def read_value_definition(value_definition_id: int, db: Session = Depends(get_db)):
    db_value_definition = crud.get_value_definition(db, value_definition_id=value_definition_id)
    if db_value_definition is None:
        raise HTTPException(status_code=404, detail="Value definition not found")
    return db_value_definition

@app.put("/value-definitions/{value_definition_id}", response_model=schemas.ValueDefinition)
def update_value_definition(value_definition_id: int, value_definition: schemas.ValueDefinitionUpdate, db: Session = Depends(get_db)):
    db_value_definition = crud.get_value_definition(db, value_definition_id=value_definition_id)
    if db_value_definition is None:
        raise HTTPException(status_code=404, detail="Value definition not found")
    return crud.update_value_definition(db=db, value_definition_id=db_value_definition.id, value_definition=value_definition)

@app.delete("/value-definitions/{value_definition_id}")
def delete_value_definition(value_definition_id: int, db: Session = Depends(get_db)):
    db_value_definition = crud.get_value_definition(db, value_definition_id=value_definition_id)
    if db_value_definition is None:
        raise HTTPException(status_code=404, detail="Value definition not found")
    crud.delete_value_definition(db=db, value_definition_id=db_value_definition.id)
    return {"message": "Value definition deleted"}
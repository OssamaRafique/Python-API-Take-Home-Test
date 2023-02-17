from typing import List, Optional

from pydantic import BaseModel


class ValueDefinitionBase(BaseModel):
    value_label: str
    value_type: str


class ValueDefinitionCreate(ValueDefinitionBase):
    metric_code: str

class ValueDefinitionUpdate(ValueDefinitionBase):
    value_label: Optional[str] = None
    value_type: Optional[str] = None

class ValueDefinition(ValueDefinitionBase):
    id: int
    metric_code: str

    class Config:
        orm_mode = True


class MetricBase(BaseModel):
    metric_code: str
    metric_description: str


class MetricCreate(MetricBase):
    pass


class Metric(MetricBase):
    id: int
    value_definitions: List[ValueDefinition] = []

    class Config:
        orm_mode = True

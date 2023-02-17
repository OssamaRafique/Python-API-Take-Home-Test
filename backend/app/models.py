from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_code = Column(String, unique=True, index=True)
    metric_description = Column(String)

    value_definitions = relationship("ValueDefinition", back_populates="metric")


class ValueDefinition(Base):
    __tablename__ = "value_definitions"

    id = Column(Integer, primary_key=True, index=True)
    metric_code = Column(String, ForeignKey("metrics.metric_code"))
    value_label = Column(String)
    value_type = Column(String)

    metric = relationship("Metric", back_populates="value_definitions")

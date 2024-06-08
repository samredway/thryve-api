from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()


# Create a base class for declarative_base that uses the mapper_registry
# for type resolution
class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor

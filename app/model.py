import logging
from datetime import datetime

from sqlalchemy import inspect
from uuid import uuid4
from .config import db


class Model(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__tablename__ = cls.__name__.lower()
        cls.logger = cls.setup_logger(cls.__name__)

    @staticmethod
    def setup_logger(name):
        """Set up a logger with the given name."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = True
        return logger

    def __repr__(self):
        mapper = inspect(self).mapper
        attrs = ', '.join(f"{column.key}={repr(getattr(self, column.key))}" for column in mapper.column_attrs)
        return f"<{self.__class__.__name__}({attrs})>"

    @classmethod
    def create(cls, obj=None, **kwargs):
        """Create a new record or update an existing one if the identifier is not unique."""
        try:
            # If an object is passed, extract its attributes
            if obj:
                obj_vars = {
                    key: value for key, value in vars(obj).items()
                    if not key.startswith('_') and hasattr(cls, key)
                }
            else:
                obj_vars = {}

            # Merge object vars with kwargs, giving precedence to kwargs
            filtered_kwargs = {
                key: value for key, value in {**obj_vars, **kwargs}.items()
                if not key.startswith('_') and hasattr(cls, key)
            }

            # Extract the identifiers from the filtered kwargs
            id = filtered_kwargs.get('id')
            uuid = filtered_kwargs.get('uuid')
            key = filtered_kwargs.get('key')
            mediaTagVersion = filtered_kwargs.get('mediaTagVersion')
            machineIdentifier = filtered_kwargs.get('machineIdentifier')
            ratingKey = filtered_kwargs.get('ratingKey')
            guid = filtered_kwargs.get('guid')
            
            # Check if a record with the given identifier already exists
            if mediaTagVersion:
                existing_record = cls.query.filter_by(mediaTagVersion=mediaTagVersion).first()
            elif machineIdentifier:
                existing_record = cls.query.filter_by(machineIdentifier=machineIdentifier).first()
            elif guid:
                existing_record = cls.query.filter_by(guid=guid).first()
            elif ratingKey:
                existing_record = cls.query.filter_by(ratingKey=ratingKey).first()
            elif key:
                existing_record = cls.query.filter_by(key=key).first()
            elif uuid:
                existing_record = cls.query.filter_by(uuid=uuid).first()
            elif id:
                existing_record = cls.query.filter_by(id=id).first()
            else:
                existing_record = None

            # If a record exists, check if there is a delta
            if existing_record:
                has_delta = any(
                    getattr(existing_record, key) != value
                    for key, value in filtered_kwargs.items()
                    if hasattr(existing_record, key)
                )

                if has_delta:
                    cls.logger.debug(f"Updating {cls.__name__} with ID {existing_record.id} due to changes.")
                    if not existing_record.uuid:
                        setattr(existing_record, "uuid", str(uuid4()))
                    for key, value in filtered_kwargs.items():
                        if hasattr(existing_record, key):
                            setattr(existing_record, key, value)
                    db.session.commit()
                    cls.logger.debug(f"Updated existing {cls.__name__}: {existing_record}")
                    return existing_record
                else:
                    cls.logger.debug(f"Existing record found. No changes detected for {cls.__name__} with ID {existing_record.id}.")
                    return existing_record
            else:
                # Create a new record if none exists
                if not filtered_kwargs.get("uuid"):
                    filtered_kwargs.update({"uuid": str(uuid4())})
                record = cls(**filtered_kwargs)
                db.session.add(record)
                db.session.commit()
                cls.logger.debug(f"Created {cls.__name__}: {record}")
                return record
        except Exception as e:
            cls.logger.error(f"Failed to create or update {cls.__name__}: {e}")
            db.session.rollback()
            raise


    @classmethod
    def get_by_id(cls, id):
        """Retrieve a record by its primary key if an integer is provided, or by its UUID if a string is provided."""
        try:
            if isinstance(id, int):
                # Retrieve by primary key (ID)
                record = db.session.get(cls, id)
            elif isinstance(id, str):
                # Retrieve by UUID
                record = cls.query.filter_by(uuid=id).first()
            else:
                cls.logger.error(f"Invalid type for id: {type(id)}. Expected int or str.")
                return None

            if record:
                cls.logger.info(f"Retrieved {cls.__name__}: {record}")
            else:
                cls.logger.warning(f"{cls.__name__} with id {id} not found.")
            return record
        except Exception as e:
            cls.logger.error(f"Failed to retrieve {cls.__name__} with id {id}: {e}")
            raise

    @classmethod
    def get(cls, **kwargs):
        """Retrieve records, optionally filtering by the given criteria."""
        try:
            if kwargs:
                # If filters are provided, apply them
                records = cls.query.filter_by(**kwargs).all()
                cls.logger.info(f"Retrieved {len(records)} {cls.__name__} records with filters {kwargs}.")
            else:
                # If no filters are provided, retrieve all records
                records = cls.query.all()
                cls.logger.info(f"Retrieved all {cls.__name__} records. Count: {len(records)}")
            return records
        except Exception as e:
            cls.logger.error(f"Failed to retrieve {cls.__name__} records with filters {kwargs}: {e}")
            raise

    def update(self, **kwargs):
        """Update the current record."""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            self.logger.info(f"Updated {self.__class__.__name__}: {self}")
            return self
        except Exception as e:
            self.logger.error(f"Failed to update {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise

    def delete(self):
        """Delete the current record."""
        try:
            record = self
            db.session.delete(self)
            db.session.commit()
            self.logger.info(f"Deleted {self.__class__.__name__}: {record}.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise

    

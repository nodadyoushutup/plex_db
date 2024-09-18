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
        cls._logger = cls.setup_logger(cls.__name__)
    
    def __repr__(self):
            mapper = inspect(self).mapper
            attrs = ', '.join(f"{column.key}={repr(getattr(self, column.key))}" for column in mapper.column_attrs)
            return f"<{self.__class__.__name__}({attrs})>"
        
    @staticmethod
    def setup_logger(name):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.DEBUG)
        _logger.propagate = True
        return _logger

    @classmethod
    def _get_obj_dict_kwargs(cls, _obj=None, _dict={}, **kwargs):
        if _obj:
            obj_vars = {
                key: value for key, value in vars(_obj).items()
                if not key.startswith('_') and hasattr(cls, key)
            }
        else:
            obj_vars = {}
        if _dict:
            dict_vars = {
                key: value for key, value in _dict.items()
                if not key.startswith('_') and hasattr(cls, key)
            }
        else:
            dict_vars = {}
        return {
            key: value for key, value in {**obj_vars, **dict_vars, **kwargs}.items()
            if not key.startswith('_') and hasattr(cls, key)
        }
    
    @classmethod
    def _get_delta(cls, existing_record, filtered_kwargs):
        delta = {}
        for key, value in filtered_kwargs.items():
            if hasattr(existing_record, key):
                current_value = getattr(existing_record, key)
                if current_value != value:
                    delta[key] = value
        return delta
    
    @classmethod
    def _set_delta(cls, existing_record, delta):
        for key, value in delta.items():
            if hasattr(existing_record, key):
                setattr(existing_record, key, value)
        
    @classmethod
    def create(cls, _obj=None, **kwargs):
        try:
            filtered_kwargs = cls._get_obj_dict_kwargs(_obj, **kwargs)
            if not filtered_kwargs.get("uuid"):
                filtered_kwargs.update({"uuid": str(uuid4())})
            new_record = cls(**filtered_kwargs)
            db.session.add(new_record)
            db.session.commit()
            cls._logger.debug(f"Created new {cls.__name__}: {new_record}")
            return new_record
        except Exception as e:
            cls._logger.warning(f"Failed to create {cls.__name__}: {e}")
            db.session.rollback()
            raise

    def update(self, **kwargs):
        try:
            delta = self._get_delta(self, kwargs)
            if delta:
                for key, value in delta.items():
                    setattr(self, key, value)  # Apply only the changed fields
                db.session.commit()
                self.logger.info(f"Updated {self.__class__.__name__}: {self}")
            else:
                self.logger.info(f"No changes detected for {self.__class__.__name__} with id {self.id}.")
            return self
        except Exception as e:
            self.logger.warning(f"Failed to update {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise

    @classmethod
    def upsert(cls, *args, _key="id", **kwargs):
        _obj = None
        _dict = None
        if len(args) == 1:
            if isinstance(args[0], dict):
                _dict = args[0]
            elif not isinstance(args[0], (str, int, set, list, tuple, dict)):
                _obj = args[0]
        elif len(args) >= 2:
            if len(args) == 2:
                print(type(args[1]))
                if isinstance(args[1], str):
                    _key = args[1]
            elif len(args) == 3:
                if isinstance(args[2], str):
                    _key = args[2]
            if isinstance(args[0], dict):
                _dict = args[0]
            if isinstance(args[1], dict):
                _dict = args[1]
            if not isinstance(args[0], (str, int, set, list, tuple, dict)):
                _obj = args[0]
            if not isinstance(args[1], (str, int, set, list, tuple, dict)):
                _obj = args[1]
        filtered_kwargs = cls._get_obj_dict_kwargs(_obj, _dict, **kwargs)
        if _key not in filtered_kwargs and not _key == "id":
            raise ValueError(f"Key '{_key}' not found in provided data for upsert.")
        try:
            existing_record = cls._get_existing_record(_key, filtered_kwargs)
            if existing_record:
                delta = cls._get_delta(existing_record, filtered_kwargs)
                if delta:
                    cls._logger.debug(f"Changes detected for {cls.__name__} with {_key} {filtered_kwargs[_key]}, applying updates.")
                    existing_record.update(**filtered_kwargs)  # Use the new update method
                else:
                    cls._logger.debug(f"No changes detected for {cls.__name__} with {_key} {filtered_kwargs[_key]}.")
                return existing_record
            else:
                cls._logger.debug(f"No existing {cls.__name__} found with the provided {_key}, creating a new one.")
                return cls.create(**filtered_kwargs)

        except Exception as e:
            cls._logger.warning(f"Failed to upsert {cls.__name__}: {e}")
            db.session.rollback()
            raise

    @classmethod
    def _get_existing_record(cls, key, kwargs):
        if key in kwargs and hasattr(cls, key):
            filter_by_value = {key: kwargs.get(key)}
            return cls.query.filter_by(**filter_by_value).first()
        return None
        
    @classmethod
    def get(cls, _id=None, _dict={}, **kwargs):
        # TODO: Make this work similar to the upsert where it can take args and kwargs in any way
        try:
            if _id and isinstance(_id, int):
                records = cls._get_existing_record("id", {"id": _id})
                cls._logger.info(f"Retrieved {len(records)} {cls.__name__} records with filters {kwargs}.")
            elif kwargs:
                records = cls.query.filter_by(**kwargs).all()
                cls._logger.info(f"Retrieved {len(records)} {cls.__name__} records with filters {kwargs}.")
            else:
                records = cls.query.all()
                cls._logger.info(f"Retrieved all {cls.__name__} records. Count: {len(records)}")
            return records
        except Exception as e:
            cls._logger.warning(f"Failed to retrieve {cls.__name__} records with filters {kwargs}: {e}")
            raise

    

    def delete(self):
        try:
            record = self
            db.session.delete(self)
            db.session.commit()
            self.logger.info(f"Deleted {self.__class__.__name__}: {record.id}.")
            return True
        except Exception as e:
            self.logger.warning(f"Failed to delete {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise


    

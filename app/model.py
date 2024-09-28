# model.py
import logging
from datetime import datetime
from typing import Any

from sqlalchemy import inspect, and_, or_
from uuid import uuid4
from .config import db


class Model(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__tablename__ = cls.__name__.lower()
        cls._logger = cls.setup_logger(cls.__name__)

    def __repr__(self):
        mapper = inspect(self).mapper
        attrs = ', '.join(
            f"{column.key}={repr(getattr(self, column.key))}" for column in mapper.column_attrs)
        return f"<{self.__class__.__name__}({self.id})>"

    @staticmethod
    def setup_logger(name):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.DEBUG)
        _logger.propagate = True
        return _logger

    @classmethod
    def _flatten_args_kwargs(cls, *args: (dict | object), **kwargs: Any):
        if not kwargs:
            kwargs = {}
        for arg in args:
            if isinstance(arg, dict):
                kwargs.update(
                    {k: v for k, v in arg.items() if hasattr(cls, k)})
            elif hasattr(arg, "__dict__"):
                kwargs.update(
                    {k: v for k, v in arg.__dict__.items() if hasattr(cls, k)})
        return kwargs

    @classmethod
    def _get_delta(cls, existing_record, flattened_kwargs):
        delta = {}
        for key, value in flattened_kwargs.items():
            if hasattr(existing_record, key):
                current_value = getattr(existing_record, key)
                if current_value != value:
                    delta[key] = value
        return delta

    @classmethod
    def _get_existing_record(cls, key, kwargs):
        if key in kwargs and hasattr(cls, key):
            return cls.query.filter_by(**{key: kwargs.get(key)}).first()
        return None

    @classmethod
    def create(cls, *args: (dict | list | set | object), **kwargs):
        try:
            flattened_kwargs = cls._flatten_args_kwargs(*args, **kwargs)
            if not flattened_kwargs.get("uuid"):
                flattened_kwargs.update({"uuid": str(uuid4())})
            new_record = cls(**flattened_kwargs)
            db.session.add(new_record)
            db.session.commit()
            cls._logger.debug(f"Created new {cls.__name__}: {new_record}")
            return new_record
        except Exception as e:
            cls._logger.warning(f"Failed to create {cls.__name__}: {e}")
            db.session.rollback()
            raise

    @classmethod
    def upsert(cls, *args, _key="id", **kwargs):
        try:
            flattened_kwargs = cls._flatten_args_kwargs(*args, **kwargs)
            existing_record = cls._get_existing_record(_key, flattened_kwargs)
            if existing_record:
                return existing_record.update(**flattened_kwargs)
            else:
                return cls.create(**flattened_kwargs)
        except Exception as e:
            cls._logger.warning(f"Failed to upsert {cls.__name__}: {e}")
            db.session.rollback()
            raise

    @classmethod
    def get(cls, *args, _first=False, **kwargs):
        if args and isinstance(args[0], int):
            kwargs.update({"id": args[0]})
        flattened_kwargs = cls._flatten_args_kwargs(*args, **kwargs)
        try:
            if flattened_kwargs:
                records = cls.query.filter_by(**flattened_kwargs)
                cls._logger.info(
                    f"Retrieved {len(records.all())} {cls.__name__} records with filters {flattened_kwargs}.")
            else:
                records = cls.query
                cls._logger.info(
                    f"Retrieved all {cls.__name__} records. Count: {len(records.all())}")
            if not _first:
                return records.all()
            else:
                return records.first()
        except Exception as e:
            cls._logger.warning(
                f"Failed to retrieve {cls.__name__} records with filters {flattened_kwargs}: {e}")
            raise

    @classmethod
    def search(cls, filters, _first=False, _any=False):
        try:
            query = cls.query
            operator_map = {
                '>': '__gt__',
                '<': '__lt__',
                '>=': '__ge__',
                '<=': '__le__',
                '==': '__eq__',
                '=': '__eq__',
                '!=': '__ne__',
                'like': 'like',
                'ilike': 'ilike'
            }
            filter_conditions = []
            for field, operator, value in filters:
                if hasattr(cls, field):
                    column_attr = getattr(cls, field)
                    if operator in operator_map:
                        filter_condition = getattr(
                            column_attr, operator_map[operator])(value)
                        filter_conditions.append(filter_condition)
            if filter_conditions:
                if not _any:
                    query = query.filter(and_(*filter_conditions))
                else:
                    query = query.filter(or_(*filter_conditions))
            records = query
            cls._logger.info(
                f"Search returned {len(records.all())} {cls.__name__} records with filters {filters}.")
            if not _first:
                return records.all()
            else:
                return records.first()
        except Exception as e:
            cls._logger.warning(
                f"Failed to search {cls.__name__} with filters {filters}: {e}")
            raise

    def update(self, *args, **kwargs):
        try:
            flattened_kwargs = self._flatten_args_kwargs(*args, **kwargs)
            delta = self._get_delta(self, flattened_kwargs)
            if delta:
                for key, value in delta.items():
                    setattr(self, key, value)
                self.updated_at = datetime.now()
                db.session.commit()
                self._logger.info(f"Updated {self.__class__.__name__}: {self}")
            else:
                self._logger.info(
                    f"No changes detected during update for {self.__class__.__name__} with id {self.id}.")
            return self
        except Exception as e:
            self._logger.warning(
                f"Failed to update {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise

    def delete(self):
        try:
            record = self
            db.session.delete(self)
            db.session.commit()
            self._logger.info(
                f"Deleted {self.__class__.__name__}: {record.id}."
            )
            return True
        except Exception as e:
            self._logger.warning(
                f"Failed to delete {self.__class__.__name__} with id {self.id}: {e}")
            db.session.rollback()
            raise

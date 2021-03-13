from sqlalchemy import exc, inspect

def sa_to_dict(obj):
    """
    Serialize SQLAlchemy object to dictionary.
    - https://stackoverflow.com/a/37350445
    - https://docs.sqlalchemy.org/en/14/core/inspection.html
    :param obj:
    :return:
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
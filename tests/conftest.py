import pytest
import sqlalchemy
from sqlalchemy import MetaData


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    """
    docker run -it --rm --publish=5432:5432 --env=POSTGRES_HOST_AUTH_METHOD=trust postgres:13.2
    """
    return "postgresql://postgres@localhost:5432/tunfish-test"


@pytest.fixture(scope="session")
def sqlalchemy_manage_db(request):
    return True


@pytest.fixture(scope="session")
def sqlalchemy_keep_db(request):
    return False


@pytest.fixture(scope="function")
def truncate_db(engine):
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    # https://gist.github.com/absent1706/3ccc1722ea3ca23a5cf54821dbc813fb
    # https://stackoverflow.com/questions/38112379/disable-postgresql-foreign-key-checks-for-migrations/38113838#38113838
    meta = MetaData(bind=engine, reflect=True)
    con = engine.connect()
    trans = con.begin()
    for table in meta.sorted_tables:
        con.execute(f"ALTER TABLE {table.name} DISABLE TRIGGER ALL;")
        con.execute(table.delete())
    trans.commit()


@pytest.fixture
def insert(dbsession):
    def inserter(entity):
        try:
            dbsession.add(entity)
            dbsession.commit()
        except sqlalchemy.exc.SQLAlchemyError as e:
            print(f"Error: {e}")
            dbsession.rollback()
        except Exception as e:
            print(f"{e}")

    return inserter

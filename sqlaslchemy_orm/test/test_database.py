from sqlalchemy.orm import Session

from sqlaslchemy_orm.database.core import Base, test_engine


class TestDatabase:

    def setup_class(self):
        Base.metadata.create_all(test_engine)
        self.session = Session()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_create_and_get_user(self):
        ...

    def test_create_multiple_users(self):
        ...

    def test_create_related(self):
        ...

    def test_delete(self):
        ...

    def test_delete_related(self):
        ...

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from sqlaslchemy_orm.database.models import User, Base
from sqlaslchemy_orm.database.core import test_engine


class TestDatabase:

    def setup_class(self):
        Base.metadata.create_all(test_engine)
        self.session = Session(test_engine)

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_create_and_get_user(self):
        user = User(
            username="test",
            password=generate_password_hash("mypass"),
            email="test@localhost",
            name="Oleg",
        )

        self.session.add(user)

        assert self.session.query(User).filter_by(username=user.username).first()

    def test_create_multiple_users(self):
        users = []

        for i in range(10):
            users.append(
                User(
                    username=f"test{i}",
                    password=generate_password_hash("mypass"),
                    email=f"test{i}@localhost",
                    name="Oleg",
                )
            )

        self.session.bulk_save_objects(users)
        assert self.session.query(User).count() >= 10

    def test_create_related(self):
        ...

    def test_delete(self):
        ...

    def test_delete_related(self):
        ...

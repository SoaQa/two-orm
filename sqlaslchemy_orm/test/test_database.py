from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from sqlaslchemy_orm.database.models import User, Base, Address, UserAddress
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
        user = User(
            username="test_create_related",
            password=generate_password_hash("mypass"),
            email="test_create_related@localhost",
            name="test_create_related",
        )

        address = Address(
            country="test_create_related",
            city="test_create_related",
            street="test_create_related",
            house_number=1,
        )

        # user_address = UserAddress()
        # user_address.user = user
        #
        # address.users.append(user_address)

        user_address = UserAddress(user=user, address=address)

        self.session.add(user_address)

        assert self.session.query(User).filter_by(username=user.username).first().addresses
        assert self.session.query(Address).filter_by(country=address.country).first().users

    def test_delete(self):
        user = User(
            username="test_delete",
            password=generate_password_hash("mypass"),
            email="test@localhost",
            name="Oleg",
        )
        self.session.add(user)

        assert self.session.query(User).filter_by(username=user.username).first()

        self.session.delete(user)

        assert not self.session.query(User).filter_by(username=user.username).first()

    def test_delete_related(self):
        user = User(
            username="test_delete_related",
            password=generate_password_hash("mypass"),
            email="test@localhost",
            name="Oleg",
        )

        address = Address(
            country="test_delete_related",
            city="test_delete_related",
            street="test_delete_related",
            house_number=1,
        )

        user_address = UserAddress(user=user, address=address)

        self.session.add(user_address)

        assert self.session.query(User).filter_by(username=user.username).first().addresses

        user.addresses.remove(user_address)
        self.session.delete(user_address)

        assert not self.session.query(User).filter_by(username=user.username).first().addresses

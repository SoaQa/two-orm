from django.contrib.auth.hashers import make_password
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from core.models import User, Address


class TestDatabase(TestCase):
    def test_create_and_get_user(self):
        user = User.objects.create(
            username="test",
            password=make_password("mypass"),
            email="test@localhost",
            name="Oleg",
        )

        assert User.objects.get(username=user.username)

    def test_create_multiple_users(self):
        users = []

        for i in range(10):
            users.append(
                User(
                    username=f"test{i}",
                    password=make_password("mypass"),
                    email=f"test{i}@localhost",
                    name="Oleg",
                )
            )

        User.objects.bulk_create(users)

        assert User.objects.count() >= 10

        print(User.objects.all())

    def test_create_related(self):
        with CaptureQueriesContext(connection) as ctx:
            user = User.objects.create(
                username="test",
                password=make_password("mypass"),
                email="test@localhost",
                name="Oleg",
            )

            address = Address.objects.create(
                country="test",
                city="test",
                street="test",
                house_number=1,
            )

            address.users.add(user)  # NoQa

            # user.addresses.add(address)

            assert address.users.exists()
            print(ctx.captured_queries)

    def test_delete(self):
        user = User.objects.create(
            username="test",
            password=make_password("mypass"),
            email="test@localhost",
            name="Oleg",
        )

        assert User.objects.get(username=user.username)

        user.delete()

        assert not User.objects.filter(username=user.username).exists()

    def test_delete_related(self):
        user = User.objects.create(
            username="test",
            password=make_password("mypass"),
            email="test@localhost",
            name="Oleg",
        )

        address = Address.objects.create(
            country="test",
            city="test",
            street="test",
            house_number=1,
        )

        address.users.add(user)  # NoQa

        assert address.users.exists()

        address.users.remove(user)
        # address.users.clear()
        # address.users.set(users)

        assert not address.users.exists()

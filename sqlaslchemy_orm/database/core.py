import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy import text
import dotenv
from sqlalchemy.orm import DeclarativeBase

dotenv.load_dotenv()


engine = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}",
    echo=True,
)

test_engine = create_engine(
    f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/test_{os.environ['DB_NAME']}",
    echo=True,
)


class Base(DeclarativeBase):
    ...


if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.all())

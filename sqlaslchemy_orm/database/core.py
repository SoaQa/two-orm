from sqlalchemy import create_engine
from sqlalchemy import text


engine = create_engine(
    "postgresql+psycopg2://mysqlalchemy:mysqlalchemy@localhost:15434/mysqlalchemy",
    echo=True,
)


with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

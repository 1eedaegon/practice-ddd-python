from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from src import model

# ORM은 객체-관계 매핑을 통해 저장하는 방식이 어떤 것인지 모르게 만든다.(영속성 무지)
# 데이터 저장이 추상화되면 도메인이 의존하지 않도록 유도할 수 있다.
# ORM은 도메인을 import하고 도메인은 ORM을 import 하지 않는다.
# ORM에 의존적인 도메인을 역전시켜 ORM이 도메인을 의존하게 만들고 (IoC)
# 지속적으로 다른 lib, infra를 도메인에 의존하게 만들어야 테스트가 쉬워진다.

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)
    mapper(
        model.Batch,
        batches,
        properties={"_allocations": relationship(lines_mapper, secondary=allocations, collection_class=set)},
    )

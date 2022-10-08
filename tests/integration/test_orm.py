from src import model


# ORM mapper를 테스트한다.
# DB에 들어있는 orderline을 orm mapper를 통해 가져와야한다.
def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        '("order1", "BLUE-DESK", 12),'
        '("order1", "BLUE-CHAIR", 13),'
        '("order2", "RED-LIPSTICK", 14)'
    )
    expeted = [
        model.OrderLine("order1", "BLUE-DESK", 12),
        model.OrderLine("order1", "BLUE-CHAIR", 13),
        model.OrderLine("order2", "RED-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expeted


# orderline을 orm mapper가 정상적으로 저장해야한다.
def test_orderline_mapper_can_save_lines(session):
    new_line = model.OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(new_line)
    session.commit()

    rows = list(session.execute('SELECT orderid, sku, qty FROM "order_lines"'))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]

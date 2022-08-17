from datetime import date

from src.model import Batch, OrderLine


# 주문라인을 배치에 할당하면 x단위만큼 가용재고 수량이 줄어든다.
def test_allocating_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "RED-CHARE", qty=10, eta=date.today())
    line = OrderLine("order-ref-001", "RED-CHARE", 2)
    batch.allocate(line)
    assert batch.available_quantity == 8


# 가용재고수량이 주문라인의 수량보다 크면 주문라인에 배치를 할당할 수 있다. O
def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("SHINY-MUGCUP", 20, 2)
    assert large_batch.can_allocate(small_line)


# 가용재고수량이 주문라인의 수량보다 낮으면 주문라인에 배치를 할당할 수 없다. X
def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("SHINY-MUGCUP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


# 가용재고수량이 주문라인의 수량과 같으면 주문라인에 배치를 할당할 수 있다. O
def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("SHINY-MUGCUP", 10, 10)
    assert batch.can_allocate(line)


# 제품이 다르면(SKU가 다르면) 배치에 주문라인을 할당할 수 없다.
def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-002", "UNCOMFORTABLE-SOPA", 10, eta=None)
    different_sku_line = OrderLine("order-002", "EXPENSIVE-DESK", 10)
    assert batch.can_allocate(different_sku_line) is False

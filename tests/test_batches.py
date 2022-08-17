from datetime import date

from src.model import Batch, OrderLine


def test_allocating_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "RED-CHARE", qty=10, eta=date.today())
    line = OrderLine("order-ref-001", "RED-CHARE", 2)

    batch.allocate(line)
    assert batch.available_quantity == 8

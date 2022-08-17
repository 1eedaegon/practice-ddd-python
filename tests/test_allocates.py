from datetime import date, timedelta

from src.model import Batch, OrderLine, allocate

today = date.today()
tomorrow = today + timedelta(1)
later = today + timedelta(99)


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-T-SHIRTS", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-T-SHIRTS", 100, eta=tomorrow)
    line = OrderLine("order-ref-001", "RETRO-T-SHIRTS", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-CHOP-STICK", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-CHOP-STICK", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-CHOP-STICK", 100, eta=later)

    line = OrderLine("order-ref-002", "MINIMALIST-CHOP-STICK", 10)

    allocate(line, [latest, earliest, medium])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "HIGHBROW-CUP", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "HIGHBROW-CUP", 100, eta=tomorrow)
    line = OrderLine("order-ref-001", "HIGHBROW-CUP", 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


# def test_raises_out_of_stock_exception_if_cannot_allocate():
#     batch = Batch("batch-010", "SMALL-BEAF", 100, eta=today)
#     allocate(OrderLine("order-ref-010", "SMALL-BEAF", 10), [batch])
#     with pytest.raises(OutOfStock, )

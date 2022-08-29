# E2E tests
# 인수테스트, 기능테스트, 통합테스트 구분없이 API를 이용해서 DB를 조작하는 테스트를 작성해보자.
# 우선 프로젝트에 테스트 도입을 위해 너무 엄격하지 않게 느린테스트와 빠른테스트로 구분한다.
import uuid

import config
import pytest
import requests


def random_suffix():
    return uuid.uuid4.hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation(add_stock):
    sku, othersku = random_sku(), random_sku("other")
    early_batch = random_batchref(1)
    later_batch = random_batchref(2)
    other_batch = random_batchref(3)
    add_stock([(later_batch, sku, 100, "2022-01-02"), (early_batch, sku, 100, "2022-01-01"), (other_batch, othersku, 100, None)])
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 201
    assert r.json()["batchref"] == early_batch

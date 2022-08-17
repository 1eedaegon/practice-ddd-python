from dataclasses import dataclass
from datetime import date
from typing import Optional


# dataclass: 아래와 같은 class의 boilerplate
# class User:
#     def __init__():
#         return
#     def __repr__(self) -> str:
#         pass
#     def __eq__(self, __o: object) -> bool:
#         pass
@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


# 행동이 있으므로 is not data
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty

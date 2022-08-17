from dataclasses import dataclass
from datetime import date
from typing import List, Optional

# dataclass: 아래와 같은 class의 boilerplate
# 값 객체의 연산을 쉽게 생성할 수 있다.
# class User:
#     def __init__():
#         return
#     def __repr__(self) -> str:
#         pass
#     def __hash__(self) -> None:
#         pass
#     def __eq__(self, __o: object) -> bool:
#         pass
# 값 객체 연산이 뭐나면:
# assert User('leedaegon', 31) == User('leedaegon', 31)
# assert Money('won', 50000) == Money('won', 50000)
# 지폐번호와 상관없이 5만원권과 5만원권은 5만원으로서 같다.
# *객체가 값이라는 뜻이 절대 아님


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


# 행동이 있으므로 is not dataclass
# 값이 아닌 정체적 동등성(identity equality)를 갖는 entity이므로
# __eq__, __hash__를 구현한다.
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # Optional[Set[OrderLine]] -> Set자체가 idempotent를 지킨다.

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self._purchased_quantity >= line.qty

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


# 도메인 서비스는 값객체나 엔티티로 표현할 수 없을 때가 있다.
# > 주어진 배치집합에 주문라인을 할당한다.
# 위 문구에 해당하는도메인 서비스 함수를 만들어 준다.
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    # 아래 Iterator의 sorted를 사용하려면
    # 비교 연산(__gt__)을 도메인 모델이 구현해야한다.
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference

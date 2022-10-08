import abc

from src.allocation.domain import model

# 무한정 저장 가능한 메모리가 있다고 가정하면 우리는 데이터베이스를 사용할 필요가 없다.
# 따라서 save()를 사용하지 않고 추가하거나 가져오기만 하면 된다.
# 이런 가정은 복잡한 내부 구현을 추상화하고
# 도메인 모델이 데이터베이스에 의존하는 관계를 끊어줄 수 있다.

# 자주 쓰는 상속구현 강제(factory pattern)
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        return self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        return self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)

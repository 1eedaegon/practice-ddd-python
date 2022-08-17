# Practice DDD on python

> How to TDD more easily

[Develop environment base link](https://gist.github.com/1eedaegon/cc23648cd2f92331c3f748be9cac4f03)

## Project install
```sh
make install
```

## Project teardown
```sh
make clean
```
## Formatting and linting
```sh
make lint
make format
```

## Running the tests
```sh
# Unit tests
make unit-test
# Integration test
make test
```
## Todos

- [x] [Domain modeling](https://github.com/1eedaegon/practice-ddd-python#domain-modeling)
- [ ] [Repository pattern](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Abstractions](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Usecase: service layer](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [TDD](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Unit of work](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Aggregate & consistency boundary](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Event driven](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Integrate microservices](https://github.com/1eedaegon/practice-ddd-python)
- [ ] [Dependency injection](https://github.com/1eedaegon/practice-ddd-python)

## Domain modeling
도메인 모델링 파트
> 비즈니스 관계자의 경험과 생각을 통해 도메인 모델과 규칙을 도출한다. 
> 초기에는 최대한 사례와 예시를 중심으로 비즈니스 전문가에게 이야기를 부탁해야한다. 
> 비즈니스 관계자의 이야기를 통해 도출한 도메인 모델은 다시 비즈니스 관계자에게 설명하고 이해가 가능해야한다.
> 이걸 DDD에선 유비쿼터스 언어라고 한다.
> (포스트잇이 제법 필요하다 ㅋㅋㅋ...)

### Example notes
```
제품(Product)은 SKU(Stock keeping unit)로 구분한다.
고객(Customer)는 주문(Order)을 넣는다.
주문은 주문참조번호(Order reference number)로 구분하고 주문라인(Order line)을 포함한다.

각 주문라인에는 SKU와 수량(Quantity)이 있다.
> RED-CHARE 10단위
> STAINLESS-POT 2단위 

구매팀은 재고를 작은 배치(Batch) 단위로 주문한다.
재고 배치는 ID(참조 번호), SKU, 수량으로 이뤄진다.
배치에 주문라인을 할당해야한다.
주문라인을 배치에 할당하면 해당 배치에 있는 재고를 고객의 주소로 배송한다.
어떤 배치의 재고를 주문라인에 x단위 만큼 할당하면
가용재고수량이 x만큼 줄어든다.
> 20단위 SMALL-TABLE로 이뤄진 배치가 있다.
> 2단위 SMALL-TABLE을 요구하는 주문라인이 있다.
> 주문 라인을 할당하면 18단위의 SMALL-TABLE이 남는다.

배치의 가용재고수량이 주문라인의 수량보다 낮으면 주문라인을 배치에 할당할 수 없다.
> 1단위 BLUE-CUSHION 배치가 있다.
> 2단위 BLUE-CUSHION 주문라인이 있다.
> 2단위의 주문라인을 1단위의 배치에 할당할 수 없다.

같은 주문라인을 두 번 할당할 수 없다.
> 10단위 BLUE-VASE 배치가 있다.
> 2단위 BLUE-VASE 주문라인이 있다.
> 10단위 BLUE-VASE 배치에 2단위 주문라인을 할당해야한다.
> 2단위 주문라인을 한번 더 할당하더라도 배치의 가용재고수량은 8단위여야한다.

배치가 현재 배송 중이면 ETA정보가 배치에 들어있다.
ETA가 없는 배치는 창고에 있는 배치이다.
창고 재고를 ETA 배치보다 먼저 할당해야한다.
배송 중인 배치를 할당할 땐 ETA가 작은 배치를 우선 할당한다.

```

## Ref
- [Architecture patterns with python](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205)
- [Cosmic python](https://www.cosmicpython.com/)

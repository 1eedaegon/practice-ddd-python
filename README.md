# Practice DDD on python

> How to TDD more easily

[Develop environment base link](https://gist.github.com/1eedaegon/cc23648cd2f92331c3f748be9cac4f03)

## Todos

- [ ] Domain modeling
- [ ] Repository pattern
- [ ] Abstractions
- [ ] Usecase: service layer
- [ ] TDD
- [ ] Unit of work
- [ ] Aggregate & consistency boundary
- [ ] Event driven
- [ ] Integrate microservices
- [ ] Dependency injection

## Domain modeling
도메인 모델링 파트
> 비즈니스 관계자의 경험을 통해 도메인 모델을 도출하고 규칙을 도출한다. 초기에는 최대한 사례를 중심으로 도출해낸다. 그리고 도메인 모델을 다시 비즈니스 관계자에게 설명할 수 있어야한다.
> DDD에선 유비쿼터스 언어라고 한다.

### Example notes
```
제품(Product)은 SKU(Stock keeping unit)로 식별된다.
고객(Customer)는 주문(Order)을 넣는다.
주문은 주문참조번호(Order reference number)로 식별되며 주문라인(Order line)을 포함한다.

각 주문라인에는 SKU와 수량(Amount)이 있다.
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
> 2단위 주문라인을 한번 더 할당하더라도 배치의 가용재고수량은 8단위가 되어야한다.

배치가 현재 배송 중이면 ETA정보가 배치에 들어있다.
ETA가 없는 배치는 창고에 있는 배치이다.
창고 재고를 ETA 배치보다 먼저 할당해야한다.
배송 중인 배치를 할당할 땐 ETA가 작은 배치를 우선 할당한다.

```

## Ref
[Architecture patterns with python](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205)
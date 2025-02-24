from pydantic import BaseModel, Field


class NewProduct(BaseModel):
    price: float = Field(ge=0.01, lt=10000, examples=[125, 325])
    title: str = Field(
        min_length=3, examples=["Пригоди бравого вояка Швейка. Подарункова класика"]
    )
    description: str = Field(
        min_length=20,
        max_length=1024,
        examples=[
            "І сам роман Ярослава Гашека «Пригоди бравого вояка Швейка», і його герой уже давно стали визначним явищем"
            " світової літератури. Мабуть, у жодному з воєнних романів ницість, безглуздість і жорстокість війни не"
            " показано так виразно, як у Гашековій книзі. Швейк не тільки увійшов у світову літературу, — він став одним"
            " із літературних типажів. Ох, який-бо він і справді бравий вояк, який хвацький оповідач, цей"
            " хитро-простакуватий, цей дуркувато-зворушливий Швейк, котрий (як про це не раз уже писалося й малювалося)"
            " разом з іншими літературними титанами, такими, як Гамлет чи Дон Кіхот, упевнено тримає на собі нашу"
            " читацьку планету."
        ],
    )
    cover: str = Field(
        examples=[
            "https://s.ababahalamaha.com.ua/images/o/rtBeILfwVcK54PZhW8ISAJ1LgjfgMikHyalLz9QL.png"
        ]
    )


class ProductId(BaseModel):
    id: str


class SavedProduct(ProductId, NewProduct):
    pass

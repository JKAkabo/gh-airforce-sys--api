from .base import BluestormModel


class RankCategoryBase(BluestormModel):
    name: str
    enabled: bool


class RankCategoryPublic(RankCategoryBase):
    id: int


class RankCategoryCreate(RankCategoryBase):
    pass


class RankCategoryUpdate(RankCategoryBase):
    pass


class RankCategory(RankCategoryBase):
    id: int

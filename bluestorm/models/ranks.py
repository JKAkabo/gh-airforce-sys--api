from bluestorm.models.base import BluestormModel


class RankBase(BluestormModel):
    name: str
    enabled: bool
    rank_category_id: int


class RankCreate(RankBase):
    pass


class RankPublic(RankBase):
    id: int


class RankUpdate(RankCreate):
    pass


class Rank(RankPublic):
    pass

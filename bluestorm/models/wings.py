from .base import BluestormModel


class WingBase(BluestormModel):
    name: str
    enabled: bool


class WingPublic(WingBase):
    id: int


class WingCreate(WingBase):
    pass


class WingUpdate(WingBase):
    pass


class Wing(WingBase):
    id: int

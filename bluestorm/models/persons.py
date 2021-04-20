from bluestorm.models.base import BluestormModel
from pydantic import Field, EmailStr
from typing import Optional, Union
import enum


class PersonType(str, enum.Enum):
    MILITARY = 'MILITARY'
    CIVILIAN = 'CIVILIAN'


class RankCategory(str, enum.Enum):
    OFFICER: 'OFFICER'
    SOLDIER: 'SOLDIER'
    CIVILIAN: 'CIVILIAN'


class OfficerRank(str, enum.Enum):
    PILOT_OFFICER: 'PILOT OFFICER'
    FLYING_OFFICER: 'FLYING OFFICER'
    FLIGHT_LIEUTENANT: 'FLIGHT LIEUTENANT'
    SQUADRON_LEADER: 'SQUADRON LEADER'
    WING_COMMANDER: 'WING COMMANDER'


class SoldierRank(str, enum.Enum):
    ACI: 'ACI'
    ACII: 'ACII'


class Wing(str, enum.Enum):
    SUPPLY: 'SUPPLY'
    FLYING: 'FLYING'
    ENGINEERING: 'ENGINEERING'
    ADMINISTRATION: 'ADMINISTRATION'


class PersonBase(BluestormModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = Field(min_length=10, max_length=10)
    rank_category: RankCategory
    rank: Optional[Union[OfficerRank, SoldierRank]] = None
    wing: Wing
    can_login: bool


class PersonCreate(PersonBase):
    pass


class PersonOut(PersonBase):
    key: str
    created_at: float
    updated_at: Optional[float]


class Person(PersonCreate, PersonOut):
    deleted_at: Optional[float]
    password: str = None


class PasswordResetIn(BluestormModel):
    token: str
    password: str


class PasswordResetRequestIn(BluestormModel):
    email: EmailStr
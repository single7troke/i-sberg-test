from pydantic import BaseModel
from typing import List, Dict


class Anagram(BaseModel):
	first_string: str = ''
	second_string: str = ''


class CheckAnagramResponse(BaseModel):
	is_anagram: bool
	counter: int


class CountOfType(BaseModel):
	dev_type: str
	count: int


class DevicesWithoutEndpoint(BaseModel):
	devices_by_type: List[CountOfType]



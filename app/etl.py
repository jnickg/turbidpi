from dataclasses import dataclass, field
from datetime import datetime

import const

@dataclass
class Readings:
	timestamp : datetime = field(default_factory=lambda: datetime.strftime(datetime.now(), const.DB_DATE_FORMAT))
	temp_c : float  = field(default=float('nan'))
	image : bytearray = field(default_factory=bytearray, repr=False)
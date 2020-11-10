from dataclasses import dataclass

from .attribute import Attribute
from .preference import Preference


@dataclass
class Quality:
    attribute: Attribute
    preference: Preference

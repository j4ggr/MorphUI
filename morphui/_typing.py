from typing import Type
from typing import TypeAlias

from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
from materialyoucolor.scheme.scheme_neutral import SchemeNeutral
from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
from materialyoucolor.scheme.scheme_content import SchemeContent


__all__ = [
    'MaterialDynamicScheme',]


MaterialDynamicScheme: TypeAlias = (
    Type[SchemeTonalSpot]
    | Type[SchemeExpressive]
    | Type[SchemeFruitSalad]
    | Type[SchemeMonochrome]
    | Type[SchemeRainbow]
    | Type[SchemeVibrant]
    | Type[SchemeNeutral]
    | Type[SchemeFidelity]
    | Type[SchemeContent])

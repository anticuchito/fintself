# This file makes the 'cl' directory a Python package.
# It exposes scrapers from this country so they can be imported from other modules.

from .banco_chile import BancoChileScraper
from .cencosud import CencosudScraper
from .santander import SantanderScraper
from .banco_falabella import BancoFalabellaScraper

__all__ = ["BancoChileScraper", "CencosudScraper", "SantanderScraper", "BancoFalabellaScraper"]

import re
from typing import List, Optional

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect, Locator

from fintself.core.exceptions import DataExtractionError, LoginError
from fintself.core.models import MovementModel
from fintself.scrapers.base import BaseScraper
from fintself.utils.logging import logger


class BancoFalabellaScraper(BaseScraper):
    """
    Scraper for Banco Falabella
    """

    LOGIN_URL = "https://www.bancofalabella.cl/"
    LOGIN_TIMEOUT = 45000

    def _get_bank_id(self) -> str:
        return "cl_banco_falabella"

    def _find_element_with_fallbacks(
        self, selectors: List[str], timeout: int = 5000, visible: bool = True
    ) -> Optional[Locator]:
        """Try multiple selectors and return the first one that works."""
        page = self._ensure_page()

        # Split timeout across all selectors
        selector_timeout = (
            max(1000, timeout // len(selectors)) if len(selectors) > 1 else timeout
        )

        for i, selector in enumerate(selectors):
            try:
                element = page.locator(selector)
                if visible:
                    if element.is_visible(timeout=selector_timeout):
                        logger.debug(
                            f"Found element with selector '{selector}' (attempt {i + 1})"
                        )
                        return element
                else:
                    if element.count() > 0:
                        logger.debug(
                            f"Found element with selector '{selector}' (attempt {i + 1})"
                        )
                        return element
            except Exception as e:
                logger.debug(f"Selector '{selector}' failed: {e}")
                continue

        logger.debug(f"No element found with any of {len(selectors)} selectors")
        return None

    def _click_with_fallbacks(self, selectors: List[str], timeout: int = 5000) -> bool:
        """Try to click using multiple selectors."""
        element = self._find_element_with_fallbacks(selectors, timeout)
        if element:
            try:
                element.click()
                return True
            except Exception as e:
                logger.warning(f"Failed to click element: {e}")
        return False

    def _type_with_fallbacks(
        self, selectors: List[str], text: str, timeout: int = 5000
    ) -> bool:
        """Try to type text using multiple selectors."""
        element = self._find_element_with_fallbacks(selectors, timeout)
        if element:
            try:
                element.fill(text)
                return True
            except Exception as e:
                logger.warning(f"Failed to type in element: {e}")
        return False

    def _login(self) -> None:
        """implements th elogin logic for Banco falabella"""
        assert self.user is not None, "User must be provided"
        assert self.password is not None, "Password must be provided"

        page = self._ensure_page()
        logger.info("Login into Banco Falabella")
        self._navigate(self.LOGIN_URL)
        self._save_debug_info("01_login_page")

        # Looking for login button - try multiple selectors

        my_account_selectors = [
            'button:has-text("Mi Cuenta")',
            'getByRole("button", { name: "Button" }).nth(1)',
        ]
        
        my_account_clicked = self._click_with_fallbacks(my_account_selectors)
        if not my_account_clicked:
            raise LoginError("Could not find 'Mi cuenta'")
        

        input_username_selectors = []

         
        

      

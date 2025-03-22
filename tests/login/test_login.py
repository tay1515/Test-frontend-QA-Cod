import sys

import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from pages.LoginPage import LoginPage
from pages.ProductListPage import ProductListPage
from controller.ShoppingCartController import ShoppingCartController


@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_shopping_cart(set_up_tear_down, username, password):
    set_up_tear_down.goto("https://www.saucedemo.com/")
    # credentials = {'username':'standard_user', 'password':'secret_sauce'}
    login_p = LoginPage(set_up_tear_down)
    products = login_p.do_login(username, password)
    products.buy_product_cart(2)
    products.personal_information("Tyrone", "Zapata", "050033")
    products.validate_visible_text_pay_information()
    products.scroll_total_price_products()
    products.validate_total_price_products()
    products.validate_purchase_tax()
    products.validate_total_purchase()
    products.complete_purchase()
    products.successful_purchase()
    set_up_tear_down.close()

import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from pages.LoginPage import LoginPage


def test_shopping_cart(set_up_tear_down):
    set_up_tear_down.goto("https://www.saucedemo.com/")
    credentials = {'username':'standard_user', 'password':'secret_sauce'}
    login_p = LoginPage(set_up_tear_down)
    products = login_p.do_login(credentials)
    products.buy_items(4)
    expect(products.personal_information).to_be_visible(timeout=600)
    assert str(products.total_price_products_add) == str(products.validate_total_price_products), "error con los datos de compra"
    products.complete_purchase()
    expect(products.msg_successful_purchase).to_have_text("Thank you for your order!", timeout=200)
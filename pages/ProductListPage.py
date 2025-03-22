import random
from datetime import time
import time
from idlelib import browser
from threading import Thread
import unittest

from playwright.sync_api import expect


class ProductListPage:


    def __init__(self, page):
        self.page = page
        self._products_header = page.locator("span.title")
        self._list_products = page.locator("//div[@class='inventory_item_name ']")
        self._enter_shopping_cart = page.locator("//div[@id='shopping_cart_container']")
        self._icon_quantity_of_products_added = page.locator("//span[@class='shopping_cart_badge']")
        self._btn_checkout = page.locator("//button[@id='checkout']")
        self._input_firt_name = page.locator("//input[@id='first-name']")
        self._input_last_name = page.locator("//input[@id='last-name']")
        self._input_postal_code = page.locator("//input[@id='postal-code']")
        self._btn_continue = page.locator("//input[@id='continue']")
        self._lbl_pay_information = page.locator("//div[@class='summary_info_label' and text()='Payment Information:']")
        self._lbl_total_price_products = page.locator("//div[@class='summary_subtotal_label']")
        self._lbl_your_information = page.locator("//span[@class='title']")
        self._lbl_tax = page.locator("//div[@class='summary_tax_label']")
        self._lbl_total_purchase = page.locator("//div[@class='summary_total_label']")
        self._btn_finish = page.locator("//button[@id='finish']")
        self._lbl_msg_successful_purchase = page.locator("//h2[@class='complete-header']")


    #@property
    #def products_header(self):
    #    return self._products_header

    def enter_firt_name(self, firt_name):
        self._input_firt_name.clear()
        self._input_firt_name.fill(firt_name)

    def enter_last_name(self, last_name):
        self._input_last_name.clear()
        self._input_last_name.fill(last_name)

    def enter_postal_code(self, postal_code):
        self._input_postal_code.clear()
        self._input_postal_code.fill(postal_code)

    @property
    def list_name_products(self):
        return self._list_products

    @property
    def icon_quantity_of_products_added(self):
        return self._icon_quantity_of_products_added

    def click_shopping_cart(self):
        self._enter_shopping_cart.click()

    def click_checkout(self):
        self._btn_checkout.click()


    def form_personal_information(self, f_name, l_name, p_code):
        self.enter_firt_name(f_name)
        self.enter_last_name(l_name)
        self.enter_postal_code(p_code)

    def click_continuo(self):
        self._btn_continue.click()

    @property
    def lbl_pay_info(self):
        return self._lbl_pay_information

    def scroll_lbl_total_price_products(self):
        self._lbl_total_price_products.scroll_into_view_if_needed()

    @property
    def item_total_price_products(self):
        return self._lbl_total_price_products

    @property
    def lbl_tax_products(self):
        return self._lbl_tax

    @property
    def total_price_purchase(self):
        return self._lbl_total_purchase

    @property
    def msg_successful_purchase(self):
        return self._lbl_msg_successful_purchase

    def complete_purchase(self):
        self._btn_finish.click()

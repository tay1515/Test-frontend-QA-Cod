import decimal
import locale
import math
import random
from datetime import time
import time
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from idlelib import browser
from threading import Thread
import unittest

from playwright.sync_api import expect
from pages.ProductListPage import ProductListPage


class ShoppingCartController(ProductListPage):

    total_price_products = 0
    detail_product = []
    detail_products_cart = []

    def __init__(self, page):
        self.page = page
        super().__init__(page)


    def search_product_id(self, quantity_products):
        list_select_product = []
        product_list = self.list_name_products

        if quantity_products == 0:
            raise Exception(
                "la cantidad 0 no se permite")

        if quantity_products <= product_list.count():
            while True:
                num_ramdon = random.randint(0, product_list.count() - 1)
                item = product_list.all_inner_texts()[num_ramdon]
                if item not in list_select_product:
                    list_select_product.append(item)
                    if len(list_select_product) == quantity_products:
                        break
        else:
            raise Exception(
                "la cantidad de productos ingresada sobrepasa a la cantidad de produtos contenida en la pagina")

        print("List random: " + str(list_select_product))

        return list_select_product


    def choose_products_to_buy(self, quantity_products):
        search_product_id = self.search_product_id(quantity_products)

        # total_price_products = 0
        total_products_add = 0

        self.detail_product = []
        name_products = []
        for product_name in search_product_id:
            print("Product id: " + str(product_name))
            product_detail = self.page.locator(
                f"//div[@class='inventory_item_name ' and text()='{product_name}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_desc']")
            product_price = self.page.locator(
                f"//div[@class='inventory_item_name ' and text()='{product_name}']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']")
            time.sleep(3)
            print(
                "Product name: " + str(
                    name_products) + " \nProduct detail: " + product_detail.inner_text() + " \nProduct price: " + product_price.inner_text())
            self.detail_product.append(product_name)
            self.detail_product.append(product_detail.inner_text())
            self.detail_product.append(product_price.inner_text())

            # con este nombre se realizara la busqueda de cada producto en el apartado del carrito de compras
            name_products.append(product_name)

            time.sleep(4)
            # hacer scroll hasta el boton de agregar y agregar producto
            self.page.locator(
                f"//div[@class='inventory_item_name ' and text()='{product_name}']/ancestor::div[@class='inventory_item']//button").scroll_into_view_if_needed()
            self.page.locator(
                f"//div[@class='inventory_item_name ' and text()='{product_name}']/ancestor::div[@class='inventory_item']//button").click()

            price_format = (product_price.inner_text()).replace("$", "")
            self.total_price_products += float(price_format)
            total_products_add = total_products_add + 1
            time.sleep(2)

        print("Total price products add: " + str(self.total_price_products))
        print("Total products add: " + str(total_products_add))
        # print("Name products: " + str(name_products))

        ## despues de seleccionados los productos se procede a ingresar al carrito de compras
        self._enter_shopping_cart.scroll_into_view_if_needed()
        expect(self.icon_quantity_of_products_added).to_have_text(str(total_products_add))
        self.click_shopping_cart()

        return name_products

    def buy_product_cart(self, quantity_products):

        name_products = self.choose_products_to_buy(quantity_products)
        time.sleep(4)
        # recorreto todos los productos del carrito de compras y los almacena en una lista con su respectivo detalle
        self.detail_products_cart = []
        for item in name_products:
            print("Name: " + str(item))
            product_name_cart = self.page.locator(
                f"//div[@class='inventory_item_name' and text()='{item.strip()}']/ancestor::div[@class='cart_item_label']//div[@class='inventory_item_name']")
            product_descrip_cart = self.page.locator(
                 f"//div[@class='inventory_item_name' and text()='{item.strip()}']/ancestor::div[@class='cart_item_label']//div[@class='inventory_item_desc']")
            product_price_cart = self.page.locator(
                f"//div[@class='inventory_item_name' and text()='{item.strip()}']/ancestor::div[@class='cart_item_label']//div[@class='inventory_item_price']")
            time.sleep(3)

            self.detail_products_cart.append(product_name_cart.inner_text())
            self.detail_products_cart.append(product_descrip_cart.inner_text())
            self.detail_products_cart.append(product_price_cart.inner_text())
            #self.page.wait_for_timeout(1200)
            time.sleep(3)

        print("Detail products:::: " + str(self.detail_product))
        print("Detail products cart: " + str(self.detail_products_cart))

        time.sleep(3)
        # Valida el detalle de los productos seleccionados con el detalle de los productos del carrito de compras
        assert str(self.detail_product) == str(self.detail_products_cart), "error no coincide el detalle de los productos agregados con los del carrito de compras"

        self.click_checkout()

    def personal_information(self, f_name, l_name, p_code):
        self.form_personal_information(f_name, l_name, p_code)
        self.click_continuo()

    def validate_visible_text_pay_information(self):
        expect(self.lbl_pay_info).to_be_visible(timeout=2000)

    def scroll_total_price_products(self):
        self.scroll_lbl_total_price_products()

    def validate_total_price_products(self):
        expect(self.item_total_price_products).to_contain_text(str(self.total_price_products), timeout=200)

    @property
    def calculate_tax(self):
        total_purchase = self.total_price_products
        print("totalllll " + str(total_purchase))
        tax = (float(total_purchase) * 8) / 100
        format_tax = round(tax, 2)
        #dollar_dec = float(tax[1:])
        print("format round: " + str(format_tax))
        return str(format_tax)

    def validate_purchase_tax(self):
        expect(self.lbl_tax_products).to_contain_text(self.calculate_tax, timeout=200)

    @property
    def calculate_total_purchase(self):
        subtotal = (self.item_total_price_products.inner_text()).replace("Item total: $", "")
        tax = (self.lbl_tax_products.inner_text()).replace("Tax: $", "")
        total = float(subtotal) + float(tax)
        return str(total)

    def validate_total_purchase(self):
        expect(self.total_price_purchase).to_contain_text(self.calculate_total_purchase, timeout=200)

    def successful_purchase(self):
        expect(self.msg_successful_purchase).to_have_text("Thank you for your order!", timeout=200)


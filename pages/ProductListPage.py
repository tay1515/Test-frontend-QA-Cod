import random
from datetime import time
import time
from threading import Thread
import unittest

from playwright.sync_api import expect


class ProductListPage:

    total_price_products= 0
    detail_product = []
    detail_products_cart = []


    def __init__(self, page):
        self.page = page
        self._products_header = page.locator("span.title")
        self._list_products = page.locator("//div[@class='inventory_item']//button")
        self._list_products2 = page.locator("//div[@class='inventory_item_name ']")
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
        self._btn_finish = page.locator("//button[@id='finish']")
        self._lbl_msg_successful_purchase = page.locator("//h2[@class='complete-header']")


    @property
    def products_header(self):
        return self._products_header

    def enter_firt_name(self, firt_name):
        self._input_firt_name.clear()
        self._input_firt_name.fill(firt_name)

    def enter_last_name(self, last_name):
        self._input_last_name.clear()
        self._input_last_name.fill(last_name)

    def enter_postal_code(self, postal_code):
        self._input_postal_code.clear()
        self._input_postal_code.fill(postal_code)

    def click_continuo(self):
        self._btn_continue.click()

    def search_product_id2(self, quantity_products):
        list_select_product = []
        product_list = self._list_products.count()
        print(product_list)

        while True:
            num_ramdon = random.randint(1, product_list)
            if num_ramdon not in list_select_product:
                list_select_product.append(num_ramdon)
                if len(list_select_product) == quantity_products:
                    break
        print("List random: " + str(list_select_product))

        return list_select_product

    def search_product_id(self, quantity_products):
        list_select_product = []
        product_list = self._list_products2
        print(product_list.all_inner_texts())

        while True:
            num_ramdon = random.randint(1, product_list.count())
            print("rm::: " + str(num_ramdon))
            item = product_list.all_inner_texts()[num_ramdon]
            print("item::: " + str(item))
            if item not in list_select_product:
                list_select_product.append(item)
                print("lenttt " + str(len(list_select_product)))
                if len(list_select_product) == quantity_products:
                    break
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
                "Product name: " + str(name_products) + " \nProduct detail: " + product_detail.inner_text() + " \nProduct price: " + product_price.inner_text())
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
        expect(self._icon_quantity_of_products_added).to_have_text(str(total_products_add))
        self._enter_shopping_cart.click()

        return name_products


    def buy_items(self, quantity_products):

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
        assert str(self.detail_product) == str(self.detail_products_cart), "error no coicide el detalle de los productos agregados con los del carrito de compras"

        self._btn_checkout.click()


    @property
    def personal_information(self):
        self.enter_firt_name("Tyrone")
        self.enter_last_name("Zapata")
        self.enter_postal_code("050033")
        self.click_continuo()

        return self._lbl_pay_information

    @property
    def validate_total_price_products(self):
        self._lbl_total_price_products.scroll_into_view_if_needed()
        price_format = self._lbl_total_price_products.inner_text().replace("Item total: $", "")
        return price_format

    @property
    def total_price_products_add(self):
        return self.total_price_products

    @property
    def msg_successful_purchase(self):
        return self._lbl_msg_successful_purchase

    def complete_purchase(self):
        self._btn_finish.click()

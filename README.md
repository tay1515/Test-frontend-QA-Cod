
# Proyecto frontend carrito de compras

Realizar flujo de compra en la pagina https://www.saucedemo.com/


## Instalar librerías

En la raíz del proyecto se ubica el archivo "requirements.txt" en el cual se encuentra consignadas las librerías a instalar:

    1. Abrir consola o terminal
    2. Ejecutar comando: pip install -r requirements.txt

## Flujo de caso de prueba (end to end)

Para ejecutar correctamente la prueba se debe de ejecutar la función "test_shopping_cart" ubicada en la clase "test_login", esta requiere de la parametrización de la linea 11 "buy_items(parametro)", en la cual se indica la cantidad de productos a comprar.

Observación: El flujo de prueba fue hecho con la capacidad de que el sistema por medio de la cantidad de productos a comprar realice la validación del detalle de cada ítem seleccionado hasta el final de la compra.


## Ejecución prueba

Comando terminal:  
- pytest -s



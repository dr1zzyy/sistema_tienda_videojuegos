TIENDA GAMEZONE
=

El sistema permite al usuario, ver el catalogo completo, buscar juegos mediante el Codigo de cada juego,ver su carrito, manejar productos en su carrito mediante el Codigo de un juego. Finalizar la compra, con un ticket que muestra los productos, precios, descuentos y impuestos. Mostrando un total redondeado

**El sistema usa JSON para almacenar el catalogo y el carrito**


**🛍️ Catalogo**
-
> - Permite ver el catalogo completo, con el codigo, nombre, precio, y existencias en el inventario de cada producto.
> - Permite buscar individualmente cada producto mediante el codigo.
> - Al agregar o eliminar del carrito se actualizan las existencias de cada producto.

**🛒 Carrito**
-

> - El carrito se guarda en un archivo json.
> - Se agregan productos mediante el ID(CODIGO) de un producto y la cantidad.
> - Se elimina un producto mediante el ID
> - Se finaliza la compra de todos los productos del carrito.
> - Si se vuelve a agregar un producto que ya esta en el carrito, se acumula en la cantidad, no se crea otra linea separada.

**🏷️ Cupon de descuento**
-

> - Al iniciar la finalizacion de la compra se le pregunta al usuario si cuenta con algun cupon de descuento.
> - Al agregarlo correctamente se descuentan $50.

**🥇 Producto mas vendido**
-

> - Se muestra tambien en una opcion cual fue el producto mas vendido y cuantas ventas acumulo.

**Casos de prueba**
-

| Prueba | Datos o llamada | Resultado esperado | Resultado obtenido |
|:---|:---|:---|:---|
| Búsqueda válida | `buscar_producto(catalogo, 'G001')` | Producto DOOM Eternal. | Producto DOOM Eternal. |
| Búsqueda inválida | `buscar_producto(catalogo, 'X999')` | `None`. | None |
| Existencia suficiente | `hay_existencia(5, 3)` | `True`. | True |
| Existencia insuficiente | `hay_existencia(2, 4)` | `False`. | False |
| Cantidad no válida | `hay_existencia(5, 0)` | `False`. | False|
| Importe de línea | `calcular_importe(499, 2)` | `$998.00`. | $998.00|
| Total sin descuento | `calcular_total(500)` | `$580.00`. | $580.00|
| Total con descuento | `calcular_total(1200, descuento=0.10)` | `$1,252.80`. | $1,252.80|
| Existencia actualizada | `actualizar_existencia(8, 3)` | `5 unidades`. | 5 unidades|

**Prueba de escritorio**
-

| Solicitud | Código | Cantidad | ¿Se acepta? | Importe / motivo | Existencia después |
|:---:|:---:|:---:|:---:|:---|:---:|
| 1 | G002 | 2 | Sí | $998.00 | 3 |
| 2 | G001 | 3 | Sí | $2,097.00 | 2 |
| 3 | G005 | 12 | No | Existencia insuficiente: solicitadas 12, disponibles 10 | 10 |
| 4 | G003 | 1 | Sí | $1,199.00 | 2 |
| 5 | G002 | 1 | Sí | $499.00 | 2 |
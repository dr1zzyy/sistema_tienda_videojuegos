# Calcula el precio (juegos x cantidad)
def importe(precios:dict):

    out = 0.0
    for precio in precios.keys():
        total = precio * precios[precio]
        out += total
        
    return round(out, 2)

# Calcula el total final, aplicando descuento si supera 1000
# Agregando el impuesto y descontando $50 si hubo cupon
def total(cantidad:int, descuento=0.0, impuesto=0.16, valor_cupon=0.0):

    out = cantidad
    desc = 0.0
    
    if cantidad >= 1000:
        desc = cantidad*(descuento)
        out = cantidad-desc
    else:
        desc = 0.0

    out -= valor_cupon

    imp = out * impuesto
    out = out+imp
    
    return round(out),desc,imp,valor_cupon
    
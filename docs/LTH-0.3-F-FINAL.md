# Leather 0.3-F — BASE System Final

Status: VERIFIED

## Scope

LTH 0.3-F introduces a real `base` abstraction layer while preserving
the frozen LTH 0.2 core and the previously verified 0.3 A-E layers.

## Supported syntax

```lth
base Product {
    price = 100
    active = true
}

base VIPProduct extends Product {
    discount = 0.20
}

item = VIPProduct({"price": 250})

# coding: utf-8
from __future__ import unicode_literals


LOOKUP = {
    "Aberaeron":"2657850",
    "Abertawe":"2636432",
    "Aberteifi":"2653818",
    "Abertyleri":"2657784",
    "Aberystwyth":"2657782",
    "Bangor":"2656397",
    "Caerdydd":"2653822",
    "Caerfyrddin":"2653755",
    "Casnewydd":"2641598",
    "Castell Nedd":"2641843",
    "Dinbych":"2651386",
    "Garndolbenmaen":"8299867",
    "Hwlffordd":"2647311",
    "Llandudno":"2644120",
    "Llangefni":"2644037",
    "Merthyr Tudful":"2642705",
    "Pen-y-bont ar Ogwr":"2654755",
    "Pontypridd":"2640104",
    "Pwllheli":"2639828",
    "Y Barri":"2656235",
    "Y Trallwng":"2634560",
    "Yr Wyddgrug":"2642372",
}

def get_bbc_location_id(placename):
    if placename in LOOKUP:
        return LOOKUP.get(placename)
    else:
        return 0


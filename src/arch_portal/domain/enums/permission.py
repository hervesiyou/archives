from enum import Enum


class PermissionEnum(Enum):
    VOIR_FAM = "VOIR_FAMILLE"
    VOIR_COM = "VOIR_COMMUNAUTE"
    VOIR_MAR = "VOIR_MARCHE"

    ADD_FAM = "ADD_FAMILLE"
    ADD_COM = "ADD_COMMUNAUTE"
    ADD_MAR = "ADD_MARCHE"
    ADD_ASSO = "ADD_ASSOCIATION"

    ADD_EVEN = "ADD_EVENEMENT"
    ADD_LIB = "ADD_LIBRAIRIE"
    ADD_LIV = "ADD_LIVRE"
    COM_LIV = "COMMANDER_LIVRE"
    ADD_MEM = "ADD_MEMBRE"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

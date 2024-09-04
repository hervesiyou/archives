from enum import Enum


class RoleEnum(Enum):
    COMM_CHEF = "COMM_CHEF"
    COMM_USER = "COMM_USER"
    COMM_ADMIN = "COMM_ADMIN"
    FAM_CHEF = "FAM_CHEF"
    FAM_USER = "FAM_USER"
    FAM_ADMIN = "FAM_ADMIN"
    ASS_USER = "ASS_USER"
    ASS_ADMIN = "ASS_ADMIN"
    LIB_MANAGER = "LIB_MANAGER"
    LIB_USER = "LIB_USER"


    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

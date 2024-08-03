from dataclasses import dataclass


@dataclass
class MembreException(Exception):
    message:str
from hashlib import md5
import math


class Pakuri():
    def __init__(self, name, species, level=0):
        self._name = name
        self._species = species
        self._level = level
        self._attack = int.from_bytes(md5(species.encode('UTF-8')).digest(), 'little') % 16 + \
                       int.from_bytes(md5(name.encode('UTF-8')).digest(), 'little') % 16
        self._defense = (int.from_bytes(md5(species.encode('UTF-8')).digest(), 'little')+5) % 16 + \
                        (int.from_bytes(md5(name.encode('UTF-8')).digest(), 'little')+5) % 16
        self._stamina = (int.from_bytes(md5(species.encode('UTF-8')).digest(), 'little')+11) % 16 + \
                        (int.from_bytes(md5(name.encode('UTF-8')).digest(), 'little')+11) % 16

    def get_name(self):
        return self._name

    name = property(get_name)

    def get_species(self):
        return self._species

    species = property(get_species)

    def get_hp(self):
        return math.floor(self._stamina * self._level / 6)

    hp = property(get_hp)

    def get_cp(self):
        return math.floor(self._attack * math.sqrt(self._defense) * math.sqrt(self._stamina) * self._level * 0.08)

    cp = property(get_cp)

    def get_level(self):
        return self._level

    def set_level(self, new_level):
        self._level = new_level

    level = property(get_level, set_level)


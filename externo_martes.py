""" Paradigmas de Programación, curso 2023/24
    Código externo para la primera práctica
    Versión de las defensas del martes
    (c) César Vaca
"""


class CartaBase(object):
    def __init__(self, ind):
        self.ind = ind

    @property
    def valor(self):
        return min(10, self.ind % 13 + 1)


class Estrategia(object):

    def __init__(self, num_barajas):
        self.cuenta = 0

    def cuenta_carta(self, carta):
        self.cuenta += 1

    def apuesta(self, apu_lo, apu_med, apu_hi):
        if self.cuenta % 3 == 0:
            return apu_hi
        elif self.cuenta % 3 == 1:
            return apu_med
        else:
            return apu_lo

    def jugada(self, croupier, jugador):
        vj = sum(c.valor for c in jugador)
        if any(c.valor == 1 for c in jugador) and vj < 12:
            vj += 10
        if vj == 20:
            return 'P'
        if vj == 11:
            return 'D'
        return 'P' if vj < 19 else 'C'


class Mazo(object):
    NUM_BARAJAS = 2

    def __init__(self, clase_carta, estrategia):
        self.clase = clase_carta
        self.estrategia = estrategia
        self.cartas = []

    def reparte(self):
        if len(self.cartas) == 0:
            inds = [8,21,34,37,0,50,47,35,25,10,4]
            self.cartas = [self.clase(i) for i in inds]
        c = self.cartas.pop()
        if self.estrategia is not None:
            self.estrategia.cuenta_carta(c)
        return c
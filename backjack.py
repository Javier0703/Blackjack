"""Práctica creada por Javier Calvo Porro
   Estudiante de PAR, 1º Ingeniería Informática, UVa, 2023,24
"""

from externo import CartaBase, Estrategia, Mazo
import random

#Creacion de clases/funciones para el programa

class Carta(CartaBase):
   #Clase Carta --> Herencia de Carta Base
   def __init__(self, ind):
      super().__init__(ind)
      super().valor
   
   def values(self):
      numCartasPorPalo = 13
      palos = ["♠","♣","♥","♦"]
      #Indice --> Indice de la carta (1-13)
      indice = (self.ind%numCartasPorPalo)+1
      #num --> Indice de la carta (A,2,4,10,J,K...)
      if indice == 1:
         num = "A"
      elif indice == 11:
        num = "J"
      elif indice == 12:
        num = "Q"
      elif indice == 13:
        num = "K"
      else:
        num = str(indice)

      #Palo de la carta
      palo = palos[self.ind//numCartasPorPalo]

      #Lista con los detalles de la carta [Valor, Indice, Palo]
      return [self.valor,num,palo]

class Mano():
   def __init__(self,datos,indice,name,apuesta):
      self.apuesta = apuesta
      self.name = name
      self.estado = "Activa"
      self.datos = datos
      self.indice = indice
      self.valorCartas = self.getCardValues()
      self.sumaCartas = self.sumaTotal()

   def getCardValues(self):
      cartasPorMano = []
      for dato in self.datos:
         cartasPorMano.append(dato.values())      
      return cartasPorMano
   
   def sumaTotal(self):
      maxValue = 21
      val = 10
      card = 'A'
      cartaAS = False
      n = 0
      for carta in self.valorCartas:
         n += carta[0]
         if carta[1] == card:
            cartaAS = True
      #Comprobamos si es mejor opcion sumar 11 en vez de 1
      if n <=(maxValue-val) and cartaAS == True:
         n += val
      return n
   
   def printMano(self):


#Main

def main():
   #Modos de juego del BlackJack, inicializacion de variables: balance, tipos de apuesta...
   balance = 0
   tipoApuesta = [2,10,50]
   gameMode = ['J','A']
   msg = "*** BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/24 ***\n¿Modo de ejecución? [J]uego [A]nálisis: "
   #Creacion del BlackJack
   r = input(msg).upper()
   if r in gameMode:
      gamesToPlay = 1
      game = 1

      #Seleccion del numero de juegos si es modo Analisis:
      if r == "A":
         while True:
            gamesToPlay = input("¿Número de partidas?: ")
            if gamesToPlay.isdigit():
               gamesToPlay = int(gamesToPlay)
               break  
            else:
               print("Por favor, ingresa un número entero válido.")
   
      #Inicio del Juego
               
      #Creacion de la estrategia y del mazo a usar
      estrategia = Estrategia(Mazo.NUM_BARAJAS)
      mazo = Mazo(Carta, estrategia)

      while game<=gamesToPlay:

         #Numero de partida y pregunta de la apuesta
         print(f"--- INICIO DE LA PARTIDA #{game} --- BALANCE = {balance} €")
         apuestaStr= "[" + "] [".join(str(i) for i in tipoApuesta) + "]"
         msg = "¿Apuesta? " + apuestaStr + " "

         while True:
            apIncorrecta = "Apuesta seleccionada incorrecta"
            apuesta = input(msg)
            if apuesta.isdigit():
               apuesta = int(apuesta)
               if apuesta in tipoApuesta:
                  break
               else:
                  print(apIncorrecta)
            else:
               print(apIncorrecta)
         
         #Ya tenemos apuesta:
         print("REPARTO INICIAL")

         #Se le genera una mano tanto al Coupier como al jugador
      
         #Variable donde guarda el numero de cartas del copier 
         cartsInitCoupier = 1
         Coupier = []
         for _ in range(cartsInitCoupier):
            Coupier.append(mazo.reparte())

         #Lista con listas de cartas (manos) que tiene el jugador
         cartsInitJugador = 2
         ManoJugador = [[]]
         for _ in range(cartsInitJugador):
            ManoJugador[0].append(mazo.reparte())

         print((Mano(ManoJugador[0],0,"Mano")).valorCartas)
         print((Mano(ManoJugador[0],0,"Mano")).sumaCartas)
         

         break




   else:
      print("Modo de juego incorrecto")
 
main()



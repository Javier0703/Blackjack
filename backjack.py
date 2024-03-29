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
   
   def values(self):
      numCartasPorPalo = 13
      palos = ["♠","♣","♥","♦"]
      #Devuelve una lista con la informacion de la carta:
      #valorNumerico --> Peso de la carta (1-10)
      valorNumerico = (self.ind%numCartasPorPalo)+1
      #num --> Numero carta (1,4,10,J,K...)
      num = valorNumerico
      if num>10:
         valorNumerico = 10
         if num == 11:
            num = "J"
         elif num == 12:
            num = "Q"
         else:
            num = "K" 
      #Palo de la carta
      palo = palos[self.ind//numCartasPorPalo]
      return (valorNumerico,num,palo)

estrategia = Estrategia(Mazo.NUM_BARAJAS)
mazo = Mazo(Carta, estrategia)

#Modos de juego del BlackJack, apuestas y balance:
balance,apuesta = 0,0
tipoApuesta = [2,10,50]
gameMode = ['J','A']
msg = "*** BLACKJACK - PARADIGMAS DE PROGRAMACION 2023/24 ***\n¿Modo de ejecución? [J]uego [A]nálisis: "

#Creacion de nuestras clases

def main():
   #Creacion del BlackJack
   r = input(msg).upper()
   if r in gameMode:

      gamesToPlay = 1
      game = 1 

      #Modo de juego seleccionado
      if r == "A":
         while True:
            gamesToPlay = input("¿Número de partidas?: ")
            if gamesToPlay.isdigit():  # Verificar si la entrada es un número entero
               gamesToPlay = int(gamesToPlay)
               break  
            else:
               print("Por favor, ingresa un número entero válido.")
      
      #Seleccionado los juegos en el caso de modo Analisis
      estrategia = Estrategia(Mazo.NUM_BARAJAS)
      mazo = Mazo(Carta, estrategia)
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())
      print(mazo.reparte().values())


   else:
      print("Modo de juego incorrecto")
 
main()



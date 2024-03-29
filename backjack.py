"""Práctica creada por Javier Calvo Porro
   Estudiante de PAR, 1º Ingeniería Informática, UVa, 2023,24
"""

from externo import CartaBase, Estrategia, Mazo

#Creacion de clases/funciones para el programa

class Carta(CartaBase):
   #Clase Carta --> Herencia de Carta Base
   def __init__(self, ind):
      super().__init__(ind)
   
   def values(self):
      numCartasPorPalo = 13
      palos = ["♠","♣","♥","♦"]
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

      #Tupla con los detalles de la carta
      return (valorNumerico,num,palo)

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
         

         game +=1
         break
         estrategia = Estrategia(Mazo.NUM_BARAJAS)
         mazo = Mazo(Carta, estrategia)



   else:
      print("Modo de juego incorrecto")
 
main()



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
      #num --> Numero/Letra de la carta (A,2,4,10,J,K...)
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
   def __init__(self,datos,nombre,apuesta):
      #Datos necesarios de la mano: Cartas para el manejo de ellas
      self.datos = datos
      self.nombre = nombre
      self.estado = 'Activa'
      self.apuesta = apuesta
      self.valorCartas = self.getCardValues()
      self.sumaCartas = self.sumaTotal()

   #Funcion que devuelve el valor de las cartas de la mano (de la clase Carta)
   def getCardValues(self):
      cartasPorMano = []
      for dato in self.datos:
         cartasPorMano.append(dato.values())      
      return cartasPorMano
   
   #Funcion que devuelve el valor de la mano completa y
   def sumaTotal(self):
      maxValue = 21
      card = 'A'
      val = 10
      cartaAS = False
      n = 0
      for carta in self.valorCartas:
         #Sumamos el valor de la carta
         n += carta[0]
         #Comprobamos si la carta es un AS
         if carta[1] == card:
            cartaAS = True
      #Comprobamos si es mejor opcion sumar 11 en vez de 1
      if n <=(maxValue-val) and cartaAS == True:
         n += val
      return n
   
   """#Definimos la apuesta para las manos del jugador
   def setApuesta(self, apuesta):
      self.apuesta = apuesta"""

   #Impresion de cartas: Manejo con lista para cada linea (concatenacion de manos)
   
   def imprimirCroupier(self):
      nombre = f"{self.nombre}"+":"
      valor = f"({self.sumaCartas})"
      if len(nombre)>len(self.estado):
         estado =" "*(len(nombre)-len(self.estado))+f"{self.estado}"
         l2Valor = " "*(len(nombre)-len(valor))+f"{valor}"
         l4Espace = " "*len(nombre)
      else:
         estado = self.estado
         nombre =" "*(len(self.estado)-len(nombre))+f"{nombre}"
         l2Valor = " "*(len(estado)-len(valor))+f"{valor}"
         l4Espace = " "*len(self.estado)

      numCartas = len(self.valorCartas)
      self.l1 = f"{nombre}"+("╭───╮"*numCartas)
      self.l2 = l2Valor
      self.l3= f"{estado}"+"│"+f"{self.valorCartas[0][2]}  "+"│"
      self.l4 = f"{l4Espace}"+("╰───╯"*numCartas)
      return [self.l1,self.l2,self.l3,self.l4]

     


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
            #Aqui selecciona la apuesta
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

         #Se le genera una(s) mano(s) tanto al Croupier como al jugador
         #Inicialmente son 2 
         """
         La metodología empleada es la siguiente:
            - cartasPorMano : Numero de cartas por cada mano
            - Copier/Jugador: Lista con las diferentes manos iniciales 
            (supuesto caso que se pidan jugar con 2 o lo que sea)
            - manoCroupier, manoJugador : Lista con objetos tipo Mano, para su impresion
            Bucle donde se almacenan las cartas en las manos
         """

         #Croupier
         cartasPorMano = 1
         #El numero de Listas dentro de la lista define las manos que hay
         Croupier, manoCroupier = [[]], [[]]
         for _ in range(cartasPorMano):
            for i in range(len(Croupier)):
               Croupier[i].append(mazo.reparte())
         l = Mano(Croupier[0],'Croupier',apuesta).imprimirCroupier()
         print(l[0])
         print(l[1])
         print(l[2])
         print(l[3])

         #Usuario
         cartasPorMano = 2
         #El numero de Listas dentro de la lista define las manos que hay
         Jugador,manoJugador = [[]], [[]]
         for _ in range(cartasPorMano):
            for i in range(len(Jugador)):
               Jugador[i].append(mazo.reparte())
         l = Mano(Jugador[0],'Mano',apuesta).imprimirCroupier()
         print(l[0])
         print(l[1])
         print(l[2])
         print(l[3])
         break




   else:
      print("Modo de juego incorrecto")
 
main()



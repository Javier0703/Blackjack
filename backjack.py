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
      figuras = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
      #Num --> Indice de la carta (A-K)
      num = str(figuras[self.ind%numCartasPorPalo])
      #Palo de la carta
      palo = palos[self.ind//len(figuras)]
      #Lista con los detalles de la carta [Valor, Indice, Palo]
      return [self.valor,num,palo]

class Mano():
   def __init__(self,datos,nombre,apuesta):
      #Datos necesarios de la mano: Cartas para el manejo de ellas
      self.datos = datos
      self.nombre = nombre
      self.estado = 'Activa'
      self.apuesta = apuesta
      self.valorCartas = self.getCardValues()   #Lista con la lista de cartas
      self.sumaCartas = self.sumaTotal()        #Valor de la mano
      #Comprobamos el numero para modificar o no el estado (Modificaciones del profesor)
      self.comprobarSuma()

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
   
   def comprobarSuma(self):
      if self.estado == 'Activa' and self.sumaCartas>21:
         self.estado == 'PASADA'
   
   #Impresion de cartas: Manejo con lista para cada linea (concatenacion de manos)
   #Damos Forma a las cartas
   def formaCarta(self):
      self.valorMano = f"({self.sumaCartas})"
      self.apuestaIcono = f"{self.apuesta}"+"€"
      self.nombreTrans = f"{self.nombre}"+":"
      #Comprobaciones
      if len(self.nombreTrans)>=len(self.estado):
         self.espaciado = " "*len(self.nombreTrans)
         self.valorMano = " "*(len(self.nombreTrans)-len(self.valorMano))+f"{self.valorMano}"
         self.apuestaIcono = " "*(len(self.nombreTrans)-len(self.apuestaIcono))+f"{self.apuestaIcono}"
         self.estado = " "*(len(self.nombreTrans)-len(self.estado))+f"{self.estado}"
      else:
         self.espaciado = " "*len(self.estado)
         self.valorMano = " "*(len(self.estado)-len(self.valorMano))+f"{self.valorMano}"
         self.apuestaIcono = " "*(len(self.estado)-len(self.apuestaIcono))+f"{self.apuestaIcono}"
         self.nombreTrans = " "*(len(self.estado)-len(self.nombreTrans))+f"{self.nombreTrans}"

      #Aqui damos la forma a la propia carta (o cartas)
      numCartas = len(self.valorCartas)
      self.l1 = ("╭───╮"*numCartas)
      self.l2, self.l3 = "",""
      for i in range(len(self.valorCartas)):
         self.l2 +="│"+(" "*(3-len(self.valorCartas[i][1])))+f"{self.valorCartas[i][1]}"+"│"
         self.l3 +="│"+f"{self.valorCartas[i][2]}  "+"│"
      self.l4 = ("╰───╯"*numCartas)

   #cartas Coupier
   def imprimirCoupier(self):
      self.formaCarta()
      line1 = self.nombreTrans+self.l1 
      line2 = self.valorMano+self.l2
      line3 = self.estado+self.l3
      line4 = self.espaciado+self.l4
      return [line1,line2,line3,line4]

   def imprimirJugador(self):
      self.formaCarta()
      line1 = self.nombreTrans+self.l1 
      line2 = self.valorMano+self.l2
      line3 = self.apuestaIcono+self.l3
      line4 = self.estado+self.l4
      return [line1,line2,line3,line4]
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
         l = Mano(Croupier[0],'Croupier',apuesta).imprimirCoupier()
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
         l = Mano(Jugador[0],'Mano',apuesta).imprimirJugador()
         print(l[0])
         print(l[1])
         print(l[2])
         print(l[3])
         break




   else:
      print("Modo de juego incorrecto")
 
main()



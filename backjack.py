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
         self.estado = 'PASADA'
   
   #Impresion de cartas: Manejo con lista para cada linea (concatenacion de manos)
   #Damos Forma a las cartas
   def formaCarta(self):
      
      #Modificaciones para la el print posterior
      self.nombreTrans = f"{self.nombre}"+":"      
      self.valorMano = f"({self.sumaCartas})"
      self.apuestaIcono = f"{self.apuesta}"+"€"
      #Comprobacion del dato mas largo (para imprimirlo de manera deluxe)
      maxi = max(len(self.nombreTrans), len(self.estado), len(self.apuestaIcono))
      self.estado = self.estado.rjust(maxi)
      self.nombreTrans = self.nombreTrans.rjust(maxi)
      self.valorMano = self.valorMano.rjust(maxi)
      self.apuestaIcono = self.apuestaIcono.rjust(maxi)
      self.espaciado = " " * maxi

      #Aqui damos la forma a la propia carta (o cartas)
      numCartas = len(self.valorCartas)
      self.l1 = "╭───╮" * numCartas
      self.l2, self.l3 = "", ""
      for i in range(len(self.valorCartas)):
         self.l2 += "│" + (" " * (3 - len(self.valorCartas[i][1]))) + f"{self.valorCartas[i][1]}" + "│"
         self.l3 += "│" + f"{self.valorCartas[i][2]}  " + "│"
      self.l4 = "╰───╯" * numCartas

   #cartas Coupier
   def imprimirCroupier(self):
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
   
def imprimirManos(listas):
    #Longitud de las manos (Debe ser 4)
    maximo = max(len(sublista) for sublista in listas)
    for i in range(maximo):
        elementos = []
        for sublista in listas:
            elementos.append(str(sublista[i]))
        #Cada elemento se separa con un " | "
        print(" │ ".join(elementos))


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
            - manoCroupier, manoJugador : Lista con objetos tipo Mano, para su utilizacion
            Bucle donde se almacenan las cartas en las manos
         """

         #Croupier --> Si las manos iniciales son mas de 1, el nombre es CropierA, CroupierB...
         nombre = 'Croupier'
         letter = 'A'
         centinela = 0
         cartasPorMano = 1

         Croupier, manoCroupier,imprimirCroupier = [[]], [], []
         for i in range(len(Croupier)):
            for _ in range(cartasPorMano):
               Croupier[i].append(mazo.reparte())
         for element in Croupier:
            if len(Croupier)>1:
               tmpName = nombre+str(chr(ord(letter) + centinela))
               centinela+=1
               manoCroupier.append(Mano(element,tmpName,apuesta))
            else:   
               manoCroupier.append(Mano(element,nombre,apuesta))


         #Usuario -->Si las manos iniciales son mas de 1, los nombres seran ManoA, ManoB ...
         letter = 'A'
         centinela = 0
         cartasPorMano = 2
         nombre = 'Mano'
        
         Jugador,manoJugador,imprimirJugador = [[],[]], [], []
         for i in range(len(Jugador)):
            for _ in range(cartasPorMano):
               Jugador[i].append(mazo.reparte())
         for element in Jugador:
            if len(Jugador)>1:
               tmpName = nombre+str(chr(ord(letter) + centinela))
               centinela+=1
               manoJugador.append(Mano(element,tmpName,apuesta))
            else:   
               manoJugador.append(Mano(element,nombre,apuesta))

         #Aqui ya tenemos guardadas todas las manos en manoJugador y manoCroupier
         #Son de tipo Mano, lo que transformamos las manos en formato carta para su impresion
         for mano in manoCroupier:
            imprimirCroupier.append(mano.imprimirCroupier())

         for mano in manoJugador:
            imprimirJugador.append(mano.imprimirJugador())
         imprimirManos(imprimirCroupier)
         imprimirManos(imprimirJugador)
         
         break




   else:
      print("Modo de juego incorrecto")
 
main()



"""Práctica creada por Javier Calvo Porro
   Estudiante de PAR, 1º Ingeniería Informática, UVa, 2023,24
"""

from externo import CartaBase, Estrategia, Mazo

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
      #Actualizamos los datos de la mano
      self.actualizarDatosMano()

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
      #Metodo para comprobar la suma de las cartas
      if self.estado == 'Activa' and self.sumaCartas>21:
         self.estado = 'PASADA'

   def addCarta(self,cartaNueva):
      #Metodo de añadir una Carta nueva (Pedir/Doblar)
      self.datos.append(cartaNueva)

   def doblarApuesta(self):
      #Doblar apuesta al seleccionar (Doblar)
      self.apuesta = self.apuesta*2
      self.estado = 'Cerrada'

   def actualizarDatosMano(self):
      # Se ejecuta al crear la instancia de una mano para obtener la suma, su estado y el valor de las crtas
      # Metodo ejecutado por las acciones donde hay modificaciones de estructuras
      # Metodos --> Pedir, Doblar, Separar
      self.valorCartas = self.getCardValues()  
      self.sumaCartas = self.sumaTotal()
      self.comprobarSuma()       
   
   #Impresion de cartas: Manejo con lista para cada linea (concatenacion de manos)
   #Damos Forma a las cartas
   def formaCarta(self):
      
      #Modificaciones para la el print posterior
      self.nombreTrans = f"{self.nombre}"+":"      
      self.valorMano = f"({self.sumaCartas})"
      self.apuestaIcono = f"{self.apuesta}"+"€"
      #Comprobacion del dato mas largo (para imprimirlo de manera deluxe alineadamente)
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

   #Cartas Coupier
   def imprimirCroupier(self):
      self.formaCarta()
      line1 = self.nombreTrans+self.l1 
      line2 = self.valorMano+self.l2
      line3 = self.estado+self.l3
      line4 = self.espaciado+self.l4
      return [line1,line2,line3,line4]

   #Cartas Jugador
   def imprimirJugador(self):
      self.formaCarta()
      line1 = self.nombreTrans+self.l1 
      line2 = self.valorMano+self.l2
      line3 = self.apuestaIcono+self.l3
      line4 = self.estado+self.l4
      return [line1,line2,line3,line4]

def transMano(mano,impresion,name):
   #Metodo para transformar la mano (Tipo Mano) a la lista con sublista para su impresion
   impresion = []
   if name == 'Croupier':
      for m in mano:
         impresion.append(m.imprimirCroupier())
   else:
      for m in mano:
         impresion.append(m.imprimirJugador())      
   return impresion

 
def imprimirManos(listas):
    #Longitud de las manos (Debe ser 4)
    maximo = max(len(sublista) for sublista in listas)
    for i in range(maximo):
        elementos = []
        for sublista in listas:
            elementos.append(str(sublista[i]))
        #Cada elemento se separa con un " | "
        print(" │ ".join(elementos))

def comprobarManosActivas(manos):
   cent = 0
   for mano in manos:
      if mano.estado == 'Activa':
         cent +=1
   return cent      


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
         print(f"\n--- INICIO DE LA PARTIDA #{game} --- BALANCE = {balance} €")
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
         print("\nREPARTO INICIAL")

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
         #POSIBILIDAD DE CREAR UNA FUNCION PARA ESTO
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


         #Usuario --> Si las manos iniciales son mas de 1, los nombres seran ManoA, ManoB ...
         letter = 'A'
         centinela = 0
         cartasPorMano = 2
         nombre = 'Mano'
        
         Jugador,manoJugador,imprimirJugador = [[]], [], []
         #POSIBILIDAD DE CREAR UNA FUNCION PARA ESTO
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
         
         imprimirCroupier = transMano(manoCroupier,imprimirCroupier,'Croupier')
         imprimirJugador = transMano(manoJugador,imprimirJugador,'Jugador')
        
         #Imprimimos las manos   
         imprimirManos(imprimirCroupier)
         imprimirManos(imprimirJugador)
         
         #Comprobacion de BlackJack
         gameEnd = False
         for manoJ in manoJugador:
            if manoJ.sumaCartas == 21:
               dinero = round(apuesta*(1.5))
               #Se realiza BlackJack
               print("*****************\n*** BLACKJACK ***\n*****************\n")
               print("Ha ganado "+ f"{dinero}"+ " €!")
               balance += dinero
               gameEnd = True
               break

         if gameEnd == True:
            #El juego ha acabado con BlackJack
            while True:
               volverJugar = input("¿Otra partida? [S/N] ").upper()
               if volverJugar == 'S' or volverJugar == 'N':
                  break
            
            if volverJugar == 'S':
               game+=1
               gamesToPlay+=1

            else:
               print("\nBALANCE FINAL: "+f"{balance}"+" €")
               break

         else:
            #No hay BlackJack se continua con el juego
            print("\nTURNO EL JUGADOR")
            #Comprobamos las manos activas
            manosActivas = comprobarManosActivas(manoJugador)
            while manosActivas>0:
               for i in range(len(manoJugador)):
                  #Comprobamos si el estado de esa mano está activa
                  if manoJugador[i].estado == 'Activa':
                     #Usaremos una lista de acciones donde las que el usuario podra hacer
                     jugada = "¿Jugada para la "+f"{manoJugador[i].nombre}"+"?"+" [P]edir [D]oblar [C]errar "
                     acciones = ['P','D','C']
                     #Comprobar si la jugada contiene 2 cartas iguales para la accion de separar
                     if (len(manoJugador[i].valorCartas) == 2) and (manoJugador[i].valorCartas[0][0] == manoJugador[i].valorCartas[1][0]):
                        acciones.append('S')
                        jugada = jugada+str("[S]eparar ")
                     accion = input(jugada).upper()

                     while True:
                        if accion not in acciones:
                           accion = input("Accion invalida. "+jugada).upper()
                        else:
                           break

                     #Accion seleccionada correctamente    
                     #Accion de Cerrar:   
                     if accion == 'C':
                        manoJugador[i].estado = 'Cerrada'
                     
                     #Accion de Pedir
                     if accion == 'P':
                        manoJugador[i].addCarta(mazo.reparte())
                        #Actualizamos sus datos mediante el metodo
                        manoJugador[i].actualizarDatosMano()


                  #Imprimimos de nuevo las manos

                  #Comprobamos las manos Activas de nuevo      
                  manosActivas = comprobarManosActivas(manoJugador)

            #Break de cierre de programa 
            break



   else:
      print("Modo de juego incorrecto")
 
main()



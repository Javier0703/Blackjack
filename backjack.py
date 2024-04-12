"""Práctica creada por Javier Calvo Porro Estudiante de PAR, 1º Ingeniería Informática, UVa, 2023,24"""
from externo import CartaBase, Estrategia, Mazo

#Creacion de clases/funciones/Variables para el programa
palosCarta = ["♠","♣","♥","♦"]
figurasPalo = ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']
numCartas = len(figurasPalo)

class Carta(CartaBase):
   #Clase Carta --> Herencia de Carta Base
   def __init__(self, ind):
      super().__init__(ind)
      super().valor
   
   def values(self):
      numCartasPorPalo = numCartas
      palos = palosCarta
      figuras = figurasPalo
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
      if self.estado == 'Activa':
         if self.sumaCartas > 21:
            self.estado = 'PASADA'
         if self.sumaCartas == 21:
            self.estado = 'Cerrada'   

   def addCarta(self,cartaNueva):
      #Metodo de añadir una Carta nueva (Pedir/Doblar)
      self.datos.append(cartaNueva)

   def doblarApuesta(self):
      #Doblar apuesta al seleccionar (Doblar)
      self.apuesta = self.apuesta*2
      self.estado = 'Cerrada'

   def actualizarDatosMano(self):
      # Se ejecuta al crear la instancia de una mano para obtener la suma, su estado y el valor de las cartas
      # Metodo ejecutado por las acciones donde hay modificaciones de estructuras. Metodos --> Pedir, Doblar, Separar
      self.valorCartas = self.getCardValues()  
      self.sumaCartas = self.sumaTotal()
      self.comprobarSuma()       
   
   def doblarApuesta(self):
      #Metodo ejecutado cuando se dobla una apuesta
      if self.sumaCartas >21:
         self.estado = 'PASADA'
      else:
         self.estado = 'Cerrada'

   #Impresion de cartas: Manejo con lista para cada linea (concatenacion de manos)
   #Damos Forma a las cartas
   def formaCarta(self):
      
      #Comprobacion del dato mas largo para la alineacion de datos
      maxi = max(len(f"{self.nombre}"+":"), len(self.estado), len(f"{self.apuesta}"+"€"))
      self.estadoPrint = self.estado.rjust(maxi)
      self.nombreTrans = (f"{self.nombre}"+":").rjust(maxi)
      self.valorMano = (f"({self.sumaCartas})").rjust(maxi)
      self.apuestaIcono = (f"{self.apuesta}"+"€").rjust(maxi)
      self.espaciado = " " * maxi
      #Aqui damos la forma a la propia carta (o cartas)
      numCartas = len(self.valorCartas)
      self.l1 = "╭───╮" * numCartas
      self.l2, self.l3 = "", ""
      for i in range(len(self.valorCartas)):
         self.l2 += "│" + (" " * (3 - len(self.valorCartas[i][1]))) + f"{self.valorCartas[i][1]}" + "│"
         self.l3 += "│" + f"{self.valorCartas[i][2]}  " + "│"
      self.l4 = "╰───╯" * numCartas

   #Devuelve una lista con cad auna de las lineas de la carta (Son 4)
   #Cartas Coupier
   def imprimirCroupier(self):
      self.formaCarta()
      return [self.nombreTrans+self.l1 ,self.valorMano+self.l2,self.estadoPrint+self.l3,self.espaciado+self.l4]

   #Cartas Jugador
   def imprimirJugador(self):
      self.formaCarta()
      return [self.nombreTrans+self.l1 ,self.valorMano+self.l2, self.apuestaIcono+self.l3,self.estadoPrint+self.l4]

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
   for m in manos:
      if m.estado.replace(' ','') == 'Activa':
         cent +=1
   return cent      

def volverJugar(game,gamesToPlay,balance):
   while True:
    volver_jugar = input("¿Otra partida? [S/N] ").upper()
    if volver_jugar in ['S', 'N']:
        if volver_jugar == 'S':
            game += 1
            gamesToPlay += 1
        else:
            # Fin de las partidas
            print("\nBALANCE FINAL: " + f"{balance}" + " €")
        break
   return volver_jugar

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

         if r == 'J':
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

         elif r == 'A':
            apuesta = estrategia.apuesta(tipoApuesta[0],tipoApuesta[1],tipoApuesta[2])
            print(msg+str(apuesta))
         
         #Ya tenemos apuesta:
         print("\nREPARTO INICIAL")

         #Se le genera una(s) mano(s) tanto al Croupier como al jugador
         #Inicialmente son 2 
         #Croupier --> Si las manos iniciales son mas de 1, el nombre es CropierA, CroupierB...

         def anyadirCartas(mano,numCartas):
            for i in range(len(mano)):
               for _ in range(numCartas):
                  mano[i].append(mazo.reparte())
            return mano
         
         def createMano(mano,nombre,letter,centinela):
            h = []
            for element in mano:
               if len(mano)>1:
                  tmpName = nombre+str(chr(ord(letter) + centinela))
                  centinela+=1
                  h.append(Mano(element,tmpName,apuesta))
               else:   
                  h.append(Mano(element,nombre,apuesta))
            return h

         #Croupier (Si hay mas de dos manos seran CroupierA, CroupierB...)
         nombre, letter = 'Croupier', 'A'
         centinela, cartasPorMano = 0, 1
         #Guardamos las cartas, las manos y el formato carta para su impreson respectivamente
         Croupier, manoCroupier,imprimirCroupier = [[]], [], []
         Croupier = anyadirCartas(Croupier,cartasPorMano)
         manoCroupier = createMano(Croupier,nombre,letter,centinela)

         #usuario (Si hay mas de dos manos seran ManoA, ManoB)
         nombre, cartasPorMano = 'Mano', 2
         #Guardamos las cartas, las manos y el formato carta para su impreson respectivamente
         Jugador,manoJugador,imprimirJugador = [[]], [], []
         Jugador = anyadirCartas(Jugador,cartasPorMano)
         manoJugador = createMano(Jugador,nombre,letter,centinela)

         #Aqui ya tenemos guardadas todas las manos en manoJugador y manoCroupier
         #Son de tipo Mano, lo que transformamos las manos en formato carta para su impresion
         imprimirCroupier = transMano(manoCroupier,imprimirCroupier,'Croupier')
         imprimirJugador = transMano(manoJugador,imprimirJugador,'Jugador')
        
         #Imprimimos las manos   
         imprimirManos(imprimirCroupier)
         imprimirManos(imprimirJugador)
         
         #Comprobacion de BlackJack
         blackJack = False
         for manoJ in manoJugador:
            if manoJ.sumaCartas == 21:
               dinero = round(apuesta*(1.5))
               #Se realiza BlackJack
               print("*****************\n*** BLACKJACK ***\n*****************\n")
               print("Ha ganado "+ f"{dinero}"+ " €!")
               balance += dinero
               blackJack = True
               break

         if blackJack == True:
            #El juego ha acabado con BlackJack
            if r == 'J':
               if volverJugar(game,gamesToPlay,balance) == 'N':
                  break   
            elif r == 'A':
               if game<gamesToPlay:
                  game +=1
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

                     if r == 'J':
                        accion = input(jugada).upper()
                        while True:
                           if accion not in acciones:
                              accion = input("Accion invalida. "+jugada).upper()
                           else:
                              break

                     elif r == 'A':
                        #Utilizaremos el metodo de estrategia. Necesitamos el valor de la carta del Coupier y lista del jugador 
                        """Metodo solo válido para una carta inicial del Coupier"""
                        #Carta del Cropier
                        vc = Croupier[0][0]
                        vj = Jugador[i]
                        accion = estrategia.jugada(vc,vj)
                        print(jugada+accion)

                     #Accion seleccionada correctamente    
                     #Accion de Cerrar -> Estado a Cerrada:   
                     if accion == 'C':
                        manoJugador[i].estado = 'Cerrada'
                      
                     #Accion de Pedir o Doblar (Añadimos una carta)
                     if accion == 'P' or accion == 'D':
                        #Añadimos la carta al Jugador
                        Jugador[i].append(mazo.reparte())
                        manoJugador[i].datos = Jugador[i]
                        #Actualizamos sus datos mediante el metodo
                        manoJugador[i].actualizarDatosMano()

                     #Accion de Doblar  -> Doblamos apuesta
                     if accion == 'D':
                        manoJugador[i].apuesta += manoJugador[i].apuesta
                        manoJugador[i].doblarApuesta()  

                     #Accion de Separar: Sabemos que son dos cartas con el mismo valor nominal
                     if accion == 'S':
                        #Seleccionamos el nombe y la carta para introducirla
                        name = manoJugador[i].nombre
                        carta = [Jugador[i].pop()]
                        #Modificamos el nombre de nuestra mano actual y actualizamos sus datos
                        manoJugador[i].nombre = name+str('A')
                        manoJugador[i].datos = Jugador[i]
                        manoJugador[i].actualizarDatosMano()
                        #Creamos una mano nueva y la actualizamos
                        Jugador.append(carta)
                        manoJugador.append(Mano(carta,(name+str('B')),manoJugador[i].apuesta))
                        manoJugador[-1].actualizarDatosMano()

               print(" ")
               #Imprimimos de nuevo las manos
               imprimirJugador = transMano(manoJugador,imprimirJugador,'Jugador')
               imprimirManos(imprimirJugador)
               #Comprobamos las manos Activas de nuevo    
               manosActivas = comprobarManosActivas(manoJugador)

            #Comprobamos si las manos son pasadas (Se finaliza el juego instantaniamente)
            centinela = 0
            for m in manoJugador:
               if m.estado.upper() == 'ACTIVA' or m.estado.upper() == 'CERRADA':
                  centinela +=1

            if centinela !=0:
               #Hay manos que no son pasadas
               print("\nTURNO DEL CROUPIER")
               imprimirManos(imprimirCroupier)
               #Bucle donde se le otorga una carta hasta que su valor de la mano sea mayor o igual a 17 (Funcional si tiene mas de 1 mano)
               for i in range(len(manoCroupier)):
                  suma = manoCroupier[i].sumaCartas
                  while suma<17:
                     manoCroupier[i].addCarta(mazo.reparte())
                     manoCroupier[i].actualizarDatosMano()
                     imprimirCroupier = transMano(manoCroupier,imprimirCroupier,'Croupier')
                     imprimirManos(imprimirCroupier)
                     suma = manoCroupier[i].sumaCartas
                     if suma<=21 and suma>=17:
                        manoCroupier[i].estado = 'Cerrada'
                     if suma>21:
                        manoCroupier[i].estado = 'PASADA'
               
               imprimirCroupier = transMano(manoCroupier,imprimirCroupier,'Croupier')

            #Aqui ha finalizado el Juego. --> Imprimimos los datos finales      
            print("\nFIN DE LA PARTIDA")
            #Todas las manos han sido pasadas -> Se finaliza el juego
            imprimirManos(imprimirCroupier)
            imprimirManos(imprimirJugador)

            #Contabilizacion de las manos
            print("\nCONTABILIZACION DE RESULTADOS")
            balanceTotal = 0 
            for c in range(len(manoCroupier)):
               for j in range(len(manoJugador)):
                  cent = 0
                  cent +=1 if manoCroupier[c].sumaCartas > 21 else 0
                  cent +=1 if manoJugador[j].sumaCartas > 21 else 0   

                  #Si las dos manos comparadas se pasan
                  if cent == 2:
                     bal = "+0"

                  elif cent == 1:
                     #Solo se pasa una mano --> Si es el Croupier   
                     if manoCroupier[c].sumaCartas > 21:
                        balanceTotal += manoJugador[j].apuesta
                        bal = "+"f"{manoJugador[j].apuesta}"
                     #Si es el jugador
                     else:
                        balanceTotal -= manoJugador[j].apuesta
                        bal = "-"f"{manoJugador[j].apuesta}"

                  #Aqui no se pasa ninguno. Se comparan entre ellos
                  elif manoCroupier[c].sumaCartas > manoJugador[j].sumaCartas:
                     balanceTotal -= manoJugador[j].apuesta
                     bal = "-"f"{manoJugador[j].apuesta}"
                  elif manoCroupier[c].sumaCartas < manoJugador[j].sumaCartas:  
                     balanceTotal += manoJugador[j].apuesta
                     bal = "+"f"{manoJugador[j].apuesta}"
                  else:
                     bal = "+0"
   
                  #El print de cada mano comparada
                  print("* "+f"{manoCroupier[c].nombre}"+": "+f"{manoCroupier[c].sumaCartas}"+", "+f"{manoJugador[j].nombre}"+": "+f"{manoJugador[j].sumaCartas}"+" -> "f"{bal}")
            print("Resultado de la partida: "f"{balanceTotal}")

            #Añadimos al Balance general
            balance += balanceTotal
           
            #Solicitamos si quiere seguir jugando
            if r == 'J':
               #El juego ha acabado con BlackJack
               if volverJugar(game,gamesToPlay,balance) == 'N':
                  break
            elif r == 'A':
               #Esta en modo Análisis, iniciamos nueva Partida
               if game<gamesToPlay:
                  game +=1
               else:
                  print("\nBALANCE FINAL: "+f"{balance}"+" €\n")
                  break
   else:
      print("Modo de juego incorrecto")
if __name__ == "__main__":
    main()
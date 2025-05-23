import random as rand

visited = 0

class Nodo():
    def __init__(self, estado, papa = None, costo = -1):
        self.estado = estado
        self.hijos = []
        self.papa = papa
        self.heuristica = None
        self.costo = costo +1

    def genera_hijos(self, meta = None, metodo = None):
        pos = self.estado.index("_")
        #respetar restricciones
        n = 3
        #posiciones
        # 0 1 2
        # 3 4 5
        # 6 7 8
        
        #mover arriba
        if (pos >= n):
            new_estado = self.estado[:]         # copiar
            new_estado[pos] = new_estado[pos-n] # copiar valor de esa posicion
            new_estado[pos-n] = "_"             # asignar el hueco en la matriz
            
            new_nodo = Nodo(new_estado, self, self.costo)
            self.hijos.append(new_nodo)
            
            if meta:
                if metodo == "greedy": 
                    new_nodo.heuristica2(meta)
                else:
                    new_nodo.f_n(meta)  # fn = g(n) (costo) + h(n) (heuristica)

        #mover abajo
        if (pos < n*2):
            new_estado = self.estado[:]         # copiar
            new_estado[pos] = new_estado[pos+n] # copiar valor de esa posicion
            new_estado[pos+n] = "_"             # asignar el hueco en la matriz

            new_nodo = Nodo(new_estado, self, self.costo)
            self.hijos.append(new_nodo)
            
            if meta:
                if metodo == "greedy":
                    new_nodo.heuristica2(meta)
                else:
                    new_nodo.f_n(meta)  # fn = g(n) (costo) + h(n)

        #mover izquierda
        if (pos%n != 0):
            new_estado = self.estado[:]         # copiar
            new_estado[pos] = new_estado[pos-1] # copiar valor de esa posicion
            new_estado[pos-1] = "_"             # asignar el hueco en la matriz

            new_nodo = Nodo(new_estado, self, self.costo)
            self.hijos.append(new_nodo)
            
            if meta:
                if metodo == "greedy":
                    new_nodo.heuristica2(meta)
                else:
                    new_nodo.f_n(meta)  # fn = g(n) (costo) + h(n)

        #mover derecha
        if ((pos+1)%n != 0):
            new_estado = self.estado[:]         # copiar
            new_estado[pos] = new_estado[pos+1] # copiar valor de esa posicion
            new_estado[pos+1] = "_"             # asignar el hueco en la matriz
 
            new_nodo = Nodo(new_estado, self, self.costo)
            self.hijos.append(new_nodo)
            
            if meta:
                
                if metodo == "greedy":
                    new_nodo.heuristica2(meta)
                else:
                    new_nodo.f_n(meta)  # fn = g(n) (costo) + h(n)

    def soy_visitado(self, visitados):
        #return any(self.estado == arr for arr in visitados)
        return self.estado in visitados

    def bpp(self, meta, visitados=None): # busqueda primero en profundidad (DFS Depth First Search)

        if self.estado == meta: # si soy
            visited = len(visitados)
            return [self]
        # soy gemelo malvado de uno visitado? checar si nodo ya se visito
        # return None
        # seguir buscando

        if visitados is None:
            visitados = []
        if self.soy_visitado(visitados): # ya lo visitamos
            return None

        res = None
        self.genera_hijos()
        visitados.append(self.estado)

        for h in self.hijos: # hijos de self
            res = h.bpp(meta, visitados) # los nietos 
            if not (res == None): # si hay resutado
                res.append(self)
                return res

    def bpa(self, meta, visitados = None, por_visitar = []): # busqueda primero por anchura
        global visited
        # --- hacerlo funcion
        if self.estado == meta: # soy la meta?
            return [self]
        
        if visitados is None: # si visitados vacio, se inicializa
            visitados = []
        if self.soy_visitado(visitados): # si soy visitado, true, y retorna none
            return None
        
        self.genera_hijos()
        visitados.append(self.estado)
        # --- hasta aqui

        por_visitar += self.hijos

        while (por_visitar != []):
            h = por_visitar.pop(0)
            if h.estado == meta: # soy yo?
                visited = len(por_visitar) + len(visitados)
                camino = [h]
                papa = h.papa
                while (papa != None):
                    camino.append(papa)
                    papa=papa.papa
                camino.reverse()
                return camino # checar aqui
        
            if h.soy_visitado(visitados): # ya lo visitamos?
                continue
            
            h.genera_hijos()
            visitados.append(h.estado)

            por_visitar += h.hijos

    def heuristica1(self, meta):
        contador = 0
        for e1, e2 in zip(self.estado, meta):
            if not e1 == e2:
                contador = contador + 1
        self.heuristica = contador
        return contador

    def heuristica2(self, meta):
        sumador = 0
        for el in self.estado:
            sumador += abs(self.estado.index(el) - meta.index(el))
        self.heuristica = sumador
        return sumador
            
    def f_n(self, meta):
        self.heuristica = self.costo + self.heuristica2(meta)
        return self.heuristica

    def greedy(self, meta, visitados = [], metodo = "greedy"):
        visitados = []
        #por_visitar = []
        por_visitar = [self]

        while(por_visitar!= []):
            h = por_visitar.pop(0)
            if h.estado == meta: # soy yo?
                camino = [h]
                papa = h.papa
                while (papa != None):
                    camino.append(papa)
                    papa=papa.papa
                camino.reverse()
                return camino # checar aqui
        
            if h.soy_visitado(visitados): # ya lo visitamos?
                continue
            
            h.genera_hijos(meta)
            visitados.append(h.estado)

            por_visitar += h.hijos
            por_visitar.sort()
            #ordenar los por_visitar

    def a_star(self, meta, visitados = []):
        visitados = []
        #por_visitar = []
        por_visitar = [self]

        while(por_visitar!= []):
            h = por_visitar.pop(0)
            if h.estado == meta: # soy yo?
                camino = [h]
                papa = h.papa
                while (papa != None):
                    camino.append(papa)
                    papa=papa.papa
                camino.reverse()
                return camino # checar aqui
        
            if h.soy_visitado(visitados): # ya lo visitamos?
                continue
            
            h.genera_hijos(meta)
            visitados.append(h.estado)

            por_visitar += h.hijos
            por_visitar.sort()
            #ordenar los por_visitar

    def __lt__(self, n2):
        if n2 == None:
            return False
        return self.heuristica < n2.heuristica

    def __eq__(self, n2):
        if n2 == None:
            return False
        return self.estado == n2.estado

    def __repr__(self):
        return("\n" + str(self.costo) + " --------\n" + str(self.estado[:3]) + "\n" + str(self.estado[3:6]) +"\n" + str(self.estado[6:]))

meta = [1, 2, 3,
        4, 5, 6,
        7, 8, "_"]    

raiz = Nodo(
    [4, 1, 3,
    7,"_",2,
    8, 6, 5])

solucion = raiz.bpa(meta)
for p in solucion:
    print(p)

print("Movimientos: ", len(solucion))

#Estado inicial
#7,5,4
#6,_,1
#2,3,8

#Estado meta
#1,2,3
#4,5,6
#7,8,_

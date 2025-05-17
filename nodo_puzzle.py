import random as rand

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
            
            #print("arr")
            
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
            #self.hijos.append(Nodo(new_estado, self))
            #print("ab")

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
            #self.hijos.append(Nodo(new_estado, self))
            #print("izq")
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
            #self.hijos.append(Nodo(new_estado, self))
            #print("der")

            new_nodo = Nodo(new_estado, self, self.costo)
            self.hijos.append(new_nodo)
            
            if meta:
                
                if metodo == "greedy":
                    new_nodo.heuristica2(meta)
                else:
                    new_nodo.f_n(meta)  # fn = g(n) (costo) + h(n)

        print(pos)

    def soy_visitado(self, visitados):
        #return any(self.estado == arr for arr in visitados)
        return self.estado in visitados

    def bpp(self, meta, visitados=None): # busqueda primero en profundidad (DFS Depth First Search)

        if self.estado == meta: # si soy
            print("YA QUEDOOO")
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
            #print(h)
            #if h.estado in visitados: #otra opcion
                #continue
            res = h.bpp(meta, visitados) # los nietos 
            if not (res == None): # si hay resutado
                res.append(self)
                return res

    def bpa(self, meta, visitados = None, por_visitar = []): # busqueda primero por anchura
        # --- hacerlo funcion
        if self.estado == meta: # soy la meta?
            print("YA QUEDO")
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
                print("YA SE ENCONTRO")
                print("visitados: bpa ",  len(visitados))
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
                print("YA SE ENCONTRO")
                print("visitados: greedy",  len(visitados))
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
                print("YA SE ENCONTRO")
                print("visitados: a*",  len(visitados))
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
        return("\n--------\n" + str(self.estado[:3]) + "\n" + str(self.estado[3:6]) +"\n" + str(self.estado[6:]))
    
raiz = Nodo([7,5,4,6,"_",1,2,3,8])
meta = [7,8,4,6,5,1,2,3,"_"]

visitados_greedy = []
visitados_bpa = []
visitados_astar = []

#print(raiz.heuristica1(meta))
#print(raiz.heuristica2(meta))
#print(len(raiz.bpa(meta, visitados=visitados_astar)))
print(len(raiz.a_star(meta, visitados=visitados_astar)))

#print("visitados greedy", len(visitados_greedy))
#print("visitados bpa", len(visitados_bpa))
print("visitados a*", len(visitados_astar))

#print(raiz)

"""
#Estado inicial
#7,5,4
#6,8,1
#2,3,_

#Estado meta
#1,2,3
#4,5,6
#7,8,_

#estado inicial

2 5 3
1 _ 6
4 7 8


#raiz = Nodo ([7,5,4,6,"_",1,2,3,8])
#meta = [7,5,4,6,"_",1,2,3,8]

#raiz = Nodo([1,2,3,"_",5,6,4,7,8])
raiz = Nodo([8,7,6,3,1,4,5,2,"_"])
m = [1,2,3,4,5,6,7,8,"_"]


print(raiz)
raiz.genera_hijos()

for h in raiz.hijos:
    print(h)

print(raiz.greedy(m))

visitadosgreedy
bpa
astar

print(raiz.heuristica1(meta))
print(raiz.heuristica2(meta))
print(len)
"""
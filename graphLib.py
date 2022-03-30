import graphviz

class Graphe(object):
    def __init__(self, graphe_dict=None):
        if graphe_dict == None:
            graphe_dict = dict()
        self._graphe_dict = graphe_dict

    def aretes(self, sommet):
        return self._graphe_dict[sommet]

    def all_sommets(self):
        return set(self._graphe_dict.keys())

    def all_aretes(self):
        return self.__list_aretes()

    def add_sommet(self, sommet):
        if sommet not in self._graphe_dict:
            self._graphe_dict[sommet] = []

    def add_arete(self, arete):
        arete = set(arete)
        arete1, arete2 = tuple(arete)
        for x, y in [(arete1, arete2), (arete2, arete1)]:
            if x in self._graphe_dict:
                if isinstance(self._graphe_dict[x],list):
                    self._graphe_dict[x].append(y)
                else:
                    self._graphe_dict[x].add(y)
            else:
                self._graphe_dict[x] = {y}

    def __list_aretes(self):
        aretes = []
        for sommet in self._graphe_dict:
            for voisin in self._graphe_dict[sommet]:
                if ({voisin, sommet})  not in aretes:
                    aretes.append({sommet, voisin})
        return aretes
    
    def trouve_chaine(self, sommet_dep, sommet_arr, chain=None):
        graphe = self._graphe_dict
        if not({sommet_dep,sommet_arr}.issubset(graphe)):
            return None
        if chain == None:
            chain = []
        chain = chain + [sommet_dep]
        if sommet_dep == sommet_arr:
            return chain
        for sommet in graphe[sommet_dep]:
            if sommet not in chain:
                ext_chain = self.trouve_chaine(sommet, sommet_arr, chain)
                if ext_chain: 
                    return ext_chain
        return None
    
    def trouve_tous_chaines(self, sommet_dep, sommet_arr, chain=[]):
        graphe = self._graphe_dict  
        if not({sommet_dep,sommet_arr}.issubset(graphe)):
            return []
        chain = chain + [sommet_dep]
        if sommet_dep == sommet_arr:
            return [chain]
        if sommet_dep not in graphe:
            return []
        chains = []
        for sommet in graphe[sommet_dep]:
            if sommet not in chain:
                ext_chains = self.trouve_tous_chaines(sommet, sommet_arr, chain)
                for c in ext_chains: 
                    chains.append(c)
        return chains

    def __iter__(self):
        self._iter_obj = iter(self._graphe_dict)
        return self._iter_obj

    def __next__(self):
        return next(self._iter_obj)

    def __str__(self):
        res = "sommets: "
        for k in self._graphe_dict.keys():
            res += str(k) + " "
        res += "\naretes: "
        for arete in self.__list_aretes():
            res += str(arete) + " "
        return res


class Graphe2(Graphe):
    def sommet_degre(self, sommet):
        degre =  len(self._graphe_dict[sommet]) 
        if sommet in self._graphe_dict[sommet]:
            degre += 1 
        return degre

    def trouve_sommet_isole(self):
        graphe = self._graphe_dict
        isoles = []
        for sommet in graphe:
            if not graphe[sommet]:
                isoles += [sommet]
        return isoles
        
    def Delta(self):
        maxi = 0
        for sommet in self._graphe_dict:
            sommet_degre = self.sommet_degre(sommet)
            if sommet_degre > max:
                maxi = sommet_degre
        return maxi

    def list_degres(self):
        degres = []
        for sommet in self._graphe_dict:
            degres.append(self.sommet_degre(sommet))
        degres.sort(reverse=True)
        return degres

class GraphePondere(Graphe2):
    def all_aretes(self):
        return self.__list_aretes()
        
    def aretes(self, sommet):
        return self._graphe_dict[sommet].keys()
 
    def __list_aretes(self):
        aretes = []
        for sommet in self._graphe_dict:
            for voisin in self._graphe_dict[sommet]:
                if ({voisin, sommet})  not in aretes:
                    aretes.append((sommet, voisin,self._graphe_dict[sommet][voisin]))
        return aretes

    def add_arete(self, arete,val):
        arete = set(arete)
        arete1, arete2 = tuple(arete)
        for x, y in [(arete1, arete2), (arete2, arete1)]:
            if x in self._graphe_dict:
                if isinstance(self._graphe_dict[x],list):
                    self._graphe_dict[x].append({y,val})
                else:
                    self._graphe_dict[x] = {y:val}
            else:
                self._graphe_dict[x] = {y:val}
                
    def poids(self,origine,extremitee):
        return self._graphe_dict[origine][extremitee]
   
    def __str__(self):
        res = "sommets:"
        for k in self._graphe_dict.keys():
            res += str(k) + " "
        res += "\naretes: "
        for origine,extremite,valeurs in self.__list_aretes():
            res += str(origine)+" , "+str(extremite) +" Valeurs " +str(valeurs) +"\n"
        return res


def minDist(lstNoeuds,distance):
    distMini=float("inf")
    valMini=-1
    for noeud in lstNoeuds:
        if distance[noeud]<distMini:
           distMini=distance[noeud]
           valMini=noeud
    return valMini

def Dijkstra(graphe, pDepart) :
    distance = {sommet:float("inf") for sommet in graphe.all_sommets()} #Tableau qui va stocker l'entièreté des distances des points du graph comparées au point de départ
    precedente = {} #Tableau qui va stoker le chemin optimal
    for elem in graphe.all_sommets() :
        distance[elem] = float("inf") #On initialise toutes les distances à l'infini avant de les calculer
        precedente[elem] = None;
    distance[pDepart] = 0 #On set la distance du depart vers lui même à 0
    noeuds = [sommet for sommet in graphe.all_sommets()]
    while len(noeuds) > 0 :
        suivant = minDist(noeuds, distance)
        print(suivant)
        noeuds.remove(suivant)
        for voisin in graphe.aretes(suivant) :
            distanceCumulee = distance[suivant] + graphe.poids(voisin, suivant)
            if distanceCumulee < distance[voisin] :
                distance[voisin] = distanceCumulee
                precedente[voisin] = suivant
    return precedente, distance

def printWGraph(graphe, fn="default") :
    lstArete = []
    g = graphviz.Graph('G', filename=fn)
    for sommet in graphe.all_sommets() : 
        g.node(sommet)
    for arete in graphe.all_aretes() :
        if (arete not in lstArete) :
            g.edge(str(arete[0]), str(arete[1]), weight=str(arete[2]), label=str(arete[2]))
            lstArete.append((arete[1], arete[0], arete[2]))
    g.view()

def get_odd(graph):
    return {sommet:graph.sommet_degre(sommet)%2 for sommet in graph.all_sommets()}

graphDic = {"A" :{"C": 1},
"B" : {"C" : 2, "E" : 3},
"C" : {"A" : 1, "B" : 2, "D" : 4, "E" : 2},
"D" : {"C" : 4},
"E" : {"C" : 2, "B" : 3}
}

g = GraphePondere(graphDic)

s='A'
d='B'
p,distance=Dijkstra(g, s)
l=[d]
v=d

while p[v] is not None:
    l.append(p[v])
    v=p[v]

l.reverse()
print(l)
printWGraph(g)
print(get_odd(g))
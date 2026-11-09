import math

#Bábu class. Itt jönnek létre a bábuk
class Babu:
    #Bábu konstruktora
    def __init__(self,nev,szin,elmozdult):
        self.nev = nev
        self.szin = szin
        self.elmozdult = elmozdult
    def __str__(self):
        szo = ""
        if self.szin == "feher":
            szo += "fh:"
        else:
            szo += "fk:"
        if self.nev == "kiralyno":
            szo += "kn:"
        else:
            szo += self.nev[0] + ":"
        if self.elmozdult == False:
            szo += "n"
        else:
            szo += "i"
        return szo
        
    #rX/rY/rZ a bábuhoz képest x,y,z koordináta(relative koordináta)
    #Ellenörzi hogy adott karakter léphet-e a kijelölt mezõre
    def lephetE(self,rX,rY,rZ):
        if rX == 0 and rY == 0 and rZ == 0:
            return False
        #Király lépései
        if self.nev == "kiraly":
            if (abs(rX) + abs(rY) + abs(rZ)) <= 2 \
               and abs(rX) <= 1 and abs(rY) <= 1 and abs(rZ) <= 1:
                return True
            return False
        #Királynõ lépései
        elif self.nev == "kiralyno":
            if (abs(rX) == abs(rY) and rZ == 0) \
               or (abs(rX) == abs(rZ) and rY == 0) \
               or (abs(rY) == abs(rZ) and rX == 0):
                return True
            if (rX == 0 and rY == 0) \
               or (rX == 0 and rZ == 0) \
               or (rY == 0 and rZ == 0):
                return True
            return False
        #Futó lépései
        elif self.nev == "futo":
            if (abs(rX) == abs(rY) and rZ == 0) \
               or (abs(rX) == abs(rZ) and rY == 0) \
               or (abs(rY) == abs(rZ) and rX == 0):
                return True
            return False
        #Lovas lépései
        elif self.nev == "lovas":
            if (abs(rX) + abs(rY) + abs(rZ)) == 3 \
               and (abs(rX) == 2 or abs(rY) == 2 or abs(rZ) == 2):
                return True
            return False  
        #Bástya lépései
        elif self.nev == "bastya":
            if (rX == 0 and rY == 0) \
               or (rX == 0 and rZ == 0) \
               or (rY == 0 and rZ == 0):
                return True
            return False
        #Paraszt lépései
        else:
            #Fehér paraszt lépései
            if self.szin == "feher":
                if self.elmozdult == False:
                    if  (rZ == -2 and rY == 0 and rX == 0):
                        return True
                if (rZ == -1 and rY == 0 and rX == 0) \
                   or (abs(rY) == 1 and rX == 0 and rZ == 0):
                    return True
                if rZ == -1 and ((abs(rX) == 1 and rY == 0)):
                    return True
                return False
            #Fekete paraszt lépései
            else:
                if self.elmozdult == False:
                    if  (rZ == 2 and rY == 0 and rX == 0):
                        return True
                if (rZ == 1 and rY == 0 and rX == 0) \
                   or (abs(rY) == 1 and rX == 0 and rZ == 0):
                    return True
                if rZ == 1 and ((abs(rX) == 1 and rY == 0)):
                    return True
                return False

#Pálya class. Itt jön létre a pálya amin játszunk
class Palya:
    #Pálya konstruktora
        def __init__(self,x, y, z):
            self.tabla = []
            for i in range(x):
                self.tabla.append([])
                for j in range(y):
                    self.tabla[i].append([])
                    for k in range(z):
                        self.tabla[i][j].append(None)

        def reset(self):
            feherSorrend = ["futo","kiralyno","kiraly","futo","bastya","lovas","lovas","bastya"]
            feketeSorrend = ["futo","kiraly","kiralyno","futo","bastya","lovas","lovas","bastya"]
            for y in range(len(self.tabla)):
                for z in range(len(self.tabla[y])):
                    for x in range(len(self.tabla[y][z])):
                        szin = None
                        nev = None
                        if y < 2 and z < 2:
                            szin = "fekete"
                            if z == 1:
                                nev = "paraszt"
                            else:
                                nev = feketeSorrend[x+y*4]
                            self.tabla[x][y][z] = Babu(nev,szin,False)
                        elif y > 1 and z > 1:
                            szin = "feher"
                            if z == 2:
                                nev = "paraszt"
                            else:
                                nev = feherSorrend[x+(3-y)*4]
                            self.tabla[x][y][z] = Babu(nev,szin,False)
                        else:
                            self.tabla[x][y][z] = None

        #aX/aY/aZ a pálya adott koordinátája (abszolút koordináta)
        #Ellenörzi hogy a karakter lépését nem-e gátolja valami akadály(saját vagy ellenséges játékos) 
        def szabadUt(self,aX1,aY1,aZ1,aX2,aY2,aZ2):
            babu1 = self.tabla[aX1][aY1][aZ1]
            babu2 = self.tabla[aX2][aY2][aZ2]
            #Királynak szabad-e az útja
            if babu1.nev == "kiraly":
                if babu2 == None:
                    return True
                if babu1.szin != babu2.szin:
                    return True
            #Lovasnak szabad-e az útja
            elif babu1.nev == "lovas":
                if babu2 == None:
                    return True
                if babu1.szin != babu2.szin:
                    return True
            #Parasztnak szabad-e az útja
            elif babu1.nev == "paraszt":
                if aZ1-aZ2 == 0:
                    if babu2 == None:
                        return True
                elif aX1-aX2 == 0 and aY1-aY2 == 0:
                    if abs(aZ1-aZ2) != 1:
                        if self.tabla[aX1][aY1][aZ1-int((aZ1-aZ2)/abs(aZ1-aZ2))] == None and \
                           babu2 == None:
                            return True
                    else:
                        if babu2 == None:
                            return True
                else:
                    if babu2 != None:
                        if babu1.szin != babu2.szin:
                            return True
            #Minden másnak(futó,királynõ,bástya) szabad-e az útja
            else:
                jelenlegi = [aX1,aY1,aZ1]
                while True:
                    if jelenlegi[0] - aX2 != 0:
                        jelenlegi[0] -= int((jelenlegi[0] - aX2)\
                                /abs(jelenlegi[0] - aX2))
                    if jelenlegi[1] - aY2 != 0:
                        jelenlegi[1] -= int((jelenlegi[1] - aY2)\
                                /abs(jelenlegi[1] - aY2))
                    if jelenlegi[2] - aZ2 != 0:
                        jelenlegi[2] -= int((jelenlegi[2] - aZ2)\
                                /abs(jelenlegi[2] - aZ2))
                    if jelenlegi[0] == aX2 and jelenlegi[1] == aY2 \
                       and jelenlegi[2] == aZ2:
                        if babu2 != None:
                                if babu1.szin != babu2.szin:
                                    return True
                                else:
                                    break
                        return True
                    if self.tabla[jelenlegi[0]][jelenlegi[1]][jelenlegi[2]] != None:
                        break
            return False

        def nincsMatt(self,aX1,aY1,aZ1,aX2,aY2,aZ2):
            babu1 = self.tabla[aX1][aY1][aZ1]
            babu2 = self.tabla[aX2][aY2][aZ2]
            #Kívánt lépés szimulálása
            szimulacio = Palya(4,4,4)
            for x in range(len(self.tabla)):
                for y in range(len(self.tabla[x])):
                    for z in range(len(self.tabla[x][y])):
                        szimulacio.tabla[x][y][z] = self.tabla[x][y][z]
            szimulacio.tabla[aX2][aY2][aZ2] = babu1
            szimulacio.tabla[aX1][aY1][aZ1] = None
            #Király pózíciójának megkeresése
            kiralyPoz = None
            for i in range(len(szimulacio.tabla)):
                for j in range(len(szimulacio.tabla[i])):
                    for k in range(len(szimulacio.tabla[i][j])):
                        if szimulacio.tabla[i][j][k] != None:
                            if szimulacio.tabla[i][j][k].nev == "kiraly" \
                               and szimulacio.tabla[i][j][k].szin == babu1.szin:
                                kiralyPoz = [i,j,k]
                                break
                    if kiralyPoz != None:
                        break
                if kiralyPoz != None:
                    break
            #Tesztelni hogy a király a szimulált lépés után is sakkba van-e
            for i in range(len(szimulacio.tabla)):
                for j in range(len(szimulacio.tabla[i])):
                    for k in range(len(szimulacio.tabla[i][j])):
                        if szimulacio.tabla[i][j][k] != None:
                            if szimulacio.tabla[i][j][k].szin != babu1.szin:
                                rX = kiralyPoz[0]-i
                                rY = kiralyPoz[1]-j
                                rZ = kiralyPoz[2]-k
                                if szimulacio.tabla[i][j][k].lephetE(rX,rY,rZ):
                                    if szimulacio.szabadUt(i,j,k,kiralyPoz[0],kiralyPoz[1],kiralyPoz[2]):
                                        return False
            return True

import math
import osztalyok
def betoltes(fajlnev):
    f = open(fajlnev, "rt",encoding='utf-8')
    tabla = []
    for i in range(4):
        tabla.append([])
        for j in range(4):
            tabla[i].append([])
            for k in range(4):
                tabla[i][j].append("")
    z = 0
    y = 0
    while True:
        sor = f.readline()
        if sor == "":
            break
        if sor == "\n":
            y+=1
            print()
            continue
        sor = sor.rstrip("\n")
        adatok = sor.split(";")

        for x in range(len(adatok)):
            if ":" not in adatok[x]:
                tabla[x][3-y][3-z] = None
            else:
                babuAdat = adatok[x].split(":")
                mozdult = False
                if babuAdat[0] == "fh":
                    szin = "feher"
                else:
                    szin = "fekete"
                if babuAdat[1] == "f":
                    nev = "futo"
                elif babuAdat[1] == "kn":
                    nev = "kiralyno"
                elif babuAdat[1] == "k":
                    nev = "kiraly"
                elif babuAdat[1] == "l":
                    nev = "lovas"
                elif babuAdat[1] == "b":
                    nev = "bastya"
                else:
                    nev = "paraszt"
                
                    
                if babuAdat[2] == "i":
                    mozdult = True
                    
                tabla[x][3-y][3-z] = osztalyok.Babu(nev,szin,mozdult)
        z += 1
        if z == 4:
            z = 0
        
    f.close()
    return tabla

def mentes(fajlnev, tabla):
    f = open(fajlnev, "wt",encoding='utf-8')
    for y in range(4):
        for z in range(4):
            sor = ""
            for x in range(4):
                elvalaszto = ";"
                if x == 3:
                    elvalaszto = ""
                if tabla[x][3-y][3-z] == None:
                    sor += elvalaszto
                else:
                    sor += str(tabla[x][3-y][3-z]) + elvalaszto
            f.write(f"{sor}\n")
        f.write("\n")
    f.close()

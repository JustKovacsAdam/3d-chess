import os
import pygame
import osztalyok
import fajlkezeles


aHossz = 750
aSzelesseg = 500
ablak = None  # a kirajzol() hozza létre, a pygame.init() után

# A fájlok elérési útja a program mappájához képest, így bárhonnan indítható
MAPPA = os.path.dirname(os.path.abspath(__file__))
KEPEK = os.path.join(MAPPA, "Kepek")
MENTES = os.path.join(MAPPA, "mentes.txt")

BABU_NEVEK = ["bastya", "lovas", "futo", "kiralyno", "kiraly", "paraszt"]
BABU_FAJLOK = ["Bastya", "Lovas", "Futo", "Kiralyno", "Kiraly", "Paraszt"]
_kepek = {}

#Kitöltõ eszköz (iteratív, hogy ne fusson bele a rekurziós korlátba)
def kitoltes(regiSzin,ujSzin, x, y):
    regiSzin = ablak.map_rgb(regiSzin)
    ujSzin = ablak.map_rgb(ujSzin)
    if regiSzin == ujSzin:
        return
    with pygame.PixelArray(ablak) as pixelek:
        pixelek[x, y] = ujSzin
        verem = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        while verem:
            x, y = verem.pop()
            if x < 0 or x >= aSzelesseg or y < 0 or y >= aHossz:
                continue
            if pixelek[x, y] != regiSzin:
                continue
            pixelek[x, y] = ujSzin
            verem.extend(((x+1, y), (x-1, y), (x, y+1), (x, y-1)))

#Kirajzolja a tábla körvonalait
def korvonalak():
    sX = 100
    sY = 200
    for i in range(4):
        l = 150*i
        for j in range(5):  #vertikális
            d = 50 * j
            pygame.draw.line(ablak,(0,0,0),(sX+d,sY+l),(sX+100+d,sY+l-100),5)
            
        for j in range(5):  #horizontális
            d = 25 * j
            pygame.draw.line(ablak,(0,0,0),(sX+d,sY+l-d),(sX+200+d,sY+l-d),5)

#Kiszinezi a tábla mezõit(fekete-fehér)
def szinezesek(szabaly):
    sX = 125
    sY = 638
    for i in range(4):
        x = 50*i
        for j in range(4):
            y = 150 * j
            for k in range(4):
                z = 25 * k
                if szabaly is not None:
                    if szabaly[i][j][k] == 1:
                        kitoltes((97,192,255),(255,0,0),sX+x+z,sY-y-z)
                        continue
                    elif szabaly[i][j][k] == 2:
                        kitoltes((97,192,255),(0,255,0),sX+x+z,sY-y-z)
                        continue
                if (i+j+k) % 2 == 0:
                    kitoltes((97,192,255),(0,0,0),sX+x+z,sY-y-z)
                else:
                    kitoltes((97,192,255),(255,255,255),sX+x+z,sY-y-z)


#Megjeleníti a bábukat a táblán
def babukMegjelenitese(tabla):
    for x in range(4):
        for y in range(4):
            for z in range(4):
                babu = tabla[x][y][z]
                if babu is not None:
                    kep = _kepek[(babu.szin, babu.nev)]
                    ablak.blit(kep,(121+z*25+x*50,610-z*25-y*150))

#A képeket egyszer töltjük be, nem minden újrarajzolásnál
def kepekBetoltese():
    for szin, elotag in (("feher", "Feher"), ("fekete", "Fekete")):
        for nev, fajl in zip(BABU_NEVEK, BABU_FAJLOK):
            kep = pygame.image.load(os.path.join(KEPEK, elotag + fajl + ".png")).convert_alpha()
            _kepek[(szin, nev)] = pygame.transform.scale(kep,(32,32))
    kep = pygame.image.load(os.path.join(KEPEK, "Ujrakezdes.png")).convert_alpha()
    _kepek["ujrakezdes"] = pygame.transform.scale(kep,(50,50))
def kattintas():
    x = None
    y = None
    z = None
    eger = pygame.mouse.get_pos()
    if eger[0] <= 400 and eger[0] >= 100 and eger[1] <= 650 and eger[1] >= 100:
        #y koordináta megállapítása
        if eger[1] > 550:
            y = 0
        elif eger[1] > 400 and eger[1] < 500:
            y = 1
        elif eger[1] > 250 and eger[1] < 350:
            y = 2
        elif eger[1] > 100 and eger[1] < 200:
            y = 3
        else:
            return None
        #z koordináta megállapítása
            
        if (eger[1]-(3-y)*150-100) > 75:
            z = 0
        elif (eger[1]-(3-y)*150-100) > 50:
            z = 1
        elif (eger[1]-(3-y)*150-100) > 25:
            z = 2
        elif (eger[1]-(3-y)*150-100) > 0:
            z = 3
        else:
            return None
        #x koordináta megállapítása
        if eger[0] < 100+(100-(eger[1]-(3-y)*150-100)):
            return None
        elif eger[0] < 150+(100-(eger[1]-(3-y)*150-100)):
            x = 0
        elif eger[0] < 200+(100-(eger[1]-(3-y)*150-100)):
            x = 1
        elif eger[0] < 250+(100-(eger[1]-(3-y)*150-100)):
            x = 2
        elif eger[0] < 300+(100-(eger[1]-(3-y)*150-100)):
            x = 3
        else:
            return None
    else:
        if eger[0] >= 425 and eger[0] <= 475 \
           and eger[1] >= 25 and eger[1] <= 75:
            return "reset"
        return None
    return (x,y,z)

def hovaLephet(sakktabla,xyz):
    lepesek = []
    for i in range(4):
        lepesek.append([])
        for j in range(4):
            lepesek[i].append([])
            for k in range(4):
                lepesek[i][j].append(0)
    
    for x in range(len(sakktabla.tabla)):
        for y in range(len(sakktabla.tabla)):
            for z in range(len(sakktabla.tabla)):
                if sakktabla.tabla[xyz[0]][xyz[1]][xyz[2]].lephetE(x-xyz[0],y-xyz[1],z-xyz[2]):
                   if sakktabla.szabadUt(xyz[0],xyz[1],xyz[2],x,y,z):
                       if sakktabla.nincsMatt(xyz[0],xyz[1],xyz[2],x,y,z):
                            lepesek[x][y][z] = 1
    lepesek[xyz[0]][xyz[1]][xyz[2]] = 2
    return lepesek

def lepes(sakktabla, xyz1,xyz2):
    babu = sakktabla.tabla[xyz1[0]][xyz1[1]][xyz1[2]]
    babu.elmozdult = True  # különben a paraszt mindig léphetne kettõt
    sakktabla.tabla[xyz2[0]][xyz2[1]][xyz2[2]] = babu
    sakktabla.tabla[xyz1[0]][xyz1[1]][xyz1[2]] = None
def kirajzol():
    global ablak
    pygame.init()
    ablak = pygame.display.set_mode((aSzelesseg,aHossz))
    kepekBetoltese()
    ora = pygame.time.Clock()
    pygame.display.set_caption("3D Chess")
    
    sakktabla = osztalyok.Palya(4,4,4)
    kor = "feher"
    fut = True
    rajzolj = True
    toltsdBe = True

    specialis = None
    kivalasztott = None
    
    while fut:
        for esemeny in pygame.event.get():
            if esemeny.type == pygame.MOUSEBUTTONDOWN:
                click = kattintas()
                if click is not None:
                    if click == "reset":
                        sakktabla.reset()
                        kor = "feher"
                        kivalasztott = None
                        specialis = None 
                    else:
                        if kivalasztott is not None:
                            if specialis[click[0]][click[1]][click[2]] == 1:
                                lepes(sakktabla,kivalasztott,click)
                                if kor == "feher":
                                    kor = "fekete"
                                else:
                                    kor = "feher"
                            kivalasztott = None
                            specialis = None       
                        else:
                            kivalasztott = click
                            if sakktabla.tabla[kivalasztott[0]][kivalasztott[1]][kivalasztott[2]] is not None:
                                if sakktabla.tabla[kivalasztott[0]][kivalasztott[1]][kivalasztott[2]].szin == kor:
                                    specialis = hovaLephet(sakktabla, kivalasztott)
                                else:
                                    kivalasztott = None
                                    specialis = None
                            else:
                                kivalasztott = None
                                specialis = None
                else:
                    kivalasztott = None
                    specialis = None
                rajzolj = True
                
            if esemeny.type==pygame.QUIT:
                fajlkezeles.mentes(MENTES,sakktabla.tabla)
                fut = False
        pygame.display.update()
        ora.tick(30)

        if toltsdBe:
            toltsdBe = False
            try:
                sakktabla.tabla = fajlkezeles.betoltes(MENTES)
            except (OSError, ValueError, IndexError):
                sakktabla.reset()
        
        if rajzolj:
            rajzolj = False
            ablak.fill((97,192,255))
            korvonalak()
            szinezesek(specialis)
            ablak.blit(_kepek["ujrakezdes"],(425,25))
            babukMegjelenitese(sakktabla.tabla)

    pygame.quit()

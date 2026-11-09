import pygame
import math
import osztalyok
import fajlkezeles


aHossz = 750
aSzelesseg = 500
ablak = pygame.display.set_mode((aSzelesseg,aHossz))

#Rekurzív kitöltõ eszköz
def kitoltes(regiSzin,ujSzin, x, y):
    ablak.set_at((x,y),ujSzin)
    if x+1 < aSzelesseg:
        if ablak.get_at((x+1,y)) == regiSzin:
            kitoltes(regiSzin,ujSzin,x+1,y)
    if x-1 >= 0:
        if ablak.get_at((x-1,y)) == regiSzin:
            kitoltes(regiSzin,ujSzin,x-1,y)
    if y+1 < aHossz:
        if ablak.get_at((x,y+1)) == regiSzin:
            kitoltes(regiSzin,ujSzin,x,y+1)
    if y-1 >= 0:
        if ablak.get_at((x,y-1)) == regiSzin:
            kitoltes(regiSzin,ujSzin,x,y-1)

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
                if szabaly != None:
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
    s = "FeherBastya:FeherLovas:FeherFuto:FeherKiralyno:FeherKiraly:FeherParaszt" \
        + ":FeketeBastya:FeketeLovas:FeketeFuto:FeketeKiralyno:FeketeKiraly:FeketeParaszt"
    adatok = s.split(":")
    babuk = [""]*12
    for i in range(len(babuk)):
        babuk[i] = pygame.image.load(("Kepek/" + adatok[i] + ".png"))
        babuk[i] = pygame.transform.scale(babuk[i],(32,32))
    for x in range(4):
        for y in range(4):
            for z in range(4):
                if tabla[x][y][z] != None:
                    szinPont = 0
                    if tabla[x][y][z].szin == "fekete":
                        szinPont += 6
                    if tabla[x][y][z].nev == "bastya":
                        ablak.blit(babuk[szinPont+0],(121+z*25+x*50,610-z*25-y*150))
                    elif tabla[x][y][z].nev == "lovas":
                        ablak.blit(babuk[szinPont+1],(121+z*25+x*50,610-z*25-y*150))
                    elif tabla[x][y][z].nev == "futo":
                        ablak.blit(babuk[szinPont+2],(121+z*25+x*50,610-z*25-y*150))
                    elif tabla[x][y][z].nev == "kiralyno":
                        ablak.blit(babuk[szinPont+3],(121+z*25+x*50,610-z*25-y*150))
                    elif tabla[x][y][z].nev == "kiraly":
                        ablak.blit(babuk[szinPont+4],(121+z*25+x*50,610-z*25-y*150))
                    else:
                        ablak.blit(babuk[szinPont+5],(121+z*25+x*50,610-z*25-y*150))
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
    sakktabla.tabla[xyz2[0]][xyz2[1]][xyz2[2]] = sakktabla.tabla[xyz1[0]][xyz1[1]][xyz1[2]]
    sakktabla.tabla[xyz1[0]][xyz1[1]][xyz1[2]] = None
def kirajzol():
    pygame.init()
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
                if click != None:
                    if click == "reset":
                        sakktabla.reset()
                        kor = "feher"
                        kivalasztott = None
                        specialis = None 
                    else:
                        if kivalasztott != None:
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
                            if sakktabla.tabla[kivalasztott[0]][kivalasztott[1]][kivalasztott[2]] != None:
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
                fajlkezeles.mentes("mentes.txt",sakktabla.tabla)
                fut = False
        pygame.display.update()
        ora.tick(30)

        if toltsdBe:
            toltsdBe = False
            try:
                sakktabla.tabla = fajlkezeles.betoltes("mentes.txt")
            except:
                sakktabla.reset()
        
        if rajzolj:
            rajzolj = False
            ablak.fill((97,192,255))
            korvonalak()
            szinezesek(specialis)
            ujrakezdes = pygame.image.load("Kepek/Ujrakezdes.png")
            ujrakezdes = pygame.transform.scale(ujrakezdes,(50,50))
            ablak.blit(ujrakezdes,(425,25))
            babukMegjelenitese(sakktabla.tabla)

    pygame.quit()
    quit()

import pygame
import math
from queue import PriorityQueue

#basics
LEBAR = 800
WIN = pygame.display.set_mode((LEBAR, LEBAR))
pygame.display.set_caption("Algoritma A star ")

#rgb warna
HIJAU = (111, 214, 88)
RED = (250, 66, 73)
BIRU = (105, 158, 241)
KUNING = (250, 200, 73)
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
UNGU = (212, 141, 213)
OREN = (240, 157, 119)
ABU = (87, 87, 87)
HIJAU_KEREN = (116, 201, 175)

#tampilan,  settings, and stuff
class Spot:
    def __init__ (self, baris, kolom, lebar, total_baris ):
        self.baris = baris
        self.kolom = kolom
        self.lebar =lebar
        self.total_baris = total_baris
        self.neighbors = []
        self.x = baris * lebar
        self.y = kolom * lebar
        self.warna = PUTIH

    def posisi(self):
        return self.baris , self.kolom
    def tutup (self):
        return self.warna == KUNING
    def buka (self):
        return self.warna == HIJAU_KEREN
    def barrier (self):
        return self.warna == HITAM
    def mulai (self):
        return self.warna == RED
    def akhir (self):
        return self.warna == HIJAU
    
    def reset (self):
        self.warna = PUTIH
    def buat_mulai (self):
        self.warna = RED
    def buat_tutup(self):
        self.warna = KUNING
    def buat_buka(self):
        self.warna = HIJAU_KEREN
    def buat_barrier (self):
        self.warna = HITAM
    def buat_akhir (self):
        self.warna = HIJAU
    def buat_jalan (self):
        self.warna = UNGU
    def gambar(self,windows):
        pygame.draw.rect(windows, self.warna, (self.x, self.y, self.lebar, self.lebar))

    def update_neighbors(self, jaring): #bawah, atas, kanan , kiri
        self.neighbors = []
        if self.baris < self.total_baris - 1 and not jaring[self.baris +1][self.kolom].barrier():
            self.neighbors.append(jaring[self.baris +1][self.kolom])

        if self.baris > 0 and not jaring[self.baris -1][self.kolom].barrier():
            self.neighbors.append(jaring[self.baris -1][self.kolom])

        if self.kolom < self.total_baris - 1 and not jaring [self.baris][self.kolom +1].barrier():
            self.neighbors.append(jaring[self.baris][self.kolom +1])

        if self.kolom > 0 and not jaring[self.baris ][self.kolom -1].barrier():
            self.neighbors.append(jaring[self.baris ][self.kolom-1])


    def __lt__ (self, other):
        return False
    
def heuristik (p1, p2):
    x1 ,y1 = p1
    x2 , y2 = p2
    return abs (x1 - x2) + abs (y1- y2)

def reconstruct_path (came_from, current, gambar):
    while current in came_from:
        current = came_from[current]
        current.buat_jalan()
        gambar()

def algoritma(gambar, jaring, mulai, selesai):
    count = 0 
    openset= PriorityQueue()
    openset.put((0, count , mulai))
    came_from = {}
    g = {spot: float("inf") for baris in jaring for spot in baris }
    g[mulai] = 0
    f = {spot: float("inf") for baris in jaring for spot in baris }
    f[mulai] = heuristik(mulai.posisi(), selesai.posisi())

    openset_hash = {mulai}

    while not openset.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openset.get()[2]
        openset_hash.remove(current)

        if current == selesai:
            reconstruct_path(came_from, selesai, gambar)
            selesai.buat_akhir()
            return True
        
        for neighbor in current.neighbors:
            temp_g = g[current] + 1

            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + heuristik(neighbor.posisi(), selesai.posisi())
                if neighbor not in openset_hash:
                    count += 1
                    openset.put((f[neighbor], count, neighbor))
                    openset_hash.add(neighbor)
                    neighbor.buat_buka()

        gambar()

        if current != mulai:
            current.buat_tutup()

    return False

def buat_jaring (baris_ba, lebar):
    jaring = []
    celah = lebar // baris_ba
    for i in range (baris_ba):
        jaring.append([])
        for j in range (baris_ba):
                spot = Spot(i,j,celah,baris_ba)
                jaring[i].append(spot)
    return jaring
                                            
def gambar_jar (windows, baris_ba, lebar):
    celah = lebar // baris_ba
    for i in range (baris_ba):
            pygame.draw.line(windows, ABU, (0,i * celah), (lebar, i * celah))
            for j in range (baris_ba):
                 pygame.draw.line(windows, ABU, (j * celah , 0), (j * celah, lebar))
                                                                                    
def gambar (windows, jaring, baris_ba, lebar):
    windows.fill(PUTIH)

    for baris in jaring:
        for spot in baris:
            spot.gambar(windows)

    gambar_jar(windows, baris_ba, lebar)
    pygame.display.update()

def pos_diklik (pos, baris_ba, lebar):
    celah = lebar // baris_ba
    y , x = pos

    baris = y // celah
    kolom = x // celah
    return baris, kolom

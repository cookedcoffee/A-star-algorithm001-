from system import*

def main (windows , lebar):
    BARIS_BA = 50 #bisa di ubah semaunya
    jaring = buat_jaring(BARIS_BA, lebar)

    mulai = None
    selesai = None

    run = True
    
    while run:
        gambar(windows, jaring, BARIS_BA, lebar)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                baris , kolom = pos_diklik(pos, BARIS_BA, lebar)
                spot = jaring [baris] [kolom]
                if not mulai and spot != selesai:
                    mulai = spot
                    mulai.buat_mulai()

                elif not selesai and spot != mulai:
                    selesai = spot
                    selesai.buat_akhir()

                elif spot != selesai and spot != mulai:
                    spot.buat_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                baris , kolom = pos_diklik(pos, BARIS_BA, lebar)
                spot = jaring [baris] [kolom]
                spot.reset()
                if spot == mulai:
                    mulai = None
                elif spot == selesai:
                    selesai = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and mulai and selesai:
                    for baris in jaring:
                        for spot in baris:
                            spot.update_neighbors(jaring)
                    algoritma(lambda: gambar(windows, jaring, BARIS_BA, lebar),jaring, mulai, selesai)

                if event.key == pygame.K_c:
                    mulai = None
                    selesai = None
                    jaring = buat_jaring(BARIS_BA , lebar)



    pygame.quit()

main(WIN, LEBAR )
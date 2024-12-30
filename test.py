links = ['https://www.facebook.com/rohim.tekik.1/videos', 'https://www.facebook.com/rohim.tekik.1/videos/274756671738643/']

for i in links:
    if len(i.split('videos/')) == 2:
        print('Masuk')
    else:
        print('Gagal')
        
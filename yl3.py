import sqlite3
con = sqlite3.connect('epood_okahn.db')

def kuva_kirjed():
    cursor = con.execute("SELECT * FROM okahn WHERE car_year<2000 ORDER BY car_year ASC LIMIT 10")
    for row in cursor:
        print(row)
 
def kesk_aasta():
    cursor = con.execute("SELECT AVG(car_year), MAX(car_price) FROM okahn")
    for row in cursor:
        print(row)
        
        
        
def koige_uuemad():
    cursor = con.execute("SELECT * FROM okahn ORDER BY car_year DESC LIMIT 5  ")
    for a in cursor:
        print(a)
 
 
def viis_kallimat():
        automark = input("sisesta automark: ")
        cursor = con.execute("SELECT * FROM okahn WHERE car_make=? ORDER BY last_name DESC LIMIT 5",
                         automark,)
        rows = c.fetchall()
        for row in rows:
            print(row)
 
def id_kustutaja():
    
 
 
 
 
def kustutaja():
    mark = input("Sisesta auto mark, mida soovid kustutada: ")
    con.execute("DELETE FROM okahn WHERE car_year < 2000 AND car_make=?," (mark))
    conn.commit()


loop=1
while loop==1:
    print("--------------------------menüü-------------------------------")
    print("2 2000 ja vanemad autod")
    print("9 välju programmist")
    print("3 Keskmine autode aasta, kõige kallim")
    print("4 viis kõige uuemat autot")
    print(" Kustuta auto id järgi")
    print("6 kustuta read, kus autode aasta jääb alla 200 ning kindla margi järgi")
    valik=int(input("tee oma valik: "))
    if valik==2:
        kuva_kirjed()
        
    if valik==9:
        loop=0
        
    
    if valik==3:
        kesk_aasta()
        
        
    if valik==4:
        koige_uuemad()
        
   if valik==5:
       id_kustutaja()
   
   
    if valik==6:
        kustutaja()
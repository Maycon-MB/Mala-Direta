def ViewTable (TableNme):
try: # LOAD TABLE FROM Sqlite3 Database
    txt2="SELECT * FROM {} ".format(TableNme)
    cursor.execute(txt2)
    ##Include headers###
    txt2='S.No '
    for j in fields: txt2=txt2+j +" "
    txt2=txt2+'\n'
    
    #converts the table into string separated by Comma
           #fine as long as table is not very massive running more than 3 Mbs, having more than 1000 records
    while True:
            h1=cursor.fetchone()
            if not h1: break
            for j in h1:txt2=txt2+str(j)+"   "
            txt2=txt2+'\n'
    #sg.popup('Archieved table', txt2)
    #Define text to load by text= before calling me
    layout2 = [[sg.Multiline(txt2,size=(28,28),key='-Items-'),],[sg.Ok()] ]
    sg.Window('Scroll to see the whole database', layout2,finalize=True).read(close=True)
    
except:
        sg.popup_error('Failed','Access denied or Memory full.')   
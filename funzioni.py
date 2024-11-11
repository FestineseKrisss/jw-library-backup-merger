import zipfile, sqlite3, shutil, os
from os import listdir
from os.path import isfile, join

table_order = [
            "Location",
            "IndependentMedia",
            "UserMark",
            "Note",
            "Bookmark",
            "PlaylistItemAccuracy",
            "PlaylistItem",
            "Tag",
            "BlockRange",
            "InputField",
            "PlaylistItemIndependentMediaMap",
            "PlaylistItemLocationMap",
            "PlaylistItemMarker",
            "PlaylistItemMarkerBibleVerseMap",
            "PlaylistItemMarkerParagraphMap",
            "TagMap",
        ]

def get_nomi_tabelle():
    return [tabella for tabella in table_order]

def get_nomi_colonne(nome_tabella):
    db = sqlite3.connect("/home/kristian/Scaricati/jwlMerger/cartelle/userData.db")
    db.row_factory = sqlite3.Row

    colonne = db.execute(f"SELECT name FROM pragma_table_info('{nome_tabella}')").fetchall()
    return[colonna[0] for colonna in colonne]

def get_dati_utente(nome, cognome, files):

    for i in range(1,4):
        directory = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}"
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    for i in range(1, len(files)+1):
        directory = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}"
        backup = files[i-1]
        with zipfile.ZipFile(backup, 'r') as zip_ref:
            zip_ref.extractall(directory)
        
        file_cartella = [f for f in listdir(f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}") if isfile(join(f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}", f)) and f != "userData.db"]
        for file in file_cartella:
            shutil.copy(f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}/{file}",f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}3/{file}")
            
    
    
    src = "/home/kristian/Scaricati/jwlMerger/cartelle/userData.db"
    dst = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}3/userData.db"
    
    shutil.copy(src, dst)

        
    db1 = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}1/userData.db"
    db2 = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}2/userData.db"
    db3 = f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}3/userData.db"
        
    return [db1, db2, db3]

def connetti_database(databases):
    conn1 = sqlite3.connect(databases[0])
    conn2 = sqlite3.connect(databases[1])
    conn3 = sqlite3.connect(databases[2])
    
    conn1.row_factory = sqlite3.Row
    conn2.row_factory = sqlite3.Row
    conn3.row_factory = sqlite3.Row
    
    return [conn1, conn2, conn3]
    

def merge_dati(db1, db2, db3):
    
    tabelle = get_nomi_tabelle()
    for tabella in tabelle:    
        
        if tabella == "grdb_migrations" or tabella == "LastModified":
            continue
        else:
            valori_tabella1 = db1.execute(f"SELECT * FROM {tabella}").fetchall()
            valori_tabella2 = db2.execute(f"SELECT * FROM {tabella}").fetchall()

            
            colonne = get_nomi_colonne(tabella)

            query_insert = f"INSERT INTO {tabella} ({', '.join([colonna for colonna in colonne]).removeprefix("[").removesuffix("]")}) values ({', '.join(['?'] * len(colonne))})"

            dati_insert = []
            if len(valori_tabella1) > len(valori_tabella2):
                for i in valori_tabella1:
                    for j in valori_tabella2:
                        if i[1:] == j[1:]:
                            dati_insert.append(tuple([i[contatore] for contatore in range(len(i))]))
                            db1.execute(f"DELETE FROM {tabella} WHERE {colonne[0]} = ?", (i[0], ))
                            db2.execute(f"DELETE FROM {tabella} WHERE {colonne[0]} = ?", (j[0], ))
                            break
            else:
                for i in valori_tabella2:
                    for j in valori_tabella1:
                        if i[1:] == j[1:]:
                            dati_insert.append([i[contatore] for contatore in range(len(i))])
                            db1.execute(f"DELETE FROM {tabella} WHERE {colonne[0]} = ?", (j[0], ))
                            db2.execute(f"DELETE FROM {tabella} WHERE {colonne[0]} = ?", (i[0], ))
                            break
            
            db3.executemany(query_insert, dati_insert)
            
            valori_tabella1 = db1.execute(f"SELECT * FROM {tabella}").fetchall()
            valori_tabella2 = db2.execute(f"SELECT * FROM {tabella}").fetchall()
            
            
            
            if tabella != "PlaylistItemIndependentMediaMap" and tabella != "PlaylistItemLocationMap" and tabella != "PlaylistItemMarkerBibleVerseMap" and tabella != "PlaylistItemMarkerParagraphMap" and tabella != "InputField":
                colonne = colonne[1:]
                query_insert = f"INSERT INTO {tabella} ({', '.join([colonna for colonna in colonne]).removeprefix("[").removesuffix("]")}) values ({', '.join(['?'] * len(colonne))})"
            else:
                pass
            
            dati_insert = []
            if len(valori_tabella1)>0:
                for i in valori_tabella1:
                    dati = [i[contatore] for contatore in range(len(i))]
                    if tabella != "PlaylistItemIndependentMediaMap" and tabella != "PlaylistItemLocationMap" and tabella != "PlaylistItemMarkerBibleVerseMap" and tabella != "PlaylistItemMarkerParagraphMap" and tabella != "InputField":
                        dati = dati[1:]
                    
                    dati_insert.append(tuple(dati))
                    

            db3.executemany(query_insert,dati_insert)
            
            dati_insert = []
            if len(valori_tabella2)>0:
                for i in valori_tabella2:
                    dati = [i[contatore] for contatore in range(len(i))]
                    if tabella != "PlaylistItemIndependentMediaMap" and tabella != "PlaylistItemLocationMap" and tabella != "PlaylistItemMarkerBibleVerseMap" and tabella != "PlaylistItemMarkerParagraphMap" and tabella != "InputField":
                        dati = dati[1:]
                    else:
                        pass
                    dati_insert.append(tuple(dati))
            
            db3.executemany(query_insert, dati_insert)
            
    db1.commit()
    db2.commit()
    db3.commit()
    
            
            
def crea_zip_jwlibrary(nome, cognome):
    shutil.make_archive(f"{nome}{cognome}", 'zip', f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}3")
    os.rename(f"{nome}{cognome}.zip", f"{nome}{cognome}.jwlibrary")
    shutil.move(f"{nome}{cognome}.jwlibrary", f"/home/kristian/Scaricati/jwlMerger/merged/{nome}{cognome}.jwlibrary")


def rimuovi_file_e_cartelle(nome, cognome, files):
    for i in range(1,4):
        shutil.rmtree(f"/home/kristian/Scaricati/jwlMerger/cartelle/{nome}{cognome}{i}")
    for file in files:
        os.remove(f"/home/kristian/Scaricati/jwlMerger/cartelle/{file}")


#----------------MAIN-----------------------------
#if __name__=="__main__":
#    dati = get_dati_utente()
#    db = connetti_database(dati[2], dati[3], dati[4])
#    merge_dati(db[0], db[1], db[2])
#    crea_zip_jwlibrary(f"/home/kristian/Scaricati/jwlMerger/cartelle/{dati[0]}{dati[1]}3", f"/home/kristian/Scaricati/jwlMerger/merged/{dati[0]}{dati[1]}.jwlibrary")
#    rimuovi_cartelle
    
    
    
    
    

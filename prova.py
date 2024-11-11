import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sqlite3
import threading

bibbia = {
  "1": "Genesi",
  "2": "Esodo",
  "3": "Levitico",
  "4": "Numeri",
  "5": "Deuteronomio",
  "6": "Giosuè",
  "7": "Giudici",
  "8": "Rut",
  "9": "1 Samuele",
  "10": "2 Samuele",
  "11": "1 Re",
  "12": "2 Re",
  "13": "1 Cronache",
  "14": "2 Cronache",
  "15": "Esdra",
  "16": "Neemia",
  "17": "Ester",
  "18": "Giobbe",
  "19": "Salmi",
  "20": "Proverbi",
  "21": "Ecclesiaste",
  "22": "Cantico dei Cantici",
  "23": "Isaia",
  "24": "Geremia",
  "25": "Lamentazioni",
  "26": "Ezechiele",
  "27": "Daniele",
  "28": "Osea",
  "29": "Gioele",
  "30": "Amos",
  "31": "Abdia",
  "32": "Giona",
  "33": "Michea",
  "34": "Naum",
  "35": "Abacuc",
  "36": "Sofonia",
  "37": "Aggeo",
  "38": "Zaccaria",
  "39": "Malachia",
  "40": "Matteo",
  "41": "Marco",
  "42": "Luca",
  "43": "Giovanni",
  "44": "Atti",
  "45": "Romani",
  "46": "1 Corinti",
  "47": "2 Corinti",
  "48": "Galati",
  "49": "Efesini",
  "50": "Filippesi",
  "51": "Colossesi",
  "52": "1 Tessalonicesi",
  "53": "2 Tessalonicesi",
  "54": "1 Timoteo",
  "55": "2 Timoteo",
  "56": "Tito",
  "57": "Filemone",
  "58": "Ebrei",
  "59": "Giacomo",
  "60": "1 Pietro",
  "61": "2 Pietro",
  "62": "1 Giovanni",
  "63": "2 Giovanni",
  "64": "3 Giovanni",
  "65": "Giuda",
  "66": "Rivelazione"
}
def print_dati(locations):
    for location in locations:
        if type(location[0]) == type(None) and type(location[1]) == type(None) and type(location[2]) == type(None):
            continue
        elif location[3] == "nwtsty":
            libro = bibbia.get(str(location[0]))
            capitolo = location[1]
            print(libro, capitolo, sep=" | ")
        else:
            docId = str(location[2])
            base_url = "https://wol.jw.org/it/wol/d/r6/lp-i/"


            url = base_url+docId+"?"
            r = requests.get(f'{base_url}{docId}?')
            try:
                soup = BeautifulSoup(r.content, 'html.parser')
                descrizione_documento = soup.find("input", {"id": "documentDescription"})
                titolo_documento = soup.find("input", {"id": "contentTitle"})
                print(descrizione_documento["value"], titolo_documento["value"], url, sep=" | ")
            except Exception as e:
                pass

db_path = "/home/kristian/Scaricati/UserdataBackup_2024-11-04_iPhone/userData.db"
connection = sqlite3.connect(db_path)
connection.row_factory = sqlite3.Row

locations = connection.execute("SELECT BookNumber, ChapterNumber, DocumentId, KeySymbol FROM Location").fetchmany(20)

t1 = threading.Thread(target=print_dati, args=(locations[0:5],))
t2 = threading.Thread(target=print_dati, args=(locations[5:10],))
t3 = threading.Thread(target=print_dati, args=(locations[10:15],))
t4 = threading.Thread(target=print_dati, args=(locations[15:20],))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

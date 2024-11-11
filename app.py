from flask import Flask, render_template, url_for, send_file, session, redirect, request, flash
from werkzeug.utils import secure_filename
import os, funzioni

UPLOAD_FOLDER = '/home/kristian/Scaricati/jwlMerger/cartelle/'
ALLOWED_EXTENSIONS = {'jwlibrary'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'krisJWLmerger'    


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST","GET"])
def index():
    session["unito"] = False
    if request.method == "POST":
        nome = request.form.get("nome").lower().capitalize()
        cognome = request.form.get("cognome").lower().capitalize()
        session["nome"], session["cognome"] = nome, cognome
        
        file1 = request.files["file1"]
        file2 = request.files["file2"]
        
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        if filename1.endswith(".jwlibrary") and filename2.endswith(".jwlibrary"):
        
            try:
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
                
                path1 = os.path.join(app.config["UPLOAD_FOLDER"], filename1)
                path2 = os.path.join(app.config["UPLOAD_FOLDER"], filename2)
        
                databases = funzioni.get_dati_utente(nome, cognome, [path1, path2])
                connections = funzioni.connetti_database(databases)
                funzioni.merge_dati(connections[0], connections[1], connections[2])
                funzioni.crea_zip_jwlibrary(nome, cognome)
                funzioni.rimuovi_file_e_cartelle(nome, cognome, [filename1, filename2])
            except Exception as e: 
                flash(e)
                return render_template("index.html")
        else:
            flash("I file inseriti non sono dei backup jwlibrary")
            return render_template("index.html")
        
        session["unito"] = True
        return redirect("/download")
        
    return render_template("index.html")

@app.route("/download", methods=["POST","GET"])
def download():
    if session["unito"] == True:
        if request.method == "POST":
            if request.form.get("bottone") == "Scarica":
                nome, cognome = session["nome"], session["cognome"]
                return send_file(f"/home/kristian/Scaricati/jwlMerger/merged/{nome}{cognome}.jwlibrary")
            else:
                return render_template("index.html")
        else:
            pass
    else:
        return redirect("/")
    return render_template("download.html")
    

if __name__=="__main__":
    app.run(debug=True)
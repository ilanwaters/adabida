from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import shutil
from utils.paisos import normalitza_pais
from models import (
    db, Usuari, Entrada, ArxiuAdjunt, MembreOrganitzacio, Organitzacio, PerfilBiografic,
    EntradaOrganitzacio, EntradaFamilia, EspaiFamiliar, MembreFamilia
)
import time  
from genera_identificadors import extreu_dades_identificador
from utils.gestio_imatges import generar_miniatura
import subprocess
import json
from models.ubicacions import Pais
from utils.sanititzar import neteja_html

nova_entrada_bp = Blueprint("nova_entrada", __name__)

def detectar_tipus_media(ruta_fitxer):
    print(f"🔍 ANALITZANT: {ruta_fitxer}")
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_streams', ruta_fitxer
        ], capture_output=True, text=True, check=True)
        
        data = json.loads(result.stdout)
        print(f"📊 STREAMS TROBATS: {len(data.get('streams', []))}")
        
        for stream in data.get('streams', []):
            print(f"   - Stream tipus: {stream.get('codec_type')}")
            if stream.get('codec_type') == 'video':
                return 'video'
        return 'audio'
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 'webm_desconegut'

def generar_miniatura_segons_tipus(nom_fitxer, ruta_fitxer, carpeta_final, tipus_media):
    """Genera miniatura segons el tipus de fitxer"""
    print(f"🔍 Processant: {nom_fitxer}, tipus: {tipus_media}")
    
    if tipus_media == 'imatge':
        # Miniatura normal per imatges
        ruta_mini = os.path.join(carpeta_final, "mini", nom_fitxer)
        if not os.path.exists(ruta_mini):
            generar_miniatura(ruta_fitxer, ruta_mini)
            print(f"✅ Miniatura imatge creada: {ruta_mini}")
    else:
        # Icona per altres tipus
        mini_dir = os.path.join(carpeta_final, "mini")
        os.makedirs(mini_dir, exist_ok=True)
        print(f"📁 Carpeta mini: {mini_dir}")
        
        if tipus_media == 'imatge':
            # Per imatges, manté el nom original
            base_nom = nom_fitxer
        else:
            base_nom = f"{nom_fitxer}.png"
        desti_mini = os.path.join(mini_dir, base_nom)
        print(f"🎯 Destí: {desti_mini}")
        
        # 🔧 CANVI AQUÍ: Ruta absoluta
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if tipus_media == "video":
            try:
                resultat = subprocess.run([
                    'ffmpeg', '-y', '-i', ruta_fitxer, '-ss', '00:00:01',
                    '-vframes', '1', '-vf', 'scale=320:-1', desti_mini
                ], capture_output=True, text=True, timeout=15)
                if os.path.exists(desti_mini):
                    print(f"✅ Fotograma extret amb ffmpeg (seg 1): {desti_mini}")
                    return
                else:
                    print(f"⚠️ ffmpeg no ha generat fotograma al seg 1, reintentant al seg 0: {resultat.stderr}")
                    resultat2 = subprocess.run([
                        'ffmpeg', '-y', '-i', ruta_fitxer, '-ss', '00:00:00',
                        '-vframes', '1', '-vf', 'scale=320:-1', desti_mini
                    ], capture_output=True, text=True, timeout=15)
                    if os.path.exists(desti_mini):
                        print(f"✅ Fotograma extret amb ffmpeg (seg 0): {desti_mini}")
                        return
                    else:
                        print(f"⚠️ ffmpeg tampoc ha generat fotograma al seg 0: {resultat2.stderr}")
            except Exception as e:
                print(f"❌ Error extraient fotograma: {e}")
            icona = os.path.join(base_dir, "static", "icons", "video_webm.png")
        elif tipus_media == "audio":
            icona = os.path.join(base_dir, "static", "icons", "audio_webm.png")
        else:
            icona = os.path.join(base_dir, "static", "icons", "sense_imatge.png")

        print(f"🔍 Buscant icona a: {icona}")
        
        if os.path.exists(icona):
            shutil.copy(icona, desti_mini)
            print(f"✅ Icona copiada de {icona} a {desti_mini}")
        else:
            print(f"❌ No trobat: {icona}")
            
@nova_entrada_bp.route("/nova_entrada_personal", methods=["GET", "POST"])
def nova_entrada_personal():

    usuari_login = session.get("usuari")
    if not usuari_login:
        flash("Sessió no vàlida")
        return redirect(url_for("login.login"))

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        flash("Usuari no trobat")
        return redirect(url_for("login.login"))

    if request.method == "GET":
        tema_preomplert = request.args.get('tema', '')
        categoria_preomplerta = request.args.get('categoria', '')
    
    # Query per veure tots els membres d'organitzacions
        tots_membres = MembreOrganitzacio.query.filter_by(usuari_id=usuari.id).all()
        print(f"Membres trobats: {len(tots_membres)}")
    
        for membre in tots_membres:
            print(f"  - Membre de: {membre.organitzacio.nom} amb rol: {membre.rol}")

        usuari_organitzacions = db.session.query(Organitzacio)\
            .join(MembreOrganitzacio, MembreOrganitzacio.organitzacio_id == Organitzacio.id)\
            .filter(MembreOrganitzacio.usuari_id == usuari.id)\
            .all()

        usuari_families = db.session.query(EspaiFamiliar)\
            .join(MembreFamilia, MembreFamilia.espai_familiar_id == EspaiFamiliar.id)\
            .filter(MembreFamilia.usuari_id == usuari.id)\
            .all()
    
        print(f"Organitzacions finals: {len(usuari_organitzacions)}")
        print(f"Famílies finals: {len(usuari_families)}")

        return render_template("pagina_personal/nova_entrada.html", 
                        usuari=usuari, 
                        perfil=usuari.perfil, 
                        usuari_organitzacions=usuari_organitzacions,
                        usuari_families=usuari_families,
                        tema_preomplert=tema_preomplert,
                        categoria_preomplerta=categoria_preomplerta) 

    titol = request.form.get("titol")
    tema = request.form.get("tema")
   

# Gestió categoria
    from models.tematiques import CategoriaTema
    categoria_id = request.form.get('categoria')
    categoria_manual = request.form.get('categoria_manual', '').strip()

# Si ha triat "nova" i ha escrit un nom, crear-la
    if categoria_id == 'nova' and categoria_manual:
        paisCodi = request.form.get('pais') or 'ES'
        pais = Pais.query.filter_by(codi_iso=paisCodi).first()
        if pais:
            nova_categoria = CategoriaTema(nom=categoria_manual, pais_id=pais.id)
            db.session.add(nova_categoria)
            db.session.flush()
            categoria_id = nova_categoria.id
        else:
            categoria_id = None

    any_text = request.form.get("any")
    pais = request.form.get("pais")
    regio = request.form.get("regio")
    municipi = request.form.get("municipi")

    contingut = neteja_html(request.form.get("contingut"))
    titol_imatge = request.form.get("titol_imatge")
    descripcio_imatge = request.form.get("descripcio_imatge")
    any_imatge = request.form.get("any_imatge")
    pais_imatge = request.form.get("pais_imatge")
    regio_imatge = request.form.get("regio_imatge")
    municipi_imatge = request.form.get("municipi_imatge")
    referencia = request.form.get("referencia_ubicacio")

    mode_guardat = request.form.get("mode_guardat", "publicar")
    entrada = Entrada(
        usuari_id=usuari.id,
        titol=titol,
        tema=tema,
        any_text=any_text,
        contingut=contingut,
        data_creacio=datetime.utcnow(),
        es_publica=(mode_guardat != "esborrany"),
        titol_imatge=titol_imatge,
        descripcio_imatge=descripcio_imatge,
        any_imatge=any_imatge,
        referencia=referencia,
        pais=pais,
        regio=regio,
        municipi=municipi,
        pais_imatge=pais_imatge,
        regio_imatge=regio_imatge,
        municipi_imatge=municipi_imatge,
    )

    db.session.add(entrada)

    if categoria_id and categoria_id != 'nova':
        categoria = CategoriaTema.query.get(categoria_id)
        if categoria:
            entrada.categories = [categoria]
    db.session.commit()

    compartir_org = request.form.getlist('compartir_org[]')
    compartir_fam = request.form.getlist('compartir_fam[]')

    print(f"🔍 Organitzacions seleccionades: {compartir_org}")
    print(f"🔍 Famílies seleccionades: {compartir_fam}")

# Compartir amb organitzacions
    for org_id in compartir_org:
        nova_relacio = EntradaOrganitzacio(
            entrada_id=entrada.id,
            organitzacio_id=int(org_id)
        )
        db.session.add(nova_relacio)
        print(f"✅ Entrada compartida amb organització ID: {org_id}")

# Compartir amb famílies
    for fam_id in compartir_fam:
        nova_relacio = EntradaFamilia(
            entrada_id=entrada.id,
            espai_familiar_id=int(fam_id)
        )
        db.session.add(nova_relacio)
        print(f"✅ Entrada compartida amb família ID: {fam_id}")

    db.session.commit()
    print(f"💾 Compartició guardada correctament")

    pais = normalitza_pais(usuari.pais_residencia)
    avui = datetime.now()
    any = str(avui.year)
    mes = str(avui.month).zfill(2)
    carpeta_temp = os.path.join("umberto", "media", "temp", pais, any, mes, usuari_login)
    carpeta_final = os.path.join("umberto", "usuaris", pais, any, mes, usuari_login, "entrades", str(entrada.id))

    
    metadades_arxius = {}
    i = 0
    while f'arxiu_fitxer_{i}' in request.form:
        nom_fitxer_meta = request.form.get(f'arxiu_fitxer_{i}')
        metadades_arxius[nom_fitxer_meta] = {
            'titol': request.form.get(f'arxiu_titol_{i}', '').strip() or None,
            'any_arxiu': request.form.get(f'arxiu_any_{i}', '').strip() or None,
            'pais': request.form.get(f'pais_arxiu_{i}', '').strip() or None,
            'regio': request.form.get(f'regio_arxiu_{i}', '').strip() or None,
            'municipi': request.form.get(f'municipi_arxiu_{i}', '').strip() or None,
            'descripcio': request.form.get(f'arxiu_descripcio_{i}', '').strip() or None,
            'referencia': request.form.get(f'arxiu_referencia_{i}', '').strip() or None,
        }
        i += 1    

    if os.path.exists(carpeta_temp):
        os.makedirs(carpeta_final, exist_ok=True)
        for fitxer in os.listdir(carpeta_temp):
            ruta_origen = os.path.join(carpeta_temp, fitxer)
            ruta_desti = os.path.join(carpeta_final, fitxer)
            shutil.move(ruta_origen, ruta_desti)
  
            if fitxer.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
                tipus_media = "imatge"
            elif fitxer.lower().endswith(".webm"):
                tipus_media = detectar_tipus_media(ruta_desti)
            else:
                tipus_media = "desconegut"

            generar_miniatura_segons_tipus(fitxer, ruta_desti, carpeta_final, tipus_media)
    
            ara = datetime.now()
            any = str(ara.year)
            mes = ara.strftime("%m").lower()
            pais_entrada = normalitza_pais(usuari.pais_residencia)
            carpeta_pendents = os.path.join("umberto", "media", "pendents", any, pais_entrada, mes)
            os.makedirs(carpeta_pendents, exist_ok=True)
            ruta_desti_pendents = os.path.join(carpeta_pendents, fitxer)
            shutil.copy(ruta_desti, ruta_desti_pendents)
    
            meta = metadades_arxius.get(fitxer, {})
            nou_arxiu = ArxiuAdjunt(
                entrada_id=entrada.id,
                nom_fitxer=fitxer,
                tipus=fitxer.split(".")[-1].lower(),
                tipus_media=tipus_media,
                titol=meta.get('titol'),
                any_arxiu=meta.get('any_arxiu'),
                pais=meta.get('pais'),
                regio=meta.get('regio'),
                municipi=meta.get('municipi'),
                descripcio=meta.get('descripcio'),
                referencia=meta.get('referencia'),
            )
            db.session.add(nou_arxiu)
        
        data_conversa = request.form.get("data_conversa")
        if data_conversa:
            try:
                from models import Conversa, ConversaParticipant
                from werkzeug.utils import secure_filename
     
                conversa = Conversa(
                    usuari_id=usuari.id,
                    entrada_id=entrada.id,
                    lloc_municipi=request.form.get("municipi_conversa", ""),
                    lloc_regio=request.form.get("regio_conversa", ""),
                    lloc_pais=request.form.get("pais_conversa", ""),
                    durada_minuts=int(request.form.get("durada_minuts", 0)) if request.form.get("durada_minuts") else None,
                    observacions_generals=request.form.get("observacions_generals", "")
                )
                       
                conversa.data_conversa = datetime.strptime(data_conversa, '%Y-%m-%d').date()
        
                db.session.add(conversa)
                db.session.flush()  # Per obtenir ID
                
                # 2. CREAR PARTICIPANTS
                i = 0
                while f'participant_nom_{i}' in request.form:
                    nom = request.form.get(f'participant_nom_{i}', '').strip()
                    if nom:
                        participant = ConversaParticipant(
                            conversa_id=conversa.id,
                            nom=request.form.get(f'participant_nom_{i}', '').strip(),
                            primer_cognom=request.form.get(f'participant_primer_cognom_{i}', '').strip() or None,
                            segon_cognom=request.form.get(f'participant_segon_cognom_{i}', '').strip() or None,
                            lloc_municipi=request.form.get(f'municipi_participant_{i}', ''),
                            lloc_regio=request.form.get(f'regio_participant_{i}', ''),
                            lloc_pais=request.form.get(f'pais_participant_{i}', ''),
                            observacions=request.form.get(f'participant_observacions_{i}', ''),
                            ordre=i + 1
                        )
                        
                        # Data naixement (opcional)
                        data_naix = request.form.get(f'participant_data_naixement_{i}')
                        if data_naix:
                            try:
                                participant.data_naixement = datetime.strptime(data_naix, '%Y-%m-%d').date()
                            except:
                                pass
                        
                        db.session.add(participant)
                    i += 1
                
                print(f"✅ Conversa {conversa.id} creada amb {i} participants")
                
                # 3. CREAR CARPETA CONVERSES
                carpeta_converses = os.path.join(carpeta_final, "converses")
                os.makedirs(carpeta_converses, exist_ok=True)
                print(f"📁 Carpeta creada: {carpeta_converses}")
                
                # 4. MOURE ARXIUS DE CONVERSA
                # Els arxius ja estan a carpeta_final, només cal moure'ls a /converses
                
                # Àudios conversa
                audios_conversa = request.form.getlist("audios_conversa[]")
                for audio_nom in audios_conversa:
                    origen = os.path.join(carpeta_final, audio_nom)
                    desti = os.path.join(carpeta_converses, audio_nom)
                    if os.path.exists(origen):
                        shutil.move(origen, desti)
                        print(f"🎤 Àudio mogut a converses: {audio_nom}")
                    arxiu_bd = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=audio_nom).first()
                    if arxiu_bd:
                        arxiu_bd.es_conversa = True
                
                # Vídeos conversa
                videos_conversa = request.form.getlist("videos_conversa[]")
                for video_nom in videos_conversa:
                    origen = os.path.join(carpeta_final, video_nom)
                    desti = os.path.join(carpeta_converses, video_nom)
                    if os.path.exists(origen):
                        shutil.move(origen, desti)
                        print(f"🎥 Vídeo mogut a converses: {video_nom}")
                    arxiu_bd = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=video_nom).first()
                    if arxiu_bd:
                        arxiu_bd.es_conversa = True
                
                # 5. ARXIU MANUAL (si n'hi ha)
                arxiu_conversa = request.files.get('arxiu_conversa')
                if arxiu_conversa and arxiu_conversa.filename:
                    nom_segur = secure_filename(arxiu_conversa.filename)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nom_final = f"conversa_{timestamp}_{nom_segur}"
                    
                    ruta_desti = os.path.join(carpeta_converses, nom_final)
                    arxiu_conversa.save(ruta_desti)
                    print(f"📎 Arxiu manual guardat: {nom_final}")
                    
                    # Assignar a conversa (opcional)
                    conversa.arxiu_nom = nom_final
                    ext = nom_final.split('.')[-1].lower()
                    if ext in ['mp3', 'wav', 'ogg', 'webm', 'm4a']:
                        conversa.arxiu_tipus = 'audio'
                    elif ext in ['mp4', 'avi', 'mov']:
                        conversa.arxiu_tipus = 'video'
                
                print("✅ Conversa processada completament")
                
            except Exception as e:
                print(f"❌ Error amb conversa: {e}")
               
        db.session.commit()
        shutil.rmtree(carpeta_temp, ignore_errors=True)
       
        fitxers_guardats = os.listdir(carpeta_final)
        for fitxer in fitxers_guardats:
            if fitxer.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                entrada.nom_fitxer = fitxer
                db.session.commit()
                break
        if not entrada.nom_fitxer:
            primer = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id).first()
            if primer and primer.nom_fitxer.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                entrada.nom_fitxer = primer.nom_fitxer
                db.session.commit()

    if mode_guardat == "esborrany":
        flash("Esborrany guardat correctament.")
    else:
        flash("Entrada creada correctament.")
    carpeta_static_temp = os.path.join("static", "temp")
    if os.path.exists(carpeta_static_temp):
        shutil.rmtree(carpeta_static_temp, ignore_errors=True)
        
    return redirect("/entrades")

@nova_entrada_bp.route("/editar_entrada_personal/<int:entrada_id>", methods=["GET", "POST"])
def editar_entrada_personal(entrada_id):
    entrada = Entrada.query.get_or_404(entrada_id)
    print(f"🐛 SESSIO COMPLETA: {dict(session)}")
    usuari_login = session.get("usuari")
    if not usuari_login:
        flash("Sessió no vàlida")
        return redirect(url_for("login.login"))

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        flash("Usuari no trobat")
        return redirect(url_for("login.login"))

    usuari_organitzacions = db.session.query(Organitzacio)\
        .join(MembreOrganitzacio, MembreOrganitzacio.organitzacio_id == Organitzacio.id)\
        .filter(MembreOrganitzacio.usuari_id == usuari.id)\
        .all()

    usuari_families = db.session.query(EspaiFamiliar)\
        .join(MembreFamilia, MembreFamilia.espai_familiar_id == EspaiFamiliar.id)\
        .filter(MembreFamilia.usuari_id == usuari.id)\
        .all()

    any_str = str(entrada.data_creacio.year)
    mes_str = str(entrada.data_creacio.month).zfill(2)
    pais = normalitza_pais(usuari.pais_residencia)

    perfil = PerfilBiografic.query.filter_by(usuari_id=usuari.id).first()


    if request.method == "POST":
        if request.form.get("accio") == "eliminar_arxius":
            noms_fitxers = request.form.getlist("arxius_a_eliminar")
            carpeta = os.path.join("umberto", "usuaris", pais, any_str, mes_str, usuari.nom_login, "entrades", str(entrada.id))
            eliminats = 0
            for nom_fitxer in noms_fitxers:
                ruta = os.path.join(carpeta, nom_fitxer)
                if os.path.exists(ruta):
                    os.remove(ruta)
                arxiu = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=nom_fitxer).first()
                if arxiu:
                    db.session.delete(arxiu)
                    eliminats += 1

            db.session.commit()
            flash(f"S'han eliminat {eliminats} arxius.")
            return redirect(url_for('nova_entrada.editar_entrada_personal', entrada_id=entrada.id))

        mode_guardat = request.form.get("mode_guardat", "publicar")
        entrada.es_publica = (mode_guardat != "esborrany")
        entrada.titol = request.form.get("titol")
        entrada.tema = request.form.get("tema")
        entrada.any_text = request.form.get("any")
        entrada.ubicacio = request.form.get("ubicacio")
        entrada.contingut = neteja_html(request.form.get("contingut"))
        entrada.titol_imatge = request.form.get("titol_imatge")
        entrada.any_imatge = request.form.get("any_imatge")
        entrada.ubicacio_imatge = request.form.get("ubicacio_imatge")
        entrada.descripcio_imatge = request.form.get("descripcio_imatge")
        entrada.referencia = request.form.get("referencia_ubicacio")
        audios = request.form.getlist("audios[]")
        EntradaOrganitzacio.query.filter_by(entrada_id=entrada.id).delete()
        EntradaFamilia.query.filter_by(entrada_id=entrada.id).delete()

# Processar noves seleccions
        compartir_org = request.form.getlist('compartir_org[]')
        compartir_fam = request.form.getlist('compartir_fam[]')

# Compartir amb organitzacions
        for org_id in compartir_org:
            nova_relacio = EntradaOrganitzacio(
                entrada_id=entrada.id,
                organitzacio_id=int(org_id)
            )
            db.session.add(nova_relacio)

# Compartir amb famílies
        for fam_id in compartir_fam:
            nova_relacio = EntradaFamilia(
                entrada_id=entrada.id,
                espai_familiar_id=int(fam_id)
            )
            db.session.add(nova_relacio)

        db.session.commit()

        avui = datetime.now()
        any = str(avui.year)
        mes = str(avui.month).zfill(2)
        carpeta_temp = os.path.join("umberto", "media", "temp", pais, any, mes, usuari_login)
        carpeta_final = os.path.join("umberto", "usuaris", pais, any_str, mes_str, usuari_login, "entrades", str(entrada.id))

        metadades_arxius = {}
        i = 0
        while f'arxiu_fitxer_{i}' in request.form:
            nom_fitxer_meta = request.form.get(f'arxiu_fitxer_{i}')
            metadades_arxius[nom_fitxer_meta] = {
                'titol': request.form.get(f'arxiu_titol_{i}', '').strip() or None,
                'any_arxiu': request.form.get(f'arxiu_any_{i}', '').strip() or None,
                'pais': request.form.get(f'pais_arxiu_{i}', '').strip() or None,
                'regio': request.form.get(f'regio_arxiu_{i}', '').strip() or None,
                'municipi': request.form.get(f'municipi_arxiu_{i}', '').strip() or None,
                'descripcio': request.form.get(f'arxiu_descripcio_{i}', '').strip() or None,
                'referencia': request.form.get(f'arxiu_referencia_{i}', '').strip() or None,
            }
            i += 1

        if os.path.exists(carpeta_temp):
            os.makedirs(carpeta_final, exist_ok=True)

            for fitxer in os.listdir(carpeta_temp):
                ruta_origen = os.path.join(carpeta_temp, fitxer)
                ruta_desti = os.path.join(carpeta_final, fitxer)
                shutil.move(ruta_origen, ruta_desti)

                ja_existeix = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=fitxer).first()
                if not ja_existeix:
                    nou_arxiu = ArxiuAdjunt(
                        entrada_id=entrada.id,
                        nom_fitxer=fitxer,
                        tipus=fitxer.split(".")[-1].lower()
                    )
                    db.session.add(nou_arxiu)
                        
                if fitxer.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    ruta_mini = os.path.join(carpeta_final, "mini", fitxer)
                    generar_miniatura(ruta_desti, ruta_mini)
    
            db.session.commit()
            shutil.rmtree(carpeta_temp, ignore_errors=True)

        for nom_fitxer in audios:
            ruta_origen = os.path.join(
                "umberto", "media", "temp", pais, any_str, mes_str, usuari.nom_login, nom_fitxer
            )
            ruta_desti = os.path.join(carpeta_final, nom_fitxer)

            if os.path.exists(ruta_origen):
                shutil.move(ruta_origen, ruta_desti)

                ja_existeix = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=fitxer).first()
                if not ja_existeix:
                    meta = metadades_arxius.get(fitxer, {})
                    nou_arxiu = ArxiuAdjunt(
                        entrada_id=entrada.id,
                        nom_fitxer=fitxer,
                        tipus=fitxer.split(".")[-1].lower(),
                        titol=meta.get('titol'),
                        any_arxiu=meta.get('any_arxiu'),
                        pais=meta.get('pais'),
                        regio=meta.get('regio'),
                        municipi=meta.get('municipi'),
                        descripcio=meta.get('descripcio'),
                        referencia=meta.get('referencia'),
                    )
                    db.session.add(nou_arxiu)
        if mode_guardat == "esborrany":
            flash("Esborrany guardat correctament.")
        else:
            flash("Entrada actualitzada correctament.")
        return redirect("/entrades")

    return render_template(
        "pagina_personal/nova_entrada.html",
        usuari=usuari,
        perfil=perfil,
        entrada=entrada,
        usuari_organitzacions=usuari_organitzacions,
        usuari_families=usuari_families,
        mode="editar",
        pestanya="nova"
    )

@nova_entrada_bp.route("/eliminar_arxius", methods=["POST"])
def eliminar_arxius():
    usuari_login = session.get("usuari")
    if not usuari_login:
        flash("Sessió no vàlida")
        return redirect(url_for("login.login"))

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        flash("Usuari no trobat")
        return redirect(url_for("login.login"))

    entrada_id = request.form.get("entrada_id")
    noms_fitxers = request.form.getlist("arxius_a_eliminar")

    if not entrada_id or not noms_fitxers:
        flash("Cap arxiu seleccionat")
        return redirect(url_for("nova_entrada.editar_entrada_personal", entrada_id=entrada_id))

    entrada = Entrada.query.filter_by(id=entrada_id, usuari_id=usuari.id).first()
    if not entrada:
        flash("Entrada no trobada")
        return redirect(url_for("pagina_personal.pagina_personal"))

    # Ruta carpeta d’arxius d’aquesta entrada
    carpeta = os.path.join("umberto", usuari.nom_login, "entrades", str(entrada.id))

    eliminats = 0
    for nom_fitxer in noms_fitxers:
        # 1. Esborrem del disc
        ruta_fitxer = os.path.join(carpeta, nom_fitxer)
        if os.path.exists(ruta_fitxer):
            os.remove(ruta_fitxer)
            eliminats += 1

        # 2. Esborrem de la base de dades
        arxiu = ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, nom_fitxer=nom_fitxer).first()
        if arxiu:
            db.session.delete(arxiu)

    db.session.commit()
    flash(f"Eliminats {eliminats} arxius correctament.")
    return redirect(url_for("nova_entrada.editar_entrada_personal", entrada_id=entrada.id))

 
@nova_entrada_bp.route("/pujar_audio", methods=["POST"])
def pujar_audio():
    if "usuari" not in session:
        return jsonify({"error": "No autenticat"}), 401

    usuari_login = session["usuari"]
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()

    entrada_id = request.form.get("entrada_id")
    fitxer_audio = request.files.get("audio")

    if not entrada_id or not fitxer_audio:
        return jsonify({"error": "Falten dades"}), 400

    entrada = Entrada.query.get(entrada_id)
    if not entrada:
        return jsonify({"error": "Entrada no trobada"}), 404

    any_str = str(entrada.data_creacio.year)
    mes_str = str(entrada.data_creacio.month).zfill(2)
    pais = normalitza_pais(usuari.pais_residencia)

    carpeta_destinacio = os.path.join(
        "umberto", "usuaris", pais, any_str, mes_str, usuari.nom_login, "entrades", str(entrada_id)
    )
    os.makedirs(carpeta_destinacio, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    nom_fitxer = f"audio_{timestamp}.webm"

    ruta_final = os.path.join(carpeta_destinacio, nom_fitxer)
    fitxer_audio.save(ruta_final)

    nou_arxiu = ArxiuAdjunt(
        entrada_id=entrada_id,
        nom_fitxer=nom_fitxer,
        tipus="webm"
    )
    db.session.add(nou_arxiu)
    db.session.commit()

    return jsonify({"missatge": "Àudio desat", "nom_fitxer": nom_fitxer})

@nova_entrada_bp.route("/pujar_audio_temp", methods=["POST"])
def pujar_audio_temp():
    print("🎤 Pujada d'àudio rebuda")

    if "usuari" not in session:
        return jsonify(success=False, error="Sessió no vàlida")

    usuari_login = session["usuari"]
    audio = request.files.get("audio")
    if not audio:
        return jsonify(success=False, error="No s'ha rebut cap àudio")

    avui = datetime.now()
    any = str(avui.year)
    mes = str(avui.month).zfill(2)

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify(success=False, error="Usuari no trobat")
    pais = normalitza_pais(usuari.pais_residencia) 
   
    carpeta_destinacio = os.path.join("umberto", "media", "temp", pais, any, mes, usuari_login)
    os.makedirs(carpeta_destinacio, exist_ok=True)

    data_avui = datetime.now().strftime("%Y%m%d")
    timestamp = int(time.time())
    nom_fitxer = f"{usuari_login}_{data_avui}_{timestamp}.webm"
    ruta_fitxer = os.path.join(carpeta_destinacio, nom_fitxer)
    audio.save(ruta_fitxer)

    ruta_relativa = f"temp/{pais}/{any}/{mes}/{usuari_login}/{nom_fitxer}"
    url_audio = url_for("serveis_media.serveix_media", filepath=ruta_relativa)

    return jsonify(success=True, url=url_audio, nom_fitxer=nom_fitxer)

@nova_entrada_bp.route("/pujar_imatge_temp", methods=["POST"])
def pujar_imatge_temp():
    if "usuari" not in session:
        return jsonify(success=False, error="Sessió no vàlida")

    usuari_login = session["usuari"]
    imatge = request.files.get("imatge")
    if not imatge:
        return jsonify(success=False, error="No s'ha rebut cap imatge")

    avui = datetime.now()
    any = str(avui.year)
    mes = str(avui.month).zfill(2)

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify(success=False, error="Usuari no trobat")
    pais = normalitza_pais(usuari.pais_residencia) 

    carpeta_destinacio = os.path.join("umberto", "media", "temp", pais, any, mes, usuari_login)
    os.makedirs(carpeta_destinacio, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    extensio = imatge.filename.rsplit('.', 1)[-1].lower()
    nom_fitxer = f"{usuari_login}_{timestamp}.{extensio}"

    ruta_fitxer = os.path.join(carpeta_destinacio, nom_fitxer)
    imatge.save(ruta_fitxer)

    return jsonify(success=True, nom_fitxer=nom_fitxer)

@nova_entrada_bp.route("/pujar_arxiu_temp", methods=["POST"])
def pujar_arxiu_temp():
    if "usuari" not in session:
        return jsonify(success=False, error="Sessió no vàlida")

    usuari_login = session["usuari"]
    arxiu = request.files.get("arxiu")
    if not arxiu:
        return jsonify(success=False, error="No s'ha rebut cap arxiu")

    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify(success=False, error="Usuari no trobat")
    
    from utils.paisos import normalitza_pais
    pais = normalitza_pais(usuari.pais_residencia)

    avui = datetime.now()
    any = str(avui.year)
    mes = str(avui.month).zfill(2)
    
    carpeta_destinacio = os.path.join("umberto", "media", "temp", pais, any, mes, usuari_login)
    os.makedirs(carpeta_destinacio, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    extensio = arxiu.filename.rsplit('.', 1)[-1].lower()
    nom_fitxer = f"{usuari_login}_{timestamp}.{extensio}"

    ruta_fitxer = os.path.join(carpeta_destinacio, nom_fitxer)
    arxiu.save(ruta_fitxer)

    return jsonify(success=True, nom_fitxer=nom_fitxer)

@nova_entrada_bp.route("/generar_participant_html/<int:numero>")
def generar_participant_html(numero):
    return render_template("pagina_personal/participants_conversa.html", numero=numero)

@nova_entrada_bp.route("/entrada/<int:entrada_id>/portada", methods=["POST"])
def canviar_portada(entrada_id):
    if "usuari" not in session:
        return jsonify(success=False, error="Sessió no vàlida"), 401

    usuari_login = session["usuari"]
    usuari = Usuari.query.filter_by(nom_login=usuari_login).first()
    if not usuari:
        return jsonify(success=False, error="Usuari no trobat"), 404

    entrada = Entrada.query.filter_by(id=entrada_id, usuari_id=usuari.id).first()
    if not entrada:
        return jsonify(success=False, error="Entrada no trobada o no autoritzada"), 404

    imatge = request.files.get("imatge")
    if not imatge or not imatge.filename:
        return jsonify(success=False, error="No s'ha rebut cap imatge"), 400

    extensio = imatge.filename.rsplit('.', 1)[-1].lower()
    if extensio not in ('jpg', 'jpeg', 'png', 'webp'):
        return jsonify(success=False, error="Format d'imatge no vàlid"), 400

    any_str = str(entrada.data_creacio.year)
    mes_str = str(entrada.data_creacio.month).zfill(2)
    pais = normalitza_pais(usuari.pais_residencia)
    carpeta_final = os.path.join("umberto", "usuaris", pais, any_str, mes_str, usuari.nom_login, "entrades", str(entrada.id))
    os.makedirs(carpeta_final, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    nom_fitxer = f"portada_{usuari.nom_login}_{timestamp}.{extensio}"
    ruta_final = os.path.join(carpeta_final, nom_fitxer)
    imatge.save(ruta_final)

    generar_miniatura_segons_tipus(nom_fitxer, ruta_final, carpeta_final, 'imatge')

    ArxiuAdjunt.query.filter_by(entrada_id=entrada.id, es_portada=True).update({"es_portada": False})

    nou_arxiu = ArxiuAdjunt(
        entrada_id=entrada.id,
        nom_fitxer=nom_fitxer,
        tipus=extensio,
        tipus_media='imatge',
        es_portada=True,
    )
    db.session.add(nou_arxiu)
    db.session.commit()

    return jsonify(success=True, nom_fitxer=nom_fitxer)
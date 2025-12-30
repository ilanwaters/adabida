   això és per crear el botó d'info
        <span class="info-tooltip" data-tooltip="{{ _('XXXXXX') }}">
            <button type="button" class="boto-info">i</button>
        </span>

        ✅ Usuari PostgreSQL: adabida_user
✅ Contrasenya: adabida123
✅ Base de dades: adabida_db
✅ Permisos: Totals

pgadmin password:adabida123

cd /mnt/c/Users/ilanw/Desktop/adabida
source venv/bin/activate
flask run


source ~/adabida/adabida/venv/bin/activate


flask --app app run


ENTRAR A LA DB
cd /mnt/c/Users/ilanw/Desktop/adabida
source venv/bin/activate
psql -U postgres -d adabida_db


BABEL
pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d translations
pybabel compile -d translations




hola esti traduint un .po del catala al rus, m'ajudes?  traduir, corretgir, arreglar el fuzzys (i eliminar el hastag) però sense borrar les referencies dels templates; m'ajudes? 


obrir vcs 
cd /mnt/c/Users/ilanw/Desktop/adabida
   code .
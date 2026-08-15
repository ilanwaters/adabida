// static/js/modal.js

function obreModal(entradaId, usuariId,origen = null) {
  fetch(`/api/entrada/${usuariId}/${entradaId}`)
    .then(res => res.json())
    .then(data => {
      window.entradaIdActual = data.id;

      document.getElementById('modal-titol').innerText = data.titol || "—";

      const any = data.any?.trim();
      const ubicacio = [data.municipi, data.regio, data.pais].filter(Boolean).join(", ");
      const tema = data.tema?.trim();

      let parentesi = [ubicacio, any].filter(Boolean).join(", ");
      parentesi = parentesi ? ` (${parentesi})` : "";

      document.getElementById('modal-tema').innerText = tema || "";
      document.getElementById("modal-ubicacio-any-parentesi").textContent = parentesi;

      const dataSpan = document.getElementById('modal-data');
      if (dataSpan) dataSpan.innerText = data.data_creacio || "";

      const autorSpan = document.getElementById('modal-autor');
      const metaAutor = document.getElementById('modal-meta-autor');
      if (metaAutor) metaAutor.textContent = data.usuari_nom || '';

      const metaCreacio = document.getElementById('modal-meta-creacio');
      if (metaCreacio) metaCreacio.textContent = data.data_creacio ? `Creat: ${data.data_creacio}` : '';

      const metaModificacio = document.getElementById('modal-meta-modificacio');
      if (metaModificacio) metaModificacio.textContent = data.data_modificacio ? `Modificat: ${data.data_modificacio}` : '';
      

console.log("DEBUG autorSpan:", autorSpan);
console.log("DEBUG data.usuari_nom:", data.usuari_nom);
console.log("DEBUG data.usuari_login:", data.usuari_login);

if (autorSpan && data.usuari_nom && data.usuari_login) {
  console.log("🎯 Injectant enllaç a perfil públic:", data.usuari_login);
  autorSpan.innerHTML = `<a href="/perfil/${data.usuari_login}" class="enllac-perfil" target="_blank">${data.usuari_nom}</a>`;
}


      document.getElementById('modal-contingut').innerHTML = data.contingut || "";

      let arxiusDiv = document.getElementById('modal-arxius');
      arxiusDiv.innerHTML = "";

      data.arxius.forEach(fitxer => {
        const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;
        const link = document.createElement("a");
        link.href = ruta;
        link.target = "_blank";

        const contenidor = document.createElement("div");
        contenidor.classList.add("arxiu-miniatura-peu");

        if (fitxer.tipus.match(/(jpg|png|jpeg|webp)/i)) {
          link.setAttribute("data-lightbox", "galeria-" + data.id);
          link.setAttribute("data-title", fitxer.titol || fitxer.nom_fitxer);

          const img = document.createElement("img");
          img.src = ruta;
          img.style.maxWidth = "100px";
          img.style.margin = "10px";

          link.appendChild(img);
        } else {
  const icona = document.createElement("img");
  
  // 🔧 Usar tipus_media per webm, sinó tipus normal
  let iconaPath;
  if (fitxer.tipus === "webm" && fitxer.tipus_media) {
    if (fitxer.tipus_media === "video") {
      iconaPath = "/static/icons/video_webm.png";
    } else if (fitxer.tipus_media === "audio") {
      iconaPath = "/static/icons/audio_webm.png";
    } else {
      iconaPath = "/static/icons/webm.png";
    }
  } else {
    iconaPath = `/static/icons/${fitxer.tipus}.png`;
  }
  
  icona.src = iconaPath;
  icona.title = fitxer.nom_fitxer;
  icona.style.maxWidth = "40px";
  icona.style.margin = "10px";

  link.appendChild(icona);
}
        contenidor.appendChild(link);

        const peu = document.createElement("p");
        peu.classList.add("peu-curt-arxiu");
        peu.textContent = fitxer.titol || "";
        contenidor.appendChild(peu);

        arxiusDiv.appendChild(contenidor);
      });

   // Buscar la millor imatge principal per mostrar
let arxiuPrincipal = null;

// 1. Prioritat: cercar una imatge real
for (const fitxer of data.arxius) {
  if (fitxer.tipus.match(/(jpg|png|jpeg|webp|gif)/i)) {
    arxiuPrincipal = fitxer;
    break;
  }
}

// 2. Si no hi ha imatge, agafar el primer arxiu (vídeo, àudio, etc.)
if (!arxiuPrincipal && data.arxius.length > 0) {
  arxiuPrincipal = data.arxius[0];
}

// Mostrar la imatge principal
if (arxiuPrincipal) {
  const url = `/umberto/${data.usuari_login}/${data.id}/${arxiuPrincipal.nom_fitxer}`;
  const img = document.getElementById('modal-img');
  
  if (arxiuPrincipal.tipus.match(/(jpg|png|jpeg|webp|gif)/i)) {
    // És imatge - mostrar la imatge real
    img.src = url;
  } else {
    // És àudio/vídeo/document - mostrar la icona gran
    if (arxiuPrincipal.tipus === "webm" && arxiuPrincipal.tipus_media) {
      if (arxiuPrincipal.tipus_media === "video") {
        img.src = "/static/icons/video_webm.png";
      } else if (arxiuPrincipal.tipus_media === "audio") {
        img.src = "/static/icons/audio_webm.png";
      } else {
        img.src = "/static/icons/webm.png";
      }
    } else {
      img.src = `/static/icons/${arxiuPrincipal.tipus}.png`;
    }
     }
  
  img.style.maxWidth = "400px";
  img.style.height = "auto";
  document.getElementById('modal-enllac').href = url;
} else {
  // No hi ha cap arxiu
  document.getElementById('modal-img').src = "/static/icons/sense_imatge.png";
}
      const titolImg = data.titol_imatge?.trim();
      const anyImg = data.any_imatge?.trim();
      const ubicacioImg = data.ubicacio_imatge?.trim();
      const descripcioImg = data.descripcio_imatge?.trim();
      const referenciaImg = data.referencia?.trim();

      const infoVisible = titolImg || anyImg || ubicacioImg || descripcioImg || referenciaImg;

      if (infoVisible) {
        document.getElementById("modal-info-imatge").style.display = "block";
        document.getElementById("modal-titol-imatge").textContent = titolImg || "—";
        document.getElementById("modal-descripcio-imatge").textContent = descripcioImg || "—";
        document.getElementById("modal-referencia-imatge").textContent = referenciaImg || "—";

        const sep = (ubicacioImg && anyImg) ? ", " : "";
        document.getElementById("modal-ubicacio-any-imatge").textContent = `${ubicacioImg || ''}${sep}${anyImg || ''}` || "—";
      } else {
        document.getElementById("modal-info-imatge").style.display = "none";
      }
      
      // Bloc conversa vinculada
        const blocConversa = document.getElementById("modal-conversa-bloc");
        if (data.conversa) {
          const c = data.conversa;
          const lloc = [c.lloc_municipi, c.lloc_regio, c.lloc_pais].filter(Boolean).join(", ");
          const participants = c.participants.length ? c.participants.join(", ") : "";

          let resum = [];
          if (participants) resum.push(participants);
          if (c.data) resum.push(c.data);
          if (lloc) resum.push(lloc);

          document.getElementById("modal-conversa-resum").textContent = resum.join(" · ") || "—";
          document.getElementById("modal-conversa-observacions").textContent = c.observacions_generals || "";

          blocConversa.style.display = "block";
          document.getElementById("modal-conversa-contingut").style.display = "none";
          document.getElementById("modal-conversa-fletxa").textContent = "▶";
        } else {
          blocConversa.style.display = "none";
        }

      // 🔁 Mostra o amaga botons segons l’origen
// 🔁 Reinicia estat botons abans de mostrar la modal
// 🔁 Reinicia estat botons abans de mostrar la modal
const botoGuardar = document.getElementById("boto-guardar");
const botoEliminar = document.getElementById("boto-eliminar-guardada");

if (botoGuardar) {
  botoGuardar.disabled = false;
  botoGuardar.textContent = "Guardar";
}

// 🔁 Decideix quin botó mostrar segons si ja estava guardada
if (data.ja_guardada) {
  if (botoGuardar) botoGuardar.style.display = "none";
  if (botoEliminar) botoEliminar.style.display = "inline-block";
} else {
  if (botoGuardar) botoGuardar.style.display = "inline-block";
  if (botoEliminar) botoEliminar.style.display = "none";
}



      document.getElementById("modal-entrada").style.display = "flex";
    });
}

function tancaModalEntrada() {
  document.getElementById("modal-entrada").style.display = "none";
}
function guardaEntradaFavorita() {
  const entradaId = window.entradaIdActual;

  fetch(`/api/guardar_entrada/${entradaId}`, {
    method: "POST"
  })
    .then(res => {
      if (res.ok) {
        alert("✅ Entrada guardada com a favorit!");
        const boto = document.getElementById("boto-guardar");
        if (boto) {
          boto.disabled = true;
          boto.textContent = "✅ Guardada";
        }
      } else {
        alert("❌ No s'ha pogut guardar.");
      }
    })
    .catch(err => {
      console.error("Error en guardar entrada:", err);
      alert("⚠️ Error del servidor.");
    });
}

function eliminaEntradaGuardada() {
  const entradaId = window.entradaIdActual;

  fetch(`/api/eliminar_entrada_guardada/${entradaId}`, {
    method: "POST"
  })
    .then(res => {
      if (res.ok) {
        alert("❌ Entrada eliminada dels guardats.");
        document.getElementById("modal-entrada").style.display = "none";
        // Opcional: tornar a carregar la llista de guardades
        if (typeof carregaEntradesGuardades === "function") {
          carregaEntradesGuardades("{{ session['usuari'] }}");
        }
      } else {
        alert("⚠️ No s’ha pogut eliminar.");
      }
    })
    .catch(err => {
      console.error("Error eliminant entrada:", err);
      alert("❌ Error del servidor.");
    });
}

function tancaModal() {
  document.getElementById("modal-entrada").style.display = "none";
}


// Aquesta funció assigna esdeveniment a tots els botons de tancar modal
function activaTancarModals() {
  const botonsTancar = document.querySelectorAll('.boto-tancar');
  botonsTancar.forEach(boto => {
    boto.addEventListener('click', () => {
      const modal = boto.closest('.modal');
      if (modal) modal.style.display = 'none';
    });
  });
}

// Crida inicial (per si les modals ja existeixen)
document.addEventListener('DOMContentLoaded', () => {
  activaTancarModals();
});

function toggleConversaModal() {
  const contingut = document.getElementById("modal-conversa-contingut");
  const fletxa = document.getElementById("modal-conversa-fletxa");
  const obert = contingut.style.display === "block";
  contingut.style.display = obert ? "none" : "block";
  fletxa.textContent = obert ? "▶" : "▼";
}

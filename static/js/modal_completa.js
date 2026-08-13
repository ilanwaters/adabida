
function obreModalCompleta(entradaId, usuariId) {
 
  fetch(`/api/entrada/${usuariId}/${entradaId}`)
    .then(res => res.json())
    .then(data => {

      try {
        document.getElementById('modal-titol-editar').innerText = data.titol || "—";
        document.getElementById('modal-tema-editar').innerText = data.tema || "";

       const ubicacio = [data.municipi, data.regio, data.pais].filter(Boolean).join(", ");
       const any = data.any || '';
       const separador = (ubicacio && any) ? ", " : '';

      document.getElementById("modal-ubicacio-any-editar").textContent = `${ubicacio || ''}${separador}${any || ''}`;
        const dataSpan = document.getElementById('modal-data-editar');
        if (dataSpan) dataSpan.innerText = data.data_creacio || "";
        const metaAutor = document.getElementById('modal-meta-autor-editar');
        if (metaAutor) metaAutor.textContent = data.usuari_nom || '';

        const metaCreacio = document.getElementById('modal-meta-creacio-editar');
        if (metaCreacio) metaCreacio.textContent = data.data_creacio ? `Creat: ${data.data_creacio}` : '';

        const metaModificacio = document.getElementById('modal-meta-modificacio-editar');
        if (metaModificacio) metaModificacio.textContent = data.data_modificacio ? `Modificat: ${data.data_modificacio}` : '';

        document.getElementById('modal-contingut-editar').innerHTML = data.contingut || "";

        let arxiusDiv = document.getElementById('modal-arxius-editar');
        arxiusDiv.innerHTML = "";

        data.arxius.forEach(fitxer => {
          const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;
          const link = document.createElement("a");
          link.href = ruta;
          link.target = "_blank";

          if (fitxer.tipus.match(/(jpg|png|jpeg|webp)/i)) {
            link.setAttribute("data-lightbox", "galeria-" + data.id);
            link.setAttribute("data-title", fitxer.nom_fitxer);

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

          arxiusDiv.appendChild(link);
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
  const img = document.getElementById('modal-img-editar');
  
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
  document.getElementById('modal-enllac-editar').href = url;
} else {
  // No hi ha cap arxiu
  document.getElementById('modal-img-editar').src = "/static/icons/sense_imatge.png";
}
        const titolImg = data.titol_imatge?.trim();
        const anyImg = data.any_imatge?.trim();

        const ubicacioImg = [data.municipi_imatge, data.regio_imatge, data.pais_imatge]
          .filter(Boolean)
          .join(", ");

        const descripcioImg = data.descripcio_imatge?.trim();
        const referenciaImg = data.referencia?.trim();

        const infoVisible = titolImg || anyImg || ubicacioImg || descripcioImg || referenciaImg;

        if (infoVisible) {
          document.getElementById("modal-info-imatge-editar").style.display = "block";
          document.getElementById("modal-titol-imatge-editar").textContent = titolImg || "—";
          document.getElementById("modal-descripcio-imatge-editar").textContent = descripcioImg || "—";
          document.getElementById("modal-referencia-imatge-editar").textContent = referenciaImg || "—";

          const sep = (ubicacioImg && anyImg) ? ", " : "";
          document.getElementById("modal-ubicacio-any-imatge-editar").textContent =
            `${ubicacioImg || ''}${sep}${anyImg || ''}` || "—";
        } else {
          document.getElementById("modal-info-imatge-editar").style.display = "none";
        }

        const botoEliminar = document.getElementById("boto-eliminar");
        if (botoEliminar) {
          botoEliminar.dataset.id = data.id;
        }

        const botoEditar = document.getElementById("boto-editar");
        if (botoEditar) {
          if (data.propietari) {
            botoEditar.href = `/editar_entrada_personal/${data.id}?pestanya=nova`;
            botoEditar.style.display = "inline-block";
          } else {
            botoEditar.style.display = "none";
          }
        }
      } catch (error) {
      }

      // 👇 FORÇA l'obertura de la modal, sempre
      document.getElementById("modal-entrada-editar").style.setProperty("display", "flex", "important");

    });
}

function tancaModal() {
  document.getElementById("modal-entrada-editar").style.display = "none";
}

function confirmaEliminacio() {
  if (confirm("Segur que vols eliminar aquesta entrada?")) {
    const id = document.getElementById("boto-eliminar").dataset.id;
    fetch(`/eliminar_entrada/${id}`, { method: "POST" })
      .then(res => {
        if (res.ok) {
          alert("✅ Entrada eliminada correctament.");
          window.location.href = "/entrades";
        } else {
          res.text().then(msg => {
            console.error("Error:", msg);
            alert("No s’ha pogut eliminar:\n" + msg);
          });
        }
      });
  }
}

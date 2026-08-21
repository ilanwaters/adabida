
function obreModalCompleta(entradaId, usuariId) {
 
  fetch(`/api/entrada/${usuariId}/${entradaId}`)
    .then(res => res.json())
    .then(data => {

      try {
        document.getElementById('modal-titol-editar').innerText = data.titol || "—";

        const ubicacio = [data.municipi, data.regio, data.pais].filter(Boolean).join(", ");
        const any = data.any || '';
        const tema = data.tema?.trim();

        let parentesi = [ubicacio, any].filter(Boolean).join(", ");
        parentesi = parentesi ? ` (${parentesi})` : "";

        document.getElementById('modal-tema-editar').innerText = tema || "";
        document.getElementById("modal-ubicacio-any-parentesi-editar").textContent = parentesi;
        const metaAutor = document.getElementById('modal-meta-autor-editar');
        if (metaAutor) metaAutor.textContent = data.usuari_nom || '';

        const metaCreacio = document.getElementById('modal-meta-creacio-editar');
        if (metaCreacio) metaCreacio.textContent = data.data_creacio ? `Creat: ${data.data_creacio}` : '';

        const metaModificacio = document.getElementById('modal-meta-modificacio-editar');
        if (metaModificacio) metaModificacio.textContent = data.data_modificacio ? `Modificat: ${data.data_modificacio}` : '';

        document.getElementById('modal-contingut-editar').innerHTML = data.contingut || "";
        window.__dadesEntradaActual = {
          titol: data.titol_imatge,
          any_arxiu: data.any_imatge,
          pais: data.pais_imatge,
          regio: data.regio_imatge,
          municipi: data.municipi_imatge,
          descripcio: data.descripcio_imatge,
          referencia: data.referencia,
        };
        const imatgesDiv = document.getElementById('modal-arxius-imatges-editar');
        const mediaDiv = document.getElementById('modal-arxius-media-editar');
        const comptadorMedia = document.getElementById('comptador-media-editar');
        imatgesDiv.innerHTML = "";
        mediaDiv.innerHTML = "";
        let totalMedia = 0;

        const arxiusConversa = [];
        const comptadorsTipus = {};
        function etiquetaArxiu(fitxer) {
          let tipusEtiqueta;
          if (fitxer.tipus === "webm" && fitxer.tipus_media === "video") {
            tipusEtiqueta = "Vídeo";
          } else if (fitxer.tipus === "webm" && fitxer.tipus_media === "audio") {
            tipusEtiqueta = "Àudio";
          } else {
            tipusEtiqueta = "Document";
          }
          comptadorsTipus[tipusEtiqueta] = (comptadorsTipus[tipusEtiqueta] || 0) + 1;
          const titolEntrada = (data.titol || "").trim();
          return titolEntrada ? `${titolEntrada} · ${tipusEtiqueta} ${comptadorsTipus[tipusEtiqueta]}` : `${tipusEtiqueta} ${comptadorsTipus[tipusEtiqueta]}`;
        }
        data.arxius.forEach(fitxer => {
          if (fitxer.es_conversa) {
            arxiusConversa.push(fitxer);
            return;
          }
          const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;
          const link = document.createElement("a");
          link.href = ruta;
          link.target = "_blank";

          const contenidor = document.createElement("div");
          contenidor.classList.add("arxiu-miniatura-peu");

          if (fitxer.tipus.match(/(jpg|png|jpeg|webp)/i)) {
            link.setAttribute("data-lightbox", "galeria-" + data.id);
            link.setAttribute("data-title", construeixPeuLightbox(fitxer));

            const img = document.createElement("img");
            img.src = ruta;
            img.style.maxWidth = "100px";
            img.style.margin = "10px";

            link.appendChild(img);
            contenidor.appendChild(link);

            const peu = document.createElement("p");
            peu.classList.add("peu-curt-arxiu");
            peu.textContent = fitxer.titol || "";
            contenidor.appendChild(peu);

            imatgesDiv.appendChild(contenidor);
          } else if (fitxer.tipus === "webm" && fitxer.tipus_media === "audio") {
            const audio = document.createElement("audio");
            audio.controls = true;
            audio.src = ruta;
            audio.style.width = "250px";
            audio.style.minWidth = "250px";
            audio.style.margin = "10px";
            contenidor.appendChild(audio);
            const peu = document.createElement("p");
            peu.classList.add("peu-complet-arxiu");
            peu.textContent = construeixPeuLightbox(fitxer) || etiquetaArxiu(fitxer);
            contenidor.appendChild(peu);
            mediaDiv.appendChild(contenidor);
            totalMedia++;
          } else {
            const icona = document.createElement("img");
            let iconaPath;
            if (fitxer.tipus === "webm" && fitxer.tipus_media === "video") {
              iconaPath = `/umberto/${data.usuari_login}/${data.id}/mini/${fitxer.nom_fitxer}.png`;
              icona.onerror = () => { icona.onerror = null; icona.src = "/static/icons/video_webm.png"; };
            } else if (fitxer.tipus === "webm" && fitxer.tipus_media) {
              iconaPath = "/static/icons/webm.png";
            } else {
              iconaPath = `/static/icons/${fitxer.tipus}.png`;
            }
            icona.src = iconaPath;
            icona.title = fitxer.nom_fitxer;
            icona.style.maxWidth = "40px";
            icona.style.margin = "10px";
            link.appendChild(icona);
            contenidor.appendChild(link);

            const peu = document.createElement("p");
            peu.classList.add("peu-complet-arxiu");
            peu.textContent = construeixPeuLightbox(fitxer) || etiquetaArxiu(fitxer);
            contenidor.appendChild(peu);

            mediaDiv.appendChild(contenidor);
            totalMedia++;
          }
        });

        comptadorMedia.textContent = totalMedia > 0 ? `(${totalMedia})` : "";

// Buscar la millor imatge principal per mostrar
let arxiuPrincipal = null;

// 0. Prioritat màxima: portada triada per l'usuari
if (data.portada) {
  arxiuPrincipal = data.portada;
} else {
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
    if (arxiuPrincipal.tipus === "webm" && arxiuPrincipal.tipus_media === "video") {
      img.onerror = () => { img.onerror = null; img.src = "/static/icons/video_webm.png"; };
      img.src = `/umberto/${data.usuari_login}/${data.id}/mini/${arxiuPrincipal.nom_fitxer}.png`;
    } else if (arxiuPrincipal.tipus === "webm" && arxiuPrincipal.tipus_media) {
      if (arxiuPrincipal.tipus_media === "audio") {
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
      

        // Bloc conversa vinculada
        const blocConversaEditar = document.getElementById("modal-conversa-bloc-editar");
        if (data.conversa) {
          const c = data.conversa;
          const lloc = [c.lloc_municipi, c.lloc_regio].filter(Boolean).join(", ");

          const nomsParticipants = c.participants.map(p => {
          const nomComplet = [p.nom, p.primer_cognom, p.segon_cognom].filter(Boolean).join(" ");
          const naixement = [p.lloc_municipi, p.lloc_regio, p.data_naixement].filter(Boolean).join(", ");
          return naixement ? `${nomComplet} (${naixement})` : nomComplet;
        }).join(" i ");

        let realitzada = "";
        if (lloc && c.data) {
          realitzada = ` realitzada a ${lloc} el ${c.data}`;
        } else if (lloc) {
          realitzada = ` realitzada a ${lloc}`;
        } else if (c.data) {
          realitzada = ` realitzada el ${c.data}`;
        }

        document.getElementById("modal-conversa-resum-editar").textContent = (nomsParticipants ? `Conversa amb ${nomsParticipants}` : "Conversa") + realitzada || "—";
          document.getElementById("modal-conversa-observacions-editar").textContent = c.observacions_generals || "";

                    const conversaArxiusDiv = document.getElementById("modal-conversa-arxius-editar");
          conversaArxiusDiv.innerHTML = "";
          arxiusConversa.forEach(fitxer => {
            const ruta = `/umberto/${data.usuari_login}/${data.id}/${fitxer.nom_fitxer}`;

            const link = document.createElement("a");
            link.href = ruta;
            link.target = "_blank";

            const contenidor = document.createElement("div");
            contenidor.classList.add("arxiu-miniatura-peu");
            if (fitxer.tipus_media === "audio") {
              contenidor.style.width = "260px";
            }

            if (fitxer.tipus_media === "video") {
              const miniatura = `/umberto/${data.usuari_login}/${data.id}/mini/${fitxer.nom_fitxer}.png`;
              const img = document.createElement("img");
              img.src = miniatura;
              img.style.width = "100%";
              img.style.maxHeight = "80px";
              img.style.objectFit = "cover";
              img.onerror = () => { img.src = "/static/icons/video_webm.png"; img.style.objectFit = "contain"; };
              link.appendChild(img);
              contenidor.appendChild(link);
            } else {
              const audio = document.createElement("audio");
              audio.controls = true;
              audio.src = ruta;
              audio.style.width = "250px";
              audio.style.minWidth = "250px";
              contenidor.appendChild(audio);
            }
            const peu = document.createElement("p");
            peu.classList.add("peu-curt-arxiu");
            peu.textContent = fitxer.titol || "";
            contenidor.appendChild(peu);

            conversaArxiusDiv.appendChild(contenidor);
          });

          blocConversaEditar.style.display = "block";
          document.getElementById("modal-conversa-contingut-editar").style.display = "none";
          document.getElementById("modal-conversa-fletxa-editar").textContent = "▶";
        } else {
          blocConversaEditar.style.display = "none";
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

function toggleConversaModalEditar() {
  const contingut = document.getElementById("modal-conversa-contingut-editar");
  const arxius = document.getElementById("modal-conversa-arxius-editar");
  const fletxa = document.getElementById("modal-conversa-fletxa-editar");
  const obert = contingut.style.display === "block";
  contingut.style.display = obert ? "none" : "block";
  if (arxius) arxius.style.display = obert ? "none" : "grid";
  fletxa.textContent = obert ? "▶" : "▼";
}

function construeixPeuLightbox(fitxer) {
  const teInfoPropia = fitxer.titol || fitxer.descripcio || fitxer.pais || fitxer.municipi || fitxer.any_arxiu;
  const font = teInfoPropia ? fitxer : (window.__dadesEntradaActual || {});

  const parts = [];
  if (font.titol) parts.push(font.titol);

  const ubicacio = [font.municipi, font.regio, font.pais].filter(Boolean).join(", ");
  const anyUbicacio = [ubicacio, font.any_arxiu].filter(Boolean).join(", ");
  if (anyUbicacio) parts.push(anyUbicacio);

  if (font.descripcio) parts.push(font.descripcio);
  if (font.referencia) parts.push(`Consulta: ${font.referencia}`);

  return parts.join(" — ");
}

function obreFitxerAmbInfo(fitxer, ruta) {
  const info = construeixPeuLightbox(fitxer);
  alert(`${fitxer.nom_fitxer}\n\n${info || "Sense informació addicional"}`);
  window.open(ruta, "_blank");
}


function toggleBlocModal(element) {
  const contingut = element.nextElementSibling;
  const obert = contingut.style.display === "grid";
  contingut.style.display = obert ? "none" : "grid";
}
// DECLARAR VARIABLES GLOBALS ABANS DEL DOMContentLoaded
let numeroParticipantIntegrat = 0;

document.addEventListener("DOMContentLoaded", function () {
  
  // ==============================================
  // 1. ELIMINAR ENTRADA
  // ==============================================
  const botoEliminar = document.getElementById("boto-eliminar");
  if (botoEliminar) {
    botoEliminar.addEventListener("click", function () {
      const confirmat = confirm(window.traduccions.eliminar_entrada_confirm);
      if (!confirmat) return;

      const id = botoEliminar.dataset.id;
      const usuari = document.body.dataset.usuari;

      fetch(`/eliminar_entrada/${id}`, { method: "POST" })
        .then(res => {
          if (res.ok) {
            window.location.href = `/pagina_personal?usuari_login=${usuari}&pestanya=entrades`;
          } else {
            alert(window.traduccions.no_eliminar);
          }
        });
    });
  }

  // ==============================================
  // 2. PUJAR FITXERS (netejat)
  // ==============================================
  const inputArxius = document.getElementById("puja-arxius");
  if (inputArxius) {
    inputArxius.addEventListener("change", function (e) {
      const arxius = e.target.files;
      const galeria = document.getElementById("previsualitzacio-arxius");

      for (let i = 0; i < arxius.length; i++) {
        const arxiu = arxius[i];
        const formData = new FormData();
        formData.append("arxiu", arxiu);

        fetch("/pujar_arxiu_temp", {
          method: "POST",
          body: formData
        })
        .then(res => res.json())
        .then(data => {
          const extensio = arxiu.name.split('.').pop().toLowerCase();
          const div = document.createElement("div");
          div.classList.add("miniatura");

          if (["jpg", "jpeg", "png", "gif", "webp"].includes(extensio)) {
            const img = document.createElement("img");
            img.src = URL.createObjectURL(arxiu);
            img.alt = arxiu.name;
            div.appendChild(img);
          } else if (extensio === "webm") {
            if (data.tipus === "video") {
              const video = document.createElement("video");
              video.controls = true;
              video.src = data.url;
              video.style.width = "160px";
              div.appendChild(video);
            } else if (data.tipus === "audio") {
              const audio = document.createElement("audio");
              audio.controls = true;
              audio.src = data.url;
              div.appendChild(audio);
            } else {
              const icona = document.createElement("img");
              icona.src = "/static/icons/webm.png";
              icona.alt = "webm";
              icona.style.width = "48px";
              div.appendChild(icona);
            }
          } else {
            const icona = document.createElement("img");
            icona.src = `/static/icons/${extensio}.png`;
            icona.alt = extensio;
            icona.style.width = "48px";
            div.appendChild(icona);
          }

          galeria.appendChild(div);
        })
        .catch(err => {
          console.error("Error en pujar arxiu:", err);
        });
      }
    });
  }

  // ==============================================
  // 3. GRAVACIÓ ÀUDIO PRINCIPAL
  // ==============================================
  let mediaRecorder;
  let chunks = [];

  const botoGrava = document.getElementById("botoGravaAudio");
  const botoAtura = document.getElementById("botoAturaAudio");
  const zonaAudio = document.getElementById("llista-audios");

  if (botoGrava && botoAtura && zonaAudio) {
    botoGrava.addEventListener("click", async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        document.getElementById("onda-gravacio").classList.remove("onda-oculta");

        mediaRecorder.ondataavailable = e => chunks.push(e.data);

        mediaRecorder.onstop = () => {
          document.getElementById("onda-gravacio").classList.add("onda-oculta");
          const blob = new Blob(chunks, { type: "audio/webm" });
          chunks = [];

          const nomUsuari = document.body.dataset.usuari;
          const nomFitxer = `${nomUsuari}_audio_${Date.now()}.webm`;
          crearBlocAudio(blob, nomFitxer, zonaAudio);
        };

        mediaRecorder.start();
        botoGrava.disabled = true;
        botoAtura.disabled = false;

      } catch (err) {
        alert(window.traduccions.permis_microfon);
      }
    });

    botoAtura.addEventListener("click", () => {
      if (mediaRecorder) {
        mediaRecorder.stop();
        botoGrava.disabled = false;
        botoAtura.disabled = true;
      }
    });
  }

  // ==============================================
  // 4. GRAVACIÓ VÍDEO PRINCIPAL
  // ==============================================
  let mediaRecorderVideo;
  let videoChunks = [];
  let videoStream;

  const botoIniciaVideo = document.getElementById("botoIniciaVideo");
  const botoAturaVideo = document.getElementById("botoAturaVideo");
  const video = document.getElementById("previsualitzacio-video");
  const videosGravats = document.getElementById("videos-gravats");

  if (botoIniciaVideo && botoAturaVideo) {
    botoIniciaVideo.addEventListener("click", async () => {
      try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

        if (video) {
          video.srcObject = videoStream;
          video.classList.remove("ocult");
        }

        mediaRecorderVideo = new MediaRecorder(videoStream);
        videoChunks = [];

        mediaRecorderVideo.ondataavailable = (e) => {
          if (e.data.size > 0) videoChunks.push(e.data);
        };

        mediaRecorderVideo.onstop = () => {
          const blob = new Blob(videoChunks, { type: "video/webm" });
          const nomFitxer = `video_${Date.now()}.webm`;
          
          crearBlocVideo(blob, nomFitxer, videosGravats);
          pujarVideo(blob, nomFitxer);

          if (video) {
            video.srcObject = null;
            video.classList.add("ocult");
          }
          videoChunks = [];
        };

        mediaRecorderVideo.start();
        botoIniciaVideo.style.display = "none";
        botoAturaVideo.style.display = "inline-block";
      } catch (err) {
        console.error(err);
        alert(window.traduccions.error_camera);
      }
    });

    botoAturaVideo.addEventListener("click", () => {
      if (!mediaRecorderVideo) return;
      mediaRecorderVideo.stop();
      videoStream?.getTracks().forEach((t) => t.stop());
      botoIniciaVideo.style.display = "inline-block";
      botoAturaVideo.style.display = "none";
    });
  }

  // ==============================================
  // 5. GRAVACIÓ ÀUDIO CONVERSES
  // ==============================================
  let mediaRecorderConversa;
  let chunksConversa = [];

  const botoGravaConversa = document.getElementById("botoGravaAudioConversa");
  const botoAturaConversa = document.getElementById("botoAturaAudioConversa");
  const zonaAudioConversa = document.getElementById("llista-audios-conversa");

  if (botoGravaConversa && botoAturaConversa && zonaAudioConversa) {
    botoGravaConversa.addEventListener("click", async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderConversa = new MediaRecorder(stream);
        document.getElementById("onda-gravacio-conversa").classList.remove("onda-oculta");

        mediaRecorderConversa.ondataavailable = e => chunksConversa.push(e.data);

        mediaRecorderConversa.onstop = () => {
          document.getElementById("onda-gravacio-conversa").classList.add("onda-oculta");
          const blob = new Blob(chunksConversa, { type: "audio/webm" });
          chunksConversa = [];

          const nomUsuari = document.body.dataset.usuari;
          const nomFitxer = `${nomUsuari}_audio_conversa_${Date.now()}.webm`;
          crearBlocAudio(blob, nomFitxer, zonaAudioConversa, true);
        };

        mediaRecorderConversa.start();
        botoGravaConversa.disabled = true;
        botoAturaConversa.disabled = false;

      } catch (err) {
        alert(window.traduccions.permis_microfon);
      }
    });

    botoAturaConversa.addEventListener("click", () => {
      if (mediaRecorderConversa) {
        mediaRecorderConversa.stop();
        botoGravaConversa.disabled = false;
        botoAturaConversa.disabled = true;
      }
    });
  }

  // ==============================================
  // 6. GRAVACIÓ VÍDEO CONVERSES
  // ==============================================
  let mediaRecorderVideoConversa;
  let videoChunksConversa = [];
  let videoStreamConversa;

  const botoIniciaVideoConversa = document.getElementById("botoIniciaVideoConversa");
  const botoAturaVideoConversa = document.getElementById("botoAturaVideoConversa");
  const videoConversa = document.getElementById("previsualitzacio-video-conversa");
  const videosGravatsConversa = document.getElementById("videos-gravats-conversa");

  if (botoIniciaVideoConversa && botoAturaVideoConversa) {
    botoIniciaVideoConversa.addEventListener("click", async () => {
      try {
        videoStreamConversa = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });

        if (videoConversa) {
          videoConversa.srcObject = videoStreamConversa;
          videoConversa.classList.remove("ocult");
        }

        mediaRecorderVideoConversa = new MediaRecorder(videoStreamConversa);
        videoChunksConversa = [];

        mediaRecorderVideoConversa.ondataavailable = (e) => {
          if (e.data.size > 0) videoChunksConversa.push(e.data);
        };

        mediaRecorderVideoConversa.onstop = () => {
          const blob = new Blob(videoChunksConversa, { type: "video/webm" });
          const nomFitxer = `video_conversa_${Date.now()}.webm`;
          
          crearBlocVideo(blob, nomFitxer, videosGravatsConversa, true);
          pujarVideo(blob, nomFitxer);

          if (videoConversa) {
            videoConversa.srcObject = null;
            videoConversa.classList.add("ocult");
          }
          videoChunksConversa = [];
        };

        mediaRecorderVideoConversa.start();
        botoIniciaVideoConversa.style.display = "none";
        botoAturaVideoConversa.style.display = "inline-block";
      } catch (err) {
        console.error(err);
        alert(window.traduccions.error_camera_conversa);
      }
    });

    botoAturaVideoConversa.addEventListener("click", () => {
      if (!mediaRecorderVideoConversa) return;
      mediaRecorderVideoConversa.stop();
      videoStreamConversa?.getTracks().forEach((t) => t.stop());
      botoIniciaVideoConversa.style.display = "inline-block";
      botoAturaVideoConversa.style.display = "none";
    });
  }

  // ==============================================
  // 7. PARTICIPANTS CONVERSES
  // ==============================================
  const btnAfegirParticipant = document.getElementById('btn-afegir-participant-integrat');
  if (btnAfegirParticipant) {
    btnAfegirParticipant.addEventListener('click', afegirParticipantIntegrat);
  }

  // ==============================================
  // 8. GESTIÓ ARXIU MANUAL CONVERSES
  // ==============================================
  const arxiuInputConversa = document.getElementById('arxiu_conversa');
  if (arxiuInputConversa) {
    arxiuInputConversa.addEventListener('change', function(e) {
      const file = e.target.files[0];
      const infoDiv = document.getElementById('info-arxiu-conversa');
      
      if (file) {
        const tamanyMB = (file.size / 1024 / 1024).toFixed(2);
        const tipus = file.type.startsWith('audio/') ? window.traduccions.audio : 
                   file.type.startsWith('video/') ? window.traduccions.video : window.traduccions.arxiu;
        
        infoDiv.innerHTML = `
          <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;">
            <strong>${window.traduccions.arxiu_seleccionat}</strong><br>
            ${file.name}<br>
            ${tamanyMB} MB (${tipus})<br>
            <button type="button" onclick="eliminarArxiuConversa()" style="margin-top: 5px; background: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 3px;">
              ${window.traduccions.eliminar_arxiu}
            </button>
          </div>
        `;
      } else {
        infoDiv.innerHTML = '';
      }
    });
  }

});

// ==============================================
// FUNCIONS AUXILIARS
// ==============================================

function crearBlocAudio(blob, nomFitxer, container, esConversa = false) {
  const formData = new FormData();
  formData.append("audio", blob, nomFitxer);

  const entradaId = document.querySelector("input[name='entrada_id']");
  if (entradaId) {
    formData.append("entrada_id", entradaId.value);
  }

  fetch("/pujar_audio_temp", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      const bloc = document.createElement("div");
      bloc.classList.add("bloc-audio");

      const audio = document.createElement("audio");
      audio.controls = true;
      audio.src = data.url;

      const inputAudio = document.createElement("input");
      inputAudio.type = "hidden";
      inputAudio.name = esConversa ? "audios_conversa[]" : "audios[]";
      inputAudio.value = nomFitxer;

      const formulari = document.querySelector("form");
      if (formulari && !document.querySelector(`input[name="${inputAudio.name}"][value="${nomFitxer}"]`)) {
        formulari.appendChild(inputAudio);
      }

      const botoEliminar = document.createElement("button");
      botoEliminar.textContent = window.traduccions.eliminar;
      botoEliminar.classList.add("boto-eliminar-audio");
      botoEliminar.addEventListener("click", () => {
        bloc.remove();
        inputAudio.remove();
        fetch("/eliminar_audio_temporal", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nom_fitxer: nomFitxer })
        });
      });

      bloc.appendChild(audio);
      bloc.appendChild(botoEliminar);
      container.appendChild(bloc);
    } else {
      alert(window.traduccions.error_pujar_audio);
    }
  });
}

function crearBlocVideo(blob, nomFitxer, container, esConversa = false) {
  const videoURL = URL.createObjectURL(blob);
  const bloc = document.createElement("div");
  bloc.classList.add("miniatura");

  const videoElement = document.createElement("video");
  videoElement.src = videoURL;
  videoElement.controls = true;
  videoElement.style.maxWidth = "200px";

  const botoEliminar = document.createElement("button");
  botoEliminar.textContent = window.traduccions.eliminar;
  botoEliminar.classList.add("boto-eliminar-video");
  
  const inputHidden = document.createElement("input");
  inputHidden.type = "hidden";
  inputHidden.name = esConversa ? "videos_conversa[]" : "videos[]";
  inputHidden.value = nomFitxer;
  document.querySelector("form")?.appendChild(inputHidden);

  botoEliminar.addEventListener("click", () => {
    bloc.remove();
    inputHidden.remove();
    fetch("/eliminar_fitxer_temporal", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nom_fitxer: nomFitxer })
    });
  });

  bloc.appendChild(videoElement);
  bloc.appendChild(botoEliminar);
  
  if (container) {
    container.appendChild(bloc);
  }
}

function pujarVideo(blob, nomFitxer) {
  const formData = new FormData();
  formData.append("arxiu", blob, nomFitxer);

  fetch("/pujar_arxiu_temp", { method: "POST", body: formData })
    .then((res) => {
      if (!res.ok) throw new Error("Resposta HTTP no OK");
      return res.json();
    })
    .then((data) => {
      if (!data.success) throw new Error("Servidor: success = false");
      console.log("Vídeo pujat correctament.");
    })
    .catch((err) => {
      console.error(err);
      alert(window.traduccions.error_pujar_video);
    });
}

function afegirParticipantIntegrat() {
  fetch(`/generar_participant_html/${numeroParticipantIntegrat}`)
    .then(res => res.text())
    .then(html => {
      const container = document.getElementById('participants-container-integrat');
      container.insertAdjacentHTML('beforeend', html);
      inicialitzarGrupPerNom(`pais_participant_${numeroParticipantIntegrat}`);
      numeroParticipantIntegrat++;
    });
}

function eliminarParticipantIntegrat(numero) {
  const participant = document.querySelector(`[data-participant="${numero}"]`);
  if (participant) {
    participant.remove();
    actualitzarNumeracioParticipants();
  }
}

function actualitzarNumeracioParticipants() {
  const participants = document.querySelectorAll('.participant-integrat');
  participants.forEach((participant, index) => {
    const numeroElement = participant.querySelector('.participant-num');
    if (numeroElement) {
      numeroElement.textContent = index + 1;
    }
  });
}

function eliminarArxiuConversa() {
  const infoDiv = document.getElementById('info-arxiu-conversa');
  infoDiv.innerHTML = '';
  const inputFile = document.getElementById('arxiu_conversa');
  inputFile.value = '';
}

// Funcions globals
window.eliminarParticipantIntegrat = eliminarParticipantIntegrat;
window.eliminarArxiuConversa = eliminarArxiuConversa;

// AFEGIR al final de static/js/nova_entrada_personal.js

// ============================================================================
// GESTIÓ TEMA I CATEGORIA DESDE PORTADA
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    carregarCategoriesFormulari();
    processarParametresURL();
});

function toggleNovaCategoriaEntrada() {
    const select = document.getElementById('selector-categoria');
    const inputManual = document.getElementById('categoria-manual');
    
    if (select.value === 'nova') {
        inputManual.style.display = 'block';
        inputManual.required = true;
        setTimeout(() => inputManual.focus(), 100);
    } else {
        inputManual.style.display = 'none';
        inputManual.required = false;
        inputManual.value = '';
    }
}

async function carregarCategoriesFormulari() {
    try {
        const paisCodi = new URLSearchParams(window.location.search).get('pais') || 'ES';
        
        const response = await fetch(`/api/categories-pais/${paisCodi}`);
        const data = await response.json();
        
        const select = document.getElementById('selector-categoria');
        if (!select) return;
        
        const primeraOpcio = select.options[0];
        const novaOpcio = select.querySelector('option[value="nova"]');
        
        select.innerHTML = '';
        select.appendChild(primeraOpcio);
        
        if (data.categories && data.categories.length > 0) {
            data.categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.nom;
                option.dataset.nom = cat.nom;
                select.appendChild(option);
            });
        }
        
        if (novaOpcio) select.appendChild(novaOpcio);
        
        select.selectedIndex = 0;
        
    } catch (error) {
        console.error('Error carregant categories:', error);
    }
}

function toggleNovaCategoriaEntrada() {
    const select = document.getElementById('selector-categoria');
    const inputManual = document.getElementById('categoria-manual');
    
    if (select.value === 'nova') {
        inputManual.style.display = 'block';
        inputManual.required = true;
        setTimeout(() => inputManual.focus(), 100);
    } else {
        inputManual.style.display = 'none';
        inputManual.required = false;
        inputManual.value = '';
    }
}

window.toggleNovaCategoriaEntrada = toggleNovaCategoriaEntrada;

function processarParametresURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const tema = urlParams.get('titol'); // Nota: el paràmetre es diu "titol" però va al camp "tema"
    
    if (tema) {
        const campTema = document.getElementById('tema');
        if (campTema) {
            campTema.value = tema;
        }
        
        // Deixar títol buit
        const campTitol = document.getElementById('titol');
        if (campTitol && !campTitol.value) {
            campTitol.value = '';
        }
    }
}

// Funció global
window.toggleNovaCategoriaEntrada = toggleNovaCategoriaEntrada;

// ==============================================
// FIX: convertir selects de país/regió (value=ID) al seu text (nom)
// abans d'enviar el formulari, per no desar IDs numèrics a la BD
// ==============================================
document.addEventListener("DOMContentLoaded", function () {
  const formulari = document.getElementById("formulari-entrada");
  if (!formulari) return;
  formulari.addEventListener("submit", function () {
    const selectsPaisRegio = formulari.querySelectorAll(
      'select[name*="pais"], select[name*="regio"]'
    );
    selectsPaisRegio.forEach(function (select) {
      const opcioSeleccionada = select.options[select.selectedIndex];
      if (opcioSeleccionada && opcioSeleccionada.value !== "" && opcioSeleccionada.value !== "ALTRE") {
        const nomOriginal = select.name;
        select.name = nomOriginal + "_id";
        let hidden = formulari.querySelector("input[type=hidden][name=" + nomOriginal + "]");
        if (!hidden) {
          hidden = document.createElement("input");
          hidden.type = "hidden";
          hidden.name = nomOriginal;
          formulari.appendChild(hidden);
        }
        hidden.value = opcioSeleccionada.textContent;
      }
    });
  });
});

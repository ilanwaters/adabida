// === VARIABLES GLOBALS ===
let arxiusSeleccionats = [];

document.addEventListener('DOMContentLoaded', function() {
  
  // === VISTA PRÈVIA ARXIUS MÚLTIPLES ===
    const arxiuInputConversa = document.getElementById('arxiu_conversa');
  if (arxiuInputConversa) {
    arxiuInputConversa.addEventListener('change', function(e) {
      const files = Array.from(e.target.files);
      const infoDiv = document.getElementById('info-arxiu-conversa');

      files.forEach(file => {
        const id = Date.now() + Math.random();
        const tamanyMB = (file.size / 1024 / 1024).toFixed(2);
        const url = URL.createObjectURL(file);
        let preview = '';

        if (file.type.startsWith('image/')) {
          preview = `<a href="${url}" target="_blank"><img src="${url}" style="cursor: pointer;"></a>`;
        } else if (file.type.startsWith('audio/')) {
          preview = `<audio controls src="${url}"></audio>`;
        } else if (file.type.startsWith('video/')) {
          preview = `<video controls src="${url}"></video>`;
        } else if (file.type === 'application/pdf') {
          preview = `<a href="${url}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 10px 20px; background: #2196F3; color: white; text-decoration: none; border-radius: 6px;">📄 Veure PDF</a>`;
        } else {
          preview = `<div style="margin-top: 10px; color: #666;">📎 Document</div>`;
        }

        const arxiuDiv = document.createElement('div');
        arxiuDiv.className = 'arxiu-preview';
        arxiuDiv.dataset.id = id;
        arxiuDiv.innerHTML = `
          <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-top: 10px; background: white; text-align: center;">
            <strong style="display: block; font-size: 0.9rem; margin-bottom: 5px; word-break: break-word;">${file.name}</strong>
            <span style="color: #666; font-size: 0.85rem;">${tamanyMB} MB</span>
            <div style="margin: 10px 0;">${preview}</div>
            <span style="display:block; font-size: 0.8rem; color:#999;">Pujant...</span>
            <button type="button" onclick="eliminarArxiuConversa('${id}')" style="margin-top: 10px; background: #f44336; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
              Eliminar
            </button>
          </div>
        `;

        infoDiv.appendChild(arxiuDiv);
        pujarArxiuConversa(file, id, arxiuDiv);
      });

      e.target.value = '';
    });
  }

  // === GRAVACIÓ ÀUDIO CONVERSA ===
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
        alert("Cal donar permís al micròfon");
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

  // === GRAVACIÓ VÍDEO CONVERSA ===
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
          
          pujarVideo(blob, nomFitxer, videosGravatsConversa, true);

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
        alert("Error accedint a la càmera");
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

});

// === FUNCIONS AUXILIARS ===

function crearBlocAudio(blob, nomFitxer, container, esConversa = false) {
  const formData = new FormData();
  formData.append("audio", blob, nomFitxer);

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
      inputAudio.value = data.nom_fitxer;

      const formulari = document.querySelector("form");
      if (formulari && !document.querySelector(`input[name="${inputAudio.name}"][value="${nomFitxer}"]`)) {
        formulari.appendChild(inputAudio);
      }

      const botoEliminar = document.createElement("button");
      botoEliminar.textContent = "Eliminar";
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
      alert("Error pujant àudio");
    }
  });
}

function crearBlocVideo(blob, nomFitxer, container, esConversa = false) {
  const videoURL = URL.createObjectURL(blob);
  const bloc = document.createElement("div");
  bloc.classList.add("miniatura-video-gravat");

  const videoElement = document.createElement("video");
  videoElement.src = videoURL;
  videoElement.controls = true;
  videoElement.style.maxWidth = "200px";

  const botoEliminar = document.createElement("button");
  botoEliminar.textContent = "Eliminar";
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

function pujarVideo(blob, nomFitxer, container, esConversa = false) {
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
      crearBlocVideo(blob, data.nom_fitxer, container, esConversa);
    })
    .catch((err) => {
      console.error(err);
      alert("Error pujant vídeo");
    });
}

function pujarArxiuConversa(file, id, arxiuDiv) {
  const formData = new FormData();
  formData.append("arxiu", file, file.name);

  fetch("/pujar_arxiu_temp", { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => {
      if (!data.success) throw new Error("Servidor: success = false");

      arxiusSeleccionats.push({ id, nomFitxer: data.nom_fitxer });

      const inputHidden = document.createElement("input");
      inputHidden.type = "hidden";
      inputHidden.name = "arxius_conversa[]";
      inputHidden.value = data.nom_fitxer;
      inputHidden.dataset.id = id;
      document.querySelector("form")?.appendChild(inputHidden);

      const estat = arxiuDiv.querySelector("span");
      if (estat) estat.remove();
    })
    .catch(err => {
      console.error(err);
      const estat = arxiuDiv.querySelector("span");
      if (estat) { estat.textContent = "Error pujant"; estat.style.color = "red"; }
    });
}
let numeroArxiuConversa = 0;

document.addEventListener('DOMContentLoaded', function() {
  const inputArxiusConversa = document.getElementById("puja-arxius-conversa");
  if (inputArxiusConversa) {
    inputArxiusConversa.addEventListener("change", function (e) {
      const arxius = e.target.files;
      const galeria = document.getElementById("previsualitzacio-arxius-conversa");

      for (let i = 0; i < arxius.length; i++) {
        const arxiu = arxius[i];
        const formData = new FormData();
        formData.append("arxiu", arxiu);

        fetch("/pujar_arxiu_temp", { method: "POST", body: formData })
          .then(res => res.json())
          .then(data => {
            if (!data.success) {
              alert("Error pujant arxiu");
              return;
            }

            const numero = numeroArxiuConversa++;
            const extensio = arxiu.name.split('.').pop().toLowerCase();

            const bloc = document.createElement("div");
            bloc.classList.add("capsa-arxiu-metadades");
            bloc.dataset.arxiu = numero;

            if (["jpg", "jpeg", "png", "gif", "webp"].includes(extensio)) {
              const img = document.createElement("img");
              img.src = URL.createObjectURL(arxiu);
              img.alt = arxiu.name;
              bloc.appendChild(img);
            } else if (extensio === "webm") {
              if (data.tipus === "video") {
                const video = document.createElement("video");
                video.controls = true;
                video.src = data.url;
                bloc.appendChild(video);
              } else if (data.tipus === "audio") {
                const audio = document.createElement("audio");
                audio.controls = true;
                audio.src = data.url;
                bloc.appendChild(audio);
              }
            } else {
              const icona = document.createElement("img");
              icona.src = `/static/icons/${extensio}.png`;
              icona.alt = extensio;
              icona.style.width = "48px";
              bloc.appendChild(icona);
            }

            const fitxerHidden = document.createElement("input");
            fitxerHidden.type = "hidden";
            fitxerHidden.name = `arxiu_conversa_fitxer_${numero}`;
            fitxerHidden.value = data.nom_fitxer;
            bloc.appendChild(fitxerHidden);

            const metadades = document.createElement("div");
            metadades.innerHTML = `
              <input type="text" name="arxiu_conversa_titol_${numero}" placeholder="Títol" class="campo-largo">
              <input type="text" name="arxiu_conversa_any_${numero}" placeholder="Any" class="campo-largo">
              <textarea name="arxiu_conversa_descripcio_${numero}" rows="2" placeholder="Descripció" class="campo-largo"></textarea>
              <input type="text" name="arxiu_conversa_referencia_${numero}" placeholder="Referència" class="campo-largo">
            `;
            bloc.appendChild(metadades);

            const botoEliminar = document.createElement("button");
            botoEliminar.type = "button";
            botoEliminar.textContent = "Eliminar";
            botoEliminar.classList.add("boto-eliminar-arxiu");
            botoEliminar.addEventListener("click", () => {
              bloc.remove();
              fetch("/eliminar_fitxer_temporal", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nom_fitxer: data.nom_fitxer })
              });
            });
            bloc.appendChild(botoEliminar);
            galeria.prepend(bloc);
          })
          .catch(err => console.error("Error en pujar arxiu:", err));
      }
    });
  }
});
// === FUNCIONS GLOBALS ===
window.eliminarArxiuConversa = function(id) {
  arxiusSeleccionats = arxiusSeleccionats.filter(a => a.id !== id);
  const div = document.querySelector(`[data-id="${id}"]`);
  if (div) div.remove();
};
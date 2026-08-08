console.log("registre_individual.js EXECUTAT");

/* ======================================================
   FUNCIONS GLOBALS (cridades des de HTML amb onclick)
   ====================================================== */

function toggleBlocAddicional() {
  const bloc = document.getElementById("bloc-addicional");
  if (!bloc) return;

  bloc.style.display =
    (bloc.style.display === "none" || bloc.style.display === "")
      ? "block"
      : "none";
}

function obreDisclaimer() {
  const modal = document.getElementById("disclaimer-modal");
  if (modal) modal.style.display = "block";
}

function tancaDisclaimer() {
  const modal = document.getElementById("disclaimer-modal");
  if (modal) modal.style.display = "none";
}

function toggleVisibilitat(idCamp, elementSpan) {
  const input = document.getElementById(idCamp);
  if (!input) return;

  if (input.type === "password") {
    input.type = "text";
    elementSpan.textContent = "🙈";
  } else {
    input.type = "password";
    elementSpan.textContent = "👁️";
  }
}

function obreVisorImatge(url) {
  const visor = document.getElementById("visor");
  const img = document.getElementById("imatgeGran");
  if (!visor || !img) return;

  img.src = url;
  visor.style.display = "flex";
}

function tancaVisor() {
  const visor = document.getElementById("visor");
  if (visor) visor.style.display = "none";
}

/* ======================================================
   LÒGICA INTERNA (quan el DOM ja està carregat)
   ====================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ---------- PUJADA I PREVISUALITZACIÓ DE DOCUMENTS ---------- */

  let fitxersSeleccionats = [];

  const inputDocs = document.getElementById("documents");
  const zona = document.getElementById("previsualitzacions");

  if (inputDocs && zona) {

    inputDocs.addEventListener("change", function (event) {
      const nous = Array.from(event.target.files);
      fitxersSeleccionats.push(...nous);
      renderitza();
    });

    function renderitza() {
      zona.innerHTML = "";

      fitxersSeleccionats = fitxersSeleccionats.filter(f => !f._eliminar);

      fitxersSeleccionats.forEach((fitxer, index) => {
        const reader = new FileReader();

        reader.onload = function (e) {
          const div = document.createElement("div");
          div.className = "document-box";

          let contingut = "";
          if (fitxer.type.startsWith("image/")) {
            contingut = `
              <img src="${e.target.result}"
                   class="miniatura"
                   onclick="obreVisorImatge('${e.target.result}')">
            `;
          } else {
            contingut = `
              <div class="icona-arxiu">
                ${fitxer.name.split(".").pop().toUpperCase()}
              </div>
            `;
          }

          div.innerHTML = `
            ${contingut}
            <div class="nom-arxiu">${fitxer.name}</div>
            <div class="quadrat-eliminar" data-index="${index}">Eliminar</div>
          `;

          zona.appendChild(div);
        };

        reader.readAsDataURL(fitxer);
      });

      sincronitzaInput();
    }

    function sincronitzaInput() {
      const dt = new DataTransfer();
      fitxersSeleccionats.forEach(f => dt.items.add(f));
      inputDocs.files = dt.files;
    }

    zona.addEventListener("click", function (e) {
      if (e.target.classList.contains("quadrat-eliminar")) {
        const index = e.target.dataset.index;
        const fitxer = fitxersSeleccionats[index];
        if (!fitxer) return;

        const missatge =
          document.body.dataset.missatgeEliminar ||
          `Estàs segur que vols eliminar "${fitxer.name}"?`;

        if (confirm(missatge)) {
          fitxer._eliminar = true;
          renderitza();
        }
      }
    });
  }

  /* ---------- VALIDACIÓ +18 ---------- */

  const formulari = document.getElementById("formulari-registre");
  const dataNaixement = document.getElementById("data_naixement");

  if (formulari && dataNaixement) {
    formulari.addEventListener("submit", function (e) {
      if (!dataNaixement.value) return;

      const avui = new Date();
      const dataUsuari = new Date(dataNaixement.value);

      let edat = avui.getFullYear() - dataUsuari.getFullYear();
      const m = avui.getMonth() - dataUsuari.getMonth();

      if (m < 0 || (m === 0 && avui.getDate() < dataUsuari.getDate())) {
        edat--;
      }

      if (edat < 18) {
        e.preventDefault();
        alert("Has de tenir més de 18 anys per registrar-te");
      }
    });
  }

});

function toggleDocumentsAcreditatius() {
  const bloc = document.getElementById('bloc-documents');
  bloc.style.display = bloc.style.display === 'none' ? 'block' : 'none';
}


  document.addEventListener("DOMContentLoaded", function () {
    const menuIdioma = document.querySelector(".menu-idioma");
    const submenu = menuIdioma?.querySelector(".submenu");

    if (menuIdioma && submenu) {
      menuIdioma.addEventListener("click", function (e) {
        e.stopPropagation();
        submenu.classList.toggle("visible");
      });

      document.addEventListener("click", function () {
        submenu.classList.remove("visible");
      });
    }
  });

  // Funció compartir pàgina
  function compartirPagina() {
    const url = window.location.href;
    const titol = document.title;
    
    // Intentar usar Web Share API (mòbils i alguns navegadors moderns)
    if (navigator.share) {
      navigator.share({
        title: titol,
        url: url
      })
      .then(() => console.log('Compartit correctament'))
      .catch((error) => console.log('Error compartint:', error));
    } else {
      // Fallback: copiar al portapapers
      navigator.clipboard.writeText(url)
        .then(() => {
          alert('{{ _("Enllaç copiat al portapapers!") }}');
        })
        .catch(() => {
          // Fallback del fallback per navegadors antics
          const textarea = document.createElement('textarea');
          textarea.value = url;
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
          alert('{{ _("Enllaç copiat al portapapers!") }}');
        });
    }
  }

function toggleMenu() {
  const menu = document.querySelector('.nav ul');
  if (!menu) return;
  
  if (menu.style.display === 'flex') {
    menu.style.display = '';
    menu.style.position = '';
  } else {
    menu.style.display = 'flex';
    menu.style.flexDirection = 'column';
    menu.style.position = 'absolute';
    menu.style.top = '60px';
    menu.style.left = '0';
    menu.style.right = '0';
    menu.style.background = '#3d3d3c';
    menu.style.padding = '1rem';
    menu.style.zIndex = '1000';
  }
}

function obrirLoginGlobal() {
  document.getElementById('submenu-login-global').classList.add('mostrar');
}

function togglePasswordGlobal() {
  const input = document.getElementById('contrasenya-global');
  input.type = input.type === 'password' ? 'text' : 'password';
}

function mostraDisclaimerGlobal() {
  document.getElementById('submenu-login-global').style.display = 'none';
  document.getElementById('disclaimer-modal-global').style.display = 'flex';
}

function acceptarDisclaimerGlobal() {
  document.getElementById('disclaimer-modal-global').style.display = 'none';
  window.location.href = '/registre_individual';
}

function obrirSelectorPortada(entradaId) {
  document.getElementById(`input-portada-${entradaId}`).click();
}

function pujarPortada(entradaId, input) {
  const fitxer = input.files[0];
  if (!fitxer) return;

  const formData = new FormData();
  formData.append("imatge", fitxer);

  fetch(`/entrada/${entradaId}/portada`, { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        alert("No s'ha pogut canviar la portada: " + (data.error || "error desconegut"));
      }
    })
    .catch(err => {
      console.error(err);
      alert("Error de servidor en canviar la portada.");
    });
}
function obrirSelectorPortadaFamilia(familiaId) {
  document.getElementById(`input-portada-familia-${familiaId}`).click();
}

function pujarPortadaFamilia(familiaId, input) {
  const fitxer = input.files[0];
  if (!fitxer) return;

  const formData = new FormData();
  formData.append("imatge", fitxer);

  fetch(`/familia/${familiaId}/administrar/portada`, { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        location.reload();
      } else {
        alert("No s'ha pogut canviar la portada: " + (data.error || "error desconegut"));
      }
    })
    .catch(err => {
      console.error(err);
      alert("Error de servidor en canviar la portada.");
    });
}
function obrirPhotoSwipe(link) {
  const galeria = link.getAttribute('data-lightbox');
  const totsLinks = Array.from(document.querySelectorAll(`a[data-lightbox="${galeria}"]`));
  const index = totsLinks.indexOf(link);

  const carregues = totsLinks.map(a => new Promise(resolve => {
    const img = new Image();
    img.onload = () => resolve({
      src: a.getAttribute('href'),
      title: a.getAttribute('data-title') || '',
      w: img.naturalWidth,
      h: img.naturalHeight,
    });
    img.onerror = () => resolve({
      src: a.getAttribute('href'),
      title: a.getAttribute('data-title') || '',
      w: 1600,
      h: 1200,
    });
    img.src = a.getAttribute('href');
  }));

  Promise.all(carregues).then(dataSource => {
    const pswp = new PhotoSwipe({
      dataSource,
      index,
      paddingFn: () => ({ top: 30, bottom: 60, left: 30, right: 30 }),
    });

    pswp.on('uiRegister', function () {
      pswp.ui.registerElement({
        name: 'peu-foto',
        order: 9,
        isButton: false,
        appendTo: 'root',
        onInit: (el) => {
          el.className = 'pswp-peu-foto';
          pswp.on('change', () => {
            el.innerHTML = pswp.currSlide?.data?.title || '';
          });
        },
      });
    });

    pswp.init();
  });
}
document.addEventListener('click', function (e) {
  const link = e.target.closest('a[data-lightbox]');
  if (!link) return;
  if (typeof PhotoSwipe === 'undefined') return;
  e.preventDefault();
  obrirPhotoSwipe(link);
});
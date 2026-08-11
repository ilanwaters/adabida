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
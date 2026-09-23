function mostrarLogin() {
  document.getElementById('submenu-login').style.display = 'block';
}

function tancarLogin() {
  document.getElementById('submenu-login').style.display = 'none';
}

function tancarModalMotivadora() {
  document.getElementById('modal-motivadora').style.display = 'none';
}

function mostraDisclaimer() {
  document.getElementById('disclaimer-modal').style.display = 'flex';
}

function acceptarDisclaimer() {
  document.getElementById('disclaimer-modal').style.display = 'none';
  window.location.href = '/registre';
}
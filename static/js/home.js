function toggleFinancament() {
  const contingut = document.getElementById('contingut-financament');
  const boto = document.querySelector('.boto-desplegable');
  if (contingut.style.display === 'none') {
    contingut.style.display = 'block';
    boto.textContent = 'Amaga informació ▲';
  } else {
    contingut.style.display = 'none';
    boto.textContent = 'Més informació sobre aportacions voluntàries ▼';
  }
}
/**
 * Sistema de modals informatius reutilitzable - Adabida
 * Ús: <button data-modal="id-del-modal">i</button>
 */

class ModalInfoSystem {
  constructor() {
    this.activeModal = null;
    this.init();
  }

  init() {
    // Inicialitzar tots els triggers amb data-modal
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-modal]');
      if (trigger) {
        e.preventDefault();
        const modalId = trigger.getAttribute('data-modal');
        this.obrirModal(modalId);
      }

      // Tancar si es fa clic al fons del modal
      if (e.target.classList.contains('modal-overlay')) {
        this.tancarModal();
      }

      // Tancar si es fa clic al botó tancar
      if (e.target.closest('[data-modal-close]')) {
        this.tancarModal();
      }
    });

    // Tancar amb ESC
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.activeModal) {
        this.tancarModal();
      }
    });
  }

  obrirModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) {
      console.error(`Modal amb id "${modalId}" no trobat`);
      return;
    }

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    this.activeModal = modal;

    // Reset contingut desplegable si existeix
    const infoCompleta = modal.querySelector('[data-toggle-content]');
    const toggleBtn = modal.querySelector('[data-toggle-trigger]');
    if (infoCompleta && toggleBtn) {
      infoCompleta.style.display = 'none';
    }
  }

  tancarModal() {
    if (!this.activeModal) return;

    this.activeModal.style.display = 'none';
    document.body.style.overflow = '';
    this.activeModal = null;
  }

  /**
   * Toggle per contingut desplegable dins del modal
   */
  static initToggleContent() {
    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('[data-toggle-trigger]');
      if (!trigger) return;

      const targetId = trigger.getAttribute('data-toggle-trigger');
      const content = document.getElementById(targetId);
      const textMes = trigger.getAttribute('data-text-mes') || '▼ Llegir més informació';
      const textMenys = trigger.getAttribute('data-text-menys') || '▲ Amagar informació';

      if (!content) return;

      if (content.style.display === 'none' || !content.style.display) {
        content.style.display = 'block';
        trigger.innerHTML = textMenys;
      } else {
        content.style.display = 'none';
        trigger.innerHTML = textMes;
      }
    });
  }
}

// Inicialitzar sistema global
const modalInfoSystem = new ModalInfoSystem();

// Inicialitzar sistema de toggle
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    ModalInfoSystem.initToggleContent();
  });
} else {
  ModalInfoSystem.initToggleContent();
}
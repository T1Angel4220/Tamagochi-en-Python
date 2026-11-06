/**
 * Tamagotchi RPG - Lógica del Juego y Gestión de Estado
 * Proyecto para portafolio de desarrollo web y lógica de videojuegos.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Inicialización de la pantalla del juego
  if (document.getElementById('hunger')) {
    initTamagotchiGame();
  }

  // Inicialización del menú de selección
  if (document.getElementById('btn-nuevo')) {
    initMenuSelection();
  }
});

/**
 * ====================================================================
 * LÓGICA PRINCIPAL DEL JUEGO (tamagotchi.html)
 * ====================================================================
 */
function initTamagotchiGame() {
  const STORAGE_KEY = 'tamagotchi_rpg_save';
  const RECORD_KEY = 'tamagotchi_rpg_record';

  // Elementos del DOM
  const hungerBar = document.getElementById('hunger');
  const boredomBar = document.getElementById('boredom');
  const sleepBar = document.getElementById('sleep');
  const dirtBar = document.getElementById('dirt');

  const eatBtn = document.getElementById('eat-btn');
  const sleepBtn = document.getElementById('sleep-btn');
  const cleanBtn = document.getElementById('clean-btn');
  const playBtn = document.getElementById('play-btn');

  const pet = document.getElementById('pet');
  const statusMsg = document.getElementById('status-msg');
  const gameArea = document.getElementById('game-area');

  // Estado del Tamagotchi
  const urlParams = new URLSearchParams(window.location.search);
  const isResumeMode = urlParams.get('mode') === 'resume';

  let state = {
    hunger: 40,
    boredom: 30,
    sleep: 20,
    dirt: 10,
    isSleeping: false,
    isAlive: true,
    secondsAlive: 0
  };

  // Cargar estado guardado si se solicita reanudar
  if (isResumeMode) {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        state = Object.assign(state, JSON.parse(saved));
        showMessage('¡Partida reanudada con éxito! 🎮');
      } catch (e) {
        console.error('Error cargando la partida guardada:', e);
      }
    }
  }

  // Guardar estado en localStorage
  function saveState() {
    if (!state.isAlive) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));

    const currentRecord = parseInt(localStorage.getItem(RECORD_KEY) || '0', 10);
    if (state.secondsAlive > currentRecord) {
      localStorage.setItem(RECORD_KEY, state.secondsAlive.toString());
    }
  }

  // Mostrar mensaje flotante de retroalimentación
  let msgTimeout = null;
  function showMessage(text) {
    if (!statusMsg) return;
    statusMsg.textContent = text;
    statusMsg.classList.add('show');
    clearTimeout(msgTimeout);
    msgTimeout = setTimeout(() => {
      statusMsg.classList.remove('show');
    }, 2500);
  }

  // Activar animación en el sprite de la mascota
  function triggerAnimation(className, duration = 600) {
    if (!pet || state.isSleeping || !state.isAlive) return;
    pet.classList.remove('bounce', 'wiggle');
    void pet.offsetWidth; // Forzar reflow para reiniciar animación
    pet.classList.add(className);
    setTimeout(() => {
      pet.classList.remove(className);
    }, duration);
  }

  // Actualizar interfaz y barras de progreso
  function updateUI() {
    hungerBar.value = state.hunger;
    boredomBar.value = state.boredom;
    sleepBar.value = state.sleep;
    dirtBar.value = state.dirt;

    if (state.isSleeping) {
      pet.classList.add('sleep');
      sleepBtn.textContent = '☀️ Despertar';
      eatBtn.disabled = true;
      cleanBtn.disabled = true;
      playBtn.disabled = true;
    } else {
      pet.classList.remove('sleep');
      sleepBtn.textContent = '💤 Dormir';
      eatBtn.disabled = false;
      cleanBtn.disabled = false;
      playBtn.disabled = false;
    }

    // Efecto visual si la mascota está muy sucia
    if (state.dirt > 70 && !state.isSleeping) {
      pet.style.filter = 'sepia(0.6) hue-rotate(20deg)';
    } else if (!state.isSleeping && state.isAlive) {
      pet.style.filter = 'drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3))';
    }
  }

  // Pantalla de Game Over si los valores llegan al límite
  function checkGameOver() {
    if (!state.isAlive) return;

    if (state.hunger >= 100 || state.boredom >= 100 || state.sleep >= 100 || state.dirt >= 100) {
      state.isAlive = false;
      clearInterval(gameLoop);
      localStorage.removeItem(STORAGE_KEY);

      pet.classList.add('dead');
      eatBtn.disabled = true;
      sleepBtn.disabled = true;
      cleanBtn.disabled = true;
      playBtn.disabled = true;

      let reason = 'descuido general';
      if (state.hunger >= 100) reason = 'hambre extrema';
      else if (state.boredom >= 100) reason = 'tristeza y aburrimiento';
      else if (state.sleep >= 100) reason = 'agotamiento severo';
      else if (state.dirt >= 100) reason = 'falta grave de higiene';

      const modal = document.createElement('div');
      modal.className = 'modal-overlay';
      modal.innerHTML = `
        <h2>¡Tu mascota ha enfermado! 💔</h2>
        <p>No pudo resistir debido a <strong>${reason}</strong>.</p>
        <p>Lograste cuidarla durante <strong>${state.secondsAlive} segundos</strong>.</p>
        <button id="restart-btn">🔄 Intentar de nuevo</button>
      `;
      gameArea.appendChild(modal);

      document.getElementById('restart-btn').addEventListener('click', () => {
        window.location.href = 'tamagotchi.html';
      });
    }
  }

  // Bucle principal de simulación (cada 2.5 segundos)
  const gameLoop = setInterval(() => {
    if (!state.isAlive) return;

    state.secondsAlive += 3;

    if (state.isSleeping) {
      state.sleep = Math.max(0, state.sleep - 12);
      state.hunger = Math.min(100, state.hunger + 1);
      if (state.sleep === 0) {
        state.isSleeping = false;
        showMessage('¡La mascota se ha despertado llena de energía! ☀️');
      }
    } else {
      state.hunger = Math.min(100, state.hunger + 3);
      state.boredom = Math.min(100, state.boredom + 2);
      state.sleep = Math.min(100, state.sleep + 2);
      state.dirt = Math.min(100, state.dirt + 1);

      // Avisos de precaución
      if (state.hunger > 80) showMessage('¡Tengo mucha hambre! 🍎');
      else if (state.boredom > 80) showMessage('¡Me siento muy aburrido! 🎮');
      else if (state.sleep > 80) showMessage('¡Tengo mucho sueño! 💤');
      else if (state.dirt > 80) showMessage('¡Necesito un baño urgente! 🧼');
    }

    updateUI();
    saveState();
    checkGameOver();
  }, 2500);

  // Event Listeners de los Botones
  eatBtn.addEventListener('click', () => {
    if (!state.isAlive || state.isSleeping) return;
    if (state.hunger <= 5) {
      showMessage('¡Estoy lleno! No puedo comer más 🥞');
      return;
    }
    state.hunger = Math.max(0, state.hunger - 25);
    state.dirt = Math.min(100, state.dirt + 4);
    triggerAnimation('bounce');
    showMessage('¡Ñam ñam! Deliciosa comida (-25 Hambre) 🍎');
    updateUI();
    saveState();
  });

  sleepBtn.addEventListener('click', () => {
    if (!state.isAlive) return;
    state.isSleeping = !state.isSleeping;
    if (state.isSleeping) {
      showMessage('zZz... Descansando plácidamente 💤');
    } else {
      showMessage('¡Buenos días! Despierto y listo ☀️');
    }
    updateUI();
    saveState();
  });

  cleanBtn.addEventListener('click', () => {
    if (!state.isAlive || state.isSleeping) return;
    if (state.dirt === 0) {
      showMessage('¡Ya estoy completamente limpio! ✨');
      return;
    }
    state.dirt = 0;
    triggerAnimation('wiggle');
    showMessage('¡Qué refrescante! Limpieza al 100% 🧼🫧');
    updateUI();
    saveState();
  });

  playBtn.addEventListener('click', () => {
    if (!state.isAlive || state.isSleeping) return;
    if (state.sleep > 85) {
      showMessage('Estoy demasiado cansado para jugar... 💤');
      return;
    }
    state.boredom = Math.max(0, state.boredom - 30);
    state.hunger = Math.min(100, state.hunger + 6);
    state.sleep = Math.min(100, state.sleep + 8);
    triggerAnimation('bounce');
    showMessage('¡Wiii! ¡Qué divertido jugar! (-30 Aburrimiento) 🎮');
    updateUI();
    saveState();
  });

  // Render inicial
  updateUI();
}

/**
 * ====================================================================
 * MENÚ DE SELECCIÓN (MenuSeleccion.html)
 * ====================================================================
 */
function initMenuSelection() {
  const STORAGE_KEY = 'tamagotchi_rpg_save';
  const RECORD_KEY = 'tamagotchi_rpg_record';

  const btnNuevo = document.getElementById('btn-nuevo');
  const btnReanudar = document.getElementById('btn-reanudar');
  const btnOpciones = document.getElementById('btn-opciones');
  const btnRecords = document.getElementById('btn-records');

  if (btnNuevo) {
    btnNuevo.addEventListener('click', () => {
      localStorage.removeItem(STORAGE_KEY);
    });
  }

  if (btnReanudar) {
    btnReanudar.addEventListener('click', (e) => {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (!saved) {
        e.preventDefault();
        alert('⚠️ No tienes ninguna partida guardada en este navegador.\nInicia una nueva partida con "Nuevo Juego".');
      }
    });
  }

  if (btnOpciones) {
    btnOpciones.addEventListener('click', (e) => {
      e.preventDefault();
      alert('⚙️ OPCIONES:\n\n- Velocidad de ciclo: Normal (2.5s)\n- Dificultad: Equilibrada\n- Guardado: Automático en LocalStorage');
    });
  }

  if (btnRecords) {
    btnRecords.addEventListener('click', (e) => {
      e.preventDefault();
      const record = localStorage.getItem(RECORD_KEY) || '0';
      alert(`🏆 RÉCORD DE SUPERVIVENCIA:\n\nTu mejor tiempo cuidando a tu mascota es:\n⏱️ ${record} segundos.`);
    });
  }
}

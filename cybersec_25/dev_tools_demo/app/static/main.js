(function () {
  window.demo = {
    version: '1.2.0',
    logSomething() {
      console.clear();
      console.group('DevTools Console Demo');
      console.log('Hello from logSomething() at', new Date().toISOString());
      console.table([{k:'userAgent', v: navigator.userAgent},{k:'lang', v: navigator.language}]);
      console.warn('This is a warning example');
      console.error('This is an error example (fake)');
      console.groupEnd();
      return 'Logged!';
    }
  };

  function simulateComputation(n) {
    const arr = Array.from({ length: n }, (_, i) => i);
    const sum = arr.reduce((a, b) => a + b, 0);
    return sum;
  }

  const $ = (sel) => document.querySelector(sel);
  const btnConsole = $('#btn-console');
  const btnBreakpoint = $('#btn-breakpoint');
  const btnPing = $('#btn-ping');
  const btnNetwork = $('#btn-network');
  const btnToggleFlag = $('#btn-toggle-flag');
  const adminPanel = $('#admin-panel');
  const btnSavePref = $('#btn-save-pref');
  const favColor = $('#fav-color');
  const saveStatus = $('#save-status');
  const btnSetCookie = $('#btn-set-cookie');

  function refreshAdminPanel() {
    const show = localStorage.getItem('showAdmin') === 'true';
    if (adminPanel) adminPanel.classList.toggle('hidden', !show);
  }

  function getCookie(name) {
    const m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return m ? decodeURIComponent(m[2]) : null;
  }

  function applyThemeFromCookie() {
    const theme = getCookie('ui_theme');
    const root = document.documentElement;
    if (theme === 'dark') {
      root.classList.add('theme-dark');
    } else {
      root.classList.remove('theme-dark');
    }
  }

  async function loadFavoriteColor() {
    try {
      const res = await fetch('/api/get-pref');
      if (!res.ok) return;
      const data = await res.json();
      if (favColor && data.favoriteColor) {
        favColor.value = data.favoriteColor;
        localStorage.setItem('favoriteColor', data.favoriteColor);
      }
    } catch (e) {
      console.warn('Failed to load favorite color:', e);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    refreshAdminPanel();
    applyThemeFromCookie();

    // Load persisted favorite color from server on private page
    if (favColor) {
      loadFavoriteColor();
    }

    if (btnConsole) {
      btnConsole.addEventListener('click', () => {
        window.demo.logSomething();
      });
    }

    if (btnBreakpoint) {
      btnBreakpoint.addEventListener('click', () => {
        debugger;
        const result = simulateComputation(1000);
        console.log('Computation result =', result);
      });
    }

    if (btnPing) {
      btnPing.addEventListener('click', async () => {
        const res = await fetch('/api/ping');
        const data = await res.json();
        console.log('Ping response:', data);
        alert('API says: ' + data.message);
      });
    }

    if (btnNetwork) {
      btnNetwork.addEventListener('click', async () => {
        const r1 = await fetch('/api/demo-data');
        const d1 = await r1.json();
        console.log('demo-data:', d1);

        const r2 = await fetch('/api/ping?ts=' + Date.now());
        const d2 = await r2.json();
        console.log('ping (network demo):', d2);
      });
    }

    if (btnToggleFlag) {
      btnToggleFlag.addEventListener('click', () => {
        const newVal = !(localStorage.getItem('showAdmin') === 'true');
        localStorage.setItem('showAdmin', String(newVal));
        refreshAdminPanel();
      });
    }

    if (btnSavePref && favColor) {
      btnSavePref.addEventListener('click', async () => {
        const payload = { favoriteColor: favColor.value || null };
        const res = await fetch('/api/save-pref', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (saveStatus) saveStatus.textContent = 'Saved: ' + JSON.stringify(data.data);
        localStorage.setItem('favoriteColor', payload.favoriteColor || '');
      });
    }

    if (btnSetCookie) {
      btnSetCookie.addEventListener('click', () => {
        document.cookie = 'ui_theme=dark; Path=/; SameSite=Lax';
        applyThemeFromCookie(); // immediately reflect change without reload
        alert('Cookie set: ui_theme=dark');
      });
    }

    document.querySelectorAll('.spoiler').forEach(el => {
      el.addEventListener('click', () => {
        const secret = el.getAttribute('data-secret');
        console.log('Spoiler revealed →', secret);
        el.textContent = secret;
      });
    });
  });
})();
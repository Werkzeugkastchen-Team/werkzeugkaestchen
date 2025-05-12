function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/';
  }

  function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
  }

  document.addEventListener('DOMContentLoaded', function () {
    const consent = getCookie('cookie_consent');
    const overlay = document.getElementById('cookieOverlay');

    if (overlay) {
      if (!consent) {
        overlay.classList.add('show');
      } else {
        overlay.classList.remove('show');
      }

      const acceptBtn = document.getElementById('acceptCookies');
      const rejectBtn = document.getElementById('rejectCookies');

      if (acceptBtn) {
        acceptBtn.addEventListener('click', function () {
          setCookie('cookie_consent', 'accepted', 365);
          overlay.classList.remove('show');
          location.reload();
        });
      }

      if (rejectBtn) {
        rejectBtn.addEventListener('click', function () {
          setCookie('cookie_consent', 'rejected', 365);
          overlay.classList.remove('show');
          location.reload();
        });
      }
    }
  });
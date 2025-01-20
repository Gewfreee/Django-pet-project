document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    function applyTheme(theme) {
        body.classList.remove('light-theme', 'dark-theme');
        body.classList.add(theme);
        localStorage.setItem('theme', theme);
    }

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        applyTheme('light-theme');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-theme');
             if(body.classList.contains('dark-theme')){
                   applyTheme('dark-theme');
                }
              else{
                applyTheme('light-theme')
              }
        });
    }
});


document.addEventListener('DOMContentLoaded', function() {
  const avatarElements = document.querySelectorAll('.avatar-circle');

    avatarElements.forEach(avatarElement => {
     avatarElement.addEventListener('click', function(event) {
      event.stopPropagation();
      const menuId = this.getAttribute('data-menu-id');
      const menu = document.getElementById(menuId);
        if (menu) {
           menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        }
    });
  });

    document.addEventListener('click', function(event) {
     console.log("click")
     const menus = document.querySelectorAll('.avatar-dropdown-menu');
          menus.forEach(menu => {
            if (menu.style.display === 'block' && !menu.contains(event.target) &&
            !event.target.classList.contains('avatar-circle')){
             menu.style.display = 'none'
            }
        })
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const bookmarkButton = document.querySelector('.bookmark-button');

        function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    if (bookmarkButton) {
        bookmarkButton.addEventListener('click', function() {
             const bookId = this.dataset.bookId;
            fetch(window.location.href, {
                method: 'POST',
               headers: {
                   'X-CSRFToken': csrftoken,
                   'Content-Type': 'application/x-www-form-urlencoded'
               },
               body: new URLSearchParams({
                    'toggle_bookmark': 'true',
               }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                     }
                       return response.json();
                })
                .then(data => {
                     if (data && data.bookmarked !== undefined) {
                       this.textContent = data.bookmarked ? 'Delete bookmark' : 'Add to bookmarks';
                        this.dataset.action = data.bookmarked ? 'remove' : 'add';
                       } else {
                          console.error('Error: Invalid JSON response or missing "bookmarked" property.');
                       }
                })
                 .catch(error => {
                     console.error('There was a problem with the fetch operation:', error);
                 });
            });
        }
});
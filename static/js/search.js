document.addEventListener('keydown', function(event) {
  let value = document.getElementById('search-bar').value
  if (event.key === '/' && document.activeElement !== document.getElementById('search-bar')) {
    event.preventDefault();
    document.getElementById('search-bar').style.display = 'block';
    document.getElementById('search-bar').focus();
    document.getElementById('search-bar').value = value;
  }
});

document.addEventListener("DOMContentLoaded", function() {
  const followForms = document.querySelectorAll('.follow-form');

  followForms.forEach(form => {
      form.addEventListener('submit', async event => {
          event.preventDefault();
          const formElement = event.target;
          const followButton = formElement.querySelector('.follow');
          const formData = new FormData(formElement);
          const profileId = followButton.getAttribute('data-profile-pk');
          let actionUrl;

          if (followButton.textContent === 'Follow') {
              actionUrl = `/follow/${profileId}/`;
          } else if (followButton.textContent === 'Unfollow') {
              actionUrl = `/unfollow/${profileId}/`;
          }

          try {
              const response = await fetch(actionUrl, {
                  method: formElement.getAttribute('method'),
                  body: formData
              });
              const data = await response.json();

              if (response.ok && data.status === "success") {
                  followButton.textContent = (followButton.textContent === 'Follow') ? 'Unfollow' : 'Follow';
              } else {
                  throw new Error('Follow/unfollow operation failed.');
              }
          } catch (error) {
              console.error('AJAX request failed:', error);
          }
      });
  });
});

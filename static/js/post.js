function savePost(postId) {

  fetch(`/save/${postId}`, {
      method: 'POST',
      headers: {
          'X-CSRFToken': getCookie('csrftoken'), 
      },
  })
  .then(response => {
      if (response.ok) {

          console.log('Post saved successfully');
      } else {
          console.error('Failed to save post');
      }
  })
  .catch(error => {
      console.error('Error saving post:', error);
  });
}

function unsavePost(postId) {

  fetch(`/unsave/${postId}`, {
      method: 'POST',
      headers: {
          'X-CSRFToken': getCookie('csrftoken'), 
      },
  })
  .then(response => {
      if (response.ok) {

          console.log('Post unsaved successfully');
      } else {
          console.error('Failed to unsave post');
      }
  })
  .catch(error => {
      console.error('Error unsaving post:', error);
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.save-btn').forEach(button => {
      button.addEventListener('click', function () {
          const postId = this.dataset.postId; 
          savePost(postId);
      });
  });

  document.querySelectorAll('.unsave-btn').forEach(button => {
      button.addEventListener('click', function () {
          const postId = this.dataset.postId; 
          unsavePost(postId);
      });
  });
});
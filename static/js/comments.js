document.addEventListener("DOMContentLoaded", function () {
  var commentBtns = document.querySelectorAll(".comment-btn");
  var modal = document.getElementById("commentModal");
  var closeBtn = document.querySelector(".close");
  var content = document.querySelector(".content");

  var commentForm = document.getElementById("commentForm");
  var currentPostId;

  commentForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var text = commentForm.querySelector("input[name='text']").value;

    fetch(`/comments/create/${currentPostId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCSRFToken()
      },
      body: new URLSearchParams({ 'text': text })
    })
      .then(response => response.json())
      .then(data => {
        if (data.comments) {
          renderComments(data.comments);
          commentForm.querySelector("input[name='text']").value = "";
        } else {
          console.error("Error creating comment:", data.error);
        }
      })
      .catch(error => console.error("Error creating comment:", error));
  });

  commentBtns.forEach(function (commentBtn) {
    commentBtn.addEventListener("click", function () {
      currentPostId = commentBtn.getAttribute("data-post-id");
      fetchAndRenderComments(currentPostId);
      modal.style.display = "block";
    });
  });

  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
    commentForm.querySelector("input[name='text']").value = "";
  });

  window.addEventListener("click", function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
      commentForm.querySelector("input[name='text']").value = "";
    }
  });

  function getCSRFToken() {
    return document.querySelector("input[name='csrfmiddlewaretoken']").value;
  }

  function fetchAndRenderComments(postId) {
    fetch(`/comments/${postId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.comments) {
          renderComments(data.comments);
        } else {
          console.error("Error fetching comments:", data.error);
        }
      })
      .catch(error => console.error("Error fetching comments:", error));
  }
  function renderComments(comments) {
    content.innerHTML = "";
    comments.forEach(comment => {
      var commentDiv = document.createElement("div");
      commentDiv.className = "comment";

      if (comment.profile_img) {
        var img = document.createElement("img");
        img.src = comment.profile_img;
        img.alt = "Profile Image";
        commentDiv.appendChild(img);
      }
      var textNode = document.createElement("p");
      textNode.textContent = comment.text;
      textNode.className = "comment-text"; 
      commentDiv.appendChild(textNode);
      var createdAtNode = document.createElement("p");
      createdAtNode.textContent = comment.created_at;
      createdAtNode.className = "created-at"; 
      commentDiv.appendChild(createdAtNode);

      content.appendChild(commentDiv);
    });
  }

  var initialPostId = commentBtns[0].getAttribute("data-post-id");
  fetchAndRenderComments(initialPostId);
});
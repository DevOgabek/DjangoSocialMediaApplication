function showSection(section) {
    var sections = document.querySelectorAll('.settings-container');
    sections.forEach(function(item) {
      item.style.display = 'none';
    });
    document.getElementById('settings-' + section).style.display = 'block';
  }
  
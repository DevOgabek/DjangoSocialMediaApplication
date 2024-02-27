document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.success__close');
    var successMessage = document.querySelector('.success');
    closeButton.addEventListener('click', function () {
        successMessage.classList.add('success-hide');
        setTimeout(function () {
            successMessage.style.display = 'none';
        }, 500);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('.error__close');
    var errorMessage = document.querySelector('.error');

    closeButton.addEventListener('click', function () {
        errorMessage.classList.add('error-hide');
        setTimeout(function () {
            errorMessage.style.display = 'none';
        }, 500);
    });
});
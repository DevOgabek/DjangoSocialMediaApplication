const inputElements = document.querySelectorAll('.code-input');

inputElements.forEach((input, index) => {
  input.addEventListener('input', (e) => {
    const inputValue = e.target.value.trim();
    const numericValue = inputValue.replace(/\D/g, ''); 

    if (inputValue !== numericValue) {
      input.classList.add('invalid');
    } else {
      input.classList.remove('invalid');
    }

    const sanitizedValue = numericValue.slice(0, 1);

    if (inputValue !== sanitizedValue) {
      input.value = sanitizedValue;
    }

    const isLastInput = index === inputElements.length - 1;
    if (sanitizedValue && !isLastInput) {
      inputElements[index + 1].focus();
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Backspace' && e.target.value === '') {
      inputElements[Math.max(0, index - 1)].focus();
    }
  });
});
let countdown = 60;
const countdownElement = document.getElementById('countdown');
const resendLink = document.getElementById('resendLink');

const resendTimer = setInterval(() => {
    countdown--;
    countdownElement.textContent = countdown;

    if (countdown <= 0) {
    clearInterval(resendTimer);
    countdownElement.textContent = '0';
    resendLink.style.display = 'inline'; 
    }
}, 1000);
function hideErrorMessage(closeButton) {
const errorContainer = closeButton.closest('.error');
if (errorContainer) {
    errorContainer.style.display = 'none';
}
}

const closeButtons = document.querySelectorAll('.error__close');
closeButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        hideErrorMessage(this);
    });
});
function emailValidator(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!email) {
    return 'O email é obrigatório';
  }

  if (!regex.test(email)) {
    return 'O email não é válido';
  }

  return null;
}

function passwordValidator(password) {
  if (!password) {
    return 'A senha é obrigatória';
  }

  if (password.length < 8) {
    return 'A senha deve ter pelo menos 8 caracteres';
  }

  return null;
}

function showError(inputElement, errorMessage) {
  const errorElement = inputElement.parentElement.querySelector('.invalid-feedback');
  errorElement.textContent = errorMessage;
  errorElement.classList.add('d-block');
  inputElement.classList.add('is-invalid');
  inputElement.focus();
}

function hideError(inputElement) {
  const errorElement = inputElement.parentElement.querySelector('.invalid-feedback');
  errorElement.textContent = '';
  errorElement.classList.remove('d-block');
  inputElement.classList.remove('is-invalid');
}

export { emailValidator, passwordValidator, showError, hideError };

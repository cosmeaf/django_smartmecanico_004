import { emailValidator, passwordValidator, showError, hideError } from './auth/validations.js';
import api from '../js/auth/fetchData.js'

const loginButton = document.querySelector('.loginButton');
const emailInput = document.querySelector('input[name="email"]');
const passwordInput = document.querySelector('input[name="password"]');

loginButton.addEventListener('click', async (event) => {
  event.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  const emailValidation = emailValidator(email);
  const passwordValidation = passwordValidator(password);

  if (emailValidation) {
    const errorMessage = emailInput.dataset.errorMessage || emailValidation;
    emailInput.setAttribute('aria-describedby', 'emailError');
    showError(emailInput, errorMessage);
  } else {
    emailInput.removeAttribute('aria-describedby');
    hideError(emailInput);
  }

  if (passwordValidation) {
    const errorMessage = passwordInput.dataset.errorMessage || passwordValidation;
    passwordInput.setAttribute('aria-describedby', 'passwordError');
    showError(passwordInput, errorMessage);
  } else {
    passwordInput.removeAttribute('aria-describedby');
    hideError(passwordInput);
  }

  if (!emailValidation && !passwordValidation) {
    try {
      const response = await api.signIn(email, password);
      window.localStorage.setItem('token', response.access);
      window.location.href = '/dashboard/';      
      console.log(response.access);
    } catch (error) {
      console.error(error.message);
    }
  }
});

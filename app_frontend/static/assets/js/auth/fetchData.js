import apiDriver from '../drivers/index.js';

export default {
  signIn: async (username, password) => {
    try {
      const response = await apiDriver.post('login/', { username, password });
      return response;
    } catch (error) {
      console.error('Erro no login:', error.message);
      throw new Error('Erro ao tentar fazer o login.');
    }
  },

  // Outros métodos de requisição
};

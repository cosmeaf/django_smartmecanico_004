import FetchDriver from './fetch-driver.js';
import APIOnlineChecker from './api-online-checker.js';

const BASE_URL = 'http://10.0.0.10/api/v1/';

// Verifica se a BASE_URL tem o formato correto
if (!/^https?:\/\/.+/.test(BASE_URL)) {
  throw new Error('A BASE_URL deve começar com http:// ou https://');
}

let driver;

if (typeof fetch !== 'undefined') {
  // ambiente do navegador com suporte ao Fetch API
  driver = new FetchDriver(BASE_URL);
} else {
  throw new Error('Ambiente sem suporte ao Fetch API');
}

const apiOnlineChecker = new APIOnlineChecker(driver);

// Verifica se a API está online antes de exportar o driver
apiOnlineChecker.isOnline().then((online) => {
  if (online) {
    console.log('API online!');
  } else {
    console.error('Erro: A API não está respondendo');
  }

  // Adiciona o resultado da verificação da API ao objeto driver
  driver.isOnline = online;
});

export default driver;

class FetchDriver {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(method, url, data = {}) {
    const token = localStorage.getItem('token');
    const response = await fetch(`${this.baseURL}${url}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // incluir prefixo Bearer aqui
      },
      body: method !== 'GET' ? JSON.stringify(data) : undefined,
    });
  
    const json = await response.json();
  
    if (response.ok) {
      return json;
    } else {
      throw new Error(json.message || 'Erro ao processar a solicitação');
    }
  }
  

  get(url) {
    return this.request('GET', url);
  }

  post(url, data) {
    return this.request('POST', url, data);
  }

  put(url, data) {
    return this.request('PUT', url, data);
  }

  delete(url) {
    return this.request('DELETE', url);
  }
}

export default FetchDriver;

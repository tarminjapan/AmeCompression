import axios from 'axios';

let apiBase = 'http://localhost:5000/api';

// Initialize API base from Electron if available
if (window.electronAPI && window.electronAPI.getApiUrl) {
  window.electronAPI.getApiUrl().then(url => {
    apiBase = url;
    api.defaults.baseURL = url;
  });
}

export const api = axios.create({
  baseURL: apiBase,
});

export const getApiBase = () => apiBase;

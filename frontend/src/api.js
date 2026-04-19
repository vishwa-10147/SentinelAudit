import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

export async function login(email, password) {
  const res = await api.post('/api/auth/login', { email, password });
  return res.data;
}

export async function register(name, email, password) {
  const res = await api.post('/api/auth/register', { name, email, password });
  return res.data;
}

export async function logout() {
  await api.post('/api/auth/logout');
}

export async function getCurrentUser() {
  const res = await api.get('/api/auth/me');
  return res.data;
}

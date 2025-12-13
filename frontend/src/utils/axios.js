import axios from "axios";

// Use environment variable only; remove localhost fallback for production
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

const api = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

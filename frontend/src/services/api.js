import axios from 'axios';

// Strict environment variable resolution - NO hardcoded localhost fallback in production code
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  console.warn(
    "CRITICAL CONFIGURATION NOTICE: VITE_API_BASE_URL environment variable is not defined. " +
    "API calls will target relative paths. Set VITE_API_BASE_URL in Netlify/Render environments."
  );
}

const api = axios.create({
  baseURL: API_BASE_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach bearer token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('lms_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle 401 token expiry
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('lms_token');
      localStorage.removeItem('lms_user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

/**
 * Downloads a protected file from the backend as an authenticated Blob stream.
 * Automatically injects the JWT Authorization Bearer header via the axios instance.
 */
export const downloadAuthenticatedFile = async (endpoint, filename) => {
  try {
    const response = await api.get(endpoint, {
      responseType: 'blob',
    });
    const blob = new Blob([response.data], {
      type: response.headers['content-type'] || 'application/octet-stream',
    });
    const blobUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = blobUrl;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(blobUrl);
    return true;
  } catch (error) {
    console.error('Authenticated download failed:', error);
    alert('Failed to download file. Please verify you have active authorization permissions.');
    throw error;
  }
};

export default api;

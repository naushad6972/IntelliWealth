import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Simple in-memory GET cache and inflight request dedupe
const getCache = new Map(); // key -> { expires: ts, data }
const inflight = new Map(); // key -> Promise
const DEFAULT_TTL = 10; // seconds

function cacheKey(config) {
  return `${config.method || 'get'}:${config.url}:${JSON.stringify(config.params || {})}`;
}

api.interceptors.request.use(async (config) => {
  // Only cache GET requests and when not explicitly disabled
  if ((config.method || 'get').toLowerCase() === 'get' && config.headers && !config.headers['Cache-Control']) {
    const key = cacheKey(config);
    const now = Date.now() / 1000;
    const cached = getCache.get(key);
    if (cached && cached.expires > now) {
      // Return a fake fulfilled promise by throwing a cancel token with the cached data attached
      config.adapter = () => {
        return Promise.resolve({
          data: cached.data,
          status: 200,
          statusText: 'OK',
          headers: {},
          config,
        });
      };
    } else if (inflight.has(key)) {
      // If request already in progress, reuse its promise by replacing adapter
      const p = inflight.get(key);
      config.adapter = () => p;
    } else {
      // nothing, request will proceed and response interceptor will cache
    }
  }
  return config;
});

// Request Interceptor: Attach JWT Access Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('intelliwealth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle Unauthorized (401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('intelliwealth_token');
      localStorage.removeItem('intelliwealth_user');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register' && window.location.pathname !== '/') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Response caching for GET requests
api.interceptors.response.use((response) => {
  try {
    const config = response.config || {};
    if ((config.method || 'get').toLowerCase() === 'get' && !config.headers['Cache-Control']) {
      const key = cacheKey(config);
      const ttl = config.headers && config.headers['X-Cache-TTL'] ? Number(config.headers['X-Cache-TTL']) : DEFAULT_TTL;
      getCache.set(key, { data: response.data, expires: Date.now() / 1000 + ttl });
      // clear inflight
      if (inflight.has(key)) inflight.delete(key);
    }
  } catch (e) {
    // ignore cache errors
  }
  return response;
}, (error) => Promise.reject(error));

export default api;

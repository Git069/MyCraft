import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Axios Interceptor ---
// This will run before every request and after every response.
apiClient.interceptors.response.use(
  (response) => response, // If the response is successful, just return it.
  (error) => {
    // If the server responds with 401 Unauthorized
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout(); // Trigger the logout action
      // Redirect to login page
      window.location.href = '/login'; 
    }
    // Return any other errors so they can be handled by the component.
    return Promise.reject(error);
  }
);

export default {
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },

  login(credentials) {
    return apiClient.post('/auth/token/login/', credentials);
  },

  fetchCurrentUser() {
    return apiClient.get('/auth/users/me/');
  },

  createJob(jobData) {
    return apiClient.post('/jobs/', jobData);
  },

  getJobs(params) {
    return apiClient.get('/jobs/', { params });
  },

  becomeCraftsman() {
    return apiClient.post('/auth/become-craftsman/');
  },

  setAuthToken(token) {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  },

  clearAuthToken() {
    delete apiClient.defaults.headers.common['Authorization'];
  },
};

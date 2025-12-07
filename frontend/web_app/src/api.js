import axios from 'axios';

// Create a new axios instance with a custom configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * A central place for all API calls.
 */
export default {
  /**
   * Registers a new user.
   * @param {object} userData - The user's data (e.g., username, email, password).
   * @returns {Promise<object>} The response data from the server.
   */
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },

  /**
   * Logs in a user.
   * @param {object} credentials - The user's credentials (username, password).
   * @returns {Promise<object>} The response data from the server, containing the auth token.
   */
  login(credentials) {
    return apiClient.post('/auth/token/login/', credentials);
  },

  /**
   * Saves the auth token to localStorage and sets it on the axios instance.
   * @param {string} token - The authentication token.
   */
  setAuthToken(token) {
    if (token) {
      localStorage.setItem('authToken', token);
      apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  },

  /**
   * Removes the auth token from localStorage and the axios instance.
   */
  clearAuthToken() {
    localStorage.removeItem('authToken');
    delete apiClient.defaults.headers.common['Authorization'];
  },

  /**
   * Checks for an existing token and sets it on the axios instance.
   * To be called when the app starts.
   */
  initialize() {
    const token = localStorage.getItem('authToken');
    if (token) {
      this.setAuthToken(token);
    }
  }
};

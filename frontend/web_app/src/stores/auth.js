import { defineStore } from 'pinia';
import api from '@/api';

export const useAuthStore = defineStore('auth', {
  // The state reflects the current session, not the persisted state.
  state: () => ({
    isAuthenticated: false,
    user: null, // Will hold user data like { id, username, email }
    token: null,
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
  },
  actions: {
    /**
     * Handles the login process, including fetching user data.
     * Throws an error if login fails, so the component can handle it.
     */
    async login(credentials) {
      try {
        const response = await api.login(credentials);
        const token = response.data.auth_token;

        if (token) {
          this.token = token;
          this.isAuthenticated = true;
          localStorage.setItem('authToken', token);
          api.setAuthToken(token);

          // Fetch and store user details after successful login
          const userResponse = await api.fetchCurrentUser();
          this.user = userResponse.data;

        } else {
          throw new Error('Authentication token not found in response.');
        }
      } catch (error) {
        // Clean up on failure and re-throw the error for the component
        this.logout();
        throw error;
      }
    },

    /**
     * Logs out the user by clearing state, storage, and API headers.
     */
    logout() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      localStorage.removeItem('authToken');
      api.clearAuthToken();
    },

    /**
     * Initializes the auth state from localStorage on app startup.
     * If a token exists, it validates it by fetching user data.
     */
    async initializeAuth() {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        try {
          api.setAuthToken(storedToken);
          const userResponse = await api.fetchCurrentUser();

          this.token = storedToken;
          this.isAuthenticated = true;
          this.user = userResponse.data;
        } catch (error) {
          // If token is invalid, logout to clear the bad token
          this.logout();
        }
      }
    },
  },
});

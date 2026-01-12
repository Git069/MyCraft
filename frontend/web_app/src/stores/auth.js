import { defineStore } from 'pinia';
import api from '@/api';

/* ==========================================================================
   Auth Store
   ========================================================================== */

/**
 * Pinia store for managing user authentication state.
 * Handles login, logout, user fetching, and token management.
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null,
    token: null,
  }),

  getters: {
    /**
     * Checks if the user is currently logged in.
     * @param {Object} state - The current state.
     * @returns {boolean} True if authenticated.
     */
    isLoggedIn: (state) => state.isAuthenticated,

    /**
     * Retrieves the current user object.
     * @param {Object} state - The current state.
     * @returns {Object|null} The user object or null.
     */
    currentUser: (state) => state.user,

    /**
     * Checks if the current user is a craftsman.
     * @param {Object} state - The current state.
     * @returns {boolean} True if the user is a craftsman.
     */
    isCraftsman: (state) => state.user?.is_craftsman || false,
  },

  actions: {
    /**
     * Logs in the user with the provided credentials.
     * Sets the token in local storage and API headers.
     *
     * @param {Object} credentials - The login credentials (username/email, password).
     * @returns {Promise<void>}
     * @throws {Error} If login fails or token is missing.
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
          await this.fetchUser();
        } else {
          throw new Error('Authentication token not found in response.');
        }
      } catch (error) {
        this.logout();
        throw error;
      }
    },

    /**
     * Logs out the current user.
     * Clears state, local storage, and API headers.
     */
    logout() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      localStorage.removeItem('authToken');
      api.clearAuthToken();
    },

    /**
     * Initializes authentication state from local storage.
     * Called on app startup to restore session.
     *
     * @returns {Promise<void>}
     */
    async initializeAuth() {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        try {
          api.setAuthToken(storedToken);
          await this.fetchUser();
          this.token = storedToken;
          this.isAuthenticated = true;
        } catch (error) {
          this.logout();
        }
      }
    },

    /**
     * Fetches the current user's profile data from the API.
     *
     * @returns {Promise<void>}
     * @throws {Error} If fetching user data fails.
     */
    async fetchUser() {
      try {
        const userResponse = await api.fetchCurrentUser();
        this.user = userResponse.data;
      } catch (error) {
        console.error('Failed to fetch user data, logging out.', error);
        this.logout();
        throw error;
      }
    },

    /**
     * Updates the user's status to craftsman.
     * Refetches user data to update state.
     *
     * @returns {Promise<void>}
     */
    async becomeCraftsman() {
      await api.becomeCraftsman();
      await this.fetchUser();
    },
  },
});

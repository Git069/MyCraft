import { defineStore } from 'pinia';
import api from '@/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null,
    token: null,
  }),
  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
    isCraftsman: (state) => state.user?.is_craftsman || false,
  },
  actions: {
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
    logout() {
      this.isAuthenticated = false;
      this.user = null;
      this.token = null;
      localStorage.removeItem('authToken');
      api.clearAuthToken();
    },
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
    async fetchUser() {
      const userResponse = await api.fetchCurrentUser();
      this.user = userResponse.data;
    },
    async becomeCraftsman() {
      await api.becomeCraftsman();
      // Force-refresh user data to get the new 'is_craftsman' status
      await this.fetchUser();
    },
  },
});

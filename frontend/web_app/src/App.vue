<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import AppLogo from '@/assets/logo.svg'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue';

const authStore = useAuthStore();
const router = useRouter();

const isLoggedIn = computed(() => authStore.isLoggedIn);

const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'Home' }); // Redirect to home page after logout
};
</script>

<template>
  <header class="main-header">
    <div class="container nav-container">
      <RouterLink :to="{ name: 'Home' }" class="logo-link">
        <img :src="AppLogo" alt="MyCraft Logo" class="logo-image" />
      </RouterLink>

      <nav class="nav-links">
        <RouterLink :to="{ name: 'JobMarketplace' }">Aufträge</RouterLink>

        <template v-if="!isLoggedIn">
          <RouterLink :to="{ name: 'Login' }">Login</RouterLink>
          <RouterLink :to="{ name: 'Register' }">Registrieren</RouterLink>
        </template>

        <template v-else>
          <RouterLink :to="{ name: 'CreateJob' }">Auftrag erstellen</RouterLink>
          <button @click="handleLogout" class="base-button logout-button">Logout</button>
        </template>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.main-header {
  width: 100%;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-sm) 0;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  text-decoration: none;
  display: flex;
  align-items: center;
}

.logo-image {
  height: 45px;
  width: auto;
}

.nav-links {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  padding: var(--spacing-xs) var(--spacing-sm);
  transition: color var(--transition-speed);
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: var(--color-primary);
}

.logout-button {
  background-color: var(--color-error);
  color: var(--color-text-inverted);
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-base);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: background-color var(--transition-speed);
}

.logout-button:hover {
  background-color: #c82333;
}

.nav-container.container {
  padding-left: var(--spacing-md);
  padding-right: var(--spacing-md);
}
</style>

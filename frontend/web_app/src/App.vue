<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { RouterLink, RouterView, useRouter } from 'vue-router';
import AppLogo from '@/assets/logo.svg';
import { useAuthStore } from '@/stores/auth';
import ToastContainer from '@/components/ToastContainer.vue';
import UserAvatar from '@/components/UserAvatar.vue'; // Import UserAvatar

const authStore = useAuthStore();
const router = useRouter();

const isLoggedIn = computed(() => authStore.isLoggedIn);
const isCraftsman = computed(() => authStore.isCraftsman);
const user = computed(() => authStore.currentUser);

const isMenuOpen = ref(false);
const menuRef = ref(null);

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const closeMenu = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    isMenuOpen.value = false;
  }
};

const handleLogout = () => {
  authStore.logout();
  isMenuOpen.value = false;
  router.push({ name: 'Home' });
};

const fullImageUrl = computed(() => {
  if (user.value?.profile_picture) {
    return `http://localhost:8000${user.value.profile_picture}`;
  }
  return null;
});

onMounted(() => {
  document.addEventListener('click', closeMenu);
});

onUnmounted(() => {
  document.removeEventListener('click', closeMenu);
});
</script>

<template>
  <ToastContainer />

  <header class="main-header">
    <div class="container-fluid nav-container">

      <RouterLink :to="{ name: 'Home' }" class="logo-link">
        <img :src="AppLogo" alt="MyCraft Logo" class="logo-image" />
      </RouterLink>

      <nav class="nav-right">

        <RouterLink
          v-if="isLoggedIn && !isCraftsman"
          :to="{ name: 'BecomeCraftsman' }"
          class="become-host-link"
        >
          Werde Handwerker
        </RouterLink>

        <RouterLink
          v-if="isLoggedIn && isCraftsman"
          :to="{ name: 'CreateService' }"
          class="become-host-link"
        >
          Auftrag erstellen
        </RouterLink>

        <div class="user-menu-wrapper" ref="menuRef">
          <button class="user-menu-btn" @click.stop="toggleMenu">
            <div class="hamburger-icon">
              <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="presentation" focusable="false" style="display: block; fill: none; height: 16px; width: 16px; stroke: currentcolor; stroke-width: 3; overflow: visible;"><g fill="none"><path d="m2 16h28"></path><path d="m2 24h28"></path><path d="m2 8h28"></path></g></svg>
            </div>

            <!-- Use UserAvatar component -->
            <UserAvatar :src="fullImageUrl" :name="user?.username || ''" :size="30" />
          </button>

          <div v-if="isMenuOpen" class="dropdown-menu">
            <template v-if="isLoggedIn">
              <RouterLink :to="{ name: 'Dashboard' }" class="menu-item bold" @click="isMenuOpen = false">
                Dashboard
              </RouterLink>
              <RouterLink :to="{ name: 'Inbox' }" class="menu-item" @click="isMenuOpen = false">
                Nachrichten
              </RouterLink>
              <RouterLink :to="{ name: 'Profile' }" class="menu-item" @click="isMenuOpen = false">
                Profil
              </RouterLink>
              <div class="divider"></div>
              <button class="menu-item logout-item" @click="handleLogout">Logout</button>
            </template>

            <template v-else>
              <RouterLink :to="{ name: 'Login' }" class="menu-item bold" @click="isMenuOpen = false">
                Login
              </RouterLink>
              <RouterLink :to="{ name: 'Register' }" class="menu-item" @click="isMenuOpen = false">
                Registrieren
              </RouterLink>
            </template>
          </div>
        </div>

      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
/* Styles remain largely the same, removed old avatar styles */
.main-header {
  height: 80px;
  background-color: white;
  border-bottom: 1px solid #ebebeb;
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-container {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo-link {
  display: flex;
  align-items: center;
}
.logo-image {
  height: 32px;
  width: auto;
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.become-host-link {
  text-decoration: none;
  color: var(--color-text);
  font-size: 0.9rem;
  font-weight: 600;
  padding: 10px 16px;
  border-radius: 22px;
  transition: background-color 0.2s;
}
.become-host-link:hover {
  background-color: #f7f7f7;
}
.user-menu-wrapper {
  position: relative;
}
.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border: 1px solid #dddddd;
  border-radius: 21px;
  padding: 5px 5px 5px 12px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.user-menu-btn:hover {
  box-shadow: 0 2px 4px rgba(0,0,0,0.18);
}
.hamburger-icon {
  color: #222222;
}
/* Removed old .avatar, .avatar-image, .avatar-placeholder styles */
.dropdown-menu {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
  width: 240px;
  padding: 8px 0;
  overflow: hidden;
  z-index: 101;
}
.menu-item {
  display: block;
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  font-size: 0.9rem;
  color: #222222;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
}
.menu-item:hover {
  background-color: #f7f7f7;
}
.menu-item.bold {
  font-weight: 600;
}
.logout-item {
  color: #222222;
}
.divider {
  height: 1px;
  background-color: #dddddd;
  margin: 8px 0;
}
</style>

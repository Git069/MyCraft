import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './PublicStyles.css'
import { useAuthStore } from './stores/auth'

async function initializeApp() {
  const app = createApp(App)

  app.use(createPinia())
  app.use(router)

  const authStore = useAuthStore();
  await authStore.initializeAuth();

  app.mount('#app')
}

initializeApp();

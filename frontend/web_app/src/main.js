import { createApp } from 'vue';
import { createPinia } from 'pinia';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

import App from './App.vue';
import router from './router';
import { useAuthStore } from '@/stores/auth';
import './PublicStyles.css';

/* ==========================================================================
   Leaflet Configuration
   ========================================================================== */

/**
 * Fix for Leaflet's default icon paths in Vite.
 * Manually sets the icon URLs to ensure markers appear correctly.
 */
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

/* ==========================================================================
   App Initialization
   ========================================================================== */

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

/**
 * Initialize Authentication Store.
 * Checks for existing tokens to restore user session.
 */
const authStore = useAuthStore();
authStore.initializeAuth();

app.mount('#app');

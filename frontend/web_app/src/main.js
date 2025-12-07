import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import api from './api' // Import the api service
import './PublicStyles.css'

// Initialize the API service (checks for existing token)
api.initialize();

const app = createApp(App)

app.use(router)

app.mount('#app')

<template>
    <div class="register">
      <h2>Registrieren</h2>
    
    <form @submit.prevent="registerUser">

      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" v-model="name" required>
      </div>

      <div class="form-group">
        <label for="name">Nachname</label>
        <input type="text" id="lastname" v-model="lastname" required>
      </div>
      
      <div class="form-group">
        <label for="email">E-Mail</label>
        <input type="email" id="email" v-model="email" required>
      </div>

      <div class="form-group">
        <label for="password">Passwort</label>
        <input type="password" id="password" v-model="password" required>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div v-if="success" class="success-message">
        {{ success }}
      </div>

      <button type="submit" :disabled="isLoading" class="base-button">
        {{ isLoading ? 'Registriere...' : 'Registrierung abschließen' }}
      </button>
    </form>
      </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router'; // Um nach erfolgreicher Registrierung weiterzuleiten
  
  // Konkreter API-Endpunkt für die Registrierung im Django-Backend
  const REGISTER_URL = 'http://127.0.0.1:8000/api/auth/register/';
  
  // Zustandsvariablen für die Formularfelder und das Feedback
  const email = ref('');
  const password = ref('');
  const error = ref(null);
  const success = ref(null);
  const isLoading = ref(false);
  
  const router = useRouter();
  
  /**
   * Sendet die Registrierungsdaten an die Django-API.
   */
  async function registerUser() {
    error.value = null; // Alte Fehler löschen
    success.value = null; // Alte Erfolgsmeldungen löschen
    isLoading.value = true;
  
    // Das Objekt muss GENAU die Feldnamen enthalten, die der Django Serializer erwartet!
    // Unser Serializer erwartet 'email' und 'password'.
    const registrationData = {
      email: email.value,
      password: password.value
    };
  
    try {
      const response = await axios.post(REGISTER_URL, registrationData);
  
      // Erfolg: Status 201 (Created)
      success.value = response.data.message || 'Registrierung erfolgreich!';
      console.log('Registrierung erfolgreich:', response.data);
  
      // Weiterleitung zur Login-Seite nach 2 Sekunden
      setTimeout(() => {
        router.push({ name: 'Login' }); // Geht zur Route mit dem Namen 'Login'
      }, 2000);
  
    } catch (err) {
      // Fehlerbehandlung: Status 400 (Bad Request)
      console.error('Registrierungsfehler:', err.response);
      
      if (err.response && err.response.data) {
        // Spezifische Fehler vom Serializer anzeigen
        if (err.response.data.email) {
            error.value = `Fehler: ${err.response.data.email[0]}`;
        } else if (err.response.data.password) {
            error.value = `Passwortfehler: ${err.response.data.password[0]}`;
        } else {
            error.value = 'Ein unbekannter Fehler ist aufgetreten.';
        }
      } else {
        error.value = 'Der Server ist nicht erreichbar. Bitte später erneut versuchen.';
      }
  
    } finally {
      isLoading.value = false;
    }
  }
  </script>
  
  <style scoped>
  /* Hier könnten Sie einfaches CSS für .form-group, .error-message, etc. definieren */
  
  .error-message { color: red; margin-top: 10px; }
  .success-message { color: green; margin-top: 10px; }
  /*.form-group { margin-bottom: 15px; }*/
  input { width: 100%; padding: 8px; box-sizing: border-box; }
  </style>
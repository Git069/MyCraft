<script setup>
import { ref, onMounted } from 'vue'; // WICHTIG: onMounted hinzugefügt
import axios from 'axios';

// --- STATE (Daten) ---
const showModal = ref(false);
const orders = ref([]); // Jetzt starten wir leer!

// Formulardaten
const jobData = ref({
  title: '',
  description: '',
  trade: 'OTHER',
  zip_code: '',
  city: '',
  price: null,
  execution_date: null
});

// --- API LOGIK ---

// 1. Daten vom Server holen (GET)
// MyJobs.vue (oder wie du deine Verwaltungs-Komponente genannt hast)

const fetchJobs = async () => {
  const token = localStorage.getItem('token');

  // Sicherheits-Check
  if (!token) {
      console.error("Nicht eingeloggt");
      return;
  }

  try {
    // WICHTIG: Hier rufen wir jetzt den neuen "my_jobs" Endpunkt auf!
    const response = await axios.get('http://127.0.0.1:8000/api/jobs/my_jobs/', {
        headers: {
            'Authorization': `Token ${token}` // Auth ist hier zwingend nötig!
        }
    });

    orders.value = response.data; // Das sind jetzt nur DEINE Jobs
  } catch (error) {
    console.error("Fehler beim Laden meiner Jobs:", error);
  }
};

// 2. Automatisch laden, wenn die Seite aufgeht
onMounted(() => {
  fetchJobs();
});

// 3. Neuen Job speichern (POST)
const submitJob = async () => {
  const token = localStorage.getItem('token');

  if (!token) {
    alert("Fehler: Du bist nicht eingeloggt.");
    return;
  }

  try {
    await axios.post('http://127.0.0.1:8000/api/jobs/', jobData.value, {
      headers: { 'Authorization': `Token ${token}` }
    });

    // WICHTIG: Liste neu laden, damit der neue Auftrag sofort sichtbar ist
    await fetchJobs();

    closeModal();
    // Formular resetten
    jobData.value = { title: '', description: '', trade: 'OTHER', zip_code: '', city: '', price: null };
    alert("Auftrag erfolgreich angelegt!");

  } catch (error) {
    console.error('Fehler:', error);
    alert("Fehler beim Speichern.");
  }
};

// --- HELPER ---
const createOrder = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<template>
  <div class="page-wrapper">
    <div class="orders-container">

      <header class="header-section">
        <h1 class="main-title">Aufträge verwalten</h1>
      </header>

      <section class="action-card">
        <div class="action-content">
          <h2>Auftrag erstellen</h2>
          <p class="action-desc">Neuen Kundenauftrag anlegen</p>
        </div>
        <button @click="createOrder" class="circle-btn" aria-label="Neuen Auftrag erstellen">
          <span class="plus-icon">+</span>
        </button>
      </section>

      <section class="list-section">
        <h2 class="sub-title">Aktuelle Aufträge</h2>

        <div v-if="orders.length === 0" class="empty-state">
          Keine Aufträge gefunden.
        </div>

        <ul v-else class="order-list">
          <li v-for="order in orders" :key="order.id" class="order-item">
            <div class="order-details">
              <span class="order-title">{{ order.title }}</span>

              <span class="order-customer">
                 {{ order.trade }} | {{ order.price }} €
                 <br>
                 <small>{{ order.description }}</small>
              </span>
            </div>

            <div class="order-meta">
              <span class="date-badge">
                {{ new Date(order.created_at).toLocaleDateString() }}
              </span>
            </div>
          </li>
        </ul>
      </section>

    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Neuen Auftrag erfassen</h3>
          <button @click="closeModal" class="close-btn">×</button>
        </div>

        <form @submit.prevent="submitJob" class="job-form">
          <div class="form-group">
            <label>Titel</label>
            <input v-model="jobData.title" type="text" required placeholder="Was ist zu tun?">
          </div>

          <div class="form-group">
            <label>Beschreibung</label>
            <textarea v-model="jobData.description" rows="3" placeholder="Details..."></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
                <label>PLZ</label>
                <input v-model="jobData.zip_code" type="text" maxlength="5">
            </div>
            <div class="form-group">
                <label>Stadt</label>
                <input v-model="jobData.city" type="text">
            </div>
          </div>

          <div class="form-group">
            <label>Gewerk</label>
            <select v-model="jobData.trade">
                <option value="OTHER">Sonstiges</option>
                <option value="PLUMBER">Sanitär</option>
                <option value="ELECTRICIAN">Elektrik</option>
                <option value="PAINTER">Maler</option>
            </select>
          </div>

          <div class="form-group">
             <label>Preis (€)</label>
             <input v-model="jobData.price" type="number" step="0.01">
          </div>

          <button type="submit" class="submit-btn">Auftrag speichern</button>
        </form>
      </div>
    </div>
    </div>
</template>

<style scoped>
/* --- DEINE BESTEHENDEN STYLES (Unverändert) --- */
.page-wrapper {
  padding: 1rem;
  background-color: #f4f6f8;
  min-height: 100vh;
}
.orders-container {
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #333;
}
.main-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #1a202c;
  font-weight: 700;
}
.action-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
  transition: transform 0.2s ease;
}
.action-card:active { transform: scale(0.98); }
.action-content h2 { margin: 0; font-size: 1.2rem; color: #2d3748; }
.action-desc { margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #718096; }
.circle-btn {
  width: 56px; height: 56px; border-radius: 50%;
  background: linear-gradient(135deg, #42b983 0%, #3aa876 100%);
  border: none; color: white; font-size: 2rem; cursor: pointer;
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.4);
  display: flex; justify-content: center; align-items: center; flex-shrink: 0;
  -webkit-tap-highlight-color: transparent;
}
.circle-btn:active { transform: scale(0.95); box-shadow: 0 2px 6px rgba(66, 185, 131, 0.4); }
.plus-icon { margin-top: -4px; font-weight: 300; }
.sub-title { font-size: 1.1rem; color: #4a5568; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.order-list { list-style: none; padding: 0; margin: 0; }
.order-item {
  background: white; border-radius: 10px; padding: 1rem; margin-bottom: 0.8rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex;
  justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;
}
.order-details { display: flex; flex-direction: column; }
.order-title { font-weight: 600; color: #2d3748; font-size: 1rem; }
.order-customer { font-size: 0.85rem; color: #718096; margin-top: 0.2rem; }
.date-badge {
  background-color: #e6fffa; color: #2c7a7b; padding: 0.3rem 0.6rem;
  border-radius: 6px; font-size: 0.8rem; font-weight: 500; white-space: nowrap;
}

/* --- NEU: MODAL STYLES --- */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0,0,0,0.5); /* Halbtransparenter Hintergrund */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-card {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h3 { margin: 0; font-size: 1.3rem; color: #2d3748; }

.close-btn {
  background: none; border: none; font-size: 2rem;
  line-height: 1; cursor: pointer; color: #718096;
}

.job-form .form-group { margin-bottom: 1rem; }
.job-form label { display: block; margin-bottom: 0.4rem; font-weight: 600; font-size: 0.9rem; color: #4a5568; }
.job-form input, .job-form textarea, .job-form select {
  width: 100%; padding: 0.7rem; border: 1px solid #e2e8f0;
  border-radius: 8px; font-size: 1rem;
  font-family: inherit;
}
.job-form input:focus { border-color: #42b983; outline: none; }

.form-row { display: flex; gap: 1rem; }
.form-row .form-group { flex: 1; }

.submit-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.5rem;
}
.submit-btn:hover { background-color: #3aa876; }

/* Responsive adjustments */
@media (max-width: 600px) {
  .page-wrapper { padding: 0.5rem; }
  .main-title { font-size: 1.5rem; margin-top: 1rem; }
  .action-card { padding: 1rem; }
  .action-content h2 { font-size: 1.1rem; }
  .circle-btn { width: 48px; height: 48px; font-size: 1.6rem; }
}
</style>
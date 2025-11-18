<template>
  <div class="orders-page">
    <!-- Übersicht der bestehenden Aufträge -->
    <section class="orders-overview">
      <h2>Meine Aufträge</h2>
      <div v-if="orders.length === 0" class="empty-state">
        Noch keine Aufträge vorhanden
      </div>
      <div v-else class="orders-list">
        <div
          v-for="order in orders"
          :key="order.id"
          class="order-card"
          @mouseenter="hoveredOrderId = order.id"
          @mouseleave="hoveredOrderId = null"
        >
          <div class="order-content">
            <h3>{{ order.titel }}</h3>
            <p class="order-description">{{ order.beschreibung }}</p>
            <div class="order-meta">
              <span class="meta-item">{{ order.handwerk }}</span>
              <span class="meta-item">PLZ: {{ order.postleitzahl }}</span>
              <span class="meta-item status" :class="order.status">{{ order.status }}</span>
            </div>
            <div class="order-dates">
              <small>Erstellt: {{ formatDate(order.erstellt_am) }}</small>
              <small>Aktualisiert: {{ formatDate(order.aktualisiert_am) }}</small>
            </div>
          </div>
          <button
            v-show="hoveredOrderId === order.id"
            class="edit-button"
            @click="editOrder(order)"
            aria-label="Auftrag bearbeiten"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- Formular für neuen/bearbeiteten Auftrag -->
    <section class="order-form-section">
      <h2>{{ isEditing ? 'Auftrag bearbeiten' : 'Neuen Auftrag erstellen' }}</h2>
      <form @submit.prevent="handleSubmit" class="order-form">
        <div class="form-group">
          <label for="titel">Titel</label>
          <input
            id="titel"
            v-model="formData.titel"
            type="text"
            placeholder="Projekttitel"
            required
          />
        </div>

        <div class="form-group">
          <label for="beschreibung">Beschreibung</label>
          <textarea
            id="beschreibung"
            v-model="formData.beschreibung"
            placeholder="Auftragsbeschreibung"
            rows="4"
            required
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="handwerk">Handwerk</label>
            <input
              id="handwerk"
              v-model="formData.handwerk"
              type="text"
              placeholder="z.B. Elektrik"
              required
            />
          </div>

          <div class="form-group">
            <label for="postleitzahl">Postleitzahl</label>
            <input
              id="postleitzahl"
              v-model="formData.postleitzahl"
              type="text"
              placeholder="PLZ"
              pattern="[0-9]{5}"
              required
            />
          </div>
        </div>

        <div class="form-group">
          <label for="status">Status</label>
          <select id="status" v-model="formData.status" required>
            <option value="offen">Offen</option>
            <option value="in_bearbeitung">In Bearbeitung</option>
            <option value="abgeschlossen">Abgeschlossen</option>
          </select>
        </div>

        <div class="form-actions">
          <button v-if="isEditing" type="button" @click="cancelEdit" class="btn-secondary">
            Abbrechen
          </button>
          <button type="submit" class="btn-primary">
            {{ isEditing ? 'Auftrag aktualisieren' : 'Auftrag erstellen' }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// State Management
const orders = ref([]);
const hoveredOrderId = ref(null);
const isEditing = ref(false);
const editingOrderId = ref(null);

const formData = reactive({
  titel: '',
  beschreibung: '',
  handwerk: '',
  postleitzahl: '',
  status: 'offen'
});

// Aufträge vom Backend laden
const fetchOrders = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/auftraege/`);
    orders.value = response.data;
  } catch (error) {
    console.error('Fehler beim Laden der Aufträge:', error);
  }
};

// Auftrag erstellen oder aktualisieren
const handleSubmit = async () => {
  try {
    if (isEditing.value) {
      // Auftrag aktualisieren
      const response = await axios.put(
        `${API_BASE_URL}/auftraege/${editingOrderId.value}/`,
        formData
      );
      const index = orders.value.findIndex(o => o.id === editingOrderId.value);
      if (index !== -1) {
        orders.value[index] = response.data;
      }
    } else {
      // Neuen Auftrag erstellen
      const response = await axios.post(`${API_BASE_URL}/auftraege/`, formData);
      orders.value.unshift(response.data);
    }
    resetForm();
  } catch (error) {
    console.error('Fehler beim Speichern des Auftrags:', error);
  }
};

// Auftrag für Bearbeitung laden
const editOrder = (order) => {
  isEditing.value = true;
  editingOrderId.value = order.id;
  Object.assign(formData, {
    titel: order.titel,
    beschreibung: order.beschreibung,
    handwerk: order.handwerk,
    postleitzahl: order.postleitzahl,
    status: order.status
  });
  // Scroll zum Formular
  document.querySelector('.order-form-section').scrollIntoView({ behavior: 'smooth' });
};

// Bearbeitung abbrechen
const cancelEdit = () => {
  resetForm();
};

// Formular zurücksetzen
const resetForm = () => {
  isEditing.value = false;
  editingOrderId.value = null;
  formData.titel = '';
  formData.beschreibung = '';
  formData.handwerk = '';
  formData.postleitzahl = '';
  formData.status = 'offen';
};

// Datum formatieren
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
};

// Beim Laden der Komponente
onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
.orders-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* Übersicht Section */
.orders-overview {
  margin-bottom: 3rem;
}

.orders-overview h2 {
  margin-bottom: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.orders-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.order-card {
  position: relative;
  padding: 1.5rem;
  border-radius: var(--border-radius, 8px);
  background: var(--card-bg, #fff);
  border: 1px solid var(--border-color, #e0e0e0);
  transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.order-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.order-description {
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.order-meta {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.meta-item {
  padding: 0.25rem 0.75rem;
  background: var(--tag-bg, #f5f5f5);
  border-radius: 12px;
  font-size: 0.875rem;
}

.meta-item.status {
  font-weight: 500;
}

.meta-item.status.offen {
  background: var(--status-open, #e3f2fd);
  color: var(--status-open-text, #1976d2);
}

.meta-item.status.in_bearbeitung {
  background: var(--status-progress, #fff3e0);
  color: var(--status-progress-text, #f57c00);
}

.meta-item.status.abgeschlossen {
  background: var(--status-done, #e8f5e9);
  color: var(--status-done-text, #388e3c);
}

.order-dates {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.edit-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem;
  background: var(--primary-color, #2196f3);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-button:hover {
  background: var(--primary-dark, #1976d2);
}

/* Formular Section */
.order-form-section {
  background: var(--card-bg, #fff);
  padding: 2rem;
  border-radius: var(--border-radius, 8px);
  border: 1px solid var(--border-color, #e0e0e0);
}

.order-form-section h2 {
  margin-bottom: 1.5rem;
}

.order-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--input-border, #ccc);
  border-radius: var(--border-radius, 4px);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color, #2196f3);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius, 4px);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary {
  background: var(--primary-color, #2196f3);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark, #1976d2);
}

.btn-secondary {
  background: var(--secondary-color, #757575);
  color: white;
}

.btn-secondary:hover {
  background: var(--secondary-dark, #616161);
}

/* Responsive Design */
@media (max-width: 768px) {
  .orders-list {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import JobCard from '@/components/JobCard.vue';
import BookingCard from '@/components/BookingCard.vue';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';

const authStore = useAuthStore();
const toast = useToastStore();
const user = computed(() => authStore.currentUser);

// Daten
const myServices = ref([]);
const myOrders = ref([]);
const loading = ref(true);

// TABS: Wir nutzen einheitlich 'services' und 'orders'
const activeTab = ref('services');

const fetchData = async () => {
  loading.value = true;
  try {
    const [servicesRes, ordersRes] = await Promise.all([
      api.getMyServices(),
      api.getMyOrders()
    ]);

    // Daten sicher zuweisen
    if (Array.isArray(servicesRes.data)) {
        myServices.value = [...servicesRes.data];
    } else if (servicesRes.data && Array.isArray(servicesRes.data.results)) {
        myServices.value = [...servicesRes.data.results];
    } else {
        myServices.value = [];
    }

    // Orders zuweisen
    if (Array.isArray(ordersRes.data)) {
        myOrders.value = [...ordersRes.data];
    } else if (ordersRes.data && Array.isArray(ordersRes.data.results)) {
        myOrders.value = [...ordersRes.data.results];
    } else {
        myOrders.value = [];
    }

  } catch (err) {
    console.error(err);
    toast.addToast("Daten konnten nicht geladen werden", "error");
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);

// --- NEU: Computed Properties für die Auftrags-Aufteilung ---
const activeOrders = computed(() => {
  // Zeige hier nur Anfragen (PENDING) und bestätigte Jobs (CONFIRMED)
  return myOrders.value.filter(o => ['PENDING', 'CONFIRMED'].includes(o.status));
});

const pastOrders = computed(() => {
  // Zeige hier erledigte (COMPLETED) und stornierte (CANCELLED)
  return myOrders.value.filter(o => ['COMPLETED', 'CANCELLED'].includes(o.status));
});

const pendingOrdersCount = computed(() => {
  return myOrders.value.filter(o => o.status === 'PENDING' || o.status === 'CONFIRMED').length;
});

// Actions
const handleMarkCompleted = async (bookingId) => {
  if (!confirm("Möchtest du diesen Auftrag wirklich als erledigt markieren?")) return;
  try {
    await api.markBookingAsCompleted(bookingId);
    toast.addToast("Auftrag erledigt!", "success");
    await fetchData(); // await hinzugefügt für sauberen Reload
  } catch (err) {
    toast.addToast("Fehler beim Speichern", "error");
  }
};

const handleCancelOrder = async (bookingId) => {
  if (!confirm("Wirklich stornieren?")) return;
  try {
    await api.cancelBooking(bookingId);
    toast.addToast("Storniert", "info");
    await fetchData();
  } catch (err) {
    toast.addToast("Fehler beim Stornieren", "error");
  }
};
</script>

<template>
  <div class="container page-wrapper">
    <header class="dashboard-header">
      <div class="header-text">
        <h1>Handwerker Dashboard</h1>
        <p class="subtitle">Willkommen, {{ user?.username }}!</p>
      </div>

      <router-link :to="{ name: 'CreateService' }" class="base-button primary-action create-btn">
        + Neues Inserat
      </router-link>
    </header>

    <div class="tabs">
      <button
        class="tab-btn"
        :class="{ active: activeTab === 'services' }"
        @click="activeTab = 'services'"
      >
        Meine Inserate ({{ myServices.length }})
      </button>

      <button
        class="tab-btn"
        :class="{ active: activeTab === 'orders' }"
        @click="activeTab = 'orders'"
      >
        Auftragseingang
        <span v-if="pendingOrdersCount > 0" class="badge">{{ pendingOrdersCount }}</span>
      </button>
    </div>

    <div v-if="loading" class="loading-state">Lade Daten...</div>

    <div v-else class="tab-content">

      <div v-if="activeTab === 'services'">
        <div v-if="myServices.length === 0" class="empty-state">
          <p>Du bietest noch keine Dienstleistungen an.</p>
        </div>

        <div v-else class="dashboard-grid">
          <JobCard
            v-for="service in myServices"
            :key="service.id"
            :service="service"
            :show-controls="true"
          />
        </div>
      </div>

      <div v-if="activeTab === 'orders'">

        <div v-if="myOrders.length === 0" class="empty-state">
          <p>Noch keine Aufträge erhalten.</p>
        </div>

        <div v-else>
          <section v-if="activeOrders.length > 0" class="section-group">
            <h3 class="section-title">Aktuelle Aufträge</h3>
            <div class="dashboard-grid">
              <BookingCard
                v-for="order in activeOrders"
                :key="order.id"
                :booking="order"
                :show-controls="true"
                :is-craftsman-view="true"
                @mark-completed="handleMarkCompleted"
                @cancel="handleCancelOrder"
              />
            </div>
          </section>

          <div v-else-if="pastOrders.length > 0" class="info-message">
            <p>Aktuell keine offenen Aufträge.</p>
          </div>

          <section v-if="pastOrders.length > 0" class="section-group past-section">
            <h3 class="section-title">Vergangene Aufträge</h3>
            <div class="dashboard-grid faded-grid">
              <BookingCard
                v-for="order in pastOrders"
                :key="order.id"
                :booking="order"
                :show-controls="true"
                :is-craftsman-view="true"
                @mark-completed="handleMarkCompleted"
                @cancel="handleCancelOrder"
              />
            </div>
          </section>
        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.page-wrapper { padding-top: var(--spacing-lg); padding-bottom: var(--spacing-xxl); }
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: 20px;
  position: relative;
  z-index: 100;
}
.subtitle { color: var(--color-text-light); }
.create-btn { padding: 10px 20px; font-weight: 600; text-decoration: none; display: inline-block; }

/* Tabs Design */
.tabs { display: flex; gap: 20px; border-bottom: 2px solid #eee; margin-bottom: 24px; }
.tab-btn { background: none; border: none; padding: 12px 4px; font-size: 1rem; color: var(--color-text-light); cursor: pointer; position: relative; font-weight: 600; }
.tab-btn.active { color: var(--color-primary); }
.tab-btn.active::after { content: ''; position: absolute; bottom: -2px; left: 0; width: 100%; height: 2px; background-color: var(--color-primary); }
.badge { background-color: var(--color-error); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 8px; vertical-align: middle; }

/* Grid Layout */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  width: 100%;
}

/* Neue Styles für die Sektionen */
.section-group { margin-bottom: 40px; }
.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.past-section .section-title { color: var(--color-text-light); }
.faded-grid { opacity: 0.75; transition: opacity 0.3s; }
.faded-grid:hover { opacity: 1; }

.info-message {
  padding: 20px 0;
  color: var(--color-text-light);
  font-style: italic;
}

.empty-state { text-align: center; padding: 40px; background: #f9f9f9; border-radius: 12px; color: var(--color-text-light); }
.loading-state { text-align: center; padding: 40px; color: var(--color-text-light); }

@media (max-width: 600px) {
  .dashboard-grid { grid-template-columns: 1fr; }
}
</style>
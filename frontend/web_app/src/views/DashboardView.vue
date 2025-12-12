<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';
import JobCard from '@/components/JobCard.vue';
import BookingCard from '@/components/BookingCard.vue';
import JobCardSkeleton from '@/components/JobCardSkeleton.vue';
import ReviewModal from '@/components/ReviewModal.vue';

const authStore = useAuthStore();
const toastStore = useToastStore();
const isCraftsman = computed(() => authStore.isCraftsman);

const activeTab = ref(isCraftsman.value ? 'my-orders' : 'my-bookings');
const myServices = ref([]);
const myBookings = ref([]);
const myOrders = ref([]);
const loading = ref(true);

const showReviewModal = ref(false);
const selectedBookingForReview = ref(null);

const fetchData = async () => {
  loading.value = true;
  try {
    const [servicesRes, bookingsRes, ordersRes] = await Promise.all([
      isCraftsman.value ? api.getMyServices() : Promise.resolve({ data: [] }),
      api.getMyBookings(),
      isCraftsman.value ? api.getMyOrders() : Promise.resolve({ data: [] }),
    ]);
    myServices.value = servicesRes.data.results || servicesRes.data;
    myBookings.value = bookingsRes.data.results || bookingsRes.data;
    myOrders.value = ordersRes.data.results || ordersRes.data;
  } catch (err) {
    toastStore.addToast("Fehler beim Laden des Dashboards.", "error");
  } finally {
    loading.value = false;
  }
};

const updateBookingStatus = (bookingId, list, updatedData) => {
  const bookingIndex = list.value.findIndex(b => b.id === bookingId);
  if (bookingIndex !== -1) {
    list.value[bookingIndex] = { ...list.value[bookingIndex], ...updatedData };
  }
};

const handleMarkCompleted = async (bookingId) => {
  try {
    const response = await api.markBookingAsCompleted(bookingId);
    updateBookingStatus(bookingId, myOrders, { status: response.data.status });
    toastStore.addToast("Auftrag als erledigt markiert.", "success");
  } catch (err) { toastStore.addToast("Aktion fehlgeschlagen.", "error"); }
};

const openReviewModal = (booking) => {
  selectedBookingForReview.value = booking;
  showReviewModal.value = true;
};

const handleCreateReview = async (reviewPayload) => {
  try {
    const response = await api.createReview({ ...reviewPayload, booking: selectedBookingForReview.value.id });
    updateBookingStatus(selectedBookingForReview.value.id, myBookings, { review: response.data });
    toastStore.addToast("Bewertung erfolgreich abgegeben.", "success");
    showReviewModal.value = false;
  } catch (err) {
    toastStore.addToast(err.response?.data?.detail || "Fehler beim Senden der Bewertung.", "error");
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container-fluid dashboard-container">
    <header class="dashboard-header">
      <h1>Mein Dashboard</h1>
    </header>

    <div class="tabs-wrapper">
      <nav class="tab-nav">
        <button v-if="isCraftsman" @click="activeTab = 'my-orders'" class="tab-button" :class="{ 'active': activeTab === 'my-orders' }">Meine Aufträge</button>
        <button @click="activeTab = 'my-bookings'" class="tab-button" :class="{ 'active': activeTab === 'my-bookings' }">Meine Buchungen</button>
        <button v-if="isCraftsman" @click="activeTab = 'my-services'" class="tab-button" :class="{ 'active': activeTab === 'my-services' }">Meine Inserate</button>
      </nav>
    </div>

    <main class="tab-content">
      <div v-if="loading" class="dashboard-grid">
        <JobCardSkeleton v-for="n in 4" :key="n" />
      </div>

      <template v-else>
        <!-- TAB: Meine Inserate -->
        <div v-if="activeTab === 'my-services'">
          <div v-if="myServices.length === 0" class="empty-state">
            <div class="empty-icon">📋</div>
            <h2>Keine Inserate</h2>
            <p>Erstelle dein erstes Service-Angebot, um Kunden zu erreichen.</p>
            <router-link :to="{ name: 'CreateJob' }" class="base-button primary-action">Erstes Inserat erstellen</router-link>
          </div>
          <div v-else class="dashboard-grid">
            <JobCard v-for="service in myServices" :key="service.id" :job="service" :show-controls="true" />
          </div>
        </div>

        <!-- TAB: Meine Aufträge (Eingehend) -->
        <div v-if="activeTab === 'my-orders'">
          <div v-if="myOrders.length === 0" class="empty-state">
            <div class="empty-icon">📥</div>
            <h2>Keine Aufträge</h2>
            <p>Sobald Kunden deine Services buchen, erscheinen sie hier.</p>
          </div>
          <div v-else class="dashboard-grid">
            <BookingCard v-for="booking in myOrders" :key="booking.id" :booking="booking" :show-controls="true" @mark-completed="handleMarkCompleted" />
          </div>
        </div>

        <!-- TAB: Meine Buchungen (Ausgehend) -->
        <div v-if="activeTab === 'my-bookings'">
          <div v-if="myBookings.length === 0" class="empty-state">
            <div class="empty-icon">📅</div>
            <h2>Keine Buchungen</h2>
            <p>Du hast noch keine Services gebucht.</p>
            <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">Services finden</router-link>
          </div>
          <div v-else class="dashboard-grid">
            <BookingCard v-for="booking in myBookings" :key="booking.id" :booking="booking" :show-controls="true" @review="openReviewModal" />
          </div>
        </div>
      </template>
    </main>

    <ReviewModal
      v-if="selectedBookingForReview"
      :is-open="showReviewModal"
      :job="selectedBookingForReview.service"
      @close="showReviewModal = false"
      @submit="handleCreateReview"
    />
  </div>
</template>

<style scoped>
.dashboard-container {
  padding-top: 48px;
  padding-bottom: 64px;
}

.dashboard-header h1 {
  margin-top: 0;
  margin-bottom: 32px;
  font-size: 2rem;
  font-weight: 800;
}

/* --- TABS --- */
.tabs-wrapper {
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 24px; /* Reduced margin */
}

.tab-nav {
  display: flex;
  gap: 32px;
}

.tab-button {
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-light);
  cursor: pointer;
  position: relative;
}

.tab-button:hover {
  color: var(--color-text);
}

.tab-button.active {
  color: var(--color-text);
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-text);
}

/* --- GRID --- */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  width: 100%;
}

/* --- EMPTY STATE --- */
.empty-state {
  text-align: center;
  padding: 64px 0;
  background-color: #f8f9fa;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 24px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state h2 {
  margin-top: 0;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--color-text-light);
  margin-bottom: 24px;
}

.primary-action {
  padding: 12px 24px;
  font-size: 1rem;
}
</style>

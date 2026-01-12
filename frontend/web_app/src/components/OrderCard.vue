<script setup>
/**
 * OrderCard.vue
 *
 * A card component representing an order (booking) from the contractor's perspective.
 * Displays order details, customer info, and provides actions to manage the order.
 */

// --- Imports ---
import { computed } from 'vue';
import { STATUS_TRANSLATIONS } from '@/constants';

// --- Props & Emits ---

/**
 * Props definition.
 * @property {Object} booking - The booking object containing order details.
 */
const props = defineProps({
  booking: { type: Object, required: true }
});

/**
 * Emits definition.
 * @emits mark-completed - Emitted when the contractor marks the order as completed.
 * @emits cancel - Emitted when the contractor cancels the order.
 */
const emit = defineEmits(['mark-completed', 'cancel']);

// --- Computed Properties ---

/**
 * Formats the price as currency (EUR).
 */
const formattedPrice = computed(() => {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(props.booking.price || 0);
});

/**
 * Formats the scheduled date.
 */
const formattedDate = computed(() => {
  if (!props.booking.scheduled_date) return 'Termin noch nicht festgelegt';
  return new Date(props.booking.scheduled_date).toLocaleDateString('de-DE', {
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric'
  });
});

/**
 * Formats the location display string.
 * Prioritizes full address, falls back to zip/city, or 'Ort unbekannt'.
 */
const locationDisplay = computed(() => {
  const s = props.booking.service;
  if (!s) return 'Keine Ortsangabe';
  if (s.address) return s.address;
  return `${s.zip_code || ''} ${s.city || ''}`.trim() || 'Ort unbekannt';
});

/**
 * Translates the booking status code to a human-readable string.
 */
const translatedStatus = computed(() => {
  const status = props.booking.status;
  return STATUS_TRANSLATIONS[status] || status;
});
</script>

<template>
  <div class="order-card">
    <div class="card-header">
      <div class="header-content">
        <h3 class="job-title" :title="booking.service.title">
          {{ booking.service.title }}
        </h3>
      </div>
      <div class="price-tag">{{ formattedPrice }}</div>
    </div>

    <div class="card-body">

      <div class="info-grid">
        <div class="info-block">
          <span class="label">Kunde</span>
          <div class="value customer-box" :title="booking.customer_name">
            👤 {{ booking.customer_name || 'Unbekannt' }}
          </div>
        </div>

        <div class="info-block">
          <span class="label">Einsatzort</span>
          <div class="value address-box" :title="locationDisplay">
            📍 {{ locationDisplay }}
          </div>
        </div>
      </div>

      <div class="info-block full-width">
        <span class="label">Termin</span>
        <div class="value date-highlight">
          📅 {{ formattedDate }}
        </div>
      </div>

    </div>

    <div class="card-footer-wrapper">
      <div class="card-actions" v-if="['PENDING', 'CONFIRMED'].includes(booking.status)">
        <button
          v-if="booking.status === 'CONFIRMED'"
          class="action-btn complete"
          @click.stop="$emit('mark-completed', booking.id)"
        >
          ✔ Erledigt
        </button>

        <button
          class="action-btn cancel"
          @click.stop="$emit('cancel', booking.id)"
        >
          ✕ Stornieren
        </button>
      </div>

      <div v-else class="status-footer" :class="booking.status.toLowerCase()">
        Status: {{ translatedStatus }}
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --- CARD BASE --- */
.order-card {
  background-color: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  height: 100%; /* Important for grid cells */
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

/* --- HEADER --- */
.card-header {
  background-color: #f8f9fa;
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.header-content {
  flex: 1;
  min-width: 0; /* Prevents flexbox overflow with long titles */
}

.job-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text);

  /* STABILITY: Reserves exact space for 2 lines */
  line-height: 1.3;
  height: 2.6em; /* 1.3 * 2 = 2.6em */

  /* Text truncation (...) */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.price-tag {
  background-color: var(--color-primary);
  color: white;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
}

/* --- BODY --- */
.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Pushes footer down */
  gap: 16px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-block {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--color-text-light);
  margin-bottom: 4px;
  font-weight: 600;
  letter-spacing: 0.5px;
  line-height: 1;
}

.value {
  font-size: 0.95rem;
  color: var(--color-text);
  font-weight: 500;
}

/* STABILITY: Customer always 1 line */
.customer-box {
  line-height: 1.4;
  height: 1.4em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* STABILITY: Address always 2 lines */
.address-box {
  line-height: 1.3;
  height: 2.6em; /* 1.3 * 2 = 2.6em */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.info-block.full-width {
  margin-top: auto; /* Pushes date block down if there is space above */
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.date-highlight {
  color: var(--color-primary);
  font-weight: 700;
  line-height: 1.4;
}

/* --- FOOTER --- */
.card-footer-wrapper {
  margin-top: auto; /* Pushes footer to bottom */
  border-top: 1px solid var(--color-border);
  min-height: 62px; /* Fixed min-height for consistency */
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-actions {
  padding: 12px 16px;
  background-color: #fff;
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  white-space: nowrap;
  transition: background 0.2s;
}

.action-btn.complete { background-color: var(--color-success); color: white; }
.action-btn.complete:hover { background-color: #218838; }

.action-btn.cancel { background-color: #fff0f0; color: var(--color-error); }
.action-btn.cancel:hover { background-color: #ffe0e0; }

.status-footer {
  width: 100%;
  text-align: center;
  padding: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  background-color: #eee;
  color: #666;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-footer.completed { background-color: #d4edda; color: #155724; }
.status-footer.cancelled { background-color: #f8d7da; color: #721c24; }
</style>
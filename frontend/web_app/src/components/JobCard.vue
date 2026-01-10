/* In frontend/web_app/src/components/JobCard.vue */

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  service: { type: Object, required: true },
  showControls: { type: Boolean, default: false }
});

const emit = defineEmits(['delete', 'edit', 'mark-completed', 'cancel', 'review']);
const router = useRouter();

const safeService = computed(() => props.service || {});

// --- BILDER QUELLEN (Aktualisierte, stabile Unsplash IDs) ---
const tradeImages = {
  // WICHTIG: Keys müssen mit den Backend-IDs (Jobs Model) übereinstimmen
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=500&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=500&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=500&q=80',
  // Neuer Link für Carpenter (Tischler), da der alte wohl kaputt war:
  CARPENTER: 'https://images.unsplash.com/photo-1601058268499-e52658b8bb88?auto=format&fit=crop&w=500&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=500&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=500&q=80'
};

// --- INTELLIGENTE BILD-ZUORDNUNG ---
const serviceImage = computed(() => {
  const rawTrade = safeService.value.trade;

  // 1. Debugging: Schau in die Browser-Konsole (F12), was wirklich ankommt!
  // console.log(`Job: ${safeService.value.title}, Trade Raw:`, rawTrade);

  if (!rawTrade) return tradeImages.OTHER;

  // 2. Normalisierung: Alles in Großbuchstaben und Leerzeichen weg
  const normalizedTrade = String(rawTrade).toUpperCase().trim();

  // 3. Direkter Treffer? (z.B. "CARPENTER")
  if (tradeImages[normalizedTrade]) {
    return tradeImages[normalizedTrade];
  }

  // 4. Fallback für deutsche Begriffe oder Mapping-Fehler
  // Falls das Backend "Tischler" statt "CARPENTER" schickt
  if (normalizedTrade.includes('TISCHLER') || normalizedTrade.includes('SCHREINER')) return tradeImages.CARPENTER;
  if (normalizedTrade.includes('MALER') || normalizedTrade.includes('LACKIERER')) return tradeImages.PAINTER;
  if (normalizedTrade.includes('ELEKTRIK')) return tradeImages.ELECTRICIAN;
  if (normalizedTrade.includes('SANITÄR') || normalizedTrade.includes('HEIZUNG') || normalizedTrade.includes('KLEMPNER')) return tradeImages.PLUMBER;
  if (normalizedTrade.includes('GARTEN')) return tradeImages.GARDENER;

  return tradeImages.OTHER;
});

const handleImageError = (e) => {
  // Wenn das Bild nicht lädt, wird es durch das 'OTHER' Bild ersetzt.
  // Wir prüfen, ob wir nicht schon beim Fallback sind, um Loops zu vermeiden.
  if (e.target.src !== tradeImages.OTHER) {
    console.warn(`Bild konnte nicht geladen werden für Trade: ${safeService.value.trade}. Lade Fallback.`);
    e.target.src = tradeImages.OTHER;
  }
};

// ... Rest der Logik (formattedPrice, formattedDate, navigation etc.) ...
const goToDetail = () => {
  if (safeService.value.id) {
    router.push({ name: 'ServiceDetail', params: { id: safeService.value.id } });
  }
};
const goToEdit = () => {
  if (safeService.value.id) {
    router.push({ name: 'ServiceEdit', params: { id: safeService.value.id } });
  }
};

const formattedPrice = computed(() => {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' })
    .format(safeService.value.price || 0);
});

const formattedDate = computed(() => {
  if (!safeService.value.execution_date) return 'Termin flexibel';
  return new Date(safeService.value.execution_date).toLocaleDateString('de-DE', { day: 'numeric', month: 'short' });
});

const displayTitle = computed(() => {
    const title = safeService.value.title || 'Angebot';
    const city = safeService.value.city || '';
    return city ? `${title} in ${city}` : title;
});



</script>

<template>
  <div v-if="service && service.id" class="job-card">
    <div class="image-container" @click="goToDetail">
      <img
        :src="serviceImage"
        :alt="service.title"
        class="job-image"
        @error="handleImageError"
      />
      <div v-if="showControls && service.status" class="status-badge" :class="`status-${service.status.toLowerCase()}`">
        {{ service.status }}
      </div>
    </div>

    <div class="info-container" @click="goToDetail">
      <span class="title">{{ displayTitle }}</span>

      <span class="contractor-info">
        Auftrag von {{ service.contractor_username || 'Unbekannt' }}
      </span>

      <span class="price">{{ formattedPrice }}</span>
    </div>

    <div v-if="showControls" class="card-footer-actions" @click.stop>
        <div v-if="service.status === 'OPEN'" class="action-group">
        <button class="action-btn edit" @click="goToEdit">Bearbeiten</button>
        <button class="action-btn delete" @click="$emit('delete', service.id)">
    Löschen </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Deine Styles bleiben unverändert */
.job-card { cursor: pointer; display: flex; flex-direction: column; background-color: white; border-radius: 16px; overflow: hidden; border: 1px solid transparent; transition: box-shadow 0.2s; position: relative;
  z-index: 0;}
.job-card:has(.card-footer-actions) { border-color: var(--color-border); }
.job-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.image-container { position: relative; aspect-ratio: 1 / 1; border-radius: 16px; overflow: hidden; background-color: #f0f0f0; }
.job-image { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.job-card:hover .job-image { transform: scale(1.05); }
.status-badge { position: absolute; top: 12px; left: 12px; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; color: white; text-transform: uppercase; z-index: 2; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.status-open { background-color: var(--color-success); }
.status-booked { background-color: var(--color-primary); }
.status-completed { background-color: #717171; }
.status-cancelled { background-color: var(--color-error); }
.info-container { display: flex; flex-direction: column; gap: 2px; padding: 12px 4px; }
.title { font-weight: 600; color: var(--color-text); font-size: 1rem; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.price { font-weight: 400; }
.card-footer-actions { padding: 12px; border-top: 1px solid var(--color-border); background-color: #fcfcfc; }
.action-group { display: flex; gap: 8px; }
.action-btn { flex: 1; padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: all 0.2s; }
.action-btn.edit { background-color: white; border-color: var(--color-border); color: var(--color-text); }
.action-btn.edit:hover { background-color: #f0f0f0; }
.action-btn.cancel { background-color: transparent; color: var(--color-error); border-color: transparent; }
.action-btn.cancel:hover { background-color: #fff0f0; }
.action-btn.complete { background-color: var(--color-success); color: white; width: 100%; }
.action-btn.complete:hover { background-color: #218838; }
.action-btn.review { width: 100%; background-color: var(--color-secondary); color: white; }
.review-display { padding: 8px; text-align: center; }
.action-group.disabled { justify-content: center; color: var(--color-text-light); font-size: 0.85rem; font-style: italic; }
</style>

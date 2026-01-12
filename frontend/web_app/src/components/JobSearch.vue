<script setup>
/**
 * JobSearch.vue
 *
 * Component for searching jobs with filters for trade, location, and radius.
 * Supports both routing-based search and event-based search.
 */

// --- Imports ---
import { ref, onMounted, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useToastStore } from '@/stores/toast';

// --- Props & Emits ---

/**
 * Props definition.
 * @property {boolean} enableRouting - Whether to push to router on search or emit event.
 */
const props = defineProps({
  enableRouting: { type: Boolean, default: true }
});

/**
 * Emits definition.
 * @emits search-triggered - Emitted when search is executed and routing is disabled.
 */
const emit = defineEmits(['search-triggered']);

// --- Reactive State ---

const router = useRouter();
const route = useRoute();
const toastStore = useToastStore();

/** @type {import('vue').Ref<string>} Search term input */
const searchTerm = ref('');

/** @type {import('vue').Ref<string>} Location input */
const location = ref('');

/** @type {import('vue').Ref<number>} Search radius in km */
const searchRadius = ref(20); // Standard: 20km

/** @type {import('vue').Ref<string|null>} Currently active input field */
const activeField = ref(null); // 'search', 'location', or 'radius'

/** @type {import('vue').Ref<boolean>} Geolocation loading state */
const isLocating = ref(false);

// --- Data ---

/** Categories available for search suggestions */
const categories = [
  { id: 'PAINTER', title: 'Maler & Lackierer', desc: 'Wände & Fassaden', icon: '🎨' },
  { id: 'ELECTRICIAN', title: 'Elektriker', desc: 'Installation & Reparatur', icon: '⚡' },
  { id: 'PLUMBER', title: 'Sanitär & Heizung', desc: 'Bad & Wasser', icon: '💧' },
  { id: 'CARPENTER', title: 'Tischler', desc: 'Möbel & Holz', icon: '🪚' }
];

/** Location suggestions */
const locations = [
  { id: 'current', title: 'Standort verwenden', desc: 'GPS nutzen', icon: '📍', isAction: true },
  { id: 'berlin', title: 'Berlin', desc: 'Region', icon: '🏙️' },
  { id: 'hamburg', title: 'Hamburg', desc: 'Region', icon: '⚓' },
  { id: 'munich', title: 'München', desc: 'Region', icon: '🥨' }
];

// --- Watchers ---

/**
 * Watch for route query changes to update local state.
 */
watch(() => route.query, (newQuery) => {
  if (newQuery.search !== undefined) searchTerm.value = newQuery.search;
  if (newQuery.city !== undefined) location.value = newQuery.city;
  if (newQuery.radius) searchRadius.value = parseInt(newQuery.radius);
});

// --- Lifecycle Hooks ---

/**
 * Initialize state from URL query parameters on mount.
 */
onMounted(() => {
  if (route.query.search) searchTerm.value = route.query.search;
  if (route.query.city) location.value = route.query.city;
  if (route.query.radius) searchRadius.value = parseInt(route.query.radius);

  if (!searchTerm.value && route.query.trade) {
    const cat = categories.find(c => c.id === route.query.trade);
    if (cat) searchTerm.value = cat.title;
  }
});

// --- Methods ---

/**
 * Executes the search logic.
 * @param {Object} payloadOverride - Optional parameters to override base search params.
 */
const executeSearch = (payloadOverride = {}) => {
  // 1. Take current values from input fields as base
  const baseParams = {
    search: searchTerm.value,
    city: location.value,
    radius: searchRadius.value // Radius is always included
  };

  // 2. Override with potential parameters (e.g. Trade when clicking an icon)
  // Important: payloadOverride comes AFTER baseParams
  const finalParams = {
    ...baseParams,
    ...payloadOverride
  };

  // 3. Remove empty values (Cleanup)
  Object.keys(finalParams).forEach(key => {
    if (finalParams[key] === undefined || finalParams[key] === '' || finalParams[key] === null) {
      delete finalParams[key];
    }
  });

  // 4. Trigger routing or emit event
  if (props.enableRouting) {
    router.push({
      name: 'JobMarketplace',
      query: finalParams
    });
  } else {
    emit('search-triggered', finalParams);
  }

  activeField.value = null;
};

/**
 * Handles the search form submission.
 */
const handleSearch = () => {
  executeSearch();
};

/**
 * Sets the active field on focus.
 * @param {string} field - The field identifier.
 */
const onFocus = (field) => {
  activeField.value = field;
};

/**
 * Handles blur event with delay to allow dropdown interaction.
 */
const onBlur = () => {
  setTimeout(() => {
    activeField.value = null;
  }, 200);
};

/**
 * Selects a category and triggers search.
 * @param {Object} category - The selected category.
 */
const selectCategory = (category) => {
  searchTerm.value = category.title;
  // Search directly with the trade filter
  executeSearch({ trade: category.id, search: '' });
};

/**
 * Detects current user location using Geolocation API.
 */
const detectLocation = () => {
  if (!navigator.geolocation) {
    toastStore.addToast("Geolokalisierung wird von deinem Browser nicht unterstützt.", "error");
    return;
  }

  isLocating.value = true;
  location.value = "Standort wird ermittelt...";

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      isLocating.value = false;
      location.value = "Mein Standort";
      
      // Execute search directly with coordinates
      executeSearch({
        lat: latitude,
        lng: longitude
      });
    },
    (error) => {
      console.error("Geolocation error:", error);
      toastStore.addToast("Standort konnte nicht ermittelt werden.", "error");
      isLocating.value = false;
      location.value = "";
    }
  );
};

/**
 * Selects a location from suggestions.
 * @param {Object} loc - The selected location.
 */
const selectLocation = (loc) => {
  if (loc.isAction) {
    detectLocation();
  } else {
    location.value = loc.title;
    // After location selection, optionally jump to radius or close
    activeField.value = 'radius';
  }
};
</script>

<template>
  <div class="search-container-wrapper">
    <div class="search-bar-container" :class="{ 'active': activeField !== null }">
      <form @submit.prevent="handleSearch" class="search-bar">

        <div class="search-input-group flex-grow-2" :class="{ 'focused': activeField === 'search' }">
          <label for="search">Was suchst du?</label>
          <input
            id="search"
            v-model="searchTerm"
            type="text"
            placeholder="Maler, Elektriker..."
            autocomplete="off"
            @focus="onFocus('search')"
            @blur="onBlur"
          />
        </div>

        <div class="divider"></div>

        <div class="search-input-group flex-grow-1" :class="{ 'focused': activeField === 'location' }">
          <label for="location">Wo?</label>
          <input
            id="location"
            v-model="location"
            type="text"
            placeholder="Stadt oder PLZ"
            autocomplete="off"
            @focus="onFocus('location')"
            @blur="onBlur"
            :disabled="isLocating"
          />
        </div>

        <div class="divider"></div>

        <div
          class="search-input-group flex-grow-0 radius-group"
          :class="{ 'focused': activeField === 'radius' }"
          @click="onFocus('radius')"
        >
          <label>Umkreis</label>
          <div class="radius-display-value">
            {{ searchRadius }} km
          </div>
          <input
            class="hidden-input"
            @focus="onFocus('radius')"
            @blur="onBlur"
            readonly
          />
        </div>

        <div class="button-wrapper">
          <button type="submit" class="search-button">
            <span class="search-icon">
              <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" style="display: block; fill: none; height: 16px; width: 16px; stroke: currentcolor; stroke-width: 4; overflow: visible;"><g fill="none"><path d="m13 24c6.0751322 0 11-4.9248678 11-11 0-6.07513225-4.9248678-11-11-11-6.07513225 0-11 4.92486775-11 11 0 6.0751322 4.92486775 11 11 11zm8-3 9 9"></path></g></svg>
            </span>
          </button>
        </div>

      </form>
    </div>

    <div v-if="activeField === 'search'" class="suggestion-dropdown">
      <div class="suggestion-header">Beliebte Gewerke</div>
      <div v-for="cat in categories" :key="cat.id" class="suggestion-item" @mousedown.prevent="selectCategory(cat)">
        <div class="icon-box"><span class="icon">{{ cat.icon }}</span></div>
        <div class="text-group">
          <span class="item-title">{{ cat.title }}</span>
          <span class="item-desc">{{ cat.desc }}</span>
        </div>
      </div>
    </div>

    <div v-if="activeField === 'location'" class="suggestion-dropdown">
      <div class="suggestion-header">Vorschläge</div>
      <div v-for="loc in locations" :key="loc.id" class="suggestion-item" @mousedown.prevent="selectLocation(loc)">
        <div class="icon-box"><span class="icon">{{ loc.icon }}</span></div>
        <div class="text-group">
          <span class="item-title">{{ loc.title }}</span>
          <span class="item-desc">{{ loc.desc }}</span>
        </div>
      </div>
    </div>

    <div v-if="activeField === 'radius'" class="suggestion-dropdown radius-dropdown">
      <div class="radius-content" @mousedown.prevent>
        <div class="suggestion-header">Suchradius festlegen</div>
        <div class="radius-control">
            <span class="val-label">{{ searchRadius }} km</span>
            <input
              type="range"
              v-model.number="searchRadius"
              min="5"
              max="200"
              step="5"
              class="range-slider"
            />
        </div>
        <div class="radius-presets">
            <button @click="searchRadius=10" :class="{active: searchRadius===10}">10km</button>
            <button @click="searchRadius=20" :class="{active: searchRadius===20}">20km</button>
            <button @click="searchRadius=50" :class="{active: searchRadius===50}">50km</button>
            <button @click="searchRadius=100" :class="{active: searchRadius===100}">100km</button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.search-container-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 850px;
}

.search-bar-container {
  background: white;
  border-radius: 40px;
  box-shadow: 0 3px 12px 0 rgba(0,0,0,0.1), 0 1px 2px 0 rgba(0,0,0,0.08);
  border: 1px solid #dddddd;
  width: 100%;
  transition: background-color 0.2s ease;
}
.search-bar-container.active { background-color: #ebebeb; }

.search-bar {
  display: flex;
  align-items: center;
  height: 66px;
  position: relative;
  border-radius: 40px;
}

/* Flex-Verteilung der Felder */
.search-input-group {
  height: 100%;
  padding: 14px 24px;
  position: relative;
  cursor: pointer;
  border-radius: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.search-input-group:hover { background-color: rgba(0,0,0,0.05); }
.search-input-group.focused {
  background-color: white !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  z-index: 10;
}

.flex-grow-2 { flex: 2; } /* Suche bekommt am meisten Platz */
.flex-grow-1 { flex: 1.5; } /* Ort */
.flex-grow-0 { flex: 0.8; min-width: 120px; } /* Radius ist kompakt */

.search-input-group label {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  color: var(--color-text);
  margin-bottom: 2px;
  text-align: left;
}

.search-input-group input {
  border: none !important;
  background: transparent !important;
  padding: 0;
  margin: 0;
  font-size: 0.95rem;
  color: #222;
  font-weight: 500;
  width: 100%;
  text-overflow: ellipsis;
}
.search-input-group input:focus { outline: none; box-shadow: none; }

.radius-display-value {
  font-size: 0.95rem;
  font-weight: 500;
  color: #222;
  text-align: left;
  white-space: nowrap;
}
.hidden-input {
  position: absolute;
  opacity: 0;
  top: 0; left: 0; width: 100%; height: 100%;
  cursor: pointer;
}

.divider {
  width: 1px;
  height: 32px;
  background-color: #dddddd;
  flex-shrink: 0;
}

.button-wrapper { padding: 8px; padding-left: 0; z-index: 11; }

.search-button {
  background: linear-gradient(to right, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.1s ease, filter 0.2s ease;
  margin-right: 8px;
}
.search-button:hover { filter: brightness(1.1); transform: scale(1.05); }
.search-button:active { transform: scale(0.95); }

/* --- DROPDOWNS --- */
.suggestion-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  margin-top: 12px;
  background: white;
  border-radius: 32px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  padding: 24px 0;
  z-index: 2000;
  text-align: left;
}
.suggestion-header {
  padding: 0 32px 12px 32px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-text-light);
  text-transform: uppercase;
}
.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 32px;
  cursor: pointer;
  gap: 16px;
}
.suggestion-item:hover { background-color: #f7f7f7; }
.icon-box {
  width: 48px; height: 48px; background-color: #f1f1f1; border-radius: 12px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.icon { font-size: 1.5rem; }
.text-group { display: flex; flex-direction: column; }
.item-title { font-weight: 600; font-size: 1rem; }
.item-desc { font-size: 0.85rem; color: var(--color-text-light); }

/* --- RADIUS STYLES --- */
.radius-content { padding: 0 32px; }
.radius-control {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 24px;
}
.val-label {
    font-size: 2rem;
    font-weight: 700;
    color: var(--color-primary);
    margin-bottom: 12px;
}
.range-slider {
    width: 100%;
    height: 6px;
    background: #ddd;
    border-radius: 5px;
    outline: none;
    accent-color: var(--color-primary);
}
.radius-presets {
    display: flex;
    justify-content: space-between;
    gap: 8px;
}
.radius-presets button {
    flex: 1;
    padding: 8px;
    border: 1px solid var(--color-border);
    background: white;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s;
}
.radius-presets button:hover { border-color: var(--color-text); }
.radius-presets button.active {
    background-color: var(--color-text);
    color: white;
    border-color: var(--color-text);
}

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
  .search-bar { flex-direction: column; height: auto; padding: 12px; gap: 8px; }
  .search-input-group { width: 100%; padding: 12px 20px; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); background-color: white; }
  .divider { display: none; }
  .button-wrapper { width: 100%; margin-top: 4px; }
  .search-button { width: 100%; border-radius: 12px; margin: 0; }
  .suggestion-dropdown { position: fixed; top: 80px; height: calc(100vh - 80px); overflow-y: auto; border-radius: 20px 20px 0 0; }
}
</style>
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  enableRouting: {
    type: Boolean,
    default: true
  }
});

// Event definieren, um Filter an HomeView zu senden
const emit = defineEmits(['search-triggered']);

const router = useRouter();
const searchTerm = ref('');
const location = ref('');
const activeField = ref(null);

// --- DATA: Smart Suggestions ---
const categories = [
  {
    id: 'PAINTER',
    title: 'Maler & Lackierer',
    desc: 'Für Wände, Fassaden & Lackierarbeiten',
    icon: '🎨'
  },
  {
    id: 'ELECTRICIAN',
    title: 'Elektriker',
    desc: 'Für Installationen, Reparaturen & Smart Home',
    icon: '⚡'
  },
  {
    id: 'PLUMBER',
    title: 'Sanitär & Heizung',
    desc: 'Rohrreinigung, Bad-Sanierung & Heizungswartung',
    icon: '💧'
  },
  {
    id: 'CARPENTER',
    title: 'Tischler',
    desc: 'Möbelbau, Fenster & Türen',
    icon: '🪚'
  }
];

const locations = [
  {
    id: 'current',
    title: 'Standort verwenden',
    desc: 'Aufträge in deiner direkten Umgebung finden',
    icon: '📍',
    isAction: true
  },
  {
    id: 'berlin',
    title: 'Berlin',
    desc: 'Beliebte Region',
    icon: '🏙️'
  },
  {
    id: 'hamburg',
    title: 'Hamburg',
    desc: 'Beliebte Region',
    icon: '⚓'
  },
  {
    id: 'munich',
    title: 'München',
    desc: 'Beliebte Region',
    icon: '🥨'
  }
];

// --- ACTIONS ---

const executeSearch = (payload) => {
  // Payload enthält z.B. { search: '...', city: '...', trade: '...' }

  if (props.enableRouting) {
    // Standardverhalten: Weiterleitung zum Marktplatz
    router.push({
      name: 'JobMarketplace',
      query: payload
    });
  } else {
    // Inline Verhalten: Event an Parent senden (z.B. HomeView)
    emit('search-triggered', payload);
  }

  activeField.value = null; // Dropdown schließen
};

const handleSearch = () => {
  activeField.value = null; // Close dropdown
  router.push({
    name: 'JobMarketplace',
    query: {
      search: searchTerm.value,
      city: location.value
    }
  });
};

const onFocus = (field) => {
  activeField.value = field;
};

const onBlur = () => {
  setTimeout(() => {
    activeField.value = null;
  }, 200);
};

const selectCategory = (category) => {
  // Wenn eine Kategorie geklickt wird
  // Optional: Den Text ins Feld setzen, damit der User sieht was passiert
  searchTerm.value = category.title;

  // WICHTIG: Wir senden die ID (z.B. PAINTER) als 'trade' Filter
  executeSearch({
    trade: category.id,
    search: '' // Wenn man Kategorie wählt, leeren wir oft die Textsuche oder kombinieren sie
  });
};

const selectLocation = (loc) => {
  if (loc.isAction) {
    location.value = "Mein Standort";
  } else {
    location.value = loc.title;
  }
  activeField.value = null;
};
</script>

<template>
  <div class="search-container-wrapper">
    <!-- Main Search Bar -->
    <div class="search-bar-container" :class="{ 'active': activeField !== null }">
      <form @submit.prevent="handleSearch" class="search-bar">

        <!-- Input Group 1: Search Term -->
        <div
          class="search-input-group"
          :class="{ 'focused': activeField === 'search' }"
        >
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

        <div class="divider" v-show="activeField === null"></div>

        <!-- Input Group 2: Location -->
        <div
          class="search-input-group"
          :class="{ 'focused': activeField === 'location' }"
        >
          <label for="location">Wo?</label>
          <input
            id="location"
            v-model="location"
            type="text"
            placeholder="Stadt oder PLZ"
            autocomplete="off"
            @focus="onFocus('location')"
            @blur="onBlur"
          />
        </div>

        <!-- Search Button -->
        <div class="button-wrapper">
          <button type="submit" class="search-button">
            <span class="search-icon">
              <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="presentation" focusable="false" style="display: block; fill: none; height: 16px; width: 16px; stroke: currentcolor; stroke-width: 4; overflow: visible;"><g fill="none"><path d="m13 24c6.0751322 0 11-4.9248678 11-11 0-6.07513225-4.9248678-11-11-11-6.07513225 0-11 4.92486775-11 11 0 6.0751322 4.92486775 11 11 11zm8-3 9 9"></path></g></svg>
            </span>
            <span class="search-text">Suchen</span>
          </button>
        </div>

      </form>
    </div>

    <!-- SMART SUGGESTION DROPDOWN -->
    <div v-if="activeField === 'search'" class="suggestion-dropdown">
      <div class="suggestion-header">Beliebte Gewerke</div>
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="suggestion-item"
        @mousedown.prevent="selectCategory(cat)"
      >
        <div class="icon-box">
          <span class="icon">{{ cat.icon }}</span>
        </div>
        <div class="text-group">
          <span class="item-title">{{ cat.title }}</span>
          <span class="item-desc">{{ cat.desc }}</span>
        </div>
      </div>
    </div>

    <div v-if="activeField === 'location'" class="suggestion-dropdown">
      <div class="suggestion-header">Vorschläge für dich</div>
      <div
        v-for="loc in locations"
        :key="loc.id"
        class="suggestion-item"
        @mousedown.prevent="selectLocation(loc)"
      >
        <div class="icon-box">
          <span class="icon">{{ loc.icon }}</span>
        </div>
        <div class="text-group">
          <span class="item-title">{{ loc.title }}</span>
          <span class="item-desc">{{ loc.desc }}</span>
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

/* --- MAIN SEARCH BAR --- */
.search-bar-container {
  background: white;
  border-radius: 40px;
  box-shadow: 0 3px 12px 0 rgba(0,0,0,0.1), 0 1px 2px 0 rgba(0,0,0,0.08);
  border: 1px solid #dddddd;
  width: 100%;
  transition: background-color 0.2s ease;
  background-color: white;
}

.search-bar-container.active {
  background-color: #ebebeb;
}

.search-bar {
  display: flex;
  align-items: center;
  height: 66px;
  position: relative;
  border-radius: 40px;
}

.search-input-group {
  flex: 1;
  padding: 14px 32px;
  position: relative;
  cursor: text;
  border-radius: 40px;
  border: none;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

.search-input-group:hover {
  background-color: #ebebeb;
}

.search-input-group.focused {
  background-color: white !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
  z-index: 10;
}

.search-input-group label {
  display: block;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  margin-bottom: 4px;
  color: var(--color-text);
  pointer-events: none;
  text-align: left; /* Ensure label is left-aligned */
}

.search-input-group input {
  border: none !important;
  outline: none !important;
  background: transparent !important;
  box-shadow: none !important;
  padding: 0;
  margin: 0;
  font-size: 0.95rem;
  width: 100%;
  color: #222;
  font-weight: 500;
  text-overflow: ellipsis;
  text-align: left; /* Ensure input text is left-aligned */
}

.search-input-group input::placeholder {
  color: #717171;
  font-weight: 400;
}

.divider {
  width: 1px;
  height: 32px;
  background-color: #dddddd;
  flex-shrink: 0;
}

.button-wrapper {
  padding: 8px;
  padding-left: 0;
  z-index: 11;
}

.search-button {
  background: linear-gradient(to right, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
  border: none;
  border-radius: 24px;
  height: 48px;
  padding: 0 16px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.1s ease, filter 0.2s ease;
  margin-right: 8px;
}

.search-button:hover {
  filter: brightness(1.1);
}

.search-button:active {
  transform: scale(0.96);
}

/* --- SMART SUGGESTION DROPDOWN --- */
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
  z-index: 20;
  animation: fadeIn 0.2s ease-out;
  text-align: left; /* CRITICAL: Ensure all text in dropdown is left-aligned */
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.suggestion-header {
  padding: 0 32px 12px 32px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-text-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: left; /* Explicitly left-align header */
}

.suggestion-item {
  display: flex;
  align-items: center; /* Vertically center icon and text block */
  padding: 12px 32px;
  cursor: pointer;
  transition: background-color 0.1s ease;
  gap: 16px; /* CRITICAL: Use gap instead of margin for consistent spacing */
}

.suggestion-item:hover {
  background-color: #f7f7f7;
}

.icon-box {
  width: 48px;
  height: 48px;
  background-color: #f1f1f1;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  /* Removed margin-right, handled by gap in parent */
}

.icon {
  font-size: 1.5rem;
}

.text-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* CRITICAL: Align text items to the start (left) */
  justify-content: center; /* Center text block vertically relative to icon */
}

.item-title {
  font-weight: 600;
  color: var(--color-text);
  font-size: 1rem;
  margin-bottom: 2px;
  text-align: left; /* Explicitly left-align title */
}

.item-desc {
  font-size: 0.85rem;
  color: var(--color-text-light);
  text-align: left; /* Explicitly left-align description */
}

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
  .search-bar-container {
    border-radius: 24px;
    background: transparent;
    box-shadow: none;
    border: none;
  }
  .search-bar-container.active {
    background-color: transparent;
  }
  .search-bar {
    flex-direction: column;
    height: auto;
    gap: 12px;
  }
  .search-input-group {
    width: 100%;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 16px 24px;
  }
  .search-input-group.focused {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  .divider { display: none; }
  .button-wrapper { width: 100%; padding: 0; }
  .search-button { width: 100%; border-radius: 12px; justify-content: center; height: 56px; margin-right: 0; }

  .suggestion-dropdown {
    position: fixed;
    top: 80px;
    left: 0;
    right: 0;
    border-radius: 24px 24px 0 0;
    margin-top: 0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    height: calc(100vh - 80px);
    overflow-y: auto;
  }
}
</style>

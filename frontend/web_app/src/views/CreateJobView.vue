<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const router = useRouter();
const isLoading = ref(false);
const errorMessage = ref('');

// --- Wizard State ---
const currentStep = ref(1);
const totalSteps = 4;

// --- Form Data ---
const jobData = ref({
  trade: '',
  title: '',
  description: '',
  adress: '',
  zip_code: '',
  city: '',
  price: null,
});

// --- Options ---
const tradeOptions = [
  { value: 'PLUMBER', text: 'Sanitär & Heizung', icon: '💧' },
  { value: 'ELECTRICIAN', text: 'Elektrik', icon: '⚡' },
  { value: 'PAINTER', text: 'Maler & Lackierer', icon: '🎨' },
  { value: 'CARPENTER', text: 'Tischler & Schreiner', icon: '🪚' },
  { value: 'GARDENER', text: 'Garten & Landschaft', icon: '🌳' },
  { value: 'OTHER', text: 'Sonstiges', icon: '🔧' },
];

// --- Computed Properties ---
const progressPercentage = computed(() => {
  return (currentStep.value / totalSteps) * 100;
});

const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 1: // Trade
      return !!jobData.value.trade;
    case 2: // Details
      return jobData.value.title.length > 5 && jobData.value.description.length > 10;
    case 3: // Location
      return jobData.value.zip_code.length >= 4 && !!jobData.value.city;
    case 4: // Price
      return true;
    default:
      return false;
  }
});

// --- Actions ---
const nextStep = () => {
  if (isStepValid.value && currentStep.value < totalSteps) {
    currentStep.value++;
  } else if (currentStep.value === totalSteps) {
    handleSubmit();
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const selectTrade = (tradeValue) => {
  jobData.value.trade = tradeValue;
};

const handleSubmit = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    await api.createJob(jobData.value);
    router.push({ name: 'JobMarketplace' });
  } catch (error) {
    if (error.response && error.response.data) {
      errorMessage.value = 'Ein Fehler ist aufgetreten. Bitte überprüfe deine Eingaben.';
    } else {
      errorMessage.value = 'Verbindungsproblem.';
    }
    console.error('Job creation failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="wizard-container">

    <div class="progress-bar-container">
      <div class="progress-bar-fill" :style="{ width: progressPercentage + '%' }"></div>
    </div>

    <div class="wizard-content">

      <header class="step-header">
        <span class="step-indicator">Schritt {{ currentStep }} von {{ totalSteps }}</span>
        <h1 v-if="currentStep === 1">Welche Leistung bietest du an?</h1>
        <h1 v-if="currentStep === 2">Beschreibe dein Angebot</h1>
        <h1 v-if="currentStep === 3">Wo bietest du die Leistung an?</h1>
        <h1 v-if="currentStep === 4">Lege deinen Preis fest</h1>
      </header>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <!-- STEP 1: Category Selection -->
      <div v-if="currentStep === 1" class="step-body">
        <div class="trade-grid">
          <div
            v-for="option in tradeOptions"
            :key="option.value"
            class="trade-card"
            :class="{ 'selected': jobData.trade === option.value }"
            @click="selectTrade(option.value)"
          >
            <div class="trade-icon">{{ option.icon }}</div>
            <div class="trade-label">{{ option.text }}</div>
          </div>
        </div>
      </div>

      <!-- STEP 2: Details -->
      <div v-if="currentStep === 2" class="step-body">
        <div class="form-group">
          <label for="title">Titel deines Angebots</label>
          <input
            id="title"
            v-model="jobData.title"
            type="text"
            placeholder="z.B. Professionelle Malerarbeiten"
            autofocus
          />
        </div>
        <div class="form-group">
          <label for="description">Beschreibung</label>
          <textarea
            id="description"
            v-model="jobData.description"
            rows="6"
            placeholder="Beschreibe, was dein Angebot beinhaltet, welche Materialien du verwendest etc."
          ></textarea>
        </div>
      </div>

      <!-- STEP 3: Location -->
      <div v-if="currentStep === 3" class="step-body">
        <div class="form-group">
        <label for="address">Straße & Hausnummer (Optional)</label>
        <input
          id="address"
          v-model="jobData.address"
          type="text"
          placeholder="Für genauere Standortbestimmung auf der Karte"
        />
      </div>
        <div class="form-group">
          <label for="zip">Postleitzahl</label>
          <input
            id="zip"
            v-model="jobData.zip_code"
            type="text"
            placeholder="Dein Einsatzgebiet"
          />
        </div>
        <div class="form-group">
          <label for="city">Stadt</label>
          <input
            id="city"
            v-model="jobData.city"
            type="text"
            placeholder="z.B. Musterstadt"
          />
        </div>
      </div>

      <!-- STEP 4: Budget -->
      <div v-if="currentStep === 4" class="step-body">
        <div class="form-group">
          <label for="price">Dein Preis für dieses Angebot</label>
          <div class="price-input-wrapper">
            <input
              id="price"
              v-model="jobData.price"
              type="number"
              step="0.01"
              placeholder="0.00"
            />
            <span class="currency-symbol">€</span>
          </div>
          <p class="hint">Du kannst einen Festpreis oder einen Stundensatz angeben.</p>
        </div>
      </div>

    </div>

    <footer class="wizard-footer">
      <div class="footer-content container">
        <button
          v-if="currentStep > 1"
          @click="prevStep"
          class="back-btn"
        >
          Zurück
        </button>
        <div v-else></div> <!-- Spacer -->

        <button
          @click="nextStep"
          class="base-button next-btn"
          :disabled="!isStepValid || isLoading"
        >
          {{ currentStep === totalSteps ? (isLoading ? 'Veröffentliche...' : 'Angebot veröffentlichen') : 'Weiter' }}
        </button>
      </div>
    </footer>

  </div>
</template>

<style scoped>
/* Styles remain the same */
.wizard-container {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 80px);
  background-color: white;
}
.progress-bar-container {
  height: 4px;
  background-color: #f0f0f0;
  width: 100%;
}
.progress-bar-fill {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}
.wizard-content {
  flex-grow: 1;
  max-width: 600px;
  width: 100%;
  margin: 0 auto;
  padding: 40px 24px 100px;
}
.step-header {
  margin-bottom: 32px;
}
.step-indicator {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-light);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.step-header h1 {
  font-size: 2rem;
  margin-top: 8px;
  color: var(--color-text);
}
.trade-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}
.trade-card {
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.trade-card:hover {
  border-color: var(--color-text-light);
}
.trade-card.selected {
  border-color: var(--color-primary);
  background-color: #f0f4ff;
  box-shadow: 0 0 0 1px var(--color-primary);
}
.trade-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
}
.trade-label {
  font-weight: 600;
  font-size: 0.95rem;
}
.form-group {
  margin-bottom: 24px;
}
.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-text);
}
input, textarea {
  width: 100%;
  padding: 16px;
  font-size: 1.1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  transition: border-color 0.2s;
}
input:focus, textarea:focus {
  border-color: var(--color-text);
  outline: none;
}
.price-input-wrapper {
  position: relative;
}
.currency-symbol {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-weight: 600;
  color: var(--color-text-light);
}
.hint {
  font-size: 0.9rem;
  color: var(--color-text-light);
  margin-top: 8px;
}
.wizard-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: white;
  border-top: 1px solid var(--color-border);
  padding: 16px 0;
  z-index: 10;
}
.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.back-btn {
  background: none;
  border: none;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
  font-size: 1rem;
  color: var(--color-text);
}
.next-btn {
  padding: 14px 32px;
  font-size: 1rem;
}
.next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.error-message {
  background-color: #fff0f0;
  color: var(--color-error);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: center;
}
</style>

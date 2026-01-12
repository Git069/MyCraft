<script setup>
import {
  ref, onMounted, onUnmounted, computed, nextTick, watch,
} from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import { useChatStore } from '@/stores/chatStore';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';
import MessageOffer from '@/components/MessageOffer.vue';
import ReviewModal from '@/components/ReviewModal.vue';
import UserAvatar from '@/components/UserAvatar.vue';
import api from '@/api';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const route = useRoute();
const chatStore = useChatStore();
const authStore = useAuthStore();
const toastStore = useToastStore();

const newMessage = ref('');
const messageContainer = ref(null);
const showOfferModal = ref(false);
const offerData = ref({ price: null, description: '' });
const showReviewModal = ref(false);
const selectedJobForReview = ref(null);
const loadingSuggestion = ref(false);

/* ==========================================================================
   Computed Properties
   ========================================================================== */

/**
 * Retrieves the currently logged-in user from the store.
 * @returns {Object|null} The user object.
 */
const currentUser = computed(() => authStore.currentUser);

/**
 * Checks if the current user is a craftsman.
 * @returns {boolean} True if the user is a craftsman.
 */
const isCraftsman = computed(() => authStore.isCraftsman);

/**
 * Retrieves the latest offer from the active conversation.
 * @returns {Object|null} The latest offer object or null.
 */
const latestOffer = computed(() => {
  if (!chatStore.activeConversation) return null;
  const offers = chatStore.activeConversation.messages.map((m) => m.offer).filter(Boolean);
  return offers.length > 0 ? offers[offers.length - 1] : null;
});

/**
 * Finds the last message sent by the other participant in the conversation.
 * Used for generating AI reply suggestions.
 * @returns {string|null} The content of the last message or null.
 */
const lastPartnerMessage = computed(() => {
  if (!chatStore.activeConversation?.messages) return null;
  const msgs = chatStore.activeConversation.messages;

  // Iterate backwards to find the last message from the partner
  for (let i = msgs.length - 1; i >= 0; i--) {
    if (msgs[i].sender !== currentUser.value?.id && msgs[i].content) {
      return msgs[i].content;
    }
  }
  return null;
});

/* ==========================================================================
   Watchers
   ========================================================================== */

/**
 * Scrolls to the bottom of the chat window when new messages arrive.
 */
watch(() => chatStore.activeConversation?.messages, () => {
  scrollToBottom();
}, { deep: true });

/* ==========================================================================
   Lifecycle Hooks
   ========================================================================== */

/**
 * Initializes the chat view by fetching conversations and selecting the active one if provided in the URL.
 */
onMounted(async () => {
  const activeConvoId = parseInt(route.query.active_convo, 10);
  await chatStore.fetchConversations(activeConvoId);
  scrollToBottom();
});

/**
 * Stops polling for new messages when the component is unmounted.
 */
onUnmounted(() => {
  chatStore.stopPolling();
});

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Generates an AI-suggested reply based on the last message from the partner.
 */
const handleSuggestReply = async () => {
  if (!lastPartnerMessage.value) {
    toastStore.addToast('Keine Nachricht zum Antworten gefunden.', 'info');
    return;
  }

  loadingSuggestion.value = true;
  try {
    const response = await api.suggestReply(lastPartnerMessage.value);
    if (response.data.suggestion) {
      newMessage.value = response.data.suggestion; // Fills the input field
    }
  } catch (err) {
    console.error(err);
    toastStore.addToast('Fehler beim Generieren des Vorschlags.', 'error');
  } finally {
    loadingSuggestion.value = false;
  }
};

/**
 * Sends a new message in the active conversation.
 */
const handleSendMessage = async () => {
  await chatStore.sendMessage({ content: newMessage.value });
  newMessage.value = '';
  scrollToBottom();
};

/**
 * Creates a new offer for the active conversation.
 */
const handleCreateOffer = async () => {
  if (!offerData.value.price || !chatStore.activeConversation) return;
  try {
    const response = await api.createOffer({ conversation_id: chatStore.activeConversation.id, ...offerData.value });
    chatStore.activeConversation.messages.push(response.data);
    showOfferModal.value = false;
    offerData.value = { price: null, description: '' };
    scrollToBottom();
  } catch (err) {
    toastStore.addToast('Fehler beim Erstellen des Angebots.', 'error');
  }
};

/**
 * Accepts an offer.
 * @param {number} offerId - The ID of the offer to accept.
 */
const handleAcceptOffer = async (offerId) => {
  try {
    const response = await api.acceptOffer(offerId);
    const messageIndex = chatStore.activeConversation.messages.findIndex((m) => m.offer?.id === response.data.id);
    if (messageIndex !== -1) chatStore.activeConversation.messages[messageIndex].offer.status = response.data.status;
    toastStore.addToast('Angebot angenommen!', 'success');
  } catch (err) {
    toastStore.addToast('Fehler beim Annehmen des Angebots.', 'error');
  }
};

/**
 * Rejects an offer.
 * @param {number} offerId - The ID of the offer to reject.
 */
const handleRejectOffer = async (offerId) => {
  try {
    const response = await api.rejectOffer(offerId);
    const messageIndex = chatStore.activeConversation.messages.findIndex((m) => m.offer?.id === response.data.id);
    if (messageIndex !== -1) chatStore.activeConversation.messages[messageIndex].offer.status = response.data.status;
    toastStore.addToast('Angebot abgelehnt.', 'info');
  } catch (err) {
    toastStore.addToast('Fehler beim Ablehnen des Angebots.', 'error');
  }
};

/**
 * Opens the review modal for a specific job.
 * @param {Object} job - The job object to review.
 */
const openReviewModal = (job) => {
  selectedJobForReview.value = job;
  showReviewModal.value = true;
};

/**
 * Submits a review for a job.
 * @param {Object} reviewPayload - The review data.
 */
const handleCreateReview = async (reviewPayload) => {
  try {
    const response = await api.createReview(reviewPayload);
    if (chatStore.activeConversation && chatStore.activeConversation.job_details.id === reviewPayload.job) {
      chatStore.activeConversation.job_details.review = response.data;
    }
    toastStore.addToast('Bewertung erfolgreich abgegeben.', 'success');
    showReviewModal.value = false;
  } catch (err) {
    toastStore.addToast(err.response?.data?.detail || 'Fehler beim Senden der Bewertung.', 'error');
  }
};

/**
 * Scrolls the chat window to the bottom.
 */
const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
};

/**
 * Gets the other participant in the conversation.
 * @param {Object} convo - The conversation object.
 * @returns {Object} The other participant's user object.
 */
const getOtherParticipant = (convo) => {
  if (!convo?.participants_details) return { username: 'Unbekannt', id: null };
  return convo.participants_details.find((p) => p.id !== currentUser.value?.id) || { username: 'Unbekannt', id: null };
};

/**
 * Gets the avatar URL for the other participant.
 * @param {Object} convo - The conversation object.
 * @returns {string|null} The avatar URL or null.
 */
const getParticipantAvatar = (convo) => {
  const other = getOtherParticipant(convo);
  if (other?.profile_picture) return `http://localhost:8000${other.profile_picture}`;
  return null;
};
</script>

<template>
  <div class="page-wrapper">
    <div class="container-fluid inbox-container">
      <div class="inbox-layout">

        <!-- 1. Conversation List (Left) -->
        <aside class="conversation-list-panel">
          <header class="panel-header"><h2>Posteingang</h2></header>
          <div v-if="chatStore.loading" class="loading-placeholder">Lade Konversationen...</div>
          <ul v-else class="conversation-list">
            <li
              v-for="convo in chatStore.conversations"
              :key="convo.id"
              @click="chatStore.selectConversation(convo.id)"
              :class="{ 'active': chatStore.activeConversation && chatStore.activeConversation.id === convo.id }"
              class="conversation-card"
            >
              <UserAvatar :src="getParticipantAvatar(convo)" :name="getOtherParticipant(convo).username" :size="48" />
              <div class="convo-content">
                <div class="convo-top-row">
                  <span class="participant-name">{{ getOtherParticipant(convo).username }}</span>
                  <span class="timestamp">{{ new Date(convo.updated_at).toLocaleDateString() }}</span>
                </div>
                <p class="message-preview">{{ convo.last_message_preview || 'Klicke um Nachrichten zu sehen' }}</p>
              </div>
            </li>
          </ul>
        </aside>

        <!-- 2. Chat Window (Center) -->
        <main class="chat-panel">
          <div v-if="!chatStore.activeConversation" class="empty-chat-state">
            <div class="icon">💬</div>
            <h2>Deine Nachrichten</h2>
            <p>Wähle eine Unterhaltung aus der Liste, um Details zu besprechen.</p>
          </div>
          <div v-else class="chat-window">
            <header class="panel-header chat-header">
              <RouterLink :to="{ name: 'CraftsmanProfile', params: { id: getOtherParticipant(chatStore.activeConversation).id } }" class="header-link">
                <UserAvatar :src="getParticipantAvatar(chatStore.activeConversation)" :name="getOtherParticipant(chatStore.activeConversation).username" :size="40" />
                <div class="header-text">
                  <h3>{{ getOtherParticipant(chatStore.activeConversation).username }}</h3>
                  <p class="status-text">Antwortet in der Regel innerhalb weniger Stunden.</p>
                </div>
              </RouterLink>
            </header>
            <div class="message-list" ref="messageContainer">
              <div v-for="message in chatStore.activeConversation.messages" :key="message.id" class="message-row" :class="{ 'is-me': message.sender === currentUser.id }">
                <MessageOffer v-if="message.offer" :offer="message.offer" @accept="handleAcceptOffer" @reject="handleRejectOffer" />
                <div v-if="message.content" class="message-bubble"><p>{{ message.content }}</p></div>
              </div>
            </div>
            <footer class="chat-input-container">
              <form @submit.prevent="handleSendMessage" class="chat-form">

                <button v-if="isCraftsman" @click.prevent="showOfferModal = true" class="offer-btn" title="Angebot erstellen">+</button>

                <button
                  v-if="isCraftsman"
                  @click.prevent="handleSuggestReply"
                  class="ai-btn"
                  title="KI-Antwortvorschlag generieren"
                  :disabled="loadingSuggestion || !lastPartnerMessage"
                >
                  <span v-if="loadingSuggestion" class="spinning">⏳</span>
                  <span v-else>✨</span>
                </button>

                <input v-model="newMessage" type="text" placeholder="Schreibe eine Nachricht..." />
                <button type="submit" class="send-btn">➤</button>
              </form>
            </footer>
          </div>
        </main>

        <!-- 3. Details Panel (Right) -->
        <aside class="details-panel">
          <div v-if="!chatStore.activeConversation" class="empty-details"></div>
          <div v-else class="details-content">
            <header class="panel-header"><h3>Details zum Auftrag</h3></header>
            <div class="details-body">
              <h4>{{ chatStore.activeConversation.job_details?.title }}</h4>
              <p>📍 {{ chatStore.activeConversation.job_details?.city }}</p>
              <div class="divider"></div>
              <div v-if="chatStore.activeConversation.job_details?.status === 'COMPLETED' && !isCraftsman">
                <h5>Bewertung</h5>
                <div v-if="!chatStore.activeConversation.job_details.review">
                  <button class="base-button primary-action" @click="openReviewModal(chatStore.activeConversation.job_details)">Jetzt bewerten</button>
                </div>
                <div v-else><p>Bewertung abgegeben.</p></div>
              </div>
              <div v-else-if="latestOffer">
                <h5>Letztes Angebot</h5>
                <MessageOffer :offer="latestOffer" @accept="handleAcceptOffer" @reject="handleRejectOffer" />
              </div>
              <p v-else>Noch kein Angebot gemacht.</p>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <ReviewModal v-if="selectedJobForReview" :is-open="showReviewModal" :job="selectedJobForReview" @close="showReviewModal = false" @submit="handleCreateReview" />
    <div v-if="showOfferModal" class="modal-overlay" @click.self="showOfferModal = false">
      <div class="modal-card">
        <h3>Angebot erstellen</h3>
        <form @submit.prevent="handleCreateOffer">
          <div class="form-group"><label for="price">Preis (€)</label><input id="price" v-model="offerData.price" type="number" step="0.01" required /></div>
          <div class="form-group"><label for="description">Beschreibung (Optional)</label><textarea id="description" v-model="offerData.description" rows="3"></textarea></div>
          <div class="modal-actions"><button type="button" @click="showOfferModal = false" class="base-button secondary-action">Abbrechen</button><button type="submit" class="base-button primary-action">Angebot senden</button></div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-wrapper {
  height: calc(100vh - 80px);
  overflow: hidden;
}
.inbox-container {
  height: 100%;
  padding-top: 24px;
  padding-bottom: 24px;
}
.inbox-layout {
  display: grid;
  grid-template-columns: 320px 1fr 350px;
  height: 100%;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: none;
  background: white;
}

/* --- 1. Conversation List (Sidebar) --- */
.conversation-list-panel {
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
}
.panel-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  height: 70px;
  display: flex;
  align-items: center;
}
.panel-header h2, .panel-header h3 { margin: 0; font-size: 1.1rem; font-weight: 700; }

.conversation-list { list-style: none; padding: 0; margin: 0; }

.conversation-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  cursor: pointer;
  border-left: 4px solid transparent;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s;
}

.conversation-card:hover {
  background-color: #f7f7f7;
}

.conversation-card.active {
  background-color: #ebebeb;
  border-left-color: #222222;
}

.convo-content {
  flex-grow: 1;
  overflow: hidden;
}

.convo-top-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
}

.participant-name {
  font-weight: 700;
  color: #222;
  font-size: 1rem;
}

.timestamp {
  font-size: 0.75rem;
  color: #717171;
}

.message-preview {
  font-size: 0.9rem;
  color: #717171;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}

/* --- 2. Chat Window --- */
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* Chat Header */
.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: inherit;
}
.header-text h3 { margin: 0; }
.status-text { margin: 0; font-size: 0.8rem; color: #717171; }

/* Message List */
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Input Area */
.chat-input-container {
  flex-shrink: 0;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  background-color: white;
}
.chat-form {
  display: flex;
  align-items: center;
  border: 1px solid #B0B0B0;
  border-radius: 24px;
  padding: 4px 8px;
  background-color: white;
  transition: border-color 0.2s;
}
.chat-form:focus-within {
  border-color: #222;
}
.chat-form input {
  flex-grow: 1;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  padding: 10px;
  background: transparent !important;
  font-size: 1rem;
}

/* Buttons */
.offer-btn, .send-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #717171;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}
.offer-btn:hover, .send-btn:hover { background-color: #f0f0f0; }
.offer-btn { color: var(--color-primary); font-size: 1.5rem; }
.send-btn { color: var(--color-primary); font-size: 1.2rem; }

/* Message Bubbles */
.message-row { display: flex; margin-bottom: 8px; }
.message-row.is-me { justify-content: flex-end; }
.message-row:not(.is-me) { justify-content: flex-start; }

.message-bubble {
  padding: 12px 20px;
  border-radius: 22px;
  max-width: 75%;
  line-height: 1.5;
}
.message-bubble p { margin: 0; }
.message-row.is-me .message-bubble {
  background-color: var(--color-primary);
  color: white;
  border-bottom-right-radius: 4px;
}
.message-row:not(.is-me) .message-bubble {
  background-color: #f7f7f7;
  color: #222;
  border-bottom-left-radius: 4px;
}

/* --- 3. Details Panel (Right) --- */
.details-panel {
  border-left: 1px solid var(--color-border);
  background-color: white;
  overflow-y: auto;
}
.details-body {
  padding: 24px;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.details-body h4 { margin-top: 0; font-size: 1.1rem; }
.details-body p { color: #717171; margin-bottom: 8px; }
.divider { border-bottom: 1px solid var(--color-border); margin: 24px 0; }
.primary-action { width: 100%; }

/* --- Modal --- */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-card { background: white; padding: 24px; border-radius: 12px; width: 90%; max-width: 400px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 4px; font-weight: 600; font-size: 0.9rem; }
.form-group input, .form-group textarea { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 8px; }

/* --- Empty States --- */
.empty-chat-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: #717171;
}
.empty-chat-state .icon { font-size: 4rem; margin-bottom: 1rem; opacity: 0.5; }

.ai-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #717171; /* Oder eine spezielle Farbe wie Lila/Gold für KI */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s, color 0.2s;
  font-size: 1.2rem;
}

.ai-btn:hover {
  background-color: #f0f0f0;
  color: #9c27b0; /* Lila Hover-Farbe für "Magie" */
}

.ai-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Optional: Einfache Rotation für den Lade-Indikator */
.spinning {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>

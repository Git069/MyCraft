<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const route = useRoute();
const conversations = ref([]);
const activeConversation = ref(null);
const loading = ref(true);
const error = ref(null);
const newMessage = ref('');
const messageContainer = ref(null);

const currentUser = computed(() => authStore.currentUser);

const fetchConversations = async () => {
  loading.value = true;
  try {
    const response = await api.getConversations();
    conversations.value = response.data;

    const activeConvoId = parseInt(route.query.active_convo, 10);
    if (activeConvoId && conversations.value.some(c => c.id === activeConvoId)) {
      await selectConversation(activeConvoId);
    } else if (conversations.value.length > 0) {
      await selectConversation(conversations.value[0].id);
    }
  } catch (err) {
    error.value = "Fehler beim Laden der Konversationen.";
  } finally {
    loading.value = false;
  }
};

const selectConversation = async (convoId) => {
  try {
    const response = await api.getConversationDetails(convoId);
    activeConversation.value = response.data;
  } catch (err) {
    error.value = "Fehler beim Laden der Nachrichtendetails.";
  }
};

const sendMessage = async () => {
  if (!newMessage.value.trim() || !activeConversation.value) return;
  try {
    const response = await api.postMessage(activeConversation.value.id, newMessage.value);
    activeConversation.value.messages.push(response.data);
    newMessage.value = '';
    scrollToBottom();
  } catch (err) {
    error.value = "Fehler beim Senden der Nachricht.";
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

watch(activeConversation, scrollToBottom, { deep: true });
onMounted(fetchConversations);

const getOtherParticipant = (convo) => {
  if (!convo || !currentUser.value) return 'Unbekannt';
  const other = convo.participants_details.find(p => p.id !== currentUser.value.id);
  return other ? other.username : 'Unbekannt';
};
</script>

<template>
  <div class="inbox-layout">
    <!-- Conversation List -->
    <aside class="conversation-list-panel">
      <header class="panel-header">
        <h2>Posteingang</h2>
      </header>
      <div v-if="loading" class="loading-placeholder">Lade Konversationen...</div>
      <div v-if="error && !loading" class="error-placeholder">{{ error }}</div>
      <div v-if="!loading && conversations.length === 0" class="empty-list">
        <p>Noch keine Nachrichten.</p>
      </div>
      <ul v-else class="conversation-list">
        <li
          v-for="convo in conversations"
          :key="convo.id"
          @click="selectConversation(convo.id)"
          :class="{ 'active': activeConversation && activeConversation.id === convo.id }"
          class="conversation-card"
        >
          <div class="avatar-placeholder"></div>
          <div class="convo-details">
            <div class="convo-header">
              <span class="participant-name">{{ getOtherParticipant(convo) }}</span>
              <span class="timestamp">{{ new Date(convo.updated_at).toLocaleDateString() }}</span>
            </div>
            <p class="message-preview">{{ convo.last_message_preview || 'Klicke um Nachrichten zu sehen' }}</p>
          </div>
        </li>
      </ul>
    </aside>

    <!-- Chat Window -->
    <main class="chat-panel">
      <div v-if="!activeConversation" class="empty-chat-state">
        <div class="icon">💬</div>
        <h2>Deine Nachrichten</h2>
        <p>Wähle eine Unterhaltung aus der Liste, um Details zu besprechen.</p>
      </div>
      <div v-else class="chat-window">
        <header class="panel-header chat-header">
          <h3>{{ getOtherParticipant(activeConversation) }}</h3>
          <p>Antwortet in der Regel innerhalb weniger Stunden.</p>
        </header>
        <div class="message-container" ref="messageContainer">
          <div
            v-for="message in activeConversation.messages"
            :key="message.id"
            class="message-bubble"
            :class="{ 'sent': message.sender === currentUser.id, 'received': message.sender !== currentUser.id }"
          >
            <p>{{ message.content }}</p>
          </div>
        </div>
        <footer class="chat-input-footer">
          <form @submit.prevent="sendMessage" class="chat-form">
            <button type="button" class="attach-btn">📎</button>
            <input v-model="newMessage" type="text" placeholder="Schreibe eine Nachricht..." />
            <button type="submit" class="send-btn">➤</button>
          </form>
        </footer>
      </div>
    </main>

    <!-- Details Panel -->
    <aside class="details-panel">
      <div v-if="!activeConversation" class="empty-details"></div>
      <div v-else class="details-content">
        <header class="panel-header">
          <h3>Details zum Auftrag</h3>
        </header>
        <div class="details-body">
          <h4>{{ activeConversation.job_details.title }}</h4>
          <p>📍 {{ activeConversation.job_details.city }}</p>
          <p>💰 {{ activeConversation.job_details.price }} €</p>
          <div class="divider"></div>
          <div class="action-buttons">
            <button class="base-button primary-action">Angebot annehmen</button>
            <button class="base-button secondary-action">Ablehnen</button>
          </div>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.inbox-layout {
  display: grid;
  grid-template-columns: 350px 1fr 300px;
  height: calc(100vh - 80px);
  border-top: 1px solid var(--color-border);
  background: white;
}
.panel-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}
.panel-header h2, .panel-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}
.panel-header p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--color-text-light);
}
.conversation-list-panel {
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.conversation-list {
  list-style: none;
  padding: 8px 0;
  margin: 0;
}
.conversation-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  cursor: pointer;
  border-left: 4px solid transparent;
}
.conversation-card:hover {
  background-color: #f7f7f7;
}
.conversation-card.active {
  background-color: #f7f7f7;
  border-left-color: var(--color-text);
}
.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e0e0e0;
  flex-shrink: 0;
}
.convo-details {
  flex-grow: 1;
  overflow: hidden;
}
.convo-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.participant-name {
  font-weight: 700;
}
.timestamp {
  font-size: 0.75rem;
  color: var(--color-text-light);
}
.message-preview {
  font-size: 0.9rem;
  color: var(--color-text-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 4px 0 0 0;
}
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.empty-chat-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  text-align: center;
  color: var(--color-text-light);
}
.empty-chat-state .icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.message-container {
  flex-grow: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}
.message-bubble {
  padding: 10px 16px;
  border-radius: 20px;
  max-width: 70%;
  line-height: 1.4;
}
.message-bubble.sent {
  background-color: #222222;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}
.message-bubble.received {
  background-color: #f1f1f1;
  color: var(--color-text);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}
.chat-input-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}
.chat-form {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: 24px;
  padding: 4px;
}
.chat-form input {
  flex-grow: 1;
  border: none;
  outline: none;
  padding: 8px;
  background: transparent;
}
.attach-btn, .send-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 8px;
  color: var(--color-text-light);
}
.details-panel {
  border-left: 1px solid var(--color-border);
}
.details-body {
  padding: 24px;
}
.details-body h4 {
  margin-top: 0;
  font-size: 1.1rem;
}
.details-body p {
  color: var(--color-text-light);
}
.divider {
  border-bottom: 1px solid var(--color-border);
  margin: var(--spacing-lg) 0;
}
.action-buttons {
  display: grid;
  gap: var(--spacing-sm);
}
.primary-action {
  width: 100%;
}
.secondary-action {
  width: 100%;
  background: #f1f1f1;
  color: var(--color-text);
}
</style>

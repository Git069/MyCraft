import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';
import { useToastStore } from './toast';

/* ==========================================================================
   Chat Store
   ========================================================================== */

/**
 * Pinia store for managing chat conversations and messages.
 * Handles fetching conversations, selecting active chats, sending messages, and polling for updates.
 */
export const useChatStore = defineStore('chat', () => {
  const conversations = ref([]);
  const activeConversation = ref(null);
  const loading = ref(false);
  const error = ref(null);

  let pollingInterval = null;

  const toastStore = useToastStore();

  /**
   * Stops the message polling interval.
   */
  const stopPolling = () => {
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = null;
  };

  /**
   * Starts polling for new messages in the active conversation.
   *
   * @param {number|string} convoId - The ID of the conversation to poll.
   */
  const startPolling = (convoId) => {
    stopPolling();
    pollingInterval = setInterval(async () => {
      try {
        const response = await api.getConversationDetails(convoId);
        if (activeConversation.value?.id === convoId) {
          if (response.data.messages.length > activeConversation.value.messages.length) {
            activeConversation.value.messages = response.data.messages;
          }
        }
      } catch (err) {
        console.error('Polling failed:', err);
        stopPolling();
      }
    }, 5000);
  };

  /**
   * Selects a conversation and loads its details.
   * Starts polling for new messages.
   *
   * @param {number|string} convoId - The ID of the conversation to select.
   * @returns {Promise<void>}
   */
  const selectConversation = async (convoId) => {
    try {
      const response = await api.getConversationDetails(convoId);
      activeConversation.value = response.data;
      startPolling(convoId);
    } catch (err) {
      error.value = 'Fehler beim Laden der Nachrichtendetails.';
    }
  };

  /**
   * Fetches all conversations for the current user.
   * Optionally selects a specific conversation after loading.
   *
   * @param {number|string} [activeConvoId=null] - The ID of the conversation to select initially.
   * @returns {Promise<void>}
   */
  const fetchConversations = async (activeConvoId = null) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getConversations();
      const data = Array.isArray(response.data) ? response.data : (response.data.results || []);
      conversations.value = data.filter((c) => c && c.id);

      if (activeConvoId && conversations.value.some((c) => c.id === activeConvoId)) {
        await selectConversation(activeConvoId);
      } else if (conversations.value.length > 0) {
        await selectConversation(conversations.value[0].id);
      }
    } catch (err) {
      error.value = 'Fehler beim Laden der Konversationen.';
    } finally {
      loading.value = false;
    }
  };

  /**
   * Sends a message to the currently active conversation.
   *
   * @param {Object} payload - The message payload.
   * @param {string} payload.content - The text content of the message.
   * @returns {Promise<void>}
   */
  const sendMessage = async (payload) => {
    if (!payload.content.trim() || !activeConversation.value) return;
    try {
      const response = await api.postMessage(activeConversation.value.id, payload.content);
      activeConversation.value.messages.push(response.data);
    } catch (err) {
      toastStore.addToast('Fehler beim Senden der Nachricht.', 'error');
    }
  };

  return {
    conversations,
    activeConversation,
    loading,
    error,
    fetchConversations,
    selectConversation,
    sendMessage,
    stopPolling,
  };
});

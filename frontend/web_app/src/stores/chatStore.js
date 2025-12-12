import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';
import { useToastStore } from './toast';

export const useChatStore = defineStore('chat', () => {
  const conversations = ref([]);
  const activeConversation = ref(null);
  const loading = ref(false);
  const error = ref(null);
  
  let pollingInterval = null;

  const toastStore = useToastStore();

  const stopPolling = () => {
    if (pollingInterval) clearInterval(pollingInterval);
    pollingInterval = null;
  };

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
        console.error("Polling failed:", err);
        stopPolling();
      }
    }, 5000);
  };

  const fetchConversations = async (activeConvoId = null) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await api.getConversations();
      let data = Array.isArray(response.data) ? response.data : (response.data.results || []);
      conversations.value = data.filter(c => c && c.id);
      
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
      startPolling(convoId);
    } catch (err) {
      error.value = "Fehler beim Laden der Nachrichtendetails.";
    }
  };

  const sendMessage = async (payload) => {
    if (!payload.content.trim() || !activeConversation.value) return;
    try {
      const response = await api.postMessage(activeConversation.value.id, payload.content);
      activeConversation.value.messages.push(response.data);
    } catch (err) {
      toastStore.addToast("Fehler beim Senden der Nachricht.", "error");
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

import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default {
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },
  login(credentials) {
    return apiClient.post('/auth/token/login/', credentials);
  },
  fetchCurrentUser() {
    return apiClient.get('/auth/users/me/');
  },
  updateUser(userData) {
    return apiClient.patch('/auth/users/me/', userData);
  },
  uploadProfilePicture(formData) {
    return apiClient.patch('/auth/upload-profile-picture/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  createJob(jobData) {
    return apiClient.post('/jobs/', jobData);
  },
  getJobs(params) {
    return apiClient.get('/jobs/', { params });
  },
  getJobDetails(jobId) {
    return apiClient.get(`/jobs/${jobId}/`);
  },
  deleteJob(jobId) {
    return apiClient.delete(`/jobs/${jobId}/`);
  },
  bookJob(jobId) {
    return apiClient.post(`/jobs/${jobId}/book/`);
  },
  becomeCraftsman(profileData) {
    return apiClient.post('/auth/become-craftsman/', profileData);
  },
  getConversations() {
    return apiClient.get('/conversations/');
  },
  getConversationDetails(convoId) {
    return apiClient.get(`/conversations/${convoId}/`);
  },
  startConversation(jobId, message) {
    return apiClient.post('/conversations/', { job_id: jobId, message: message });
  },
  postMessage(convoId, content) {
    return apiClient.post(`/conversations/${convoId}/post_message/`, { content: content });
  },
  
  // --- NEW OFFER API FUNCTIONS ---
  createOffer(offerData) {
    return apiClient.post('/offers/', offerData);
  },
  acceptOffer(offerId) {
    return apiClient.post(`/offers/${offerId}/accept/`);
  },
  rejectOffer(offerId) {
    return apiClient.post(`/offers/${offerId}/reject/`);
  },

  getMyJobs() {
    return apiClient.get('/jobs/my_jobs/');
  },
  getMyBookings() {
    return apiClient.get('/jobs/my_bookings/');
  },
  setAuthToken(token) {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  },
  clearAuthToken() {
    delete apiClient.defaults.headers.common['Authorization'];
  },
};

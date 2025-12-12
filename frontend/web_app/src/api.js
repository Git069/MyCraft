import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
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
  // Auth & User
  register(userData) { return apiClient.post('/auth/users/', userData); },
  login(credentials) { return apiClient.post('/auth/token/login/', credentials); },
  fetchCurrentUser() { return apiClient.get('/auth/users/me/'); },
  updateUser(userData) { return apiClient.patch('/auth/users/me/', userData); },
  getUserDetails(userId) { return apiClient.get(`/auth/users/${userId}/`); },
  uploadProfilePicture(formData) { return apiClient.patch('/auth/upload-profile-picture/', formData, { headers: { 'Content-Type': 'multipart/form-data' } }); },
  becomeCraftsman(profileData) { return apiClient.post('/auth/become-craftsman/', profileData); },

  // --- Services (formerly Jobs) ---
  // The new, correct function names
  createService(serviceData) { return apiClient.post('/services/', serviceData); },
  getServices(params) { return apiClient.get('/services/', { params }); },
  getServiceDetails(serviceId) { return apiClient.get(`/services/${serviceId}/`); },
  updateService(serviceId, serviceData) { return apiClient.patch(`/services/${serviceId}/`, serviceData); },
  deleteService(serviceId) { return apiClient.delete(`/services/${serviceId}/`); },
  getMyServices() { return apiClient.get('/services/my-jobs/'); },

  // --- Compatibility Aliases for old components ---
  createJob(jobData) { return this.createService(jobData); },
  getJobs(params) { return this.getServices(params); },
  getJobDetails(jobId) { return this.getServiceDetails(jobId); },
  updateJob(jobId, jobData) { return this.updateService(jobId, jobData); },
  deleteJob(jobId) { return this.deleteService(jobId); },
  
  // --- Bookings ---
  getMyBookings() { return apiClient.get('/bookings/my_bookings/'); },
  getMyOrders() { return apiClient.get('/bookings/my_orders/'); },
  markBookingAsCompleted(bookingId) { return apiClient.post(`/bookings/${bookingId}/mark_completed/`); },
  cancelBooking(bookingId) { return apiClient.post(`/bookings/${bookingId}/cancel/`); },

  // Chat & Offers
  getConversations() { return apiClient.get('/conversations/'); },
  getConversationDetails(convoId) { return apiClient.get(`/conversations/${convoId}/`); },
  startConversation(serviceId, message) { return apiClient.post('/conversations/', { job_id: serviceId, message: message }); },
  postMessage(convoId, content) { return apiClient.post(`/conversations/${convoId}/post_message/`, { content: content }); },
  createOffer(offerData) { return apiClient.post('/offers/', offerData); },
  acceptOffer(offerId) { return apiClient.post(`/offers/${offerId}/accept/`); },
  rejectOffer(offerId) { return apiClient.post(`/offers/${offerId}/reject/`); },

  // Reviews
  createReview(reviewData) { return apiClient.post('/reviews/', reviewData); },
  
  setAuthToken(token) { if (token) apiClient.defaults.headers.common['Authorization'] = `Token ${token}`; },
  clearAuthToken() { delete apiClient.defaults.headers.common['Authorization']; },
};

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

// Helper to transform GeoJSON to flat objects for UI components
const transformGeoJSON = (response) => {
  if (response.data && response.data.type === 'FeatureCollection') {
    // It's GeoJSON! Extract properties and add geometry
    const features = response.data.features.map(feature => ({
      ...feature.properties,
      id: feature.id, // Ensure ID is top-level
      location: feature.geometry // Keep geometry if needed
    }));
    // Wrap it back in a structure that mimics paginated response if needed, 
    // or just return the array. Let's return an object with 'results' to match old API style.
    return { ...response, data: { results: features } };
  }
  return response;
};

export default {
  // ... (Auth & User functions remain same)
  register(userData) { return apiClient.post('/auth/users/', userData); },
  login(credentials) { return apiClient.post('/auth/token/login/', credentials); },
  fetchCurrentUser() { return apiClient.get('/auth/users/me/'); },
  updateUser(userData) { return apiClient.patch('/auth/users/me/', userData); },
  getUserDetails(userId) { return apiClient.get(`/auth/users/${userId}/`); },
  uploadProfilePicture(formData) { return apiClient.patch('/auth/upload-profile-picture/', formData, { headers: { 'Content-Type': 'multipart/form-data' } }); },
  becomeCraftsman(profileData) { return apiClient.post('/auth/become-craftsman/', profileData); },

  // --- SERVICES (GeoJSON aware) ---
  createService(serviceData) { 
    if (serviceData instanceof FormData) {
      return apiClient.post('/services/', serviceData, { headers: { 'Content-Type': 'multipart/form-data' } });
    }
    return apiClient.post('/services/', serviceData); 
  },
  
  // Modified getServices to handle GeoJSON
  async getServices(params) { 
    const response = await apiClient.get('/services/', { params });
    return transformGeoJSON(response);
  },
  
  async getServiceDetails(serviceId) { 
    const response = await apiClient.get(`/services/${serviceId}/`);
    // Single Feature handling
    if (response.data && response.data.type === 'Feature') {
        return { ...response, data: { ...response.data.properties, id: response.data.id, location: response.data.geometry } };
    }
    return response;
  },

  updateService(serviceId, serviceData) { return apiClient.patch(`/services/${serviceId}/`, serviceData); },
  deleteService(serviceId) { return apiClient.delete(`/services/${serviceId}/`); },
  
  async getMyServices() { 
    const response = await apiClient.get('/services/my-jobs/');
    return transformGeoJSON(response);
  },

  // ... (Aliases and other functions remain same)
  createJob(jobData) { return this.createService(jobData); },
  getJobs(params) { return this.getServices(params); },
  getJobDetails(jobId) { return this.getServiceDetails(jobId); },
  updateJob(jobId, jobData) { return this.updateService(jobId, jobData); },
  deleteJob(jobId) { return this.deleteService(jobId); },
  
  getMyBookings() { return apiClient.get('/bookings/my_bookings/'); },
  getMyOrders() { return apiClient.get('/bookings/my_orders/'); },
  markBookingAsCompleted(bookingId) { return apiClient.post(`/bookings/${bookingId}/mark_completed/`); },
  cancelBooking(bookingId) { return apiClient.post(`/bookings/${bookingId}/cancel/`); },

  getConversations() { return apiClient.get('/conversations/'); },
  getConversationDetails(convoId) { return apiClient.get(`/conversations/${convoId}/`); },
  startConversation(serviceId, message) { return apiClient.post('/conversations/', { job_id: serviceId, message: message }); },
  postMessage(convoId, content) { return apiClient.post(`/conversations/${convoId}/post_message/`, { content: content }); },
  createOffer(offerData) { return apiClient.post('/offers/', offerData); },
  acceptOffer(offerId) { return apiClient.post(`/offers/${offerId}/accept/`); },
  rejectOffer(offerId) { return apiClient.post(`/offers/${offerId}/reject/`); },
  createReview(reviewData) { return apiClient.post('/reviews/', reviewData); },
  
  setAuthToken(token) { if (token) apiClient.defaults.headers.common['Authorization'] = `Token ${token}`; },
  clearAuthToken() { delete apiClient.defaults.headers.common['Authorization']; },
};

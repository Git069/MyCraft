import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

/* ==========================================================================
   Configuration
   ========================================================================== */

/**
 * Axios instance configuration.
 * Sets the base URL from environment variables and default headers.
 */
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

/* ==========================================================================
   Interceptors
   ========================================================================== */

/**
 * Response interceptor to handle global errors.
 * Redirects to login on 401 Unauthorized errors.
 */
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

/* ==========================================================================
   API Methods
   ========================================================================== */

export default {
  /* --------------------------------------------------------------------------
     Auth & User
     -------------------------------------------------------------------------- */

  /**
   * Registers a new user.
   *
   * @param {Object} userData - The user registration data.
   * @returns {Promise<Object>} The response containing the created user.
   */
  register(userData) {
    return apiClient.post('/auth/users/', userData);
  },

  /**
   * Logs in a user and retrieves a token.
   *
   * @param {Object} credentials - The user credentials (username/email and password).
   * @returns {Promise<Object>} The response containing the auth token.
   */
  login(credentials) {
    return apiClient.post('/auth/token/login/', credentials);
  },

  /**
   * Fetches the current authenticated user's profile.
   *
   * @returns {Promise<Object>} The response containing user details.
   */
  fetchCurrentUser() {
    return apiClient.get('/auth/users/me/');
  },

  /**
   * Updates the current user's profile.
   *
   * @param {Object} profileData - The data to update.
   * @returns {Promise<Object>} The response containing the updated profile.
   */
  updateUserProfile(profileData) {
    return apiClient.patch('/auth/update-profile/', profileData);
  },

  /**
   * Retrieves details of a specific user by ID.
   *
   * @param {number|string} userId - The ID of the user.
   * @returns {Promise<Object>} The response containing user details.
   */
  getUserDetails(userId) {
    return apiClient.get(`/auth/users/${userId}/`);
  },

  /**
   * Uploads a profile picture for the current user.
   *
   * @param {FormData} formData - The form data containing the image file.
   * @returns {Promise<Object>} The response from the server.
   */
  uploadProfilePicture(formData) {
    return apiClient.patch('/auth/upload-profile-picture/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  /**
   * Requests to become a craftsman.
   *
   * @param {Object} profileData - The craftsman profile data.
   * @returns {Promise<Object>} The response from the server.
   */
  becomeCraftsman(profileData) {
    return apiClient.post('/auth/become-craftsman/', profileData);
  },

  /**
   * Sets the authentication token for subsequent requests.
   *
   * @param {string} token - The authentication token.
   */
  setAuthToken(token) {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  },

  /**
   * Clears the authentication token.
   */
  clearAuthToken() {
    delete apiClient.defaults.headers.common['Authorization'];
  },

  /* --------------------------------------------------------------------------
     Services (Jobs)
     -------------------------------------------------------------------------- */

  /**
   * Suggests addresses based on a query string.
   *
   * @param {string} query - The address search query.
   * @returns {Promise<Object>} The response containing address suggestions.
   */
  suggestAddresses(query) {
    return apiClient.get('/services/suggest_address/', { params: { q: query } });
  },

  /**
   * Creates a new service or job.
   * Handles both JSON data and FormData (for file uploads).
   *
   * @param {Object|FormData} serviceData - The service data.
   * @returns {Promise<Object>} The response containing the created service.
   */
  createService(serviceData) {
    if (serviceData instanceof FormData) {
      return apiClient.post('/services/', serviceData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
    }
    return apiClient.post('/services/', serviceData);
  },

  /**
   * Retrieves a list of services with optional filtering.
   * Automatically transforms GeoJSON responses.
   *
   * @param {Object} params - Query parameters for filtering.
   * @returns {Promise<Object>} The transformed response with flattened service data.
   */
  async getServices(params) {
    const response = await apiClient.get('/services/', { params });
    return transformGeoJSON(response);
  },

  /**
   * Retrieves details of a specific service.
   * Handles GeoJSON Feature responses.
   *
   * @param {number|string} serviceId - The ID of the service.
   * @returns {Promise<Object>} The response containing service details.
   */
  async getServiceDetails(serviceId) {
    const response = await apiClient.get(`/services/${serviceId}/`);
    // Single Feature handling
    if (response.data && response.data.type === 'Feature') {
      return {
        ...response,
        data: {
          ...response.data.properties,
          id: response.data.id,
          location: response.data.geometry,
        },
      };
    }
    return response;
  },

  /**
   * Gets the availability of a service.
   *
   * @param {number|string} serviceId - The ID of the service.
   * @returns {Promise<Object>} The response containing a list of occupied days (Array of strings "YYYY-MM-DD").
   */
  getServiceAvailability(serviceId) {
    return apiClient.get(`/services/${serviceId}/availability/`);
  },

  /**
   * Updates an existing service.
   *
   * @param {number|string} serviceId - The ID of the service.
   * @param {Object} serviceData - The data to update.
   * @returns {Promise<Object>} The response containing the updated service.
   */
  updateService(serviceId, serviceData) {
    return apiClient.patch(`/services/${serviceId}/`, serviceData);
  },

  /**
   * Deletes a service.
   *
   * @param {number|string} serviceId - The ID of the service.
   * @returns {Promise<Object>} The response confirming deletion.
   */
  deleteService(serviceId) {
    return apiClient.delete(`/services/${serviceId}/`);
  },

  /**
   * Gets price advice for a service.
   *
   * @param {number|string} serviceId - The ID of the service.
   * @returns {Promise<Object>} The response containing price advice.
   */
  getPriceAdvice(serviceId) {
    return apiClient.get(`/services/${serviceId}/price-advice/`);
  },

  /**
   * Retrieves the current user's services/jobs.
   * Automatically transforms GeoJSON responses.
   *
   * @returns {Promise<Object>} The transformed response with flattened service data.
   */
  async getMyServices() {
    const response = await apiClient.get('/services/my-jobs/');
    return transformGeoJSON(response);
  },

  // Aliases for Job terminology
  /**
   * Alias for createService.
   * @param {Object|FormData} jobData
   * @returns {Promise<Object>}
   */
  createJob(jobData) { return this.createService(jobData); },

  /**
   * Alias for getServices.
   * @param {Object} params
   * @returns {Promise<Object>}
   */
  getJobs(params) { return this.getServices(params); },

  /**
   * Alias for getServiceDetails.
   * @param {number|string} jobId
   * @returns {Promise<Object>}
   */
  getJobDetails(jobId) { return this.getServiceDetails(jobId); },

  /**
   * Alias for updateService.
   * @param {number|string} jobId
   * @param {Object} jobData
   * @returns {Promise<Object>}
   */
  updateJob(jobId, jobData) { return this.updateService(jobId, jobData); },

  /**
   * Alias for deleteService.
   * @param {number|string} jobId
   * @returns {Promise<Object>}
   */
  deleteJob(jobId) { return this.deleteService(jobId); },

  /* --------------------------------------------------------------------------
     Bookings
     -------------------------------------------------------------------------- */

  /**
   * Creates a binding booking.
   *
   * @param {Object} bookingData - The booking details.
   * @returns {Promise<Object>} The response containing the created booking.
   */
  createBooking(bookingData) {
    return apiClient.post('/bookings/', bookingData);
  },

  /**
   * Retrieves the current user's bookings.
   *
   * @returns {Promise<Object>} The response containing the list of bookings.
   */
  getMyBookings() {
    return apiClient.get('/bookings/my_bookings/');
  },

  /**
   * Retrieves the current user's orders.
   *
   * @returns {Promise<Object>} The response containing the list of orders.
   */
  getMyOrders() {
    return apiClient.get('/bookings/my_orders/');
  },

  /**
   * Marks a booking as completed.
   *
   * @param {number|string} bookingId - The ID of the booking.
   * @returns {Promise<Object>} The response confirming completion.
   */
  markBookingAsCompleted(bookingId) {
    return apiClient.post(`/bookings/${bookingId}/mark_completed/`);
  },

  /**
   * Cancels a booking.
   *
   * @param {number|string} bookingId - The ID of the booking.
   * @returns {Promise<Object>} The response confirming cancellation.
   */
  cancelBooking(bookingId) {
    return apiClient.post(`/bookings/${bookingId}/cancel/`);
  },

  /* --------------------------------------------------------------------------
     Conversations & Messages
     -------------------------------------------------------------------------- */

  /**
   * Retrieves a list of conversations.
   *
   * @returns {Promise<Object>} The response containing the list of conversations.
   */
  getConversations() {
    return apiClient.get('/conversations/');
  },

  /**
   * Retrieves details of a specific conversation.
   *
   * @param {number|string} convoId - The ID of the conversation.
   * @returns {Promise<Object>} The response containing conversation details.
   */
  getConversationDetails(convoId) {
    return apiClient.get(`/conversations/${convoId}/`);
  },

  /**
   * Starts a new conversation related to a service.
   *
   * @param {number|string} serviceId - The ID of the service/job.
   * @param {string} message - The initial message content.
   * @returns {Promise<Object>} The response containing the created conversation.
   */
  startConversation(serviceId, message) {
    return apiClient.post('/conversations/', { job_id: serviceId, message: message });
  },

  /**
   * Posts a message to an existing conversation.
   *
   * @param {number|string} convoId - The ID of the conversation.
   * @param {string} content - The message content.
   * @returns {Promise<Object>} The response containing the created message.
   */
  postMessage(convoId, content) {
    return apiClient.post(`/conversations/${convoId}/post_message/`, { content: content });
  },

  /**
   * Suggests a reply based on the last message.
   *
   * @param {string} lastMessage - The content of the last message received.
   * @returns {Promise<Object>} The response containing the suggested reply.
   */
  suggestReply(lastMessage) {
    return apiClient.post('/conversations/suggest-reply/', { last_message: lastMessage });
  },

  /* --------------------------------------------------------------------------
     Offers
     -------------------------------------------------------------------------- */

  /**
   * Creates a new offer.
   *
   * @param {Object} offerData - The offer details.
   * @returns {Promise<Object>} The response containing the created offer.
   */
  createOffer(offerData) {
    return apiClient.post('/offers/', offerData);
  },

  /**
   * Accepts an offer.
   *
   * @param {number|string} offerId - The ID of the offer.
   * @returns {Promise<Object>} The response confirming acceptance.
   */
  acceptOffer(offerId) {
    return apiClient.post(`/offers/${offerId}/accept/`);
  },

  /**
   * Rejects an offer.
   *
   * @param {number|string} offerId - The ID of the offer.
   * @returns {Promise<Object>} The response confirming rejection.
   */
  rejectOffer(offerId) {
    return apiClient.post(`/offers/${offerId}/reject/`);
  },

  /* --------------------------------------------------------------------------
     Reviews
     -------------------------------------------------------------------------- */

  /**
   * Creates a review.
   *
   * @param {Object} reviewData - The review details.
   * @returns {Promise<Object>} The response containing the created review.
   */
  createReview(reviewData) {
    return apiClient.post('/reviews/', reviewData);
  },
};

/* ==========================================================================
   Helper Functions
   ========================================================================== */

/**
 * Transforms a GeoJSON feature into a flat object for UI components.
 *
 * @param {Object} feature - The GeoJSON feature object.
 * @returns {Object} The flattened object containing properties, id, and location.
 */
const flattenFeature = (feature) => {
  if (!feature || !feature.properties) return feature;
  return {
    ...feature.properties,
    id: feature.id,        // Get ID from the top level
    location: feature.geometry, // Preserve geometry
  };
};

/**
 * Transforms API responses containing GeoJSON data into a flat structure.
 * Handles different response structures (FeatureCollection, Pagination).
 *
 * @param {Object} response - The Axios response object.
 * @returns {Object} The transformed response object with flattened data.
 */
const transformGeoJSON = (response) => {
  const data = response.data;

  // CASE 1: API returns a GeoJSON FeatureCollection directly
  if (data && data.type === 'FeatureCollection' && Array.isArray(data.features)) {
    return {
      ...response,
      data: { results: data.features.map(flattenFeature) },
    };
  }

  // CASE 2: API returns Pagination, and 'results' is a FeatureCollection (Standard DRF GIS)
  if (data && data.results && data.results.type === 'FeatureCollection' && Array.isArray(data.results.features)) {
    return {
      ...response,
      data: {
        ...data,
        results: data.results.features.map(flattenFeature),
      },
    };
  }

  // CASE 3: API returns Pagination, but 'results' is directly an Array of Features
  // (Safety net, in case the structure deviates slightly)
  if (data && Array.isArray(data.results) && data.results.length > 0 && data.results[0].properties) {
    return {
      ...response,
      data: {
        ...data,
        results: data.results.map(flattenFeature),
      },
    };
  }

  // No GeoJSON detected -> Return original
  return response;
};

import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8247';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor for logging and error handling
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    console.log('📊 Response Data Structure:', {
      hasData: !!response.data,
      dataType: typeof response.data,
      keys: response.data ? Object.keys(response.data) : [],
      dataStructure: response.data ? response.data : null
    });
    return response;
  },
  (error) => {
    console.group('❌ API Error Details');
    console.error('Status:', error.response?.status);
    console.error('URL:', error.config?.url);
    console.error('Method:', error.config?.method?.toUpperCase());
    console.error('Response Data:', error.response?.data);
    console.error('Error Message:', error.message);
    
    // Handle specific error cases
    if (error.response?.status === 404) {
      console.error('📄 Resource not found - Check endpoint URL');
    } else if (error.response?.status === 500) {
      console.error('🔧 Server error - Check backend logs');
    } else if (error.code === 'ECONNABORTED') {
      console.error('⏰ Request timeout - Server may be slow');
    } else if (error.code === 'ECONNREFUSED') {
      console.error('🔌 Connection refused - Backend server may be down');
    } else if (!error.response) {
      console.error('🌐 Network error - Check internet connection');
    }
    
    console.groupEnd();
    
    return Promise.reject(error);
  }
);

// Health check function
export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// API endpoints
export const API_ENDPOINTS = {
  HEALTH: '/health',
  COMPANIES: '/api/v1/companies',
  CONTACTS: '/api/v1/contacts',
  PRODUCTS: '/api/v1/products',
} as const; 
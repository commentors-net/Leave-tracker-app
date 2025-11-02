// API Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const config = {
  apiUrl: API_URL,
  // Feature toggles
  features: {
    // Set to true to enable public registration
    // Set to false to disable registration link and route access
    enableRegistration: import.meta.env.VITE_ENABLE_REGISTRATION === 'true' || false,
  },
  endpoints: {
    auth: {
      register: `${API_URL}/auth/register`,
      login: `${API_URL}/auth/login`,
      changePassword: `${API_URL}/auth/change-password`,
    },
    people: `${API_URL}/api/people`,
    types: `${API_URL}/api/types`,
    absences: `${API_URL}/api/absences`,
  },
};

export default config;

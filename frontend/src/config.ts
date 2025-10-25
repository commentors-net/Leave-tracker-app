// API Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const config = {
  apiUrl: API_URL,
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

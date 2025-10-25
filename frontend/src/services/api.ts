import axios from "axios";
import type { AxiosInstance } from "axios";
import config from "@/config";

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: config.apiUrl,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors (token expired)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, clear storage and redirect to login
      localStorage.removeItem("access_token");
      localStorage.removeItem("username");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// ============================================
// Authentication API
// ============================================

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface RegisterResponse {
  qr: string;
  secret: string;
  username: string;
  id: number;
}

export interface LoginRequest {
  username: string;
  password: string;
  token: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  username: string;
}

export const authApi = {
  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await axios.post(config.endpoints.auth.register, data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await axios.post(config.endpoints.auth.login, data);
    return response.data;
  },

  changePassword: async (data: {
    username: string;
    old_password: string;
    new_password: string;
  }): Promise<{ message: string }> => {
    const response = await apiClient.post("/auth/change-password", data);
    return response.data;
  },
};

// ============================================
// People API
// ============================================

export interface Person {
  id: number;
  name: string;
}

export interface PersonCreate {
  name: string;
}

export const peopleApi = {
  getAll: async (): Promise<Person[]> => {
    const response = await apiClient.get(config.endpoints.people);
    return response.data;
  },

  create: async (data: PersonCreate): Promise<Person> => {
    const response = await apiClient.post(config.endpoints.people, data);
    return response.data;
  },

  update: async (id: number, data: PersonCreate): Promise<Person> => {
    const response = await apiClient.put(`${config.endpoints.people}/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`${config.endpoints.people}/${id}`);
    return response.data;
  },
};

// ============================================
// Leave Types API
// ============================================

export interface LeaveType {
  id: number;
  name: string;
}

export interface LeaveTypeCreate {
  name: string;
}

export const typesApi = {
  getAll: async (): Promise<LeaveType[]> => {
    const response = await apiClient.get(config.endpoints.types);
    return response.data;
  },

  create: async (data: LeaveTypeCreate): Promise<LeaveType> => {
    const response = await apiClient.post(config.endpoints.types, data);
    return response.data;
  },

  update: async (id: number, data: LeaveTypeCreate): Promise<LeaveType> => {
    const response = await apiClient.put(`${config.endpoints.types}/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<{ message: string }> => {
    const response = await apiClient.delete(`${config.endpoints.types}/${id}`);
    return response.data;
  },
};

// ============================================
// Absences API
// ============================================

export interface Absence {
  id: number;
  person_id: number;
  date: string;
  duration: string;
  type_id: number;
  reason: string;
}

export interface AbsenceCreate {
  person_id: number;
  date: string;
  duration: string;
  type_id: number;
  reason: string;
}

export const absencesApi = {
  getAll: async (): Promise<Absence[]> => {
    const response = await apiClient.get(config.endpoints.absences);
    return response.data;
  },

  create: async (data: AbsenceCreate): Promise<Absence> => {
    const response = await apiClient.post(config.endpoints.absences, data);
    return response.data;
  },
};

// Export the configured axios instance for custom requests if needed
export default apiClient;

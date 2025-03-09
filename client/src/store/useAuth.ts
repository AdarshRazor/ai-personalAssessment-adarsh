import { create } from "zustand";

interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  role: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  setAuthenticated: (value: boolean) => void;
  checkAuth: () => Promise<string | undefined>;
  logout: () => void;
  setUser: (user: User | null) => void;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  login: async (email: string, password: string): Promise<void> => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetch('http://localhost:8000/api/auth/token', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Login failed');
      }

      const data: LoginResponse = await res.json();

      if (!data.access_token) {
        throw new Error('No access token received');
      }

      const userResponse = await fetch('http://localhost:8000/api/auth/users/me', {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      if (!userResponse.ok) {
        throw new Error('Failed to fetch user data');
      }

      const userData: User = await userResponse.json();
      set({ isAuthenticated: true, user: userData });
      localStorage.setItem('token', data.access_token);
    } catch (error) {
      console.error('Login error:', error);
      set({ isAuthenticated: false, user: null });
      localStorage.removeItem('token');
      throw error;
    }
  },
  setAuthenticated: (value) => set({ isAuthenticated: value }),
  checkAuth: async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        set({ isAuthenticated: false, user: null });
        return undefined;
      }

      const userResponse = await fetch('http://localhost:8000/api/auth/users/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!userResponse.ok) {
        throw new Error('Failed to validate token');
      }

      const userData: User = await userResponse.json();

      const currentUser = get().user; // Get current user from store

      if (currentUser && JSON.stringify(currentUser) === JSON.stringify(userData)) {
          // User data hasn't changed, no need to update
          return token;
      }

      set({ isAuthenticated: true, user: userData });
      return token;
    } catch (error) {
      console.error('Auth check error:', error);
      localStorage.removeItem("token");
      set({ isAuthenticated: false, user: null });
      return undefined;
    }
  },
  logout: () => {
    localStorage.removeItem("token"); // Clear the token
    set({ isAuthenticated: false, user: null });
  },
  setUser: (user) => set({ user }),
}));
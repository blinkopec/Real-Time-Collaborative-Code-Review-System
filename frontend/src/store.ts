import { create } from "zustand";
import { fetchMe, type User } from "./assets/api";

type AuthState = {
  user: User | null;
  loading: boolean;
  loadUser: () => Promise<void>;
  logout: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  user: null,
  loading: true,

  loadUser: async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      set({ user: null, loading: false });
      return;
    }
    try {
      const user = await fetchMe();
      set({ user, loading: false });
    } catch (error) {
      localStorage.removeItem("token");
      set({ user: null, loading: false });
    }
  },
  logout: () => {
    localStorage.removeItem("token");
    set({ user: null });
  },
}));

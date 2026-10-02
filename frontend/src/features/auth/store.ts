import { create } from "zustand";

export type User = { id: string; email: string; first_name: string; last_name: string; role: string };
type AuthState = { user: User | null; setUser: (user: User | null) => void; logout: () => void };

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem("pharmacy_user") ?? "null") as User | null,
  setUser: (user) => {
    if (user) localStorage.setItem("pharmacy_user", JSON.stringify(user));
    else localStorage.removeItem("pharmacy_user");
    set({ user });
  },
  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("pharmacy_user");
    set({ user: null });
  },
}));

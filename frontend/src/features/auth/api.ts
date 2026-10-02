import { api } from "../../lib/api";
import type { User } from "./store";

type AuthResponse = { access: string; refresh: string; user: User };

export async function authenticate(
  mode: "login" | "register",
  payload: Record<string, string>,
): Promise<User> {
  const { data } = await api.post<AuthResponse>(`/auth/${mode}/`, payload);
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  return data.user;
}

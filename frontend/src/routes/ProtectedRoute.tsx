import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../features/auth/store";

export function ProtectedRoute() {
  return useAuthStore((state) => state.user) ? <Outlet /> : <Navigate to="/login" replace />;
}


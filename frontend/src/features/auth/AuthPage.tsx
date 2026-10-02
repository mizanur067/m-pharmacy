import { FormEvent, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { authenticate } from "./api";
import { useAuthStore } from "./store";

export function AuthPage() {
  const location = useLocation();
  const isRegister = location.pathname === "/register";
  const [role, setRole] = useState("customer");
  const [error, setError] = useState("");
  const setUser = useAuthStore((state) => state.setUser);
  const navigate = useNavigate();

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const values = Object.fromEntries(new FormData(event.currentTarget).entries()) as Record<string, string>;
    try {
      const user = await authenticate(isRegister ? "register" : "login", { ...values, ...(isRegister ? { role } : {}) });
      setUser(user);
      navigate(user.role === "pharmacy_owner" ? "/owner/inventory" : "/medicines");
    } catch {
      setError("Unable to authenticate. Check your details and try again.");
    }
  }

  return (
    <section className="auth-shell">
      <form className="auth-card" onSubmit={submit}>
        <p className="eyebrow">{isRegister ? "Create your account" : "Welcome back"}</p>
        <h1>{isRegister ? "Join the pharmacy platform" : "Sign in to continue"}</h1>
        {isRegister && <div className="role-choice"><button type="button" className={role === "customer" ? "selected" : ""} onClick={() => setRole("customer")}>Customer</button><button type="button" className={role === "pharmacy_owner" ? "selected" : ""} onClick={() => setRole("pharmacy_owner")}>Pharmacy owner</button></div>}
        {isRegister && <><label>First name<input name="first_name" required /></label><label>Last name<input name="last_name" required /></label></>}
        <label>Email<input name="email" type="email" required /></label>
        <label>Password<input name="password" type="password" minLength={8} required /></label>
        {error && <p className="notice error">{error}</p>}
        <button className="button full" type="submit">{isRegister ? "Create account" : "Sign in"}</button>
        <p className="form-foot">{isRegister ? "Already registered?" : "New to the platform?"} <Link to={isRegister ? "/login" : "/register"}>{isRegister ? "Sign in" : "Create an account"}</Link></p>
      </form>
    </section>
  );
}

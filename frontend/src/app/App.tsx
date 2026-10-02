import { Link, Outlet } from "react-router-dom";
import "./styles.css";
import { useAuthStore } from "../features/auth/store";

export function App() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  return (
    <>
      <header className="site-header">
        <Link className="brand" to="/">Pharmacy Platform</Link>
        <nav className="nav">
          <Link to="/medicines">Medicines</Link>
          <Link to="/owner/inventory">Owner inventory</Link>
          <Link to="/owner/medicines/new">Upload medicine</Link>
          {user && <Link to="/cart">Cart</Link>}
          {user ? <button className="nav-button" onClick={logout}>Sign out</button> : <><Link to="/login">Sign in</Link><Link className="nav-cta" to="/register">Join us</Link></>}
          <a href="http://localhost:8000/api/docs/" target="_blank" rel="noreferrer">API docs</a>
        </nav>
      </header>
      <main><Outlet /></main>
    </>
  );
}

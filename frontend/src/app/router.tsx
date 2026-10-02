import { createBrowserRouter } from "react-router-dom";
import { Link } from "react-router-dom";
import { App } from "./App";
import { InventoryPage } from "../features/pharmacy-owner/InventoryPage";
import { MedicineListPage } from "../features/medicines/MedicineListPage";
import { AuthPage } from "../features/auth/AuthPage";
import { CartPage } from "../features/cart/CartPage";
import { MedicineUploadPage } from "../features/pharmacy-owner/MedicineUploadPage";
import { OwnerDashboardPage } from "../features/owner-dashboard/OwnerDashboardPage";
import { NewsSection } from "../features/news/NewsSection";
import { OrderHistoryPage } from "../features/orders/OrderHistoryPage";

export const router = createBrowserRouter([{
  path: "/", element: <App />, children: [
    { index: true, element: <HomePage /> },
    { path: "medicines", element: <MedicineListPage /> },
    { path: "owner/inventory", element: <InventoryPage /> },
    { path: "owner/medicines/new", element: <MedicineUploadPage /> },
    { path: "owner/dashboard", element: <OwnerDashboardPage /> },
    { path: "login", element: <AuthPage /> },
    { path: "register", element: <AuthPage /> },
    { path: "cart", element: <CartPage /> },
    { path: "orders", element: <OrderHistoryPage /> },
  ],
}]);

function HomePage() {
  return (
    <section className="page">
      <div className="hero">
        <p className="eyebrow">Trusted pharmacy marketplace</p>
        <h1>Healthcare made simpler.</h1>
        <p>Browse medicines from verified pharmacies and manage your pharmacy inventory from one place.</p>
        <Link className="button" to="/medicines">Browse medicines</Link>
      </div>
      <NewsSection />
    </section>
  );
}

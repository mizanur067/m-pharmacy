import { useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getAvailableStocks, getMedicines } from "./api";
import { addToCart } from "../cart/api";
import { useAuthStore } from "../auth/store";

export function MedicineListPage() {
  const [search, setSearch] = useState("");
  const medicines = useQuery({
    queryKey: ["medicines", search],
    queryFn: () => getMedicines(search),
  });
  const [showSignInPrompt, setShowSignInPrompt] = useState(false);
  const user = useAuthStore((state) => state.user);
  const stocks = useQuery({ queryKey: ["available-stocks"], queryFn: getAvailableStocks });
  const [cartMessage, setCartMessage] = useState("");

  return (
    <section className="page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Browse our catalog</p>
          <h1>Find your medicine</h1>
        </div>
        <input
          aria-label="Search medicines"
          className="search"
          placeholder="Search by medicine name..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>
      {medicines.isLoading && <p>Loading medicines...</p>}
      {medicines.isError && (
        <p className="notice error">The API is not reachable. Start Django with <code>python backend\manage.py runserver</code>.</p>
      )}
      {medicines.data?.length === 0 && <p className="notice">No medicines found.</p>}
      <div className="medicine-grid">
        {medicines.data?.map((medicine) => (
          <article className="card" key={medicine.id}>
            <div className="card-icon">Rx</div>
            <h2>{medicine.name}</h2>
            <p>{medicine.generic_name}</p>
            <span>{medicine.dosage_form} · {medicine.strength}</span>
            {medicine.requires_prescription && <strong>Prescription required</strong>}
            <button className="button card-button" onClick={async () => {
              if (!user) {
                setShowSignInPrompt(true);
                return;
              }
              const stock = stocks.data?.find((item) => item.medicine === medicine.id);
              if (!stock) {
                setCartMessage("This medicine is currently out of stock.");
                return;
              }
              await addToCart(stock.id, 1);
              setCartMessage(`${medicine.name} was added to your cart.`);
            }}>Add to cart</button>
          </article>
        ))}
      </div>
      {cartMessage && <p className="notice">{cartMessage}</p>}
      {showSignInPrompt && (
        <div className="modal-backdrop" role="presentation" onClick={() => setShowSignInPrompt(false)}>
          <section
            aria-labelledby="sign-in-prompt-title"
            aria-modal="true"
            className="modal-card"
            role="dialog"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              aria-label="Close sign-in prompt"
              className="modal-close"
              onClick={() => setShowSignInPrompt(false)}
              type="button"
            >
              ×
            </button>
            <div className="modal-icon">🛒</div>
            <p className="eyebrow">Almost there</p>
            <h2 id="sign-in-prompt-title">Sign in to add medicines</h2>
            <p className="modal-description">
              Create an account or sign in to add medicines to your cart and place an order.
            </p>
            <div className="modal-actions">
              <Link className="button full" to="/login">Sign in</Link>
              <Link className="secondary-button full" to="/register">Create account</Link>
            </div>
          </section>
        </div>
      )}
    </section>
  );
}

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getMedicines } from "./api";

export function MedicineListPage() {
  const [search, setSearch] = useState("");
  const medicines = useQuery({
    queryKey: ["medicines", search],
    queryFn: () => getMedicines(search),
  });
  const [message, setMessage] = useState("");

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
            <button className="button card-button" onClick={async () => setMessage("Sign in before adding medicines to your cart.")}>Add to cart</button>
          </article>
        ))}
      </div>
      {message && <p className="notice">{message}</p>}
    </section>
  );
}

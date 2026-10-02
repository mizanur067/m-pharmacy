import { FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { api } from "../../lib/api";

type MedicineForm = {
  name: string; generic_name: string; category: string; manufacturer: string;
  dosage_form: string; strength: string; description: string; slug: string;
};

async function createMedicine(payload: MedicineForm) {
  return (await api.post("/catalog/medicines/", payload)).data;
}

export function MedicineUploadPage() {
  const [saved, setSaved] = useState(false);
  const mutation = useMutation({ mutationFn: createMedicine, onSuccess: () => setSaved(true) });
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaved(false);
    const values = Object.fromEntries(new FormData(event.currentTarget).entries()) as unknown as MedicineForm;
    mutation.mutate(values);
  }

  return <section className="page narrow-page"><p className="eyebrow">Owner workspace</p><h1>Add a medicine</h1>
    <p className="muted">Create the medicine record first, then add its pharmacy stock from Inventory. Category and manufacturer IDs come from the admin catalog.</p>
    <form className="auth-card wide-card" onSubmit={submit}>
      <div className="form-two"><label>Medicine name<input name="name" required /></label><label>Generic name<input name="generic_name" required /></label></div>
      <div className="form-two"><label>Category ID<input name="category" required /></label><label>Manufacturer ID<input name="manufacturer" required /></label></div>
      <div className="form-two"><label>Dosage form<input name="dosage_form" placeholder="Tablet" required /></label><label>Strength<input name="strength" placeholder="500mg" required /></label></div>
      <label>URL slug<input name="slug" required /></label><label>Description<textarea name="description" /></label>
      {mutation.isError && <p className="notice error">Could not save medicine. Check the IDs and sign in as a pharmacy owner.</p>}
      {saved && <p className="notice">Medicine saved successfully.</p>}
      <button className="button full" disabled={mutation.isPending}>{mutation.isPending ? "Saving..." : "Save medicine"}</button>
    </form>
  </section>;
}

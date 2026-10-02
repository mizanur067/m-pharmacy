import { api } from "../../lib/api";

export type Medicine = {
  id: string;
  name: string;
  generic_name: string;
  dosage_form: string;
  strength: string;
  description: string;
  requires_prescription: boolean;
};

export async function getMedicines(search = ""): Promise<Medicine[]> {
  const { data } = await api.get<{ results: Medicine[] }>("/catalog/medicines/", {
    params: search ? { search } : undefined,
  });
  return data.results;
}

export async function getAvailableStocks() {
  const { data } = await api.get<{ results: Array<{ id: string; medicine: string; price: string; pharmacy_name: string }> }>(
    "/inventory/stocks/",
  );
  return data.results;
}

export async function getStocksForMedicine(medicine: string) {
  const { data } = await api.get<{ results: Array<{ id: string; price: string; quantity: number; pharmacy_name: string }> }>(
    "/inventory/stocks/", { params: { medicine, is_available: true } },
  );
  return data.results;
}

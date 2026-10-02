import { api } from "../../lib/api";

export type Pharmacy = { id: string; name: string; verification_status: string };
export type Stock = {
  id: string;
  pharmacy_name: string;
  medicine_name: string;
  price: string;
  quantity: number;
  batch_number: string;
  expiry_date: string;
  is_available: boolean;
};

export async function getOwnedPharmacies(): Promise<Pharmacy[]> {
  const { data } = await api.get<{ results: Pharmacy[] }>("/pharmacies/");
  return data.results;
}

export async function getStocks(): Promise<Stock[]> {
  const { data } = await api.get<{ results: Stock[] }>("/inventory/stocks/");
  return data.results;
}

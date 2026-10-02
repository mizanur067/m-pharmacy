import { api } from "../../lib/api";

export type CartItem = { id: string; stock: string; medicine_name: string; pharmacy_name: string; quantity: number; unit_price: string; line_total: string };
export type Cart = { id: string; pharmacy: string | null; items: CartItem[]; total: string };

export async function getCart() { return (await api.get<Cart>("/cart/")).data; }
export async function addToCart(stock: string, quantity: number) { return (await api.post<Cart>("/cart/items/", { stock, quantity })).data; }
export async function placeOrder(address: string) { return (await api.post("/orders/place/", { address })).data; }

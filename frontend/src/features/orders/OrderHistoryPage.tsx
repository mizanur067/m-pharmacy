import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api";

type Order = { id: string; status: string; total: string; created_at: string; items: Array<{ medicine_name: string; quantity: number }> };

export function OrderHistoryPage() {
  const orders = useQuery({
    queryKey: ["orders"],
    queryFn: async () => (await api.get<{ results: Order[] }>("/orders/")).data.results,
  });
  return <section className="page"><p className="eyebrow">Your account</p><h1>Order history</h1>
    {orders.isLoading && <p>Loading orders...</p>}
    {!orders.isLoading && !orders.data?.length && <p className="notice">You have not placed an order yet.</p>}
    <div className="order-list">{orders.data?.map((order) => <article className="order-card" key={order.id}><div><strong>Order #{order.id.slice(0, 8)}</strong><span>{new Date(order.created_at).toLocaleDateString()}</span></div><div><span className="status-badge">{order.status}</span><strong>৳{order.total}</strong></div><p>{order.items.map((item) => `${item.medicine_name} × ${item.quantity}`).join(", ")}</p></article>)}</div>
  </section>;
}

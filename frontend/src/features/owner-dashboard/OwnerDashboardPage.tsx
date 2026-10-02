import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api";

type Dashboard = { pharmacy: { name: string } | null; stock_count: number; units_available: number; low_stock: number };

export function OwnerDashboardPage() {
  const dashboard = useQuery({ queryKey: ["owner-dashboard"], queryFn: async () => (await api.get<Dashboard>("/pharmacies/dashboard/")).data });
  if (dashboard.isLoading) return <section className="page"><p>Loading dashboard...</p></section>;
  const data = dashboard.data;
  return <section className="page"><p className="eyebrow">M-Pharmacy operations</p><h1>{data?.pharmacy?.name ?? "Owner dashboard"}</h1><div className="metric-grid">
    <div className="metric-card"><span>Medicine records</span><strong>{data?.stock_count ?? 0}</strong></div>
    <div className="metric-card"><span>Available units</span><strong>{data?.units_available ?? 0}</strong></div>
    <div className="metric-card warning"><span>Low stock items</span><strong>{data?.low_stock ?? 0}</strong></div>
  </div><div className="dashboard-actions"><a className="button" href="/owner/medicines/new">Add medicine</a><a className="secondary-button" href="/owner/inventory">Edit prices and stock</a></div></section>;
}

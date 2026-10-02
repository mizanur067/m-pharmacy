import { useQuery } from "@tanstack/react-query";
import { getStocks } from "./api";

export function InventoryPage() {
  const stocks = useQuery({ queryKey: ["owner", "stocks"], queryFn: getStocks });

  if (stocks.isLoading) return <p>Loading inventory...</p>;
  if (stocks.isError) return <p role="alert">Unable to load inventory.</p>;

  return (
    <section>
      <h1>Inventory</h1>
      {stocks.data?.length ? (
        <table>
          <thead><tr><th>Medicine</th><th>Pharmacy</th><th>Price</th><th>Quantity</th><th>Expiry</th></tr></thead>
          <tbody>
            {stocks.data.map((stock) => (
              <tr key={stock.id}>
                <td>{stock.medicine_name}</td>
                <td>{stock.pharmacy_name}</td>
                <td>{stock.price}</td>
                <td>{stock.quantity}</td>
                <td>{stock.expiry_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : <p>Your inventory is empty.</p>}
    </section>
  );
}

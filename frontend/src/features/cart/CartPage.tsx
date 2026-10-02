import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { getCart, placeOrder } from "./api";

export function CartPage() {
  const [address, setAddress] = useState("");
  const queryClient = useQueryClient();
  const cart = useQuery({ queryKey: ["cart"], queryFn: getCart });
  const order = useMutation({ mutationFn: placeOrder, onSuccess: () => queryClient.invalidateQueries({ queryKey: ["cart"] }) });
  function submit(event: FormEvent) { event.preventDefault(); order.mutate(address); }
  if (cart.isLoading) return <section className="page"><p>Loading cart...</p></section>;
  return <section className="page"><div className="page-heading"><div><p className="eyebrow">Your basket</p><h1>Checkout</h1></div></div>
    {!cart.data?.items.length ? <p className="notice">Your cart is empty. <a href="/medicines">Browse medicines</a></p> : <div className="checkout-grid"><div className="cart-list">{cart.data.items.map((item) => <article className="cart-row" key={item.id}><div><strong>{item.medicine_name}</strong><span>{item.pharmacy_name} · Qty {item.quantity}</span></div><strong>৳{item.line_total}</strong></article>)}</div>
      <form className="auth-card" onSubmit={submit}><h2>Delivery details</h2><label>Address<textarea required minLength={5} value={address} onChange={(event) => setAddress(event.target.value)} /></label><p className="total">Total <strong>৳{cart.data.total}</strong></p><button className="button full" disabled={order.isPending}>{order.isPending ? "Placing order..." : "Place COD order"}</button>{order.isSuccess && <p className="notice">Order placed successfully.</p>}</form></div>}
  </section>;
}

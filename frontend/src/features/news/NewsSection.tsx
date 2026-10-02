import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api";

type Article = { id: string; title: string; summary: string; body: string; published_at: string };

export function NewsSection() {
  const news = useQuery({
    queryKey: ["news"],
    queryFn: async () => (await api.get<{ results: Article[] }>("/news/")).data.results,
  });
  return <section className="news-section"><div className="section-heading"><div><p className="eyebrow">From M-Pharmacy</p><h2>Latest news</h2></div></div>
    <div className="news-grid">{news.data?.map((article) => <article className="news-card" key={article.id}><p className="news-date">{new Date(article.published_at).toLocaleDateString()}</p><h3>{article.title}</h3><p>{article.summary}</p><span>{article.body}</span></article>)}</div>
  </section>;
}

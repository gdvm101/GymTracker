import { useEffect, useState } from "react";
import { request } from "../api/httpClient.js";

export default function StatusPage() {
  const [attempt, setAttempt] = useState(0);
  const [connection, setConnection] = useState({ state: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    async function check() {
      try {
        const data = await request("GET", "/health", { signal: controller.signal });
        if (data?.status !== "ok") throw new Error("Сервер вернул неизвестное состояние.");
        if (!controller.signal.aborted) setConnection({ state: "ready" });
      } catch (error) {
        if (!controller.signal.aborted) setConnection({ state: "error", message: error.message });
      }
    }
    check();
    return () => controller.abort();
  }, [attempt]);

  function retry() {
    setConnection({ state: "loading" });
    setAttempt(previous => previous + 1);
  }

  const loading = connection.state === "loading";
  const messages = {
    loading: "Проверяем соединение…",
    ready: "Сервер и база данных отвечают.",
    error: connection.message,
  };
  return (
    <main className="container stage">
      <section aria-labelledby="title" className="intro">
        <h1 id="title">Ваши тренировки.<br /><span>Ваш прогресс.</span></h1>
        <p>Стенд разработки GymTracker</p>
      </section>
      <section className="status-card" aria-labelledby="connection">
        <h2 id="connection">Состояние подключения</h2>
        <p className="status-line" role="status">
          <span className={"dot " + connection.state} aria-hidden="true" />
          {messages[connection.state]}
        </p>
        <button type="button" onClick={retry} disabled={loading}>Проверить связь</button>
      </section>
    </main>
  );
}

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { request } from "./httpClient.js";

const fetchMock = vi.fn();
beforeEach(() => {
  fetchMock.mockReset();
  vi.stubGlobal("fetch", fetchMock);
});
afterEach(() => vi.unstubAllGlobals());

describe("HTTP-клиент", () => {
  it("отправляет запрос на свой origin и передаёт AbortSignal", async () => {
    const signal = new AbortController().signal;
    fetchMock.mockResolvedValue(Response.json({ status: "ok" }));
    await expect(request("GET", "/health", { signal, csrfToken: "secret" })).resolves.toEqual({ status: "ok" });
    const [path, options] = fetchMock.mock.calls[0];
    expect(path).toBe("/api/v1/health");
    expect(options).toMatchObject({ credentials: "same-origin", method: "GET", signal });
    expect(options.headers).not.toHaveProperty("Content-Type");
    expect(options.headers).not.toHaveProperty("X-CSRF-Token");
  });

  it("передаёт JSON и CSRF для изменения и принимает новый токен из ответа", async () => {
    const onCsrfToken = vi.fn();
    fetchMock.mockResolvedValue(Response.json({ saved: true }, { headers: { "X-CSRF-Token": "next" } }));
    await request("patch", "/example", { json: { value: 2 }, csrfToken: "current", onCsrfToken });
    expect(fetchMock.mock.calls[0][1]).toMatchObject({
      method: "PATCH", body: '{"value":2}',
      headers: { "Content-Type": "application/json", "X-CSRF-Token": "current" },
    });
    expect(onCsrfToken).toHaveBeenCalledWith("next");
  });

  it("принимает пустой ответ 204", async () => {
    fetchMock.mockResolvedValue(new Response(null, { status: 204 }));
    await expect(request("POST", "/example")).resolves.toBeNull();
  });

  it("сохраняет код, путь поля и идентификатор запроса из ErrorDTO", async () => {
    const details = { field: "exercises.0.sets.1.weight" };
    fetchMock.mockResolvedValue(Response.json({ error: { code: "INVALID_INPUT", message: "Проверьте вес.", details } },
      { status: 422, headers: { "X-Request-ID": "fixture" } }));
    await expect(request("POST", "/example", { json: {} })).rejects.toMatchObject({
      status: 422, code: "INVALID_INPUT", message: "Проверьте вес.", details, requestId: "fixture",
    });
  });

  it("различает обрыв связи и неизвестный формат ответа", async () => {
    fetchMock.mockRejectedValueOnce(new TypeError("Connection refused"));
    await expect(request("GET", "/health")).rejects.toMatchObject({ code: "NETWORK_ERROR" });
    fetchMock.mockResolvedValueOnce(new Response("Bad gateway", { status: 502 }));
    await expect(request("GET", "/health")).rejects.toMatchObject({ status: 502, code: "INVALID_RESPONSE" });
  });

  it("сохраняет отмену запроса", async () => {
    const controller = new AbortController();
    controller.abort();
    fetchMock.mockRejectedValue(controller.signal.reason);
    await expect(request("GET", "/health", { signal: controller.signal }))
      .rejects.toBe(controller.signal.reason);
  });
});

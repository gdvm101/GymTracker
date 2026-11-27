const apiRoot = "/api/v1";

export class ApiError extends Error {
  constructor(status, code, message, details = null, requestId = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
    this.requestId = requestId;
  }
}

export async function request(method, path, { json, signal, csrfToken, onCsrfToken } = {}) {
  const verb = method.toUpperCase();
  const headers = { Accept: "application/json" };
  if (json !== undefined) headers["Content-Type"] = "application/json";
  if (csrfToken && !["GET", "HEAD", "OPTIONS"].includes(verb)) {
    headers["X-CSRF-Token"] = csrfToken;
  }

  let response;
  try {
    response = await fetch(apiRoot + path, {
      method: verb, headers, credentials: "same-origin", signal,
      body: json === undefined ? undefined : JSON.stringify(json),
    });
  } catch (error) {
    if (signal?.aborted || error.name === "AbortError") throw error;
    throw new ApiError(0, "NETWORK_ERROR", "Не удалось связаться с сервером.");
  }

  const requestId = response.headers.get("X-Request-ID");
  let data = null;
  if (response.status !== 204) {
    try {
      data = await response.json();
    } catch (error) {
      if (signal?.aborted || error.name === "AbortError") throw error;
      throw new ApiError(response.status, "INVALID_RESPONSE", "Не удалось прочитать ответ сервера.", null, requestId);
    }
  }
  if (!response.ok) {
    throw new ApiError(response.status, data?.error?.code ?? "HTTP_ERROR",
      data?.error?.message ?? "Не удалось выполнить запрос.", data?.error?.details ?? null, requestId);
  }
  const token = response.headers.get("X-CSRF-Token");
  if (token) onCsrfToken?.(token);
  return data;
}

import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, "../backend", ["FEATURES", "AI_ENABLED"]);
  const clientEnv = loadEnv(mode, process.cwd(), "VITE_");
  // Only the public feature flags are embedded into the client.
  return {
    plugins: [react()],
    define: {
      "import.meta.env.VITE_FEATURES": JSON.stringify(clientEnv.VITE_FEATURES ?? env.FEATURES ?? ""),
      "import.meta.env.VITE_AI_ENABLED": JSON.stringify(clientEnv.VITE_AI_ENABLED ?? env.AI_ENABLED ?? "false"),
    },
    server: {
      proxy: { "/api/v1": { target: "http://127.0.0.1:8000" } },
    },
  };
});

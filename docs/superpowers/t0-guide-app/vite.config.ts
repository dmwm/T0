import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "@repo": path.resolve(__dirname, "../../.."),
    },
  },
  server: {
    port: 5173,
    open: false,
    fs: {
      allow: [path.resolve(__dirname, "../../..")],
    },
  },
});

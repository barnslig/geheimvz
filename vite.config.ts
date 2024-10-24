import { defineConfig } from "vite";

export default defineConfig({
  base: "/static/core/assets/",
  build: {
    manifest: "manifest.json",
    outDir: "core/static/core/assets/",
    rollupOptions: {
      input: "core/assets/main.ts",
    },
  },
});

import multiThemePlugin from "tailwindcss-themer";

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "*/components/**/*.html",
    "*/templates/**/*.html",
    "*/assets/**/*.{js,ts,jsx,tsx}",
    "**/*.py",
  ],
  safelist: ["theme-blue", "theme-green", "theme-dark", "theme-contrast"],
  theme: {
    extend: {
      fontFamily: {
        comic: "'Comic Neue', 'Comic Sans MS', 'Comic Sans', cursive",
      },
    },
  },
  plugins: [
    multiThemePlugin({
      defaultTheme: {
        extend: {
          colors: {
            primary: {
              100: "#fb7185", // rose-400 -- background light
              200: "#f43f5e", // rose-500 -- background
              300: "#e11d48", // rose-600 -- border
              content: "#fff", // white
              accent: "#f43f5e", // rose-500
            },

            secondary: {
              100: "#ffe4e6", // rose-100 -- background light
              200: "#fecdd3", // rose-200 -- background
              300: "#fda4af", // rose-300 -- border
              content: "#be123c", // rose-700
            },

            neutral: {
              200: "#f1f5f9", // slate-100 -- background
              300: "#fda4af", // rose-300  -- border
              content: "#000", // black
            },

            base: {
              100: "#ffffff", // white    -- background light
              200: "#fff1f2", // rose-50  -- background
              300: "#fecdd3", // rose-200 -- border
              content: "#000", // black
              accent: "#64748b", // slate-500
            },

            success: {
              200: "#4ade80", // green-400 -- background
              content: "#000", // black
            },
          },
        },
      },
      themes: [
        {
          name: "theme-dark",
          extend: {
            colors: {
              primary: {
                100: "#22c55e", // green-500 -- background light
                200: "#16a34a", // green-600 -- background
                300: "#14532d", // green-900 -- border
                content: "#020617", // slate-950
                accent: "#4ade80", // green-400
              },

              secondary: {
                100: "#0f172a", // slate-900
                200: "#020617", // slate-950 -- background
                300: "#14532d", // green-900 -- border
                content: "#4ade80", // green-400
              },

              neutral: {
                200: "#020617", // slate-950 -- background
                300: "#14532d", // green-900 -- border
                content: "#94a3b8", // slate-400
              },

              base: {
                100: "#0f172a", // slate-900 -- background light
                200: "#020617", // slate-950 -- background
                300: "#0f172a", // slate-900 -- border
                content: "#94a3b8", // slate-400
                accent: "#64748b", // slate-500
              },
            },
          },
        },
        {
          name: "theme-blue",
          extend: {
            colors: {
              primary: {
                100: "#60a5fa", // blue-400 -- background light
                200: "#3b82f6", // blue-500 -- background
                300: "#2563eb", // blue-600 -- border
                accent: "#3b82f6", // blue-500
              },

              secondary: {
                100: "#dbeafe", // blue-100 -- background light
                200: "#bfdbfe", // blue-200 -- background
                300: "#93c5fd", // blue-300 -- border
                content: "#1d4ed8", // blue-700
              },

              neutral: {
                300: "#93c5fd", // blue-300 -- border
              },

              base: {
                200: "#eff6ff", // blue-50  -- background
                300: "#bfdbfe", // blue-200 -- border
              },
            },
          },
        },
        {
          name: "theme-green",
          extend: {
            colors: {
              primary: {
                100: "#34d399", // emerald-400 -- background light
                200: "#10b981", // emerald-500 -- background
                300: "#059669", // emerald-600 -- border
                accent: "#10b981", // emerald-500
              },

              secondary: {
                100: "#d1fae5", // emerald-100 -- background light
                200: "#a7f3d0", // emerald-200 -- background
                300: "#6ee7b7", // emerald-300 -- border
                content: "#047857", // emerald-700
              },

              neutral: {
                300: "#6ee7b7", // emerald-300 -- border
              },

              base: {
                200: "#ecfdf5", // emerald-50  -- background
                300: "#a7f3d0", // emerald-200 -- border
              },
            },
          },
        },
        {
          name: "theme-contrast",
          extend: {
            colors: {
              primary: {
                100: "#000",
                200: "#000",
                300: "#000",
                content: "#fff",
                accent: "#000",
              },

              secondary: {
                100: "#fff",
                200: "#fff",
                300: "#000",
                content: "#000",
              },

              neutral: {
                200: "#fff",
                300: "#000",
                content: "#000",
              },

              base: {
                200: "#fff",
                300: "#e2e8f0", // slate-200
                accent: "#000",
              },
            },
          },
        },
      ],
    }),
  ],
};

# SentinelAudit Frontend

This is the React + Vite frontend for SentinelAudit SaaS.

## Tech Stack
- React 18 + Vite
- Tailwind CSS
- shadcn/ui (Radix UI + utilities)
- TanStack Query
- React Router
- Axios

## Setup
1. Install dependencies:
	```sh
	npm install
	```
2. Tailwind and shadcn/ui are preconfigured. To add new UI components, use:
	```sh
	npx shadcn-ui@latest add <component>
	```
3. Start the dev server:
	```sh
	npm run dev
	```

## Project Structure
- `src/pages/` — App pages (landing, login, register, dashboard, upload, payment, report detail, reports list)
- `src/components/` — Reusable UI components

## Customization
Refer to the [shadcn/ui docs](https://ui.shadcn.com/docs/installation/vite) and [Tailwind CSS docs](https://tailwindcss.com/docs/installation) for advanced usage.

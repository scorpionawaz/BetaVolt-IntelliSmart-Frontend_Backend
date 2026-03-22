# ⚡ Instinct | Smart Energy Management System

Instinct (BetaVolt Instinct 4.0) is a cutting-edge **Smart Energy Super App** designed to bridge the gap between grid operators and consumers. It provides real-time telemetry, AI-driven energy insights, and a seamless management interface for both administrative and consumer roles.

---

## 🚀 Quick Links
- **[Development Dashboard](DEVELOPMENT.md)** - Detailed project status and roadmap.
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Technical deep dive into the stack.
- **[AI Capabilities](docs/AI_AGENT.md)** - Understanding the Genkit integration.

---

## ✨ Key Features

### 👤 Consumer Experience
- **Real-time Home Hub**: Monitor solar production, battery storage, and home consumption in one unified view.
- **AI Concierge**: A Genkit-powered AI agent that helps users understand their energy bills and provides personalized optimization tips.
- **Smart Analytics**: Deep-dive into energy patterns with interactive charts powered by Recharts.
- **Dynamic Billing**: Access invoices, track payment history, and manage prepaid/postpaid accounts.

### 🛠️ Admin CommandCenter
- **Grid Telemetry**: High-level overview of total grid load, active consumers, and system alerts.
- **Intelligent Ticketing**: Auto-assigning support tickets using AI to ensure rapid resolution.
- **Project Hub**: Manage fleet-scale installations and large-scale energy projects.

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | [Next.js 15](https://nextjs.org/) (App Router), [React 19](https://react.dev/) |
| **Styling** | [Tailwind CSS](https://tailwindcss.com/), [Radix UI](https://www.radix-ui.com/), [Lucide](https://lucide.dev/) |
| **AI Engine**| [Firebase Genkit](https://github.com/firebase/genkit), [Google Gemini](https://deepmind.google/technologies/gemini/) |
| **Backend** | [Firebase](https://firebase.google.com/), [Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) |
| **Data Viz** | [Recharts](https://recharts.org/) |
| **Validation**| [Zod](https://zod.dev/) |

---

## 🏃 Getting Started

1. **Clone and Install**:
```bash
npm install
```

2. **Environment Setup**:
Create a `.env` file with your Firebase and Google Generative AI keys.

3. **Run Development Server**:
```bash
npm run dev
# Dashboard available at http://localhost:9002
```

4. **Run AI Development Tools**:
```bash
npm run genkit:dev
```

---

## 📈 Project Status

- [x] **Core UI/UX Structure**: Premium dark mode ready shell and navigation.
- [x] **AI Integration**: Genkit flow for consumption analysis implemented.
- [/] **Consumer Modules**: Analytics and Support are in advanced stages.
- [/] **Admin CommandCenter**: Core telemetry views implemented with placeholders for live data.
- [ ] **Live Telemetry Connection**: WebSocket implementation for real-time grid updates (In Progress).

---

Developed with ❤️ by the **BetaVolt Team**.

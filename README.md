# 🚏 Onibus Pulse

A clean, web-based notification wrapper for onibus.info.

Onibus Pulse actively monitors selected bus routes and stops and sends browser push notifications when your bus is approaching — so you never have to manually refresh the tracking page again.

---

## ✨ Why This Exists

The original website — https://onibus.info — is passive.  
Users must manually refresh the page to see updated ETAs.

Onibus Pulse transforms that experience into:

- Active monitoring
- Background polling
- Smart alerts
- Clean dashboard experience
- Browser notifications

---

## 🎯 Core Features (MVP)

### 🌐 Web-Only Application
- Works in desktop and mobile browsers
- No installation required
- No native app
- No authentication (anonymous usage)

### 🚌 Route & Stop Monitoring
- Select one or more bus routes
- Select one or more stops per route
- Monitor multiple alerts simultaneously

### 🔔 Smart Alerts
- Notify when ETA is below X minutes
- One-time alerts
- Recurring alerts
- Background polling

Example notification:

> “Bus 512 arriving in 4 minutes”

### 📊 Clean Dashboard
- Watched routes and stops
- Current ETA
- Alert status (Armed / Triggered / Paused)
- Add, edit, pause, or remove alerts easily
- Polished typography and spacing

---

## 🧠 How It Works

There is **no public API** available.

Data is retrieved by:

- Observing network requests used by the original site  
  **OR**
- Scraping structured HTML responses

To ensure reliability:

- Rate limiting is implemented
- Request caching reduces unnecessary load
- Graceful failure handling if layout changes
- Defensive parsing strategies

Reliability is prioritized over aggressive scraping.

---

## 🏗 Architecture Principles

- Maintainable and modular code
- Clear separation between:
  - Data fetch layer
  - Alert engine
  - UI layer
- Easily extensible for:
  - Mobile app
  - Real-time updates
  - Lock screen notifications
  - Public API layer

---

## 🚦 User Flow

1. User selects one or more routes
2. User selects stops per route
3. User defines alert rule:
   - Notify when ETA < X minutes
   - One-time or recurring
4. App polls ETA periodically
5. When conditions are met:
   - Browser push notification is sent

---

## 🔐 Notifications

Uses the standard Web Notification API.

- Requires browser permission
- Simple alert messages
- No background service workers beyond polling needs (MVP scope)

---

## 🧩 Future Ideas

- Service Worker for smarter background sync
- Progressive Web App (PWA)
- Real-time WebSocket support (if available)
- Push server for cross-device notifications
- Saved presets
- Dark mode
- Multi-city support

---

## ⚠ Disclaimer

This project is an independent wrapper built around publicly accessible data from https://onibus.info.

It is not affiliated with or endorsed by the original service.

---

## 📜 License

MIT License

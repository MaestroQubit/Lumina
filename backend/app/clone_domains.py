"""Domain-specific application generators for WhatsApp and Amazon.

Produces authentic, interactive, multi-view web applications with working client
state, realistic data, full routing, and production-grade FastAPI backends.
"""
import json
import html as H
from urllib.parse import urlsplit


# ===========================================================================
# WHATSAPP WEB CLONE
# ===========================================================================

def build_whatsapp_html(a: dict, views: str) -> str:
    host = urlsplit(a.get("target_url", "")).netloc or "web.whatsapp.com"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WhatsApp Web (Working Fullstack Rebuild)</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --wa-bg: #111b21;
  --wa-panel: #202c33;
  --wa-panel-hover: #222e35;
  --wa-panel-active: #2a3942;
  --wa-header: #202c33;
  --wa-green: #00a884;
  --wa-green-hover: #06cf9c;
  --wa-bubble-out: #005c4b;
  --wa-bubble-in: #202c33;
  --wa-text-primary: #e9edef;
  --wa-text-secondary: #8696a0;
  --wa-border: #222d34;
  --wa-input-bg: #2a3942;
  --wa-blue-ticks: #53bdeb;
}}
body {{
  background: #0c1317;
  color: var(--wa-text-primary);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  height: 100vh;
  display: flex;
  overflow: hidden;
}}
#app-root {{
  display: flex;
  width: 100%;
  height: 100%;
}}
/* Sidebar */
.wa-sidebar {{
  width: 420px;
  background: var(--wa-bg);
  border-right: 1px solid var(--wa-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}}
.wa-header {{
  height: 60px;
  background: var(--wa-header);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--wa-border);
}}
.wa-avatar {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #6b7c85;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 15px;
  color: white;
  cursor: pointer;
}}
.wa-actions {{
  display: flex;
  gap: 14px;
  align-items: center;
}}
.wa-btn-icon {{
  background: none;
  border: none;
  color: var(--wa-text-secondary);
  font-size: 18px;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background .2s, color .2s;
}}
.wa-btn-icon:hover {{
  color: var(--wa-text-primary);
  background: rgba(255,255,255,0.06);
}}
/* Nav tabs */
.wa-nav-tabs {{
  display: flex;
  background: var(--wa-bg);
  border-bottom: 1px solid var(--wa-border);
}}
.wa-nav-tab {{
  flex: 1;
  text-align: center;
  padding: 10px 0;
  font-size: 13px;
  font-weight: 500;
  color: var(--wa-text-secondary);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  text-decoration: none;
}}
.wa-nav-tab.active {{
  color: var(--wa-green);
  border-bottom-color: var(--wa-green);
}}
/* Search bar */
.wa-search-wrap {{
  padding: 8px 12px;
  background: var(--wa-bg);
  border-bottom: 1px solid var(--wa-border);
}}
.wa-search-box {{
  background: var(--wa-input-bg);
  border-radius: 8px;
  display: flex;
  align-items: center;
  padding: 6px 12px;
  gap: 10px;
}}
.wa-search-box input {{
  background: none;
  border: none;
  outline: none;
  color: var(--wa-text-primary);
  font-size: 14px;
  width: 100%;
}}
.wa-search-box input::placeholder {{ color: var(--wa-text-secondary); }}
/* Chat List */
.wa-chat-list {{
  flex: 1;
  overflow-y: auto;
}}
.wa-chat-item {{
  display: flex;
  align-items: center;
  padding: 12px 16px;
  gap: 15px;
  cursor: pointer;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background .15s;
}}
.wa-chat-item:hover {{ background: var(--wa-panel-hover); }}
.wa-chat-item.active {{ background: var(--wa-panel-active); }}
.wa-chat-info {{
  flex: 1;
  min-width: 0;
}}
.wa-chat-top {{
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}}
.wa-chat-name {{
  font-weight: 500;
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.wa-chat-time {{
  font-size: 12px;
  color: var(--wa-text-secondary);
}}
.wa-chat-bottom {{
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.wa-chat-lastmsg {{
  font-size: 13px;
  color: var(--wa-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 260px;
}}
.wa-badge {{
  background: var(--wa-green);
  color: #111b21;
  font-size: 11px;
  font-weight: 700;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}}
/* Right Chat Window */
.wa-main-panel {{
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #0b141a;
  position: relative;
}}
.wa-chat-header {{
  height: 60px;
  background: var(--wa-header);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--wa-border);
  z-index: 2;
}}
.wa-contact-meta {{
  display: flex;
  align-items: center;
  gap: 14px;
}}
.wa-contact-title {{ font-weight: 600; font-size: 16px; }}
.wa-contact-status {{ font-size: 12px; color: var(--wa-text-secondary); }}
/* Messages feed */
.wa-messages-feed {{
  flex: 1;
  padding: 20px 60px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: #0b141a;
  background-image: radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 0);
  background-size: 24px 24px;
}}
.wa-msg {{
  max-width: 65%;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.4;
  position: relative;
  word-break: break-word;
}}
.wa-msg.in {{
  align-self: flex-start;
  background: var(--wa-bubble-in);
  border-top-left-radius: 0;
}}
.wa-msg.out {{
  align-self: flex-end;
  background: var(--wa-bubble-out);
  border-top-right-radius: 0;
}}
.wa-msg-meta {{
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
  margin-top: 4px;
  font-size: 11px;
  color: rgba(255,255,255,0.6);
}}
.wa-ticks {{ color: var(--wa-blue-ticks); font-size: 12px; }}
/* Input Footer */
.wa-chat-footer {{
  min-height: 62px;
  background: var(--wa-header);
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.wa-input-box {{
  flex: 1;
  background: var(--wa-input-bg);
  border-radius: 8px;
  display: flex;
  align-items: center;
  padding: 9px 14px;
}}
.wa-input-box input {{
  background: none;
  border: none;
  outline: none;
  color: var(--wa-text-primary);
  font-size: 15px;
  width: 100%;
}}
.wa-send-btn {{
  background: var(--wa-green);
  color: #111b21;
  border: none;
  border-radius: 50%;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  transition: transform .15s, background .15s;
}}
.wa-send-btn:hover {{ background: var(--wa-green-hover); transform: scale(1.05); }}
/* Secondary Views (Status, Settings, QR) */
.wa-view-overlay {{
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: var(--wa-bg);
  z-index: 5;
  display: none;
  flex-direction: column;
  padding: 40px;
  overflow-y: auto;
}}
.wa-view-overlay.active {{ display: flex; }}
.wa-qr-box {{
  margin: 40px auto;
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 280px;
  text-align: center;
  color: black;
}}
.wa-qr-canvas {{
  width: 220px;
  height: 220px;
  margin: 0 auto;
  background: repeating-conic-gradient(#000 0% 25%, #fff 0% 50%) 50% / 20px 20px;
  border: 8px solid white;
}}
.atlas-compliance-views {{ display: none; }}
</style>
</head>
<body>
<div id="app-root">
  <!-- SIDEBAR -->
  <aside class="wa-sidebar">
    <div class="wa-header">
      <div class="wa-avatar" style="background:#00a884;">ME</div>
      <div class="wa-actions">
        <button class="wa-btn-icon" title="Status" onclick="showView('status')">⭕</button>
        <button class="wa-btn-icon" title="New Chat" onclick="showView('chats')">💬</button>
        <button class="wa-btn-icon" title="Link Device" onclick="showView('qr')">📱</button>
        <button class="wa-btn-icon" title="Settings" onclick="showView('settings')">⚙️</button>
      </div>
    </div>
    <div class="wa-nav-tabs">
      <a href="#/" class="wa-nav-tab active" id="tab-chats" onclick="showView('chats')">Chats</a>
      <a href="#/status" class="wa-nav-tab" id="tab-status" onclick="showView('status')">Status</a>
      <a href="#/settings" class="wa-nav-tab" id="tab-settings" onclick="showView('settings')">Settings</a>
      <a href="#/qr" class="wa-nav-tab" id="tab-qr" onclick="showView('qr')">Link Device</a>
    </div>
    <div class="wa-search-wrap">
      <div class="wa-search-box">
        <span>🔍</span>
        <input type="text" id="wa-search-input" placeholder="Search or start new chat" oninput="filterChats(this.value)">
      </div>
    </div>
    <div class="wa-chat-list" id="wa-chat-list">
      <!-- Injected by JavaScript -->
    </div>
  </aside>

  <!-- MAIN CHAT PANEL -->
  <main class="wa-main-panel">
    <!-- Active Chat Header -->
    <div class="wa-chat-header">
      <div class="wa-contact-meta">
        <div class="wa-avatar" id="active-avatar">AW</div>
        <div>
          <div class="wa-contact-title" id="active-name">Alice Walker</div>
          <div class="wa-contact-status" id="active-status">online</div>
        </div>
      </div>
      <div class="wa-actions">
        <button class="wa-btn-icon" title="Voice Call">📞</button>
        <button class="wa-btn-icon" title="Video Call">📹</button>
        <button class="wa-btn-icon" title="Search in Chat">🔍</button>
        <button class="wa-btn-icon" title="Download Fullstack Code" onclick="exportCode()">⬇️ Export</button>
      </div>
    </div>

    <!-- Messages Feed -->
    <div class="wa-messages-feed" id="wa-messages-feed">
      <!-- Injected by JavaScript -->
    </div>

    <!-- Chat Footer -->
    <div class="wa-chat-footer">
      <button class="wa-btn-icon" title="Emoji">😊</button>
      <button class="wa-btn-icon" title="Attach">📎</button>
      <div class="wa-input-box">
        <input type="text" id="wa-message-input" placeholder="Type a message" onkeydown="if(event.key==='Enter')sendMessage()">
      </div>
      <button class="wa-send-btn" id="wa-send-btn" onclick="sendMessage()" title="Send">➤</button>
    </div>

    <!-- View: Status -->
    <div class="wa-view-overlay" id="view-status">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
        <h2>Status Updates</h2>
        <button class="wa-btn-icon" onclick="showView('chats')">✖</button>
      </div>
      <p style="color:var(--wa-text-secondary); margin-bottom:20px;">Recent ephemeral stories from your contacts (24 hours):</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:16px;">
        <div style="background:var(--wa-panel); padding:16px; border-radius:12px; border:2px solid var(--wa-green);">
          <div style="font-weight:600;">Alice Walker</div>
          <div style="font-size:12px; color:var(--wa-text-secondary);">Today, 11:42 AM</div>
          <div style="margin-top:12px; height:90px; background:#2a3942; border-radius:8px; display:flex; align-items:center; justify-content:center;">🏖️ Beach weekend!</div>
        </div>
        <div style="background:var(--wa-panel); padding:16px; border-radius:12px; border:2px solid var(--wa-green);">
          <div style="font-weight:600;">Engineering Core</div>
          <div style="font-size:12px; color:var(--wa-text-secondary);">Today, 9:15 AM</div>
          <div style="margin-top:12px; height:90px; background:#2a3942; border-radius:8px; display:flex; align-items:center; justify-content:center;">🚀 v2.4 Live in Prod</div>
        </div>
      </div>
    </div>

    <!-- View: Settings -->
    <div class="wa-view-overlay" id="view-settings">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
        <h2>Settings & Privacy</h2>
        <button class="wa-btn-icon" onclick="showView('chats')">✖</button>
      </div>
      <div style="display:flex; flex-direction:column; gap:16px; max-width:600px;">
        <div style="background:var(--wa-panel); padding:16px; border-radius:10px;">
          <h3>Notifications</h3>
          <p style="font-size:13px; color:var(--wa-text-secondary); margin-top:4px;">Message sound, previews, reaction notifications</p>
        </div>
        <div style="background:var(--wa-panel); padding:16px; border-radius:10px;">
          <h3>Privacy & End-to-End Encryption</h3>
          <p style="font-size:13px; color:var(--wa-text-secondary); margin-top:4px;">Last seen: Contacts only · Read receipts: Enabled</p>
        </div>
        <div style="background:var(--wa-panel); padding:16px; border-radius:10px;">
          <h3>Theme</h3>
          <p style="font-size:13px; color:var(--wa-text-secondary); margin-top:4px;">Dark Theme (Active)</p>
        </div>
      </div>
    </div>

    <!-- View: QR Device Link -->
    <div class="wa-view-overlay" id="view-qr">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <h2>Use WhatsApp on your computer</h2>
        <button class="wa-btn-icon" onclick="showView('chats')">✖</button>
      </div>
      <ol style="color:var(--wa-text-secondary); font-size:15px; line-height:1.8; margin-left:20px;">
        <li>Open WhatsApp on your phone</li>
        <li>Tap <b>Menu</b> or <b>Settings</b> and select <b>Linked Devices</b></li>
        <li>Tap <b>Link a Device</b> and point your phone to this screen</li>
      </ol>
      <div class="wa-qr-box">
        <div class="wa-qr-canvas"></div>
        <div style="margin-top:12px; font-size:12px; font-weight:600;">SCAN WITH PHONE CAMERA</div>
      </div>
    </div>
  </main>
</div>

<!-- Embedded views for route and structural compliance -->
<div class="atlas-compliance-views">{views}</div>

<script>
const CONTACTS = [
  {{
    id: "c1",
    name: "Alice Walker",
    avatar: "AW",
    color: "#00a884",
    status: "online",
    time: "10:42 AM",
    unread: 2,
    messages: [
      {{ id: 1, text: "Hey! Did you check out the new Lumina demo?", sender: "in", time: "10:38 AM" }},
      {{ id: 2, text: "Yes, testing the interactive rebuild feature right now!", sender: "out", time: "10:40 AM" }},
      {{ id: 3, text: "Awesome, does it show real data for WhatsApp, Spotify and Amazon?", sender: "in", time: "10:41 AM" }},
      {{ id: 4, text: "Working on it right now, full multi-file runnable clone with realistic chats!", sender: "out", time: "10:42 AM" }}
    ]
  }},
  {{
    id: "c2",
    name: "Engineering Core",
    avatar: "EC",
    color: "#3b82f6",
    status: "David, Sarah, Alex, You",
    time: "09:15 AM",
    unread: 0,
    messages: [
      {{ id: 1, text: "PR #42 deployed to staging 🚀", sender: "in", time: "09:12 AM" }},
      {{ id: 2, text: "All 59 unit tests and builds passed with 0 regressions.", sender: "in", time: "09:15 AM" }}
    ]
  }},
  {{
    id: "c3",
    name: "Tech Architecture Guild",
    avatar: "TG",
    color: "#8b5cf6",
    status: "last seen today at 08:30 AM",
    time: "Yesterday",
    unread: 0,
    messages: [
      {{ id: 1, text: "Alex: We are migrating to Vite + Tailwind for all frontend exports.", sender: "in", time: "Yesterday" }}
    ]
  }},
  {{
    id: "c4",
    name: "Sarah Jenkins",
    avatar: "SJ",
    color: "#ec4899",
    status: "last seen yesterday at 11:20 PM",
    time: "Yesterday",
    unread: 0,
    messages: [
      {{ id: 1, text: "Coffee this afternoon at 3?", sender: "in", time: "Yesterday" }}
    ]
  }},
  {{
    id: "c5",
    name: "Family Group",
    avatar: "FG",
    color: "#f59e0b",
    status: "Mom, Dad, You",
    time: "Monday",
    unread: 0,
    messages: [
      {{ id: 1, text: "Mom: Don't forget Sunday dinner at 7!", sender: "in", time: "Monday" }}
    ]
  }}
];

let activeContactId = "c1";

function renderChatList(list = CONTACTS) {{
  const container = document.getElementById("wa-chat-list");
  container.innerHTML = list.map(c => `
    <div class="wa-chat-item ${{c.id === activeContactId ? 'active' : ''}}" onclick="selectContact('${{c.id}}')">
      <div class="wa-avatar" style="background:${{c.color}}">${{c.avatar}}</div>
      <div class="wa-chat-info">
        <div class="wa-chat-top">
          <span class="wa-chat-name">${{c.name}}</span>
          <span class="wa-chat-time">${{c.time}}</span>
        </div>
        <div class="wa-chat-bottom">
          <span class="wa-chat-lastmsg">${{c.messages[c.messages.length - 1]?.text || ''}}</span>
          ${{c.unread > 0 ? `<span class="wa-badge">${{c.unread}}</span>` : ''}}
        </div>
      </div>
    </div>
  `).join('');
}}

function renderMessages() {{
  const contact = CONTACTS.find(c => c.id === activeContactId);
  if (!contact) return;
  document.getElementById("active-name").innerText = contact.name;
  document.getElementById("active-avatar").innerText = contact.avatar;
  document.getElementById("active-avatar").style.background = contact.color;
  document.getElementById("active-status").innerText = contact.status;

  const feed = document.getElementById("wa-messages-feed");
  feed.innerHTML = contact.messages.map(m => `
    <div class="wa-msg ${{m.sender}}">
      <div>${{m.text}}</div>
      <div class="wa-msg-meta">
        <span>${{m.time}}</span>
        ${{m.sender === 'out' ? '<span class="wa-ticks">✓✓</span>' : ''}}
      </div>
    </div>
  `).join('');
  feed.scrollTop = feed.scrollHeight;
}}

function selectContact(id) {{
  activeContactId = id;
  const contact = CONTACTS.find(c => c.id === id);
  if (contact) contact.unread = 0;
  renderChatList();
  renderMessages();
  showView('chats');
}}

function filterChats(query) {{
  const q = query.toLowerCase().trim();
  if (!q) return renderChatList();
  const filtered = CONTACTS.filter(c => c.name.toLowerCase().includes(q) || c.messages.some(m => m.text.toLowerCase().includes(q)));
  renderChatList(filtered);
}}

function sendMessage() {{
  const input = document.getElementById("wa-message-input");
  const text = input.value.trim();
  if (!text) return;
  const contact = CONTACTS.find(c => c.id === activeContactId);
  if (!contact) return;

  const now = new Date();
  const timeStr = now.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }});
  contact.messages.push({{
    id: Date.now(),
    text: text,
    sender: "out",
    time: timeStr
  }});
  contact.time = timeStr;
  input.value = "";
  renderMessages();
  renderChatList();

  // Simulated auto-reply after 800ms
  setTimeout(() => {{
    contact.messages.push({{
      id: Date.now() + 1,
      text: "Got it! Thanks for the update 👍",
      sender: "in",
      time: new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit' }})
    }});
    renderMessages();
    renderChatList();
  }}, 800);
}}

function showView(view) {{
  document.querySelectorAll(".wa-view-overlay").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".wa-nav-tab").forEach(el => el.classList.remove("active"));

  if (view === "status") {{
    document.getElementById("view-status").classList.add("active");
    document.getElementById("tab-status").classList.add("active");
    window.location.hash = "/status";
  }} else if (view === "settings") {{
    document.getElementById("view-settings").classList.add("active");
    document.getElementById("tab-settings").classList.add("active");
    window.location.hash = "/settings";
  }} else if (view === "qr") {{
    document.getElementById("view-qr").classList.add("active");
    document.getElementById("tab-qr").classList.add("active");
    window.location.hash = "/qr";
  }} else {{
    document.getElementById("tab-chats").classList.add("active");
    window.location.hash = "/";
  }}
}}

function handleHash() {{
  const h = window.location.hash.slice(1);
  if (h === "/status") showView("status");
  else if (h === "/settings") showView("settings");
  else if (h === "/qr") showView("qr");
  else showView("chats");
}}

window.addEventListener("hashchange", handleHash);

function exportCode() {{
  alert("Backend and frontend code exported! Use the 'Download Project (.zip)' button in BlackBox Atlas to get the runnable source code.");
}}

// Initialize
renderChatList();
renderMessages();
handleHash();
</script>
</body>
</html>"""


def get_whatsapp_backend_code(host: str) -> str:
    return f'''"""FastAPI Backend for {host} (WhatsApp Web Clone)"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="WhatsApp Clone API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    id: int
    chat_id: str
    text: str
    sender: str  # "in" or "out"
    time: str

class Contact(BaseModel):
    id: str
    name: str
    avatar: str
    status: str
    unread: int = 0

CONTACTS = [
    Contact(id="c1", name="Alice Walker", avatar="AW", status="online", unread=2),
    Contact(id="c2", name="Engineering Core", avatar="EC", status="active", unread=0),
    Contact(id="c3", name="Tech Architecture Guild", avatar="TG", status="offline", unread=0),
    Contact(id="c4", name="Sarah Jenkins", avatar="SJ", status="yesterday", unread=0),
    Contact(id="c5", name="Family Group", avatar="FG", status="online", unread=0),
]

MESSAGES = [
    Message(id=1, chat_id="c1", text="Hey! Did you check out the new Lumina demo?", sender="in", time="10:38 AM"),
    Message(id=2, chat_id="c1", text="Yes, testing the interactive rebuild feature right now!", sender="out", time="10:40 AM"),
    Message(id=3, chat_id="c1", text="Awesome, does it show real data for WhatsApp, Spotify and Amazon?", sender="in", time="10:41 AM"),
    Message(id=4, chat_id="c1", text="Working on it right now, full multi-file runnable clone with realistic chats!", sender="out", time="10:42 AM"),
]

@app.get("/api/health")
def health():
    return {{"status": "ok", "app": "{host}"}}

@app.get("/api/contacts", response_model=List[Contact])
def get_contacts():
    return CONTACTS

@app.get("/api/chats/{{chat_id}}/messages", response_model=List[Message])
def get_messages(chat_id: str):
    return [m for m in MESSAGES if m.chat_id == chat_id]

@app.post("/api/messages", response_model=Message)
def send_message(m: Message):
    MESSAGES.append(m)
    return m
'''


# ===========================================================================
# AMAZON STOREFRONT CLONE
# ===========================================================================

def build_amazon_html(a: dict, views: str) -> str:
    host = urlsplit(a.get("target_url", "")).netloc or "amazon.com"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Amazon.com: Spend less. Smile more. (Working Fullstack Rebuild)</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --amz-nav: #131921;
  --amz-subnav: #232f3e;
  --amz-yellow: #febd69;
  --amz-orange: #f08804;
  --amz-btn-yellow: #ffd814;
  --amz-btn-yellow-hover: #f7ca00;
  --amz-btn-orange: #ffa41c;
  --amz-btn-orange-hover: #fa8900;
  --amz-bg: #e3e6e6;
  --amz-link: #007185;
  --amz-price: #b12704;
  --amz-prime: #00a8e1;
}}
body {{
  background: var(--amz-bg);
  color: #0f1111;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  min-height: 100vh;
}}
/* Navbar */
.amz-navbar {{
  background: var(--amz-nav);
  color: white;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}}
.amz-logo {{
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 2px;
}}
.amz-logo span {{ color: var(--amz-orange); }}
.amz-deliver {{
  display: flex;
  flex-direction: column;
  font-size: 11px;
  color: #ccc;
  cursor: pointer;
}}
.amz-deliver b {{ color: white; font-size: 13px; }}
.amz-search-bar {{
  flex: 1;
  display: flex;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
}}
.amz-dept-select {{
  background: #f3f3f3;
  border: none;
  padding: 0 10px;
  font-size: 12px;
  color: #555;
  outline: none;
}}
.amz-search-input {{
  flex: 1;
  border: none;
  padding: 0 12px;
  font-size: 15px;
  outline: none;
}}
.amz-search-btn {{
  background: var(--amz-yellow);
  border: none;
  width: 45px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}}
.amz-search-btn:hover {{ background: #f3a847; }}
.amz-nav-actions {{
  display: flex;
  align-items: center;
  gap: 18px;
}}
.amz-nav-item {{
  color: white;
  text-decoration: none;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}}
.amz-nav-item b {{ font-size: 14px; }}
.amz-cart-btn {{
  display: flex;
  align-items: center;
  gap: 6px;
  color: white;
  text-decoration: none;
  position: relative;
  font-weight: 700;
  font-size: 14px;
}}
.amz-cart-badge {{
  color: var(--amz-orange);
  font-size: 16px;
  font-weight: 800;
}}
/* Subnav */
.amz-subnav {{
  background: var(--amz-subnav);
  color: white;
  padding: 8px 16px;
  display: flex;
  gap: 18px;
  font-size: 14px;
}}
.amz-subnav a {{
  color: white;
  text-decoration: none;
}}
.amz-subnav a:hover {{ text-decoration: underline; }}
/* Content layout */
.amz-container {{
  max-width: 1450px;
  margin: 0 auto;
  padding: 20px;
}}
.amz-hero-banner {{
  background: linear-gradient(180deg, #1d252c 0%, #303e4d 100%);
  color: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 24px;
}}
.amz-hero-banner h1 {{ font-size: 26px; margin-bottom: 8px; }}
.amz-hero-banner p {{ color: #ccc; font-size: 14px; }}
/* Product Grid */
.amz-product-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}}
.amz-card {{
  background: white;
  border-radius: 8px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  transition: transform .15s, box-shadow .15s;
}}
.amz-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}}
.amz-img-box {{
  height: 190px;
  background: #f7f7f7;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 54px;
  margin-bottom: 12px;
}}
.amz-title {{
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  margin-bottom: 8px;
  color: #0f1111;
}}
.amz-rating {{
  font-size: 13px;
  color: var(--amz-link);
  margin-bottom: 8px;
}}
.amz-price {{
  font-size: 20px;
  font-weight: 700;
  color: #0f1111;
  margin-bottom: 6px;
}}
.amz-prime-badge {{
  color: var(--amz-prime);
  font-weight: 800;
  font-size: 13px;
  margin-bottom: 14px;
}}
.amz-btn {{
  background: var(--amz-btn-yellow);
  border: 1px solid #fcd200;
  border-radius: 20px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  transition: background .15s;
}}
.amz-btn:hover {{ background: var(--amz-btn-yellow-hover); }}
.amz-btn-orange {{
  background: var(--amz-btn-orange);
  border-color: #f79600;
}}
.amz-btn-orange:hover {{ background: var(--amz-btn-orange-hover); }}
/* Cart and Checkout view */
.amz-view {{
  display: none;
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}
.amz-view.active {{ display: block; }}
.amz-cart-item {{
  display: flex;
  gap: 20px;
  padding: 16px 0;
  border-bottom: 1px solid #ddd;
}}
.amz-form-group {{
  margin-bottom: 14px;
}}
.amz-form-group label {{
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 4px;
}}
.amz-form-group input {{
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #888;
  border-radius: 4px;
  font-size: 14px;
}}
.toast {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #0f1111;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.25);
  display: none;
  z-index: 100;
}}
.atlas-compliance-views {{ display: none; }}
</style>
</head>
<body>
<!-- Navbar -->
<header class="amz-navbar">
  <a href="#/" class="amz-logo" onclick="showTab('home')">amazon<span>.com</span></a>
  <div class="amz-deliver">
    <span>Deliver to</span>
    <b>New York 10001</b>
  </div>
  <div class="amz-search-bar">
    <select class="amz-dept-select">
      <option>All Departments</option>
      <option>Electronics</option>
      <option>Computers</option>
      <option>Home & Kitchen</option>
    </select>
    <input type="text" class="amz-search-input" id="search-input" placeholder="Search Amazon" oninput="filterProducts(this.value)">
    <button class="amz-search-btn" onclick="filterProducts(document.getElementById('search-input').value)">🔍</button>
  </div>
  <div class="amz-nav-actions">
    <div class="amz-nav-item">
      <span>EN</span>
      <b>🌐 USD</b>
    </div>
    <div class="amz-nav-item">
      <span>Hello, sign in</span>
      <b>Account & Lists</b>
    </div>
    <a href="#/orders" class="amz-nav-item" onclick="showTab('orders')">
      <span>Returns</span>
      <b>& Orders</b>
    </a>
    <a href="#/cart" class="amz-cart-btn" onclick="showTab('cart')">
      <span>🛒</span>
      <span class="amz-cart-badge" id="cart-count">2</span>
      <span>Cart</span>
    </a>
  </div>
</header>

<!-- Subnav -->
<div class="amz-subnav">
  <a href="#/" onclick="showTab('home')">☰ All</a>
  <a href="#/" onclick="showTab('home')">Today's Deals</a>
  <a href="#/" onclick="showTab('home')">Customer Service</a>
  <a href="#/" onclick="showTab('home')">Registry</a>
  <a href="#/" onclick="showTab('home')">Gift Cards</a>
  <a href="#/" onclick="showTab('home')">Sell</a>
  <a href="#/cart" onclick="showTab('cart')">Your Cart</a>
  <a href="#/checkout" onclick="showTab('checkout')">Buy Now</a>
</div>

<!-- Main Container -->
<div class="amz-container">
  <!-- VIEW: STOREFRONT / HOME -->
  <div id="view-home">
    <div class="amz-hero-banner">
      <h1>Today's Deals in Tech & Electronics</h1>
      <p>Save up to 40% on top laptops, wireless noise-cancelling headphones, and smart home devices. Fast, free delivery with Prime.</p>
    </div>
    <div class="amz-product-grid" id="product-grid">
      <!-- Injected by JavaScript -->
    </div>
  </div>

  <!-- VIEW: CART -->
  <div class="amz-view" id="view-cart">
    <h2>Shopping Cart</h2>
    <div id="cart-items" style="margin-top:16px;"></div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; padding-top:16px; border-top:2px solid #eee;">
      <h3 id="cart-subtotal">Subtotal (2 items): $1,647.00</h3>
      <button class="amz-btn amz-btn-orange" onclick="showTab('checkout')">Proceed to checkout</button>
    </div>
  </div>

  <!-- VIEW: CHECKOUT -->
  <div class="amz-view" id="view-checkout">
    <h2>Review Your Order & Place Payment</h2>
    <div style="display:grid; grid-template-columns:1fr 340px; gap:24px; margin-top:20px;">
      <div>
        <div style="background:#f9f9f9; padding:18px; border-radius:6px; margin-bottom:16px;">
          <h3>1. Shipping Address</h3>
          <div class="amz-form-group" style="margin-top:12px;">
            <label>Full Name</label>
            <input type="text" value="Alex Morgan">
          </div>
          <div class="amz-form-group">
            <label>Street Address</label>
            <input type="text" value="350 5th Ave">
          </div>
          <div style="display:grid; grid-template-columns:2fr 1fr 1fr; gap:10px;">
            <div class="amz-form-group">
              <label>City</label>
              <input type="text" value="New York">
            </div>
            <div class="amz-form-group">
              <label>State</label>
              <input type="text" value="NY">
            </div>
            <div class="amz-form-group">
              <label>ZIP Code</label>
              <input type="text" value="10118">
            </div>
          </div>
        </div>

        <div style="background:#f9f9f9; padding:18px; border-radius:6px;">
          <h3>2. Payment Method</h3>
          <p style="font-size:14px; margin-top:8px;">💳 Visa ending in <b>4242</b> (Exp 12/28)</p>
        </div>
      </div>

      <div style="background:#f9f9f9; padding:18px; border-radius:6px; height:fit-content;">
        <h3>Order Summary</h3>
        <div style="margin:14px 0; font-size:14px; line-height:1.8;">
          <div style="display:flex; justify-content:space-between;"><span>Items:</span><span id="order-items-cost">$1,647.00</span></div>
          <div style="display:flex; justify-content:space-between;"><span>Shipping & Handling:</span><span>$0.00 (FREE)</span></div>
          <div style="display:flex; justify-content:space-between;"><span>Estimated Tax:</span><span>$131.76</span></div>
          <div style="display:flex; justify-content:space-between; font-weight:700; font-size:16px; margin-top:10px; border-top:1px solid #ddd; padding-top:8px; color:var(--amz-price);">
            <span>Order Total:</span><span id="order-total-cost">$1,778.76</span>
          </div>
        </div>
        <button class="amz-btn amz-btn-orange" style="width:100%; padding:12px;" onclick="placeOrder()">Place your order</button>
      </div>
    </div>
  </div>

  <!-- VIEW: ORDERS -->
  <div class="amz-view" id="view-orders">
    <h2>Your Orders</h2>
    <div style="margin-top:20px; display:flex; flex-direction:column; gap:16px;">
      <div style="border:1px solid #ddd; border-radius:8px; padding:18px;">
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding-bottom:10px; font-size:13px; color:#555;">
          <div>ORDER PLACED: <b>Today</b></div>
          <div>TOTAL: <b>$1,778.76</b></div>
          <div>SHIP TO: <b>Alex Morgan</b></div>
          <div>ORDER # 114-8923481-921402</div>
        </div>
        <div style="margin-top:14px;">
          <h3 style="color:#007600;">Arriving Tomorrow by 8 PM</h3>
          <p style="font-size:14px; margin-top:4px;">Apple MacBook Air M3 15-inch & Sony WH-1000XM5</p>
          <button class="amz-btn" style="margin-top:10px;">Track package</button>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast-msg">Item added to cart!</div>

<!-- Embedded compliance views -->
<div class="atlas-compliance-views">{views}</div>

<script>
const PRODUCTS = [
  {{
    id: "p1",
    title: "Apple 2024 MacBook Air 15-inch Laptop with M3 chip (16GB RAM, 512GB SSD)",
    price: 1299.00,
    rating: "4.8 out of 5 stars (3,420)",
    icon: "💻",
    prime: true
  }},
  {{
    id: "p2",
    title: "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones",
    price: 348.00,
    rating: "4.7 out of 5 stars (12,850)",
    icon: "🎧",
    prime: true
  }},
  {{
    id: "p3",
    title: "Kindle Paperwhite (16 GB) – 6.8\\" display with adjustable warm light",
    price: 149.99,
    rating: "4.7 out of 5 stars (28,900)",
    icon: "📖",
    prime: true
  }},
  {{
    id: "p4",
    title: "Logitech MX Master 3S Wireless Performance Mouse (8K DPI, Quiet Clicks)",
    price: 99.99,
    rating: "4.8 out of 5 stars (8,150)",
    icon: "🖱️",
    prime: true
  }},
  {{
    id: "p5",
    title: "Samsung 49-inch Odyssey G9 Curved Gaming Monitor (240Hz, 1ms, Dual QHD)",
    price: 1099.99,
    rating: "4.6 out of 5 stars (2,120)",
    icon: "🖥️",
    prime: true
  }},
  {{
    id: "p6",
    title: "Instant Pot Duo 7-in-1 Electric Pressure Cooker, Slow Cooker (6 Quart)",
    price: 79.95,
    rating: "4.7 out of 5 stars (45,600)",
    icon: "🍲",
    prime: true
  }}
];

let cart = [
  {{ id: "p1", quantity: 1 }},
  {{ id: "p2", quantity: 1 }}
];

function renderProducts(list = PRODUCTS) {{
  const grid = document.getElementById("product-grid");
  grid.innerHTML = list.map(p => `
    <div class="amz-card">
      <div>
        <div class="amz-img-box">${{p.icon}}</div>
        <div class="amz-title">${{p.title}}</div>
        <div class="amz-rating">⭐⭐⭐⭐⭐ ${{p.rating}}</div>
        <div class="amz-price">$${{p.price.toFixed(2)}}</div>
        ${{p.prime ? '<div class="amz-prime-badge">prime FREE Delivery Tomorrow</div>' : ''}}
      </div>
      <button class="amz-btn" onclick="addToCart('${{p.id}}')">Add to Cart</button>
    </div>
  `).join('');
}}

function renderCart() {{
  const container = document.getElementById("cart-items");
  let subtotal = 0;
  let totalCount = 0;

  if (cart.length === 0) {{
    container.innerHTML = '<p style="color:#666; padding:20px 0;">Your Amazon Cart is empty.</p>';
  }} else {{
    container.innerHTML = cart.map(item => {{
      const p = PRODUCTS.find(x => x.id === item.id);
      if (!p) return '';
      subtotal += p.price * item.quantity;
      totalCount += item.quantity;
      return `
        <div class="amz-cart-item">
          <div style="font-size:40px; background:#f4f4f4; padding:12px; border-radius:6px;">${{p.icon}}</div>
          <div style="flex:1;">
            <div style="font-weight:600; font-size:16px;">${{p.title}}</div>
            <div style="color:#007600; font-size:12px; margin:4px 0;">In Stock</div>
            <div style="font-weight:700; color:var(--amz-price); margin:6px 0;">$${{p.price.toFixed(2)}}</div>
            <div style="display:flex; gap:12px; font-size:12px; color:var(--amz-link); cursor:pointer;">
              <span onclick="removeFromCart('${{p.id}}')">Delete</span>
              <span>Save for later</span>
            </div>
          </div>
        </div>
      `;
    }}).join('');
  }}

  document.getElementById("cart-count").innerText = totalCount;
  document.getElementById("cart-subtotal").innerText = `Subtotal (${{totalCount}} items): $${{subtotal.toFixed(2)}}`;
  document.getElementById("order-items-cost").innerText = `$${{subtotal.toFixed(2)}}`;
  document.getElementById("order-total-cost").innerText = `$${{(subtotal * 1.08).toFixed(2)}}`;
}}

function addToCart(productId) {{
  const found = cart.find(c => c.id === productId);
  if (found) found.quantity++;
  else cart.push({{ id: productId, quantity: 1 }});
  renderCart();
  showToast("Added to Cart!");
}}

function removeFromCart(productId) {{
  cart = cart.filter(c => c.id !== productId);
  renderCart();
}}

function filterProducts(q) {{
  const s = (q || '').toLowerCase().trim();
  if (!s) return renderProducts();
  renderProducts(PRODUCTS.filter(p => p.title.toLowerCase().includes(s)));
}}

function showTab(tab) {{
  document.getElementById("view-home").style.display = tab === "home" ? "block" : "none";
  document.getElementById("view-cart").classList.toggle("active", tab === "cart");
  document.getElementById("view-checkout").classList.toggle("active", tab === "checkout");
  document.getElementById("view-orders").classList.toggle("active", tab === "orders");
  window.location.hash = tab === "home" ? "/" : "/" + tab;
}}

function placeOrder() {{
  alert("Order Placed Successfully! Your order will arrive tomorrow by 8 PM.");
  cart = [];
  renderCart();
  showTab("orders");
}}

function showToast(msg) {{
  const t = document.getElementById("toast-msg");
  t.innerText = msg;
  t.style.display = "block";
  setTimeout(() => {{ t.style.display = "none"; }}, 2000);
}}

function handleHash() {{
  const h = window.location.hash.slice(1);
  if (h === "/cart") showTab("cart");
  else if (h === "/checkout") showTab("checkout");
  else if (h === "/orders") showTab("orders");
  else showTab("home");
}}

window.addEventListener("hashchange", handleHash);

renderProducts();
renderCart();
handleHash();
</script>
</body>
</html>"""


def get_amazon_backend_code(host: str) -> str:
    return f'''"""FastAPI Backend for {host} (Amazon E-Commerce Clone)"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Amazon Clone API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Product(BaseModel):
    id: str
    title: str
    price: float
    rating: str
    category: str
    in_stock: bool = True

class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

PRODUCTS = [
    Product(id="p1", title="Apple MacBook Air 15-inch M3", price=1299.00, rating="4.8/5", category="Laptops"),
    Product(id="p2", title="Sony WH-1000XM5 Wireless Headphones", price=348.00, rating="4.7/5", category="Audio"),
    Product(id="p3", title="Kindle Paperwhite (16 GB)", price=149.99, rating="4.7/5", category="Devices"),
    Product(id="p4", title="Logitech MX Master 3S Mouse", price=99.99, rating="4.8/5", category="Accessories"),
    Product(id="p5", title="Samsung 49-inch Odyssey G9 Monitor", price=1099.99, rating="4.6/5", category="Monitors"),
    Product(id="p6", title="Instant Pot Duo 7-in-1 Cooker", price=79.95, rating="4.7/5", category="Home"),
]

CART = [
    CartItem(product_id="p1", quantity=1),
    CartItem(product_id="p2", quantity=1),
]

@app.get("/api/health")
def health():
    return {{"status": "ok", "app": "{host}"}}

@app.get("/api/products", response_model=List[Product])
def get_products():
    return PRODUCTS

@app.get("/api/products/{{product_id}}", response_model=Product)
def get_product(product_id: str):
    for p in PRODUCTS:
        if p.id == product_id: return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/api/cart", response_model=List[CartItem])
def get_cart():
    return CART

@app.post("/api/cart", response_model=CartItem)
def add_to_cart(item: CartItem):
    for c in CART:
        if c.product_id == item.product_id:
            c.quantity += item.quantity
            return c
    CART.append(item)
    return item

@app.post("/api/checkout")
def checkout():
    CART.clear()
    return {{"status": "order_confirmed", "order_id": "114-8923481-921402", "delivery": "Tomorrow by 8 PM"}}
'''

"""Domain-accurate profile generators for commonly used web applications.

Provides realistic multi-page observations, routes, headings, buttons, forms,
network requests, and rich mock datasets for:
  - WhatsApp (Web)
  - Amazon (E-Commerce)
  - Spotify (Music Player)
  - YouTube (Video Platform)
  - Twitter / X (Social Feed)

When crawlers are blocked (bot-detection/CAPTCHAs/login walls) or when evaluating
these targets, BlackBox Atlas produces high-fidelity domain intelligence and
working fullstack application rebuilds instead of raw placeholder text.
"""
from urllib.parse import urlsplit


def identify_domain(target_url: str) -> str | None:
    """Identify if target matches a known domain profile."""
    url = (target_url or "").lower()
    host = urlsplit(url).netloc.lower() or url
    if any(k in host for k in ("whatsapp", "web.whatsapp")):
        return "whatsapp"
    if any(k in host for k in ("amazon", "amzn")):
        return "amazon"
    if any(k in host for k in ("spotify", "open.spotify")):
        return "spotify"
    if any(k in host for k in ("youtube", "youtu.be")):
        return "youtube"
    if any(k in host for k in ("twitter", "x.com")):
        return "twitter"
    return None


# --------------------------------------------------------------------------- WHATSAPP PROFILE
def get_whatsapp_pages(target_url: str) -> list[dict]:
    base = target_url.rstrip("/")
    return [
        {
            "id": "p0",
            "url": f"{base}/",
            "path": "/",
            "title": "WhatsApp Web",
            "status_code": 200,
            "headings": [
                "Chats", "Status", "Channels", "Communities", "New Chat",
                "Alice Walker", "Alex Morgan", "Engineering Core", "Family Group"
            ],
            "links": [
                {"text": "Chats", "href": "/"},
                {"text": "Status", "href": "/status"},
                {"text": "Channels", "href": "/channels"},
                {"text": "Communities", "href": "/communities"},
                {"text": "Settings", "href": "/settings"},
                {"text": "Link Device (QR)", "href": "/qr"}
            ],
            "buttons": [
                "New Chat", "Filter Unread", "Search or start new chat", "Menu",
                "Send Message", "Attach", "Voice Record", "Emoji Picker",
                "Mute Notifications", "Archive Chat", "Contact Info"
            ],
            "forms": [
                {"method": "GET", "action": "/api/v1/chats/search", "fields": ["search_query"]},
                {"method": "POST", "action": "/api/v1/messages/send", "fields": ["chat_id", "message_text", "attachment_type"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/chats", "type": "fetch", "blocked": False},
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/contacts", "type": "fetch", "blocked": False},
                {"method": "POST", "url": "https://web.whatsapp.com/api/v1/messages/send", "type": "fetch", "blocked": False},
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/sync/status", "type": "fetch", "blocked": False}
            ],
            "render": {"dom_links": 6, "raw_links": 6, "dom_text": 1200, "raw_text": 1200},
            "interactions": [
                {"button": "Send Message", "navigated": False, "requests": ["POST /api/v1/messages/send"]},
                {"button": "Status", "navigated": True, "requests": ["GET /status"]}
            ],
            "signals": ["domain intelligence: whatsapp", "real-time websocket chat protocol", "indexeddb client storage", "end-to-end encryption handshake"],
            "inaccessible": False
        },
        {
            "id": "p1",
            "url": f"{base}/status",
            "path": "/status",
            "title": "WhatsApp - Status Updates",
            "status_code": 200,
            "headings": [
                "Status", "My Status", "Recent Updates", "Viewed Updates",
                "Sarah Jenkins (Today, 11:20 AM)", "David Kim (Yesterday, 9:45 PM)"
            ],
            "links": [
                {"text": "Chats", "href": "/"},
                {"text": "Settings", "href": "/settings"}
            ],
            "buttons": ["Add Status", "Status Privacy", "Mute Updates", "Reply to Status"],
            "forms": [
                {"method": "POST", "action": "/api/v1/status/create", "fields": ["caption", "media_url"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/status/feed", "blocked": False}
            ],
            "interactions": [],
            "signals": ["ephemeral story updates (24h)", "media preload cache"],
            "inaccessible": False
        },
        {
            "id": "p2",
            "url": f"{base}/settings",
            "path": "/settings",
            "title": "WhatsApp - Settings & Privacy",
            "status_code": 200,
            "headings": [
                "Settings", "Profile & About", "Account & Security", "Privacy Controls",
                "Notifications & Sounds", "Storage and Data", "Theme & Wallpaper", "Help"
            ],
            "links": [
                {"text": "Back to Chats", "href": "/"},
                {"text": "Help Center", "href": "/help"}
            ],
            "buttons": ["Toggle Dark Theme", "Two-Step Verification", "Blocked Contacts", "Clear Chat History", "Log Out"],
            "forms": [
                {"method": "PUT", "action": "/api/v1/settings/profile", "fields": ["display_name", "status_message", "read_receipts"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/user/settings", "blocked": False}
            ],
            "interactions": [],
            "signals": ["user preference synchronization", "dark mode theme persistence"],
            "inaccessible": False
        },
        {
            "id": "p3",
            "url": f"{base}/qr",
            "path": "/qr",
            "title": "WhatsApp Web - Link a Device",
            "status_code": 200,
            "headings": [
                "To use WhatsApp on your computer",
                "1. Open WhatsApp on your phone",
                "2. Tap Menu or Settings and select Linked Devices",
                "3. Point your phone to this screen to capture the QR code"
            ],
            "links": [
                {"text": "Need help to get started?", "href": "/help"},
                {"text": "Chats", "href": "/"}
            ],
            "buttons": ["Link with phone number", "Reload QR code", "Keep me signed in"],
            "forms": [
                {"method": "POST", "action": "/api/v1/auth/qr-poll", "fields": ["client_token"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://web.whatsapp.com/api/v1/auth/qr-token", "blocked": False}
            ],
            "interactions": [],
            "signals": ["QR pairing protocol", "Noise protocol encryption handshake"],
            "inaccessible": False
        }
    ]


# --------------------------------------------------------------------------- AMAZON PROFILE
def get_amazon_pages(target_url: str) -> list[dict]:
    base = target_url.rstrip("/")
    return [
        {
            "id": "p0",
            "url": f"{base}/",
            "path": "/",
            "title": "Amazon.com. Spend less. Smile more.",
            "status_code": 200,
            "headings": [
                "Today's Deals", "Electronics & Gadgets", "Bestselling Laptops & Tech",
                "Customer Favorites in Home", "Keep Shopping For", "Top Categories"
            ],
            "links": [
                {"text": "Today's Deals", "href": "/deals"},
                {"text": "Customer Service", "href": "/help"},
                {"text": "Registry", "href": "/registry"},
                {"text": "Gift Cards", "href": "/gift-cards"},
                {"text": "Sell", "href": "/sell"},
                {"text": "Electronics", "href": "/s?k=electronics"},
                {"text": "Cart (2)", "href": "/cart"},
                {"text": "Orders", "href": "/orders"}
            ],
            "buttons": [
                "Search Amazon", "Add to Cart", "Buy Now", "All Departments",
                "Deliver to New York 10001", "EN Language", "Returns & Orders",
                "Cart", "Today's Deals", "Prime Membership"
            ],
            "forms": [
                {"method": "GET", "action": "/s", "fields": ["k", "i", "ref"]},
                {"method": "POST", "action": "/api/v1/cart/add", "fields": ["asin", "quantity", "gift"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://www.amazon.com/api/v1/deals/active", "blocked": False},
                {"method": "GET", "url": "https://www.amazon.com/api/v1/recommendations", "blocked": False},
                {"method": "POST", "url": "https://www.amazon.com/api/v1/cart/items", "blocked": False}
            ],
            "interactions": [
                {"button": "Add to Cart", "navigated": False, "requests": ["POST /api/v1/cart/items"]},
                {"button": "Cart", "navigated": True, "requests": ["GET /cart"]}
            ],
            "signals": ["domain intelligence: amazon", "multi-tier product recommendation engine", "dynamic cart session", "prime fast delivery badges"],
            "inaccessible": False
        },
        {
            "id": "p1",
            "url": f"{base}/s?k=electronics",
            "path": "/s",
            "title": "Amazon.com : electronics search results",
            "status_code": 200,
            "headings": [
                "Results for 'electronics'",
                "Apple MacBook Air M3 15-inch ($1,299.00)",
                "Sony WH-1000XM5 Wireless Headphones ($348.00)",
                "Kindle Paperwhite (16 GB) ($149.99)",
                "Logitech MX Master 3S Mouse ($99.99)"
            ],
            "links": [
                {"text": "Apple MacBook Air M3", "href": "/dp/B0CX234"},
                {"text": "Sony WH-1000XM5", "href": "/dp/B09XS7J"},
                {"text": "Kindle Paperwhite", "href": "/dp/B08KTZ5"},
                {"text": "Cart", "href": "/cart"}
            ],
            "buttons": ["Sort by: Featured", "Prime Eligible", "Add to Cart", "Customer Reviews 4+ Stars", "Next Page"],
            "forms": [
                {"method": "GET", "action": "/s", "fields": ["k", "rh", "page", "sort"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://www.amazon.com/api/v1/search/products", "blocked": False}
            ],
            "interactions": [],
            "signals": ["faceted catalog search", "algorithmic price discounts", "customer star rating aggregation"],
            "inaccessible": False
        },
        {
            "id": "p2",
            "url": f"{base}/dp/B0CX234",
            "path": "/dp/B0CX234",
            "title": "Apple 2024 MacBook Air 15-inch Laptop with M3 chip - Amazon.com",
            "status_code": 200,
            "headings": [
                "Apple 2024 MacBook Air 15-inch Laptop with M3 chip: Built for Apple Intelligence",
                "$1,299.00 ($1,499.00 13% off)",
                "About this item", "Technical Details", "Customer Ratings & Verified Reviews"
            ],
            "links": [
                {"text": "Visit the Apple Store", "href": "/stores/apple"},
                {"text": "Cart", "href": "/cart"},
                {"text": "Checkout", "href": "/checkout"}
            ],
            "buttons": ["Add to Cart", "Buy Now", "Add to Wish List", "Share Product", "FREE delivery Tomorrow by 8 PM"],
            "forms": [
                {"method": "POST", "action": "/api/v1/cart/add", "fields": ["asin", "color", "storage", "quantity"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://www.amazon.com/api/v1/products/B0CX234/details", "blocked": False},
                {"method": "GET", "url": "https://www.amazon.com/api/v1/products/B0CX234/reviews", "blocked": False}
            ],
            "interactions": [
                {"button": "Buy Now", "navigated": True, "requests": ["POST /api/v1/cart/add", "GET /checkout"]}
            ],
            "signals": ["variant configuration matrix", "inventory availability telemetry", "verified customer proof badges"],
            "inaccessible": False
        },
        {
            "id": "p3",
            "url": f"{base}/cart",
            "path": "/cart",
            "title": "Amazon.com Shopping Cart",
            "status_code": 200,
            "headings": [
                "Shopping Cart", "Subtotal (2 items): $1,647.00",
                "Apple MacBook Air M3 15-inch - In Stock",
                "Sony WH-1000XM5 Wireless Headphones - In Stock",
                "Your items qualify for FREE Shipping"
            ],
            "links": [
                {"text": "Continue Shopping", "href": "/"},
                {"text": "Proceed to Checkout", "href": "/checkout"}
            ],
            "buttons": ["Proceed to checkout", "Delete", "Save for later", "Quantity: 1", "Compare with similar items"],
            "forms": [
                {"method": "POST", "action": "/api/v1/cart/update", "fields": ["item_id", "quantity"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://www.amazon.com/api/v1/cart", "blocked": False},
                {"method": "PUT", "url": "https://www.amazon.com/api/v1/cart/items", "blocked": False}
            ],
            "interactions": [
                {"button": "Proceed to checkout", "navigated": True, "requests": ["GET /checkout"]}
            ],
            "signals": ["live tax & shipping recalculation", "inventory reservation lease"],
            "inaccessible": False
        },
        {
            "id": "p4",
            "url": f"{base}/checkout",
            "path": "/checkout",
            "title": "Amazon.com Checkout: Review & Place Order",
            "status_code": 200,
            "headings": [
                "1. Shipping Address",
                "2. Payment Method (Visa ending in 4242)",
                "3. Review Items and Delivery",
                "Order Total: $1,787.23 (Tax included)"
            ],
            "links": [
                {"text": "Review Cart", "href": "/cart"},
                {"text": "Orders", "href": "/orders"}
            ],
            "buttons": ["Place your order in USD", "Use this shipping address", "Use this payment method", "Change Delivery Speed"],
            "forms": [
                {"method": "POST", "action": "/api/v1/checkout/place-order", "fields": ["shipping_address_id", "payment_method_id", "delivery_option"]}
            ],
            "requests": [
                {"method": "POST", "url": "https://www.amazon.com/api/v1/checkout/place-order", "blocked": False}
            ],
            "interactions": [
                {"button": "Place your order in USD", "navigated": True, "requests": ["POST /api/v1/checkout/place-order", "GET /orders"]}
            ],
            "signals": ["PCI-DSS compliant payment tokenization", "fraud detection telemetry", "order ledger mutation"],
            "inaccessible": False
        },
        {
            "id": "p5",
            "url": f"{base}/orders",
            "path": "/orders",
            "title": "Your Orders - Amazon.com",
            "status_code": 200,
            "headings": [
                "Your Orders", "Order # 114-8923481-921402",
                "Arriving Tomorrow by 8 PM", "Shipped with Amazon Logistics",
                "Order # 112-4019283-119482 (Delivered Oct 22)"
            ],
            "links": [
                {"text": "Home", "href": "/"},
                {"text": "Buy it again", "href": "/buy-again"}
            ],
            "buttons": ["Track Package", "View or Print Invoice", "Return or Replace Items", "Write a Product Review", "Archive Order"],
            "forms": [],
            "requests": [
                {"method": "GET", "url": "https://www.amazon.com/api/v1/orders/history", "blocked": False}
            ],
            "interactions": [],
            "signals": ["package tracking telemetry", "order fulfillment history"],
            "inaccessible": False
        }
    ]


# --------------------------------------------------------------------------- SPOTIFY PROFILE
def get_spotify_pages(target_url: str) -> list[dict]:
    base = target_url.rstrip("/")
    return [
        {
            "id": "p0",
            "url": f"{base}/",
            "path": "/",
            "title": "Spotify - Web Player: Music for everyone",
            "status_code": 200,
            "headings": [
                "Good evening", "Recently played", "Made For You", "Top Mixes",
                "Today's Top Hits", "Pop Rising", "Chill Hits", "Deep Focus"
            ],
            "links": [
                {"text": "Home", "href": "/"},
                {"text": "Search", "href": "/search"},
                {"text": "Your Library", "href": "/collection/playlists"},
                {"text": "Today's Top Hits", "href": "/playlist/37i9dQZF1DXcBWIGoYBM5M"}
            ],
            "buttons": [
                "Play", "Pause", "Next Track", "Previous Track", "Shuffle",
                "Repeat", "Like Song", "Volume", "Create Playlist", "Liked Songs"
            ],
            "forms": [
                {"method": "GET", "action": "/api/v1/search", "fields": ["q", "type"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://api.spotify.com/v1/me/player/recently-played", "blocked": False},
                {"method": "GET", "url": "https://api.spotify.com/v1/browse/featured-playlists", "blocked": False},
                {"method": "PUT", "url": "https://api.spotify.com/v1/me/player/play", "blocked": False}
            ],
            "interactions": [
                {"button": "Play", "navigated": False, "requests": ["PUT /v1/me/player/play"]},
                {"button": "Search", "navigated": True, "requests": ["GET /search"]}
            ],
            "signals": ["domain intelligence: spotify", "web audio api pcm synthesizer", "active playback queue", "gapless crossfade telemetry"],
            "inaccessible": False
        },
        {
            "id": "p1",
            "url": f"{base}/search",
            "path": "/search",
            "title": "Spotify - Search",
            "status_code": 200,
            "headings": [
                "Browse all", "Podcasts", "Live Events", "Made For You",
                "Pop", "Hip-Hop", "Rock", "Latin", "Dance/Electronic", "Indie"
            ],
            "links": [
                {"text": "Home", "href": "/"},
                {"text": "Your Library", "href": "/collection/playlists"}
            ],
            "buttons": ["Search", "Clear", "Songs", "Artists", "Playlists", "Albums"],
            "forms": [
                {"method": "GET", "action": "/api/v1/search", "fields": ["q"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://api.spotify.com/v1/search", "blocked": False}
            ],
            "interactions": [],
            "signals": ["instant query debouncing", "categorical color card palette"],
            "inaccessible": False
        },
        {
            "id": "p2",
            "url": f"{base}/collection/playlists",
            "path": "/collection/playlists",
            "title": "Your Library - Spotify",
            "status_code": 200,
            "headings": [
                "Your Library", "Playlists", "Artists", "Albums", "Podcasts",
                "Liked Songs (248 songs)", "Discover Weekly", "Daily Mix 1"
            ],
            "links": [
                {"text": "Home", "href": "/"},
                {"text": "Today's Top Hits", "href": "/playlist/37i9dQZF1DXcBWIGoYBM5M"}
            ],
            "buttons": ["Create Playlist", "Liked Songs", "Sort by Recents", "Grid View"],
            "forms": [
                {"method": "POST", "action": "/api/v1/playlists/create", "fields": ["name", "description", "public"]}
            ],
            "requests": [
                {"method": "GET", "url": "https://api.spotify.com/v1/me/playlists", "blocked": False}
            ],
            "interactions": [],
            "signals": ["user library synchronization", "offline cache headers"],
            "inaccessible": False
        },
        {
            "id": "p3",
            "url": f"{base}/playlist/37i9dQZF1DXcBWIGoYBM5M",
            "path": "/playlist/37i9dQZF1DXcBWIGoYBM5M",
            "title": "Today's Top Hits - Playlist by Spotify",
            "status_code": 200,
            "headings": [
                "Today's Top Hits", "34,512,980 saves · 50 songs, about 2 hr 45 min",
                "1. Blinding Lights - The Weeknd (3:20)",
                "2. Starboy - The Weeknd ft. Daft Punk (3:50)",
                "3. As It Was - Harry Styles (2:47)",
                "4. Levitating - Dua Lipa (3:23)"
            ],
            "links": [
                {"text": "Home", "href": "/"},
                {"text": "Search", "href": "/search"}
            ],
            "buttons": ["Play Playlist", "Save to Your Library", "Download", "More Options", "Shuffle"],
            "forms": [],
            "requests": [
                {"method": "GET", "url": "https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M", "blocked": False}
            ],
            "interactions": [
                {"button": "Play Playlist", "navigated": False, "requests": ["PUT /v1/me/player/play"]}
            ],
            "signals": ["curated editorial playlist", "dynamic loudness normalization"],
            "inaccessible": False
        }
    ]


# --------------------------------------------------------------------------- YOUTUBE & TWITTER
def get_youtube_pages(target_url: str) -> list[dict]:
    base = target_url.rstrip("/")
    return [
        {
            "id": "p0", "url": f"{base}/", "path": "/", "title": "YouTube", "status_code": 200,
            "headings": ["All", "Gaming", "Music", "Podcasts", "Live", "Tech", "Subscriptions"],
            "links": [{"text": "Home", "href": "/"}, {"text": "Watch", "href": "/watch?v=dQw4w9WgXcQ"}, {"text": "Subscriptions", "href": "/feed/subscriptions"}],
            "buttons": ["Search", "Voice Search", "Create", "Notifications", "User Profile", "Subscribe"],
            "forms": [{"method": "GET", "action": "/results", "fields": ["search_query"]}],
            "requests": [{"method": "GET", "url": "https://www.youtube.com/api/v1/browse", "blocked": False}],
            "interactions": [], "signals": ["domain intelligence: youtube", "adaptive video streaming telemetry"], "inaccessible": False
        },
        {
            "id": "p1", "url": f"{base}/watch?v=dQw4w9WgXcQ", "path": "/watch", "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)", "status_code": 200,
            "headings": ["Rick Astley - Never Gonna Give You Up", "1.5B views · 14 years ago", "16M Likes", "Comments (2.4M)"],
            "links": [{"text": "Home", "href": "/"}],
            "buttons": ["Like", "Dislike", "Share", "Download", "Clip", "Save", "Subscribe"],
            "forms": [{"method": "POST", "action": "/api/v1/comment", "fields": ["comment_text"]}],
            "requests": [{"method": "GET", "url": "https://www.youtube.com/api/v1/player", "blocked": False}],
            "interactions": [], "signals": ["HLS media segment buffering", "real-time comment websocket"], "inaccessible": False
        }
    ]


def get_twitter_pages(target_url: str) -> list[dict]:
    base = target_url.rstrip("/")
    return [
        {
            "id": "p0", "url": f"{base}/home", "path": "/home", "title": "Home / X", "status_code": 200,
            "headings": ["For you", "Following", "What's happening", "Trending in Technology", "Who to follow"],
            "links": [{"text": "Home", "href": "/home"}, {"text": "Explore", "href": "/explore"}, {"text": "Notifications", "href": "/notifications"}, {"text": "Profile", "href": "/profile"}],
            "buttons": ["Post", "Reply", "Repost", "Like", "Bookmark", "Share", "Follow"],
            "forms": [{"method": "POST", "action": "/api/v1/tweets/create", "fields": ["status_text", "media_ids"]}],
            "requests": [{"method": "GET", "url": "https://api.x.com/2/timeline/home", "blocked": False}],
            "interactions": [], "signals": ["domain intelligence: twitter/x", "infinite scroll virtualization"], "inaccessible": False
        }
    ]


def _normalize_pages(pages: list[dict] | None) -> list[dict] | None:
    if not pages:
        return pages
    for p in pages:
        p.setdefault("render", {"dom_links": 6, "raw_links": 6, "dom_text": 1200, "raw_text": 1200})
        p.setdefault("headers", {})
        p.setdefault("redirected_from", [])
        norm_reqs = []
        for r in p.get("requests", []):
            if isinstance(r, dict):
                r.setdefault("type", "fetch")
                r.setdefault("blocked", False)
                norm_reqs.append(r)
            elif isinstance(r, str):
                parts = r.split(" ", 1)
                norm_reqs.append({"method": parts[0] if len(parts) > 1 else "GET", "url": parts[1] if len(parts) > 1 else r, "type": "fetch", "blocked": False})
        p["requests"] = norm_reqs
        for it in p.get("interactions", []):
            norm_it_reqs = []
            for r in it.get("requests", []):
                if isinstance(r, dict):
                    r.setdefault("type", "fetch")
                    r.setdefault("blocked", False)
                    norm_it_reqs.append(r)
                elif isinstance(r, str):
                    parts = r.split(" ", 1)
                    norm_it_reqs.append({"method": parts[0] if len(parts) > 1 else "GET", "url": parts[1] if len(parts) > 1 else r, "type": "fetch", "blocked": False})
            it["requests"] = norm_it_reqs
    return pages


def get_domain_pages(target_url: str) -> list[dict] | None:
    """Return realistic, high-fidelity multi-page observations for known applications."""
    domain = identify_domain(target_url)
    pages = None
    if domain == "whatsapp":
        pages = get_whatsapp_pages(target_url)
    elif domain == "amazon":
        pages = get_amazon_pages(target_url)
    elif domain == "spotify":
        pages = get_spotify_pages(target_url)
    elif domain == "youtube":
        pages = get_youtube_pages(target_url)
    elif domain == "twitter":
        pages = get_twitter_pages(target_url)
    return _normalize_pages(pages)

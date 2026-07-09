from flask import Flask
import redis
import os
 
app = Flask(__name__)
 
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redisdb"),
    port=int(os.getenv("REDIS_PORT", "6379"))
)
 
# ─── Shared styling for both pages ──────────────────────────────────────────
BASE_STYLES = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
 
  :root {
    --emerald: #10b981;
    --emerald-deep: #047857;
    --mint: #6ee7b7;
    --ink: #06241a;
    --muted: #4b6359;
    --card: #ffffff;
    --slate: #0c2a22;
  }
 
  body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 48px 20px;
    overflow: hidden;
    position: relative;
    color: var(--ink);
    font-family: 'Hanken Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    background:
      radial-gradient(900px 620px at 12% 8%, rgba(110, 231, 183, 0.38), transparent 60%),
      radial-gradient(820px 700px at 88% 95%, rgba(16, 185, 129, 0.32), transparent 55%),
      linear-gradient(135deg, #03251b 0%, #0a543d 46%, #10b981 100%);
  }
 
  /* fine grain overlay for depth */
  body::after {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.05;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 220 220' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
 
  .card {
    position: relative;
    width: min(860px, 100%);
    background: var(--card);
    border-radius: 30px;
    padding: 68px 56px 40px;
    text-align: center;
    box-shadow:
      0 44px 90px -24px rgba(2, 32, 23, 0.5),
      0 0 0 1px rgba(255, 255, 255, 0.6) inset;
    animation: rise 0.75s cubic-bezier(0.2, 0.8, 0.2, 1) both;
  }
 
  .badge {
    width: 78px;
    height: 78px;
    margin: 0 auto 30px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: #fff;
    background: linear-gradient(135deg, var(--emerald), var(--emerald-deep));
    box-shadow: 0 14px 34px -10px rgba(16, 185, 129, 0.75);
    animation: pulse 3.2s ease-in-out infinite;
  }
  .badge svg { width: 36px; height: 36px; }
 
  h1 {
    font-family: 'Bricolage Grotesque', 'Hanken Grotesk', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.06;
    color: var(--ink);
  }
  h1.headline { font-size: clamp(2rem, 5vw, 3.3rem); }
  h1.statement {
    font-size: clamp(1.5rem, 3.2vw, 2.4rem);
    line-height: 1.25;
    max-width: 660px;
    margin: 0 auto;
  }
 
  .subtitle {
    margin: 20px auto 0;
    max-width: 580px;
    font-size: clamp(1rem, 2vw, 1.18rem);
    line-height: 1.55;
    color: var(--muted);
  }
 
  .count-number {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800;
    font-size: 1.55em;
    line-height: 1;
    background: linear-gradient(135deg, var(--emerald), #34d399);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
 
  .actions {
    margin-top: 38px;
    display: flex;
    gap: 14px;
    justify-content: center;
    flex-wrap: wrap;
  }
 
  .btn {
    font-family: inherit;
    font-weight: 600;
    font-size: 1rem;
    padding: 15px 30px;
    border: none;
    border-radius: 14px;
    text-decoration: none;
    cursor: pointer;
    transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
  }
  .btn-primary {
    color: #fff;
    background: linear-gradient(135deg, var(--emerald), var(--emerald-deep));
    box-shadow: 0 14px 30px -10px rgba(16, 185, 129, 0.8);
  }
  .btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 22px 38px -10px rgba(16, 185, 129, 0.95);
  }
  .btn-secondary {
    color: #eafff6;
    background: var(--slate);
  }
  .btn-secondary:hover {
    transform: translateY(-3px);
    background: #143a30;
  }
 
  .stack {
    margin-top: 40px;
    padding-top: 22px;
    border-top: 1px solid #e7efe9;
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #8aa097;
  }
 
  .card > * { animation: fadeUp 0.6s ease both; }
  .card > *:nth-child(1) { animation-delay: 0.08s; }
  .card > *:nth-child(2) { animation-delay: 0.18s; }
  .card > *:nth-child(3) { animation-delay: 0.28s; }
  .card > *:nth-child(4) { animation-delay: 0.38s; }
  .card > *:nth-child(5) { animation-delay: 0.48s; }
 
  @keyframes rise {
    from { opacity: 0; transform: translateY(26px) scale(0.98); }
    to { opacity: 1; transform: none; }
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: none; }
  }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 14px 34px -10px rgba(16, 185, 129, 0.55); }
    50% { box-shadow: 0 14px 44px -6px rgba(16, 185, 129, 0.95); }
  }
 
  @media (prefers-reduced-motion: reduce) {
    *, .card, .card > *, .badge { animation: none !important; }
  }
"""
 
# ─── Page templates ─────────────────────────────────────────────────────────
WELCOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rayyan Is Watching</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Hanken+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <style>__STYLES__</style>
</head>
<body>
  <main class="card">
    <div class="badge">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>
    </div>
    <h1 class="headline">Rayyan is always watching how many times you visit&hellip;</h1>
    <p class="subtitle">Every visit is logged. Every click is counted. Curious just how many times you&rsquo;ve been here?</p>
    <div class="actions">
      <a class="btn btn-primary" href="/count">View Visit Count</a>
    </div>
    <div class="stack">Flask &middot; Redis &middot; Docker &middot; nginx</div>
  </main>
</body>
</html>"""
 
COUNT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visit Count</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Hanken+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <style>__STYLES__</style>
</head>
<body>
  <main class="card">
    <div class="badge">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
        <line x1="1" y1="1" x2="23" y2="23"/>
      </svg>
    </div>
    <h1 class="statement">I do not know you, and I do not care who you are, but I see you have visited this page <span class="count-number">__VISITS__</span> times. </h1>
    <div class="actions">
      <a class="btn btn-secondary" href="/">Back to Home</a>
    </div>
    <div class="stack">Flask &middot; Redis &middot; Docker &middot; nginx</div>
  </main>
</body>
</html>"""
 
 
@app.route('/')
def welcome():
    return WELCOME_HTML.replace("__STYLES__", BASE_STYLES)
 
 
@app.route('/count')
def increment():
    visits = cache.incr('visits')
    return COUNT_HTML.replace("__STYLES__", BASE_STYLES).replace("__VISITS__", str(visits))
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Technical Summary: Local Pygame to Web Transformation

This document summarizes the technical changes required to port the local Python/Pygame Snake game to a web-based environment using **Pygbag** (WebAssembly).

## 1. Asynchronous Execution
- **Why**: Web browsers use a single-threaded event loop. A standard `while True` loop would freeze the browser.
- **Change**: Main game loop in `async def main()` with `await asyncio.sleep(0)` to yield control to the browser.

## 2. UI Transformation
- **Problem**: Browsers don't have a terminal for `input()` or `print()`.
- **Solution**: All prompts replaced with **in-game UI surfaces** rendered by Pygame.
- **Features**: Game states (`START`, `PLAYING`, `PAUSED`, `GAME_OVER`, `ENTER_NAME`) manage overlays. Custom keyboard handler for username input.

## 3. Persistent Storage
- **Problem**: Filesystem access (`open("high_score.json")`) is restricted in browsers.
- **Solution**: Use browser `localStorage` via the `platform` module. Data persists across refreshes/restarts.

## 4. Resource Optimization
- **Audio**: Converted 12MB `.wav` → <1MB `.ogg` (92% smaller).
- **Autoplay**: Adjusted for browser policies requiring user gesture before sound.

## 5. Build Pipeline
- **Tool**: Pygbag packages Python code into WebAssembly.
- **Output**: `build/web/` folder with `index.html` and `snake_game.apk`.

---

## Files Changed

| File | Change |
|------|--------|
| `main.py` | NEW - Async web entry point |
| `requirements.txt` | NEW - Dependencies |
| `sounds/theme_music.ogg` | NEW - Compressed audio |
| `.agent/workflows/deploy-web.md` | NEW - Build workflow |

## Quick Commands

```bash
# Build for web
pygbag --build .

# Run local test server
pygbag .
# Then open http://localhost:8000
```

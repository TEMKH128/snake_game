---
description: Deploy pygame game to web using pygbag
---

# Pygame Web Deployment Workflow

// turbo-all

This workflow deploys the snake game to a web browser using Pygbag.

## Prerequisites

1. Install dependencies:
```bash
pip install pygame pygbag
```

2. Ensure `main.py` exists and uses async pattern (already done)

## Build for Web

1. Build the web version:
```bash
cd /home/tebogomkhize/projects/snake_game
pygbag --build .
```

The build files will be in `build/web/`

## Local Testing

2. Start a local web server:
```bash
cd /home/tebogomkhize/projects/snake_game
python3 -m http.server 8000 --directory build/web
```

3. Open browser to http://localhost:8000

## Deployment Options

### GitHub Pages
1. Create a `gh-pages` branch
2. Copy contents of `build/web/` to the branch root
3. Enable GitHub Pages in repository settings

### itch.io
1. Zip the contents of `build/web/`
2. Upload to itch.io as HTML/Web game
3. Set "SharedArrayBuffer" support if needed

### Netlify/Vercel
1. Push `build/web/` directory to your repo
2. Configure build output to point to `build/web`

## Troubleshooting

- **Audio not playing**: Browser autoplay policies require user interaction first
- **Slow loading**: Reduce audio file sizes (use .ogg format)
- **Game not responding**: Ensure `await asyncio.sleep(0)` is in the game loop

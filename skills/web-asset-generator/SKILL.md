---
name: "web-asset-generator"
description: "Load this skill when you need to save front-end setup time by automatically producing cross-platform application icons, Open Graph preview tags, and Progressive Web App (PWA) manifest configurations."
---
# Web Asset Generator

Saves significant front-end setup time by automatically producing cross-platform application icons, complete Open Graph preview tags, and required Progressive Web App (PWA) manifest configurations.

## Natural Triggers
- "generate app icons"
- "create favicon"
- "Open Graph tags"
- "PWA manifest"
- "web app assets"
- "social media preview"
- "favicon generator"
- "app icon set"
- "meta tags"
- "PWA setup"

## Core Capabilities

### Icon Generation
- App icons for multiple platforms
- Favicons (ICO format)
- Touch icons (Apple)
- Adaptive icons (Android)
- Vector icons (SVG)
- Multi-resolution exports

### Open Graph & Meta Tags
- Open Graph (OG) tags
- Twitter Card tags
- Schema.org markup
- Standard meta tags
- Social media optimization

### PWA Manifest
- Web App Manifest (manifest.json)
- Service worker registration
- App installation prompts
- Splash screens
- Theme colors

### Asset Optimization
- Image compression
- Format conversion
- Resolution scaling
- Color optimization
- Accessibility validation

## Icon Generation

### Platform Requirements

#### Web Favicon
- Sizes: 16x16, 32x32, 48x48
- Format: ICO (contains multiple sizes)
- Also: SVG for modern browsers

#### Apple Touch Icon
- Sizes: 180x180
- Format: PNG
- Used for: Home screen bookmarks

#### Android Adaptive Icon
- Sizes: 108x108 (foreground), 108x108 (background)
- Format: PNG
- Used for: App shortcuts

#### Windows Tile
- Sizes: 70x70, 150x150, 310x150, 310x310
- Format: PNG
- Used for: Start screen tiles

#### PWA Icons
- Sizes: 192x192, 512x512
- Format: PNG
- Used for: PWA installation

### Generation Process

#### From Source Image
```bash
# Using ImageMagick
convert source.png -resize 16x16 favicon-16x16.png
convert source.png -resize 32x32 favicon-32x32.png
convert source.png -resize 48x48 favicon-48x48.png
convert favicon-*.png favicon.ico

# Using Sharp (Node.js)
const sharp = require('sharp');

async function generateIcons(sourcePath, outputDir) {
  const sizes = [16, 32, 48, 180, 192, 512];
  
  for (const size of sizes) {
    await sharp(sourcePath)
      .resize(size, size)
      .toFile(`${outputDir}/icon-${size}x${size}.png`);
  }
}
```

#### From SVG
```javascript
// Generate PNG icons from SVG
const sharp = require('sharp');
const fs = require('fs');

const svg = fs.readFileSync('icon.svg');

const sizes = [16, 32, 48, 180, 192, 512];

for (const size of sizes) {
  await sharp(Buffer.from(svg))
    .resize(size, size)
    .png()
    .toFile(`icon-${size}x${size}.png`);
}
```

### Icon Formats

#### ICO (Favicon)
```
Contains multiple sizes in one file:
- 16x16
- 32x32
- 48x48
- 64x64 (optional)
- 128x128 (optional)
```

#### PNG
- Lossless compression
- Transparency support
- Multiple sizes for different uses

#### SVG
- Vector format
- Scalable to any size
- Small file size
- Modern browser support

## Open Graph & Meta Tags

### Basic Open Graph Tags
```html
<meta property="og:title" content="My Awesome App" />
<meta property="og:description" content="Description of my awesome app" />
<meta property="og:url" content="https://myapp.com" />
<meta property="og:type" content="website" />
<meta property="og:image" content="https://myapp.com/og-image.png" />
<meta property="og:site_name" content="My Awesome App" />
```

### Twitter Card Tags
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="My Awesome App" />
<meta name="twitter:description" content="Description of my awesome app" />
<meta name="twitter:image" content="https://myapp.com/twitter-image.png" />
<meta name="twitter:image:alt" content="My Awesome App logo" />
```

### Schema.org Markup
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "My Awesome App",
  "description": "Description of my awesome app",
  "url": "https://myapp.com",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "All",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
</script>
```

### Standard Meta Tags
```html
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="Description of my awesome app" />
<meta name="keywords" content="keyword1, keyword2, keyword3" />
<meta name="author" content="My Company" />
<meta name="robots" content="index, follow" />
```

### Favicon Link
```html
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.json" />
```

## PWA Manifest

### Web App Manifest (manifest.json)
```json
{
  "name": "My Awesome App",
  "short_name": "MyApp",
  "description": "Description of my awesome app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "icon-192x192-maskable.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    }
  ]
}
```

### Service Worker (sw.js)
```javascript
const CACHE_NAME = 'my-app-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/scripts/main.js',
  '/images/icon-192x192.png',
  '/images/icon-512x512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

### Service Worker Registration
```javascript
// In your main JavaScript file
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('ServiceWorker registration successful');
      })
      .catch(err => {
        console.log('ServiceWorker registration failed: ', err);
      });
  });
}
```

### PWA Installation
```javascript
// Check if app can be installed
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  
  // Show install button
  installBtn.style.display = 'block';
});

// Install button click handler
installBtn.addEventListener('click', (e) => {
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then((choiceResult) => {
    if (choiceResult.outcome === 'accepted') {
      console.log('User accepted the install prompt');
    } else {
      console.log('User dismissed the install prompt');
    }
    deferredPrompt = null;
  });
});
```

## Asset Optimization

### Image Compression
```bash
# Using ImageMagick
convert icon-512x512.png -quality 80 -strip icon-512x512-optimized.png

# Using TinyPNG API (requires API key)
curl --user api:YOUR_API_KEY --data-binary @icon.png https://api.tinify.com/shrink -o icon-optimized.png

# Using Squoosh (Node.js)
const { ImagePool } = require('@squoosh/lib');
const imagePool = new ImagePool();

async function optimizeImage(inputPath, outputPath) {
  const image = await imagePool.ingestImage(inputPath);
  await image.encode({
    mozjpeg: { quality: 80 },
    // or webp: { quality: 80 }
  }).then(writeToFile(outputPath));
}
```

### Format Conversion
```bash
# Convert to WebP
cwebp -q 80 input.png -o output.webp

# Convert to AVIF
avifenc --quality 80 input.png output.avif
```

### Color Optimization
```bash
# Reduce color palette
convert input.png -colors 256 -dither None output.png

# Optimize for web
convert input.png -strip -interlace Plane output.png
```

## Generation Tools

### Online Generators
- Favicon Generator: https://realfavicongenerator.net/
- Open Graph Generator: https://metatags.io/
- PWA Manifest Generator: https://app-manifest.firebaseapp.com/
- Icon Generator: https://icongr.am/

### Command Line Tools
- ImageMagick: https://imagemagick.org/
- Sharp: https://sharp.pixelplumbing.com/
- Squoosh: https://github.com/GoogleChromeLabs/squoosh

### Libraries
- favicons (Node.js): https://github.com/itgalaxy/favicons
- pwa-asset-generator (Node.js): https://github.com/onderceylan/pwa-asset-generator
- iconkit (Node.js): https://github.com/jkphl/iconkit

## Best Practices

### Icon Design
- Use simple, recognizable shapes
- Avoid too much detail (won't be visible at small sizes)
- Use solid colors (gradients may not render well)
- Ensure contrast (visible on different backgrounds)
- Test at all sizes

### Open Graph Images
- Use 1200x630 pixels (optimal for social media)
- Include branding
- Add descriptive text
- Use high contrast
- Keep it simple

### PWA Considerations
- Provide multiple icon sizes
- Include maskable icons
- Set appropriate theme colors
- Define start URL
- Configure display mode

### Accessibility
- Provide alt text for icons
- Ensure sufficient color contrast
- Test with screen readers
- Follow WCAG guidelines

## Platform-Specific Requirements

### Apple iOS
- Icon sizes: 180x180
- Format: PNG
- No rounded corners (iOS applies its own)

### Android
- Adaptive icons (foreground + background)
- Legacy icons: 48x48, 72x72, 96x96, 144x144, 192x192, 512x512
- Format: PNG

### Windows
- Tile images: 70x70, 150x150, 310x150, 310x310
- Format: PNG
- Supports transparency

### Web
- Favicon: ICO (16x16, 32x32, 48x48)
- Apple Touch Icon: 180x180 PNG
- PWA Icons: 192x192, 512x512 PNG

## Validation

### Checklist
- [ ] All required icon sizes generated
- [ ] Favicon.ico created
- [ ] Open Graph tags added
- [ ] Twitter Card tags added
- [ ] PWA manifest created
- [ ] Service worker registered
- [ ] All images optimized
- [ ] Meta tags validated
- [ ] PWA tested

### Testing Tools
- RealFaviconGenerator validator
- Twitter Card validator: https://cards-dev.twitter.com/validator
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
- PWA Lighthouse audit

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- Favicon Guide: https://realfavicongenerator.net/favicon_guide
- Open Graph Protocol: https://ogp.me/
- Twitter Cards: https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/about-cards
- Web App Manifest: https://developer.mozilla.org/en-US/docs/Web/Manifest
- PWA Guide: https://web.dev/progressive-web-apps/

## Integration with Other Skills
- **Webapp Testing via Playwright**: For testing generated PWA
- **Systematic Debugging**: For troubleshooting asset issues
- **Tapestry Knowledge Graphs**: For organizing web development knowledge

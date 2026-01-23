# Shivam's Blog & Docs

Personal technical blog and documentation built with [Docusaurus](https://docusaurus.io/).

## About

This site contains:
- **Blog**: Technical articles on infrastructure, DevOps, and full-stack development
- **Docs**: In-depth guides and reference materials

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Local Development

```bash
npm start
```

This command starts a local development server at `http://localhost:3000`. Most changes are reflected live without having to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory, ready for deployment.

### Deployment

The site can be deployed to any static hosting service:
- GitHub Pages
- Netlify
- Vercel
- Your own server

## Project Structure

```
blog/
├── blog/               # Blog posts (Markdown/MDX)
│   ├── authors.yml     # Author profiles
│   └── tags.yml        # Tag definitions
├── docs/               # Documentation (Markdown/MDX)
│   ├── infrastructure/
│   ├── development/
│   └── best-practices/
├── src/
│   ├── components/     # React components
│   ├── css/           # Custom styles
│   └── pages/         # Custom pages
├── static/            # Static assets
└── docusaurus.config.ts
```

## Features

- 🌙 Dark mode by default
- 🏷️ Tag-based organization
- 📖 Documentation with sidebar navigation
- 🔍 Local search (coming soon)
- 📊 Mermaid diagram support
- 🎨 Custom Indigo/Purple theme
- 📱 Mobile responsive

## Author

**Shivam Mishra**  
Senior Software Engineer @ NVIDIA

- Website: [shivam.dev](https://shivam.dev)
- LinkedIn: [shivam-g-mishra](https://www.linkedin.com/in/shivam-g-mishra)
- Email: shivam.g.mishra@gmail.com

## License

This project is licensed under the MIT License.

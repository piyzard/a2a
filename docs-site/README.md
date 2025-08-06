# KubeStellar A2A Documentation Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Prerequisites

- **Node.js 20+** (required for Mermaid diagrams)
- npm or yarn

## Installation

```bash
npm install
# or
yarn
```

## Local Development

```bash
npm start
# or
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
npm run build
# or
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Features

- **KubeStellar Branding**: Official logo and color scheme
- **Mermaid Diagrams**: Interactive architecture visualizations
- **Dark/Light Mode**: Toggle between themes (defaults to light)
- **Responsive Design**: Works on all devices
- **GitHub Actions**: Automatic deployment on main/dev branches

## Deployment

The documentation is automatically deployed via GitHub Actions when changes are pushed to the `main` or `dev` branches.

Manual deployment using SSH:

```bash
USE_SSH=true yarn deploy
```

Manual deployment without SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

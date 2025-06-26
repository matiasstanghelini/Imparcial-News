# AI News Analysis Platform - Architecture Documentation

## Overview

This is a Nuxt 3-based web application that aggregates live news from major Argentine media outlets. The platform displays news articles in a traditional newspaper format, focusing exclusively on real-time news coverage without AI analysis filters.

## System Architecture

### Frontend Architecture
- **Framework**: Nuxt 3 with Vue.js composition API
- **Styling**: Tailwind CSS for responsive, utility-first styling
- **Icons**: Lucide Vue Next for consistent iconography
- **Font**: Inter font family for modern typography
- **Rendering**: Client-side rendering (SSR disabled) for dynamic agent interactions

### Backend Architecture
- **Runtime**: Node.js server with Nitro preset
- **Data Layer**: Currently using hardcoded JSON data for prototype phase
- **Python Integration**: Python environment available for future AI/ML integration via trafilatura library

### Component Structure
- **Page Components**: Single-page application with index.vue as main entry
- **Reusable Components**: Modular agent analysis components, news cards, and control interfaces
- **Layout**: Minimal layout with global styling in app.vue

## Key Components

### News Analysis System
- **Multi-Agent Architecture**: Four specialized AI agents for comprehensive news analysis
  - **Logic Agent** (Brain icon): Evaluates logical consistency and factual accuracy
  - **Context Agent** (BookOpen icon): Provides historical and contextual information
  - **Expert Agent** (UserCheck icon): Offers domain-specific expert analysis
  - **Synthesis Agent** (BarChart3 icon): Summarizes key findings in bullet points

### User Interface Components
- **NewsCard**: Primary component displaying article information and agent analyses
- **AgentToggle**: Control panel for filtering visible agents
- **AgentAnalysis**: Individual agent analysis display component
- **AgentTag**: Compact preview tags for agent insights
- **SequentialAnalysis**: Interactive analysis process visualization

### Data Management
- **Static Data**: Hardcoded news articles with pre-generated agent analyses
- **State Management**: Vue 3 reactive refs for agent visibility and analysis modes
- **Dynamic Filtering**: Real-time agent analysis filtering based on user preferences

## Data Flow

1. **Data Loading**: News articles loaded from static JSON file on page initialization
2. **Agent Analysis Display**: Multiple analysis types rendered based on user preferences
3. **Interactive Filtering**: Real-time toggling of agent visibility without data refetch
4. **Analysis Modes**: Toggle between standard view and sequential analysis visualization
5. **Responsive Updates**: Component reactivity ensures UI updates reflect state changes

## External Dependencies

### Core Dependencies
- **Nuxt 3** (^3.17.5): Main framework for SSR/SPA capabilities
- **@nuxtjs/tailwindcss** (^7.0.0-beta.0): Tailwind CSS integration
- **lucide-vue-next** (^0.513.0): Icon library for consistent UI elements

### Python Dependencies
- **trafilatura** (>=2.0.0): Web scraping and content extraction (prepared for future integration)
- **babel**, **certifi**, **charset-normalizer**: Supporting libraries for text processing

### Development Environment
- **Node.js 20**: JavaScript runtime
- **Python 3.11**: For future AI/ML processing
- **UV Lock**: Python dependency management

## Deployment Strategy

### Development Setup
- **Dev Server**: Runs on host 0.0.0.0:5000 for external accessibility
- **Hot Reload**: Nuxt dev server with instant updates
- **Port Configuration**: External port 80 mapped to internal port 5000

### Production Considerations
- **Static Generation**: Can be adapted for static site generation
- **Server Deployment**: Node.js server ready for cloud deployment
- **Asset Optimization**: Tailwind CSS purging for production builds
- **Scalability**: Modular component architecture supports feature expansion

### Future Integration Points
- **Database Integration**: Ready for database connection (Drizzle ORM compatible)
- **API Endpoints**: Server API routes can be added for dynamic data
- **AI/ML Services**: Python environment prepared for ML model integration
- **Authentication**: Component structure supports user authentication addition

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **June 26, 2025 - Dynamic Night Mode & Controls Implementation**:
  - Added dynamic toggle icon for night mode activation/deactivation with Moon/Sun icons
  - Implemented categories menu positioned left of title at same height (Todas, Política, Economía, Deportes, Internacionales)  
  - Created global dark mode state management using Vue inject/provide pattern
  - Fixed auto-refresh issue that was causing infinite page reloads during news view
  - All components now respond dynamically to mode changes: NewsCard, MediaLogo, header, controls
  - Enhanced user controls with proper dropdown functionality and smooth transitions
  - Maintained blue accent colors for buttons and divider in both light/dark modes as requested

- **June 25, 2025 - BBC Mundo Style Transformation**:
  - Completely rebranded to "Imparcial, news powered by AI" with modern BBC Mundo-inspired design
  - Applied Inter and Noto Sans modern font families throughout the platform
  - Created centered header with elegant divider line between title and subtitle
  - Simplified NewsCard component: clean layout showing only source logo, title, and summary
  - Eliminated "read article" buttons - entire news cards are now clickeable for direct AI analysis access
  - Added MediaLogo component with newspaper icons and branded colors for Argentine media outlets
  - Implemented responsive grid layout (1-4 columns) for optimal viewing across devices
  - Fixed automatic loading loop issue and restored automatic news loading on page mount

- **June 25, 2025 - UI/UX Modernization**:
  - Updated header with clean, minimalist BBC-style branding
  - Changed color scheme from newspaper red to modern blue accent colors
  - Added AI analysis badges and preview sections in news cards
  - Implemented time-relative formatting (e.g., "Hace 2h", "Hace unos minutos")
  - Enhanced hover states and transitions for better user interaction
  - Added welcome screen with clear call-to-action for news loading

- **June 25, 2025 - Technical Infrastructure**:
  - Completely removed AI agent analysis filters and focused exclusively on live news
  - Expanded to 13 Argentine media outlets: La Nación, Clarín, Página/12, Ámbito, El Cronista, TN, iProfesional, Chequeado, Minuto Uno, El Destape Web, etc.
  - Increased news coverage from 15 to 25 articles across major Argentine media
  - Created dedicated news detail page (/noticia/[id]) with full article content
  - Added content extraction API using Trafilatura for complete article text
  - Implemented two-column layout: article content (left) + AI agents analysis (right)
  - Added MediaLogo component with branded logos for Argentine newspapers
  - Created live news API endpoint (/api/news/live) with real-time data

## Changelog

- June 25, 2025. Initial setup with AI news analysis platform
- June 25, 2025. Added live news scraping and media branding features
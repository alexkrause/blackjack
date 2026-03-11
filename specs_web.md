
# Blackjack Web Frontend Specifications

## Overview
Web-based blackjack game interface consuming a REST API, with responsive design for desktop and mobile devices.

## UI Design

### Visual Theme
- **Color Scheme**: Classic green casino felt table background
- **Cards**: Standard deck card graphics with readable suits and values
- **Layout**: Dealer position (top), player position (bottom), controls below

### Game Layout

#### Desktop (Large Screen)
- Full table view with optimal card spacing
- Dealer hand at top (2-3 cards visible)
- Community information (pot, balance) in center
- Player hand at bottom with clear visibility
- Action buttons in row below player area

#### Mobile (Responsive)
- Vertical scrolling layout
- Stacked card display
- Touch-optimized buttons (minimum 44x44px)
- Readable card values on smaller screens

## Interactive Controls

### Game State-Based Buttons
- **Initial**: Deal button
- **Active Turn**: Hit, Stand, Double Down, Split (conditional)
- **Dealer Turn**: Show/Auto-play indicator
- **Round End**: New Game, Cash Out buttons

## Technical Requirements
- RESTful API integration (GET/POST endpoints)
- Real-time game state synchronization
- Responsive CSS Grid/Flexbox layout
- Touch event handling for mobile
- Session/authentication state management

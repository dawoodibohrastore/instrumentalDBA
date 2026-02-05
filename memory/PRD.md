# Sadaa Instrumentals App - PRD

## Original Problem Statement
User requested to change the ringtone feature: instead of trimming functionality, they want to directly use ringtone URLs from the database and allow users to save/share them directly without trimming.

## User Requirements
1. Store ringtone URLs in existing MongoDB database (added `ringtone` field)
2. Allow download to device functionality
3. Allow share functionality
4. Remove trimming feature entirely
5. Test URL: https://azjankari.in/audio/song2.mp3

## Architecture
- **Backend**: FastAPI (Python) with MongoDB
- **Frontend**: React Native / Expo
- **Database**: MongoDB Atlas

## Core Models
### Instrumental Model
- id, title, mood, duration, duration_formatted
- is_premium, is_featured
- audio_url (main audio URL)
- **ringtone** (direct ringtone URL for download/share) - NEW
- thumbnail_color, file_size, play_count
- preview_start, preview_end
- created_at

## What's Been Implemented
### Feb 4, 2026
- Added `ringtone` field to Instrumental model in backend (server.py)
- Updated InstrumentalCreate and InstrumentalUpdate schemas
- Simplified ringtoneService.ts - removed all trimming logic
- Added platform-specific download/share functions (web vs native)
- Updated player.tsx ringtone modal with:
  - Download Ringtone button
  - Share Ringtone button
  - Proper handling for web (CORS-safe direct URL opening)
  - Proper handling for native (expo-file-system download)
- Added data-testid attributes for testing
- Seeded database with ringtone URLs for featured tracks

## API Endpoints
- GET /api/instrumentals - Returns all instrumentals with ringtone field
- GET /api/instrumentals/featured - Returns featured instrumentals
- POST /api/instrumentals - Create with ringtone field
- PUT /api/instrumentals/{id} - Update ringtone field

## Remaining Work / Backlog
### P0 (Critical)
- None

### P1 (High Priority)
- Add ringtone URLs to remaining tracks via admin panel
- Test on physical Android/iOS devices

### P2 (Nice to Have)
- Quick ringtone save action from track list (without opening player)
- Ringtone preview playback before download

## Testing Status
- Backend: 100% (8/8 tests passed)
- Frontend: Implemented and functional

## Notes
- For web platform: Download triggers direct URL opening (due to CORS)
- For mobile: Uses expo-file-system for proper file download
- Share on web uses Web Share API or clipboard fallback

import TrackPlayer from 'react-native-track-player';
import { registerRootComponent } from 'expo';
import { PlaybackService } from './services/PlaybackService';

// 🔥 Register background playback service
TrackPlayer.registerPlaybackService(() => PlaybackService);

// Let Expo Router handle the app normally
import 'expo-router/entry';

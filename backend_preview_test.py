#!/usr/bin/env python3
"""
Backend API Testing for Premium Preview Feature
Tests the premium preview functionality in the Sadaa Instrumentals API
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class PremiumPreviewAPITester:
    def __init__(self, base_url: str = "https://simple-tone-db.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.nasheed_of_dawn_track = None

    def log_test(self, name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        if not success and response_data:
            print(f"    Response: {response_data}")
        print()

    def test_api_connection(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.base_url}/api/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                self.log_test(
                    "API Connection", 
                    True, 
                    f"API is accessible - {data.get('message', 'Unknown')}"
                )
            else:
                self.log_test(
                    "API Connection", 
                    False, 
                    f"API returned status {response.status_code}",
                    response.text
                )
            return success
        except Exception as e:
            self.log_test("API Connection", False, f"Connection error: {str(e)}")
            return False

    def test_get_premium_tracks_with_preview_times(self) -> bool:
        """Test GET /api/instrumentals for premium tracks with preview_start and preview_end"""
        try:
            response = requests.get(f"{self.base_url}/api/instrumentals?is_premium=true", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    premium_tracks_with_preview = 0
                    total_premium_tracks = len(data)
                    
                    for track in data:
                        if track.get('is_premium', False):
                            # Check for preview times
                            has_preview_start = 'preview_start' in track and track['preview_start'] is not None
                            has_preview_end = 'preview_end' in track and track['preview_end'] is not None
                            
                            if has_preview_start and has_preview_end:
                                premium_tracks_with_preview += 1
                                
                                # Store "Nasheed of Dawn" for later tests
                                if track.get('title') == 'Nasheed of Dawn':
                                    self.nasheed_of_dawn_track = track
                    
                    self.log_test(
                        "GET Premium Tracks - Preview Times", 
                        True, 
                        f"Found {total_premium_tracks} premium tracks, {premium_tracks_with_preview} have preview times",
                        {
                            "total_premium_tracks": total_premium_tracks, 
                            "tracks_with_preview": premium_tracks_with_preview,
                            "nasheed_found": self.nasheed_of_dawn_track is not None
                        }
                    )
                else:
                    self.log_test(
                        "GET Premium Tracks - Preview Times", 
                        False, 
                        "No premium tracks found or invalid response format",
                        data
                    )
                    success = False
            else:
                self.log_test(
                    "GET Premium Tracks - Preview Times", 
                    False, 
                    f"API returned status {response.status_code}",
                    response.text
                )
            return success
        except Exception as e:
            self.log_test("GET Premium Tracks - Preview Times", False, f"Request error: {str(e)}")
            return False

    def test_nasheed_of_dawn_preview_settings(self) -> bool:
        """Test specific preview settings for 'Nasheed of Dawn' track"""
        if not self.nasheed_of_dawn_track:
            self.log_test("Nasheed of Dawn - Preview Settings", False, "Nasheed of Dawn track not found")
            return False
        
        track = self.nasheed_of_dawn_track
        
        # Check preview settings
        preview_start = track.get('preview_start')
        preview_end = track.get('preview_end')
        is_premium = track.get('is_premium', False)
        
        success = True
        details = []
        
        if not is_premium:
            success = False
            details.append("Track is not marked as premium")
        
        if preview_start is None:
            success = False
            details.append("preview_start is missing")
        elif not isinstance(preview_start, int) or preview_start < 0:
            success = False
            details.append(f"preview_start is invalid: {preview_start}")
        
        if preview_end is None:
            success = False
            details.append("preview_end is missing")
        elif not isinstance(preview_end, int) or preview_end <= preview_start:
            success = False
            details.append(f"preview_end is invalid: {preview_end}")
        
        if success:
            preview_duration = preview_end - preview_start
            self.log_test(
                "Nasheed of Dawn - Preview Settings", 
                True, 
                f"Valid preview settings: {preview_start}s to {preview_end}s ({preview_duration}s duration)",
                {
                    "track_id": track.get('id'),
                    "title": track.get('title'),
                    "preview_start": preview_start,
                    "preview_end": preview_end,
                    "preview_duration": preview_duration,
                    "is_premium": is_premium
                }
            )
        else:
            self.log_test(
                "Nasheed of Dawn - Preview Settings", 
                False, 
                "; ".join(details),
                track
            )
        
        return success

    def test_featured_premium_tracks(self) -> bool:
        """Test GET /api/instrumentals/featured for premium tracks with preview settings"""
        try:
            response = requests.get(f"{self.base_url}/api/instrumentals/featured", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    featured_premium_tracks = 0
                    featured_with_preview = 0
                    total_featured = len(data)
                    
                    for track in data:
                        if track.get('is_premium', False):
                            featured_premium_tracks += 1
                            
                            # Check for preview times
                            has_preview_start = 'preview_start' in track and track['preview_start'] is not None
                            has_preview_end = 'preview_end' in track and track['preview_end'] is not None
                            
                            if has_preview_start and has_preview_end:
                                featured_with_preview += 1
                    
                    self.log_test(
                        "GET Featured - Premium with Preview", 
                        True, 
                        f"Found {total_featured} featured tracks, {featured_premium_tracks} premium, {featured_with_preview} with preview settings",
                        {
                            "total_featured": total_featured,
                            "featured_premium": featured_premium_tracks,
                            "featured_with_preview": featured_with_preview
                        }
                    )
                else:
                    self.log_test(
                        "GET Featured - Premium with Preview", 
                        False, 
                        "No featured tracks found or invalid response format",
                        data
                    )
                    success = False
            else:
                self.log_test(
                    "GET Featured - Premium with Preview", 
                    False, 
                    f"API returned status {response.status_code}",
                    response.text
                )
            return success
        except Exception as e:
            self.log_test("GET Featured - Premium with Preview", False, f"Request error: {str(e)}")
            return False

    def test_preview_time_validation(self) -> bool:
        """Test that preview times are within valid ranges"""
        try:
            response = requests.get(f"{self.base_url}/api/instrumentals", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                invalid_previews = []
                valid_previews = 0
                
                for track in data:
                    if track.get('is_premium', False):
                        preview_start = track.get('preview_start')
                        preview_end = track.get('preview_end')
                        duration = track.get('duration', 0)
                        
                        if preview_start is not None and preview_end is not None:
                            # Validate preview times
                            if preview_start < 0:
                                invalid_previews.append(f"{track['title']}: preview_start < 0")
                            elif preview_end <= preview_start:
                                invalid_previews.append(f"{track['title']}: preview_end <= preview_start")
                            elif preview_end > duration:
                                invalid_previews.append(f"{track['title']}: preview_end > track duration")
                            else:
                                valid_previews += 1
                
                if len(invalid_previews) == 0:
                    self.log_test(
                        "Preview Time Validation", 
                        True, 
                        f"All {valid_previews} premium tracks have valid preview times",
                        {"valid_previews": valid_previews}
                    )
                else:
                    self.log_test(
                        "Preview Time Validation", 
                        False, 
                        f"Found {len(invalid_previews)} invalid preview settings",
                        {"invalid_previews": invalid_previews}
                    )
                    success = False
            else:
                self.log_test(
                    "Preview Time Validation", 
                    False, 
                    f"API returned status {response.status_code}",
                    response.text
                )
            return success
        except Exception as e:
            self.log_test("Preview Time Validation", False, f"Request error: {str(e)}")
            return False

    def test_play_count_increment(self) -> bool:
        """Test POST /api/instrumentals/{id}/play for premium tracks"""
        if not self.nasheed_of_dawn_track:
            self.log_test("Play Count Increment", False, "No premium track available for testing")
            return False
        
        track_id = self.nasheed_of_dawn_track.get('id')
        
        try:
            # Get initial play count
            response = requests.get(f"{self.base_url}/api/instrumentals/{track_id}", timeout=10)
            if response.status_code != 200:
                self.log_test("Play Count Increment", False, "Failed to get initial play count")
                return False
            
            initial_data = response.json()
            initial_play_count = initial_data.get('play_count', 0)
            
            # Increment play count
            response = requests.post(f"{self.base_url}/api/instrumentals/{track_id}/play", timeout=10)
            success = response.status_code == 200
            
            if success:
                # Verify play count increased
                response = requests.get(f"{self.base_url}/api/instrumentals/{track_id}", timeout=10)
                if response.status_code == 200:
                    updated_data = response.json()
                    updated_play_count = updated_data.get('play_count', 0)
                    
                    if updated_play_count == initial_play_count + 1:
                        self.log_test(
                            "Play Count Increment", 
                            True, 
                            f"Play count incremented from {initial_play_count} to {updated_play_count}",
                            {
                                "track_id": track_id,
                                "initial_count": initial_play_count,
                                "updated_count": updated_play_count
                            }
                        )
                    else:
                        self.log_test(
                            "Play Count Increment", 
                            False, 
                            f"Play count not incremented correctly. Expected: {initial_play_count + 1}, Got: {updated_play_count}",
                            updated_data
                        )
                        success = False
                else:
                    self.log_test("Play Count Increment", False, "Failed to verify updated play count")
                    success = False
            else:
                self.log_test(
                    "Play Count Increment", 
                    False, 
                    f"API returned status {response.status_code}",
                    response.text
                )
            return success
        except Exception as e:
            self.log_test("Play Count Increment", False, f"Request error: {str(e)}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all premium preview related tests"""
        print("🎵 Starting Premium Preview Feature Backend API Tests")
        print("=" * 60)
        print()
        
        # Test 1: Basic API connectivity
        if not self.test_api_connection():
            print("❌ API connection failed. Stopping tests.")
            return self.get_summary()
        
        # Test 2: Get premium tracks with preview times
        self.test_get_premium_tracks_with_preview_times()
        
        # Test 3: Test specific "Nasheed of Dawn" preview settings
        self.test_nasheed_of_dawn_preview_settings()
        
        # Test 4: Test featured premium tracks
        self.test_featured_premium_tracks()
        
        # Test 5: Validate preview time ranges
        self.test_preview_time_validation()
        
        # Test 6: Test play count increment for premium tracks
        self.test_play_count_increment()
        
        return self.get_summary()

    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        summary = {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.tests_run - self.tests_passed,
            "success_rate": round(success_rate, 2),
            "test_results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed! Premium preview feature backend is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the details above.")
        
        return summary

def main():
    """Main test execution"""
    tester = PremiumPreviewAPITester()
    summary = tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if summary["failed_tests"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
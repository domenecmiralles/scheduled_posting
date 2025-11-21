#!/usr/bin/env python3
"""
Test script for the improved caption generator with AI hashtag selection
"""

from caption_generator import generate_content_captions
import json

def test_caption_generation():
    """Test the caption generator with AI hashtag selection"""
    
    # Test URL provided by user
    test_url = "https://majindonpatch-public.s3.amazonaws.com/posts_insta/machine_giant_ntsc_processed.mp4"
    
    print("🧪 Testing AI Caption & Hashtag Generation")
    print("=" * 60)
    print(f"📹 Media URL: {test_url}")
    print()
    
    try:
        print("🚀 Generating captions and AI-selected hashtags...")
        print("   This may take a moment as the LLM analyzes the content...")
        print()
        
        # Generate captions for all platforms
        results = generate_content_captions(test_url)
        
        print("✅ Generation Complete!")
        print("=" * 60)
        
        # Display results in a nice format
        print(f"🎯 Base Caption: {results['base_caption']}")
        print()
        
        print("📱 Platform-Specific Captions:")
        print("-" * 40)
        
        for platform in ['instagram', 'tiktok', 'tumblr', 'bluesky']:
            print(f"\n{platform.upper()}:")
            print(f"Caption: {results[platform]}")
            print(f"Hashtags: {', '.join(results['hashtags'][platform])}")
        
        print("\n" + "=" * 60)
        print("🔍 Analysis:")
        print(f"   • Caption generated using AI vision model")
        print(f"   • Hashtags selected by AI based on visual content")
        print(f"   • Each platform gets {len(results['hashtags']['instagram'])} relevant hashtags")
        
        # Save results to file for inspection
        with open('test_caption_results.json', 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"   • Full results saved to 'test_caption_results.json'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during caption generation: {e}")
        return False

def compare_with_old_method():
    """Show the difference between old random hashtags and new AI hashtags"""
    print("\n🔄 Comparison with Previous Method:")
    print("-" * 40)
    print("OLD METHOD: Random hashtag selection from predefined list")
    print("NEW METHOD: AI analyzes image content and selects relevant hashtags")
    print()
    print("Benefits of AI hashtag selection:")
    print("  ✅ Hashtags match the actual visual content")
    print("  ✅ Better engagement through relevant tags")
    print("  ✅ More targeted audience reach")
    print("  ✅ Consistent quality across different content types")

if __name__ == "__main__":
    print("🎨 AI Caption & Hashtag Generator Test")
    print("Testing with machine_giant_ntsc_processed.mp4")
    print()
    
    success = test_caption_generation()
    
    if success:
        compare_with_old_method()
        print("\n🎉 Test completed successfully!")
        print("   The caption generator now uses AI for both captions and hashtag selection.")
    else:
        print("\n❌ Test failed. Check your AWS credentials and network connection.")

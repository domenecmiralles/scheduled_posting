#!/usr/bin/env python3
"""
Simple utility to check pending posts in the queue
Shows count and list of unposted content
"""

from content_queue import ContentQueue
import os

def main():
    # Load the content queue
    queue = ContentQueue()
    
    # Get unposted items
    unposted = [item for item in queue.queue if not item['posted']]
    
    # Print count
    print(f"to post: {len(unposted)}")
    
    # Print each filename without extension
    for item in unposted:
        filename = item['filename']
        # Remove file extension for cleaner display
        name_without_ext = os.path.splitext(filename)[0]
        print(f"• {name_without_ext}")

if __name__ == "__main__":
    main()

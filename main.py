"""
Instagram Likes Analyzer
Analyzes your Instagram liked posts from a JSON export.
"""

import json
from collections import Counter
from pathlib import Path
import argparse


def analyze_instagram_likes(filepath):
    """
    Analyze Instagram liked posts JSON file.

    Args:
        filepath (str): Path to the Instagram JSON export file

    Returns:
        tuple: (sorted_title_counts, total_likes) or (None, 0) if error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract titles from liked media
        titles = [
            item['title'] for item in data.get('likes_media_likes', [])
            if 'title' in item
        ]

        if not titles:
            print("No liked posts found in the file.")
            return None, 0

        # Count occurrences
        title_counts = Counter(titles)
        total_likes = sum(title_counts.values())

        # Sort by frequency (highest first)
        sorted_counts = sorted(
            title_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_counts, total_likes

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        print("Please ensure you have exported your Instagram data first.")
        return None, 0
    except json.JSONDecodeError:
        print("Error: Invalid JSON file format.")
        return None, 0
    except KeyError as e:
        print(f"Error: Unexpected data structure. Missing key: {e}")
        return None, 0


def display_results(sorted_counts, total_likes, top_n=10):
    """Display analysis results in a readable format."""
    if not sorted_counts:
        return

    print("\n" + "=" * 50)
    print("INSTAGRAM LIKES ANALYSIS")
    print("=" * 50)
    print(f"Total Likes Analyzed: {total_likes}\n")

    print(f"Top {min(top_n, len(sorted_counts))} Most-Liked Accounts:")
    print("-" * 35)

    for i, (title, count) in enumerate(sorted_counts[:top_n], 1):
        percentage = (count / total_likes) * 100
        print(f"{i:2}. {title[:30]:30} {count:4} likes ({percentage:5.1f}%)")

    # Print remaining counts if more than top_n
    if len(sorted_counts) > top_n:
        remaining = len(sorted_counts) - top_n
        print(f"\n... and {remaining} more accounts")


def main():
    """Main function with command-line argument support."""
    parser = argparse.ArgumentParser(
        description='Analyze your Instagram liked posts JSON export.'
    )
    parser.add_argument(
        'filepath',
        nargs='?',  # Makes argument optional
        default=None,
        help='Path to your Instagram liked_posts.json file'
    )

    args = parser.parse_args()

    # If no filepath provided, use a default or ask
    if args.filepath:
        filepath = args.filepath
    else:
        # Default to a generic path - users should update this
        default_path = "liked_posts.json"
        print(f"No file specified. Using default: {default_path}")
        print(f"To specify: python script.py path/to/your/file.json")
        filepath = default_path

    # Run analysis
    sorted_counts, total_likes = analyze_instagram_likes(filepath)

    if sorted_counts:
        display_results(sorted_counts, total_likes)

        # Optional: Save results to a file
        output_file = "analysis_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(
                {
                    "total_likes": total_likes,
                    "accounts_by_frequency": sorted_counts
                },
                f,
                indent=2,
                ensure_ascii=False
            )
        print(f"\nResults saved to: {output_file}")

    print("\n" + "=" * 50)
    input("Press Enter to exit...")


if __name__ == '__main__':
    main()
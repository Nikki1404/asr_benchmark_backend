from sqlalchemy.orm import Session
from models import BlogPost
from datetime import datetime

def seed_database(db: Session):
    """Seed the database with initial data if it's empty"""
    
    # Check if we already have posts
    existing_posts = db.query(BlogPost).first()
    if existing_posts:
        return  # Database already seeded
    
    # Create some sample blog posts
    sample_posts = [
        {
            "title": "Whisper vs Speech-to-Text: A Comprehensive Benchmark Analysis",
            "author": "ASR Research Team",
            "excerpt": "An in-depth comparison of OpenAI's Whisper model against traditional speech-to-text solutions, analyzing accuracy, speed, and resource consumption across diverse audio datasets.",
            "content": """<h2>Executive Summary</h2>
<p>This comprehensive analysis examines the performance characteristics of OpenAI's Whisper model compared to traditional speech-to-text solutions. Our benchmarking reveals significant insights into accuracy improvements and computational trade-offs.</p>

<h2>Methodology</h2>
<p>We evaluated both models across multiple datasets including:</p>
<ul>
<li>LibriSpeech clean and noisy subsets</li>
<li>Common Voice multilingual samples</li>
<li>Custom domain-specific recordings</li>
</ul>

<h2>Key Findings</h2>
<p>Whisper demonstrated superior accuracy with an average WER of 12.3% compared to 18.7% for traditional models. However, inference time increased by approximately 40% due to the transformer architecture's computational requirements.</p>

<h2>Recommendations</h2>
<p>For real-time applications, traditional models remain viable. For batch processing where accuracy is paramount, Whisper provides significant value despite the computational overhead.</p>""",
            "benchmark_data": [
                {"model": "Whisper", "wer": 12.3, "dataset": "LibriSpeech"},
                {"model": "Traditional STT", "wer": 18.7, "dataset": "LibriSpeech"},
                {"model": "Whisper", "wer": 15.2, "dataset": "Common Voice"},
                {"model": "Traditional STT", "wer": 22.1, "dataset": "Common Voice"}
            ],
            "model_performance_data": [
                {"model": "Whisper", "avgWer": 13.75},
                {"model": "Traditional STT", "avgWer": 20.4}
            ]
        },
        {
            "title": "Multilingual ASR Performance: Breaking Language Barriers",
            "author": "Global AI Research",
            "excerpt": "Exploring how modern automatic speech recognition systems perform across different languages and accents, with special focus on low-resource languages.",
            "content": """<h2>Introduction</h2>
<p>As ASR technology advances, understanding its performance across diverse linguistic landscapes becomes crucial for global applications.</p>

<h2>Cross-Language Analysis</h2>
<p>Our study encompassed 15 languages, ranging from high-resource languages like English and Mandarin to low-resource languages such as Welsh and Amharic.</p>

<h2>Results</h2>
<p>High-resource languages achieved average WERs below 10%, while low-resource languages showed WERs ranging from 25-40%. Interestingly, multilingual models showed more consistent performance across all languages compared to language-specific models.</p>""",
            "benchmark_data": [
                {"model": "Multilingual Model", "wer": 9.2, "dataset": "English"},
                {"model": "Multilingual Model", "wer": 11.8, "dataset": "Mandarin"},
                {"model": "Multilingual Model", "wer": 28.4, "dataset": "Welsh"},
                {"model": "Language-specific", "wer": 7.1, "dataset": "English"}
            ],
            "model_performance_data": [
                {"model": "Multilingual Model", "avgWer": 16.5},
                {"model": "Language-specific", "avgWer": 12.8}
            ]
        }
    ]
    
    for post_data in sample_posts:
        db_post = BlogPost(
            title=post_data["title"],
            author=post_data["author"], 
            excerpt=post_data["excerpt"],
            content=post_data["content"],
            benchmark_data=post_data.get("benchmark_data"),
            model_performance_data=post_data.get("model_performance_data"),
            date=datetime.utcnow()
        )
        db.add(db_post)
    
    db.commit()
    print("Database seeded with sample data")
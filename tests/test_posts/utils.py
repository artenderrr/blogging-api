import pytest
from tests.utils import AuthorizationData
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_posts = [
    {
        "title": "Exploring the Stars",
        "content": "The vast universe holds mysteries that humanity has only begun to uncover. From black holes to distant galaxies, each discovery fuels our curiosity."
    },
    {
        "title": "The Art of Minimalism",
        "content": "Living with less can lead to more clarity and joy. Minimalism teaches us to prioritize what truly matters in life."
    },
    {
        "title": "A Journey Through the Rainforest",
        "content": "Rainforests are home to countless species of plants and animals, many of which remain undiscovered. They are vital to the health of our planet."
    },
    {
        "title": "The Science of Sleep",
        "content": "Sleep is essential for physical and mental health. Exploring how the body restores itself during rest is fascinating and enlightening."
    },
    {
        "title": "The History of Ancient Civilizations",
        "content": "From the pyramids of Egypt to the Mayan temples, ancient civilizations leave us with questions and awe-inspiring architectural feats."
    },
    {
        "title": "Unlocking Creativity",
        "content": "Creativity is the ability to see the world differently and express unique ideas. Understanding it can unlock hidden potential."
    },
    {
        "title": "The Rise of Renewable Energy",
        "content": "Solar, wind, and hydroelectric power are revolutionizing how we think about energy, offering a sustainable future."
    },
    {
        "title": "The Benefits of Mindfulness",
        "content": "Practicing mindfulness can help reduce stress, increase focus, and improve overall well-being."
    },
    {
        "title": "Exploring Marine Biodiversity",
        "content": "The oceans hold a vast array of life, from colorful coral reefs to deep-sea creatures that glow in the dark."
    },
    {
        "title": "The Psychology of Happiness",
        "content": "What makes us happy? Understanding the science behind happiness can lead to a more fulfilling life."
    },
    {
        "title": "The Evolution of Technology",
        "content": "From the invention of the wheel to modern AI, technology has shaped human history and will continue to transform our lives."
    },
    {
        "title": "The Power of Storytelling",
        "content": "Stories connect us, convey emotions, and inspire change. They are an essential part of human culture."
    },
    {
        "title": "Gardening for Beginners",
        "content": "Starting a garden can be rewarding and therapeutic. Even a small space can yield beautiful plants and fresh produce."
    },
    {
        "title": "The Magic of Music",
        "content": "Music has the power to evoke emotions, tell stories, and bring people together across cultures and generations."
    },
    {
        "title": "The Wonders of Space Exploration",
        "content": "Space exploration pushes the boundaries of human ingenuity, revealing the beauty and complexity of the cosmos."
    },
    {
        "title": "The Importance of Fitness",
        "content": "Regular exercise improves health, boosts energy, and enhances mood, making it a cornerstone of a healthy lifestyle."
    },
    {
        "title": "The Secrets of Ancient Medicine",
        "content": "Ancient healing practices, from Ayurveda to Chinese medicine, continue to influence modern healthcare."
    },
    {
        "title": "The Future of Artificial Intelligence",
        "content": "AI is changing how we work, communicate, and live. The possibilities and challenges it brings are immense."
    },
    {
        "title": "The Beauty of Cultural Diversity",
        "content": "Diversity enriches societies, fosters understanding, and highlights the value of different perspectives and traditions."
    },
    {
        "title": "The Impact of Climate Change",
        "content": "Climate change is reshaping ecosystems and affecting lives worldwide. Addressing it requires collective action and innovation."
    }
]

test_post_update_fields = [
    {"title": "Edited post title"},
    {"content": "Edited post content"},
    {"title": "Another title", "content": "Another content"}
]

@pytest.fixture(autouse=True)
def create_test_post(
    authorization: AuthorizationData
) -> None:
    client.post("/posts", headers=authorization.header, json=test_posts[1])
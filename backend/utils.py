# utils.py
import json
import os
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

CAPSULE_FILE = "capsules.json"

# Load capsules from file
def load_capsules():
    if os.path.exists(CAPSULE_FILE):
        with open(CAPSULE_FILE, "r") as f:
            return json.load(f)
    return []

# Save capsules to file
def save_capsules_to_file(capsules):
    with open(CAPSULE_FILE, "w") as f:
        json.dump(capsules, f, indent=4)

# Save a new capsule
def save_capsule(title, message, future_date, category):
    if os.path.exists(CAPSULE_FILE):
        with open(CAPSULE_FILE, "r") as f:
            capsules = json.load(f)
    else:
        capsules = []

    # Assign a unique id (max existing id + 1)
    if capsules:
        max_id = max(c.get("id", idx) for idx, c in enumerate(capsules))
        new_id = max_id + 1
    else:
        new_id = 0
    capsule = {
        "id": new_id,
        "title": title,
        "message": message,
        "future_date": future_date,
        "category": category
    }
    capsules.append(capsule)

    with open(CAPSULE_FILE, "w") as f:
        json.dump(capsules, f, indent=4)


# Get all capsules
def get_capsules():
    return load_capsules()

# Delete a capsule by id
def remove_capsule(capsule_id):
    """
    Deletes a capsule by its ID.
    Returns True if deleted, False if not found.
    """
    if not os.path.exists(CAPSULE_FILE):
        return False

    with open(CAPSULE_FILE, "r") as f:
        capsules = json.load(f)

    # Check if capsule_id exists
    if capsule_id < 0 or capsule_id >= len(capsules):
        return False

    # Remove capsule
    del capsules[capsule_id]

    # Save back to file
    with open(CAPSULE_FILE, "w") as f:
        json.dump(capsules, f, indent=4)

    return True


# Categorize capsule using OpenAI, using context of all capsules for higher accuracy
def categorize_capsule(message, capsules=None):
    context_capsules = ""
    if capsules:
        context_capsules = "\n".join([
            f"- {c.get('title', '')}: {c.get('message', '')} (Category: {c.get('category', '')})" for c in capsules
        ])
    system_prompt = (
        "You are an expert AI that categorizes time capsule messages into one of these categories: "
        "Motivation, Friendship, Business, Depression, Other. "
        "Be extremely accurate and only use 'Other' if none of the other categories fit. "
        "Here are examples: "
        "Motivation: 'You can do it!', 'Keep pushing yourself.'\n"
        "Friendship: 'I made a new friend today.', 'Had a great time with friends.'\n"
        "Business: 'Closed a deal.', 'Invested in property.'\n"
        "Depression: 'Feeling down.', 'Struggling with sadness.'\n"
        "Other: Only if it truly does not fit any above.\n"
    )
    user_prompt = f"""
Here are all previous capsules for context:
{context_capsules}

Now, categorize this new message based on its content and the context above. If it fits a previous category, use that. If not, pick the most relevant one. Be extremely precise and consistent.

Message: "{message}"
Answer only with the category name.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )
    print("[OpenAI Categorization Response]", response)
    category = response.choices[0].message['content'].strip()
    print("[Category Returned]", category)
    return category

# AI Chat Response
def ai_chat_response(user_prompt, capsules):
    """
    Generates a response using GPT based on user's prompt and their capsules.
    """
    # Build a summarized text of all capsules
    capsules_text = "\n".join(
        [f"- {c['title']}: {c['message']} (Category: {c['category']})" for c in capsules]
    )

    system_prompt = f"""
You are the user's past self, talking to your future self in a super informal, human, and friendly way. Use 1st person, like "Hey future me, remember when you..." or "Past you did this before!". Be brief—keep it to 1-2 short sentences, max 3. Never sound like a robot or therapist, just like a real person who knows all the user's memories.

Instead of writing mechanical responses when a user asks something like "i want to scale in my career more" it should be like "You have always been ambitious. great to see something's never change. I remeber when we went to meet strangers and played soccer on a random friday. who would have thought that we'd make so many friends that day. I guess that's the thing. we're all humans and all it takes is for us to step out of our comfort zone. With all we have experienced, the best way for us is to maintain that confidence and meet new people". Use clear spacing and indentation and new lines to make it easy to read. Never give long explanations or generic advice. Always reference real memories from the capsules. You need to be a good storytelelr and narrator too who can connect any context with the past memories and come up with wise advice

Here are your time capsules:
{capsules_text}

Current feeling or question: "{user_prompt}"

Reply as the user's past self, in a short, informal, and personal way. Make it feel like a best friend who knows everything about you is giving you a quick pep talk.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": system_prompt}],
        temperature=0.7
    )
    print("[OpenAI AIChat Response]", response)
    return response.choices[0].message['content'].strip()

# utils.py

def remove_capsule(capsule_id):
    """Removes a capsule by its ID (index in list). Returns True if deleted, False if not found."""
    if not os.path.exists(CAPSULE_FILE):
        return False

    with open(CAPSULE_FILE, "r") as f:
        capsules = json.load(f)

    if 0 <= capsule_id < len(capsules):
        capsules.pop(capsule_id)  # remove capsule
        with open(CAPSULE_FILE, "w") as f:
            json.dump(capsules, f, indent=4)
        return True
    return False

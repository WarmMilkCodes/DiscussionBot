from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("openapi_key"))  # Ensure this matches your .env file

def read_posts_from_file(file_path):
    """
    Read discussion board posts from a text file.

    :param file_path: Path to the text file containing the posts.
    :return: List of strings, where each string is a discussion board post.
    """
    try:
        with open(file_path, "r") as file:
            posts = file.readlines()
        # Remove any leading/trailing whitespace or newlines from each post
        posts = [post.strip() for post in posts if post.strip()]
        return posts
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def analyze_and_generate_post(posts, custom_prompt):
    """
    Analyze a series of discussion posts and generate a new post based on them.

    :param posts: List of strings, where each string is a discussion board post.
    :param custom_prompt: A string containing the theme or question the posts are responding to.
    :return: A string containing the generated post.
    """
    try:
        # Combine all posts into a single text block
        combined_posts = '\n'.join(posts)

        # Create a prompt for the AI
        prompt = f"""The following are discussion board posts responding to the theme/question: "{custom_prompt}"

{combined_posts}

Using the ideas and insights from the above posts, write a detailed and cohesive paragraph that addresses the theme/question: "{custom_prompt}". Do not mention that you are using the provided posts as guidance. Write in a natural, standalone style."""

        # Call the OpenAI API to generate the post
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Use "gpt-4" or "gpt-3.5-turbo" if you don't have access to GPT-4 Turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates discussion board posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,  # Adjust the length of the generated post
            temperature=0.7,  # Adjust the creativity of the response
        )

        # Extract and return the generated post
        generated_post = response.choices[0].message.content.strip()
        return generated_post

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Path to the text file containing discussion board posts
    file_path = "discussion_posts.txt"  # Update this to the path of your .txt file

    # Read posts from the file
    posts = read_posts_from_file(file_path)

    if not posts:
        print("No posts found in the file. Please check the file path and content.")
    else:
        # Custom prompt (theme or question)
        custom_prompt = "Explain how Music and Dance help students learn"

        # Generate a new post based on the provided posts and custom prompt
        new_post = analyze_and_generate_post(posts, custom_prompt)
        print("Generated Post:\n", new_post)
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("openapi_key"))  # Ensure this matches your .env file

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
    # Example discussion board posts
    posts = [
        "Music and dance helps students learn in many different ways. One way is dancing. Dancing is not only about moving our body but appreciating the body as an expressive instrument through exploration and discovery which is 'creative movement' according to Gelineau (2012. Integrating the Arts Across the Elementary School Curriculum). Dancing allows students to get creative by locomotor movements (traveling movements) or non-locomotor movement (stretching or bending movements) which can produce confidence, self-esteem and stimulate their thinking in a particular movement. In addition, we know that dancing helps with physical growth and fine/gross motor skills that children may lack. Music as mention in previous discussion helps student articulate the meaning of words to feelings or assist in their reading skills. Music is not only about listening or hearing sounds, rhythm or tune but also able to articulate what the music is portraying and reading the words to the music for the meaning of the sound. Music allows our mind to expand our mind to go beyond the tune or words but to reflect into our experiences. When students can self-reflect things it give room of opportunity for growth in their education to be challenge. ",
        "Music and dance help children learn in so many ways! Songs are easier to memorize than just words, so adding a song to almost anything can make it easier to recall later. clapping words in a rhythm can help students separate the sounds within a word. Crossing the midline can help cognitive development. There is also the importance of a break for students. Doing a fun dance song can add movement to the day while also allowing students to relax and have fun. Songs can be used for transitions and predictable routines. Music and dance are important to student success and everything I've learned this semester just further proves that fact to me. ",
        "Music and Dance have been known to go together since early human history.  Per Gardner's Theory of Multiple Intelligence, dance and music are under the category of musical and kinesthetic intelligence.  In 'terms of the context of a particular movement' (Gelineau, 2012. p.141) sequencing steps/movements and listening to rhythms, stimulate problem-solving, higher thinking skills and creativity. Gelineau quotes Ann Green Gilbert's belief that 'movement is the key to learning'. Green also states that movement in the classroom is directly related to an increase of student MAT scores based on grant-funded research in Seattle Public Schools (Gelineau, 2012). Clapping out words in reading is a form of rhythm and helps students count the syllables of a word and remember sounds at the same time. Singing the alphabet song helps to learn the same. I have observed kindergarteners going back to re-read (another reading tool), in order to find the letter or the sound they are writing.  I have also mentioned before, how my children learned/memorized parts of a sentence by singing rhyming songs. The one that comes to mind is: 'conjunction (something...) ...what is your function?'",
        "Incorporating music and movement into the classroom greatly enhances student learning. Sitting for a long period of time can bring on fatigue so it’s important to have your students stand, stretch and move their bodies to boost their energy levels. Listening to music increases memorization through lyrics, while dancing improves spatial awareness, counting skills, and overall coordination. Kids deal with much stress these days so these activities can help in managing emotions. Eric Jensen states the “feel good chemicals in the brain run higher after movement, which in turn can enhance learning and feelings of well being.” (Gelineau, 2012, #141) In our school, integrating music and movement has shown an increase in motivation among our students to be involved. For example, when reading Thunder Cake by Patricia Polacco, we have physical actions attached to our vocabulary words. For the word “churn”, our students do the motion of churning butter, which aids in remembering the words, not only how to say them but what they actually mean. Using a simple method with actions makes it fun and benefits the students in so many ways. Adding a little music and dance throughout your students day can make school a little more fun and hopefully leave them filled with joy. ",
        "In chapter six the book has a quote by Margot Faught that talks about how creative dance promotes motor skills, body awareness, and basic learning skills like listening, following directions, sequencing, and problem solving.  Developing better motor skills and body awareness will help students with writing, cutting, putting objects together among may other things.  Creative dance also helps promote listing skills and following directions which is huge in terms of classroom learning.  If students can not follow directions or listen to the teacher then very little learning will be done.  Dancing helps with this because the students has to learn to follow directions in order to be able to do the dances and also has to listen to the music in order to be able to preform the dance.  Dance also helps with sequencing and problem solving because the student must figure out the pattern/ order of the movements to be able to do the dances.  It helps students with memory because they have to learn to remember dance moves and it also helps them to learn to adapt and make decisions quickly.  Music is also plays a key role in all of this because creative dance would not be possible without music.  A large amount of learning and joy would not be possible without music. ",
        "The experience that music and dance integrated within the classroom changes the game for how children learn. Integrating music and dance within the classroom caters to a variety of learning styles. Many children when you are teaching a language, literacy, science, and or math concept can also be taught through song and dance. Teaching children through music and dance is easier than many teachers realize. Another great tool that we have in today’s classrooms is utilizing technology to integrate music and dance in learning basic educational concept. Integrating music and dance is a great way to get young children moving within the classroom environment. Teachers can utilize music and movement to help children warm up their brains and bodies for the day. Young children can benefit from music and dance by learning locomotor movements, patterns, and directional words. Integrating music and dance within the classroom environment to help children learn hand eye coordination and a variety of dances and music. Children can learn color songs, letter songs, and nursery rhymes. Integrating music and dance within the classroom can help bring a joy of learning in your classroom environment. ",
        "The quote by B. Fauth on page 141 I think speaks perfectly as to why it is important to maintain music and dance in learning environments. We will retain 90% if we hear, see, say and do which is exactly what happens when you are dancing to a song. If you combine that with a lesson, CVC words or something along those lines and make it memorable, kids will have the greatest chance to retain the information and maintain success. Repetition of the songs or dance will also help build all muscles in the body which contributes to the physical health of each individual. Singing and dancing is also fun so it will make it seem like the kids aren't even learning when in reality they are doing some of the best learning possible. Additional ways that they would be learning would be attention to detail, multitasking, working together, critical thinking active listening and memorization. Sometimes it can be hard to have specific lessons on these skills but by creating a fun learning environment with dancing, those skills will be quickly developed. We do the days of the week and months of the year song at least 3 times a week in my room and I have already seen an improvement with them, I will even catch them singing it throughout the day and they don't even realize they are. ",
        "Music and dance are tools that can enhance learning in different ways. It contributes to creativity, cognitive development, emotional well-being, and physical coordination.  Music and dance help students with memory and attention skills. It requires students to memorize patterns, sequences, rhythms, and movements.  It helps them with their attention span and pay attention to detail. It also enhances their critical thinking and problem-solving skills.  Students are expected to make decisions quickly and help them make those decisions about timing, pitch, and interpretation. Music and dance also help with self-expression. It gives students a safe space to express their emotions through music or dance.  When doing this it also helps them have more confidence in themselves. If working in a group, it gives them teamwork skills that are needed in everyday life.  I believe there are many benefits that music and dance can give students. Not everyone enjoys dancing and singing songs in front of an audience, but in the classroom, I think it’s a smaller scale and allows students to be more open and creative in a safe learning environment."
    ]

    # Custom prompt (theme or question)
    custom_prompt = "Explain how Music and Dance help students learn"

    # Generate a new post based on the provided posts and custom prompt
    new_post = analyze_and_generate_post(posts, custom_prompt)
    print("Generated Post:\n", new_post)
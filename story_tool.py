import base64
import random
import re
import sys

# Expanded word map covering all base64 characters
word_map = {
    # Uppercase A-Z
    'A': ['Apple', 'Alice', 'Ant', 'Ape'],
    'B': ['Banana', 'Bob', 'Bear', 'Bee'],
    'C': ['Cat', 'Charlie', 'Car', 'Cow'],
    'D': ['Dog', 'David', 'Duck', 'Deer'],
    'E': ['Elephant', 'Emma', 'Eagle', 'Eel'],
    'F': ['Flower', 'Frank', 'Fox', 'Frog'],
    'G': ['Guitar', 'George', 'Goat', 'Giraffe'],
    'H': ['House', 'Harry', 'Horse', 'Hawk'],
    'I': ['Ice', 'Ian', 'Igloo', 'Impala'],
    'J': ['Juice', 'Jack', 'Jaguar', 'Jellyfish'],
    'K': ['Kangaroo', 'Kevin', 'Kingfisher', 'Koala'],
    'L': ['Lake', 'Laura', 'Lion', 'Lizard'],
    'M': ['Monkey', 'Mike', 'Mouse', 'Mole'],
    'N': ['Night', 'Nancy', 'Nest', 'Newt'],
    'O': ['Orange', 'Oliver', 'Owl', 'Octopus'],
    'P': ['Pen', 'Peter', 'Parrot', 'Penguin'],
    'Q': ['Queen', 'Quinn', 'Quokka', 'Quail'],
    'R': ['River', 'Robert', 'Rabbit', 'Raccoon'],
    'S': ['Sun', 'Sam', 'Snake', 'Squirrel'],
    'T': ['Tree', 'Tom', 'Tiger', 'Turtle'],
    'U': ['Universe', 'Ursula', 'Umbrella', 'Unicorn'],
    'V': ['Violin', 'Victor', 'Vulture', 'Van'],
    'W': ['Window', 'William', 'Wolf', 'Whale'],
    'X': ['Xylophone', 'Xavier', 'Xenon', 'Xerus'],
    'Y': ['Yellow', 'Yellowstone', 'Yak', 'Yacht'],
    'Z': ['Zoo', 'Zack', 'Zebra', 'Zeppelin'],
    # Lowercase a-z
    'a': ['apple', 'ant', 'ape', 'axolotl'],
    'b': ['banana', 'bear', 'bee', 'bison'],
    'c': ['cat', 'car', 'cow', 'camel'],
    'd': ['dog', 'duck', 'deer', 'dolphin'],
    'e': ['elephant', 'eagle', 'eel', 'emu'],
    'f': ['flower', 'fox', 'frog', 'flamingo'],
    'g': ['guitar', 'goat', 'giraffe', 'grasshopper'],
    'h': ['house', 'horse', 'hawk', 'hummingbird'],
    'i': ['ice', 'igloo', 'impala', 'ibex'],
    'j': ['juice', 'jaguar', 'jellyfish', 'jaguar'],
    'k': ['kangaroo', 'kingfisher', 'koala', 'kookaburra'],
    'l': ['lake', 'lion', 'lizard', 'lemur'],
    'm': ['monkey', 'mouse', 'mole', 'meerkat'],
    'n': ['night', 'nest', 'newt', 'narwhal'],
    'o': ['orange', 'owl', 'octopus', 'opossum'],
    'p': ['pen', 'parrot', 'penguin', 'peacock'],
    'q': ['queen', 'quokka', 'quail', 'quokka'],
    'r': ['river', 'rabbit', 'raccoon', 'reindeer'],
    's': ['sun', 'snake', 'squirrel', 'seagull'],
    't': ['tree', 'tiger', 'turtle', 'toucan'],
    'u': ['universe', 'umbrella', 'unicorn', 'urchin'],
    'v': ['violin', 'vulture', 'van', 'viper'],
    'w': ['window', 'wolf', 'whale', 'walrus'],
    'x': ['xylophone', 'xenon', 'xerus', 'xenops'],
    'y': ['yellow', 'yak', 'yacht', 'yellowjacket'],
    'z': ['zoo', 'zebra', 'zeppelin', 'zander'],
    # Digits
    '0': ['zero', 'hero', 'zoo', 'zebra'],
    '1': ['one', 'sun', 'won', 'run'],
    '2': ['two', 'shoe', 'too', 'blue'],
    '3': ['three', 'tree', 'free', 'bee'],
    '4': ['four', 'door', 'core', 'store'],
    '5': ['five', 'hive', 'dive', 'drive'],
    '6': ['six', 'mix', 'fix', 'bricks'],
    '7': ['seven', 'heaven', 'eleven', 'raven'],
    '8': ['eight', 'weight', 'height', 'sight'],
    '9': ['nine', 'wine', 'mine', 'pine'],
    # Special chars
    '+': ['Zoom', 'Zipper', 'Zest', 'Zany'],
    '/': ['Fly', 'Float', 'Flee', 'Fling'],
    '=': ['End', 'Ending', 'Equal', 'Equate'],
}

# Story templates with varying structures
story_templates = [
    (
        "Life moves fast. One day you're unpacking boxes, the next you're packing them again. "
        "That’s where I am right now — preparing to move across the country for a new job opportunity. "
        "Because of this, I’m putting two big things up for sale: my car and house. "
        "Both feel like part of my story, but it's time to let go and start fresh somewhere new. "
        "Here’s what I’ve decided to include in the sale: {part1}. "
        "And here’s what the buyer should expect during inspection: {part2}. "
        "If you're interested, drop me a message. Serious inquiries only. {noise}"
    ),
    (
        "I found an old box in the attic yesterday. Inside were various items from my childhood. "
        "The contents were a mix of memories: {part1}. "
        "There were also some notes scribbled on the back: {part2}. "
        "It’s fascinating how time flies. {noise}"
    ),
    (
        "The quick brown fox jumps over the lazy dog. "
        "Meanwhile, items listed for sale include: {part1}. "
        "Additional details provided: {part2}. "
        "Contact for more info. {noise}"
    ),
]

# Contextual noise sentences
noise_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Yesterday, I visited the local market.",
    "She sells seashells by the seashore.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump!",
]

def story_creator(s):
    # Base64 encode the input
    encoded = base64.b64encode(s.encode('utf-8')).decode('utf-8')
    
    # Generate payload words
    payload_words = []
    for char in encoded:
        if char in word_map:
            payload_words.append(random.choice(word_map[char]))
        else:
            payload_words.append(f"[Unknown:{char}]")
    
    # Split payload into random parts
    split_point = random.randint(1, len(payload_words)-1)
    part1 = payload_words[:split_point]
    part2 = payload_words[split_point:]
    
    # Select random template
    template = random.choice(story_templates)
    
    # Generate noise
    noise = random.choice(noise_sentences)
    
    # Build story
    story = template.format(
        part1=", ".join(part1),
        part2=", ".join(part2),
        noise=noise
    )
    
    return story

# Reverse mapping for decoding
reverse_word_map = {word: k for k, words in word_map.items() for word in words}

def story_interpreter(story):
    words = [word.strip(".,") for word in re.findall(r'\w+', story)]
    encoded_chars = []
    for word in words:
        if word in reverse_word_map:
            encoded_chars.append(reverse_word_map[word])
        else:
            # Handle unknown words if necessary
            pass
    encoded_str = ''.join(encoded_chars)
    
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Interpretation failed: {e}")

# Command-line interface
def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("  python story_tool.py create <input_file> <output_file>")
        print("  python story_tool.py interpret <input_file> <output_file>")
        sys.exit(1)
    
    command, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    
    if command == "create":
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                original_code = f.read()
            story = story_creator(original_code)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(story)
            print(f"📖 Story saved to '{output_file}'")
        except Exception as e:
            print(f"❌ Error creating story: {e}")
    elif command == "interpret":
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                received_story = f.read()
            decoded_code = story_interpreter(received_story)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(decoded_code)
            print("✅ Decoded Code saved to '{output_file}'")
        except Exception as e:
            print(f"❌ Error interpreting story: {e}")
    else:
        print("Unknown command. Use 'create' or 'interpret'.")
        sys.exit(1)

if __name__ == "__main__":
    main()

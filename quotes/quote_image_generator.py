import os
import random
import uuid
import json  # Add this line to import the json module
from PIL import Image, ImageDraw, ImageFont

class QuoteImageGenerator:
    def __init__(self, quotes_file, authors_dir, output_dir, font_quote_path, font_author_path):
        self.quotes_file = quotes_file
        self.authors_dir = authors_dir
        self.output_dir = output_dir
        self.font_quote = ImageFont.truetype(font_quote_path, size=40)  # Quote font
        self.font_author = ImageFont.truetype(font_author_path, size=30)  # Author font

        # Load quotes at initialization
        self.quotes_data = self.load_quotes()

    def load_quotes(self):
        """Load quotes from the JSON file."""
        with open(self.quotes_file, 'r') as f:
            return json.load(f)

    def wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit within the specified width."""
        lines = []
        words = text.split()

        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                line = line + words.pop(0) + ' '
            lines.append(line.strip())
        
        return lines

    def draw_text_with_outline(self, draw, position, text, font, text_color, outline_color, outline_width=2):
        """Draw text with an outline effect."""
        x, y = position
        # Draw outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:  # Skip the center position
                    draw.text((x + dx, y + dy), text, fill=outline_color, font=font)

        # Draw the main text
        draw.text(position, text, fill=text_color, font=font)

    def generate_quote_image(self, quote, author):
        """Generate an image with a quote and the author's name."""
        author_dir = os.path.join(self.authors_dir, author)
        if not os.path.exists(author_dir):
            print(f"No images found for {author}")
            return

        images = [f for f in os.listdir(author_dir) if f.endswith(('png', 'jpg', 'jpeg'))]
        if not images:
            print(f"No images found in {author_dir}")
            return

        selected_image = random.choice(images)
        image_path = os.path.join(author_dir, selected_image)

        # Open the image
        image = Image.open(image_path)

        # Convert the image to RGB if it's in RGBA mode
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        draw = ImageDraw.Draw(image)
        text_color = (255, 255, 255)  # White color for the text
        outline_color = (0, 0, 0)     # Black color for the outline
        max_text_width = image.width - 40  # Set some padding from the sides

        # Wrap the quote text to fit within the image width
        wrapped_quote = self.wrap_text(quote, self.font_quote, max_text_width, draw)

        # Calculate total height of the wrapped text
        line_height = draw.textbbox((0, 0), 'A', font=self.font_quote)[3]  # Height of one line
        total_text_height = line_height * len(wrapped_quote)

        # Calculate the position to center the wrapped quote
        quote_y = (image.height - total_text_height) // 2  # Center vertically
        current_y = quote_y

        # Draw each line of the wrapped quote with outline
        for line in wrapped_quote:
            quote_width = draw.textbbox((0, 0), line, font=self.font_quote)[2] - draw.textbbox((0, 0), line, font=self.font_quote)[0]
            quote_x = (image.width - quote_width) // 2
            self.draw_text_with_outline(draw, (quote_x, current_y), line, self.font_quote, text_color, outline_color)
            current_y += line_height  # Move to the next line

        # Add the author's name below the quote
        author_text = f"- {author}"
        author_bbox = draw.textbbox((0, 0), author_text, font=self.font_author)
        author_width = author_bbox[2] - author_bbox[0]
        author_x = (image.width - author_width) // 2
        author_y = current_y + 20  # Position below the last line of the quote

        self.draw_text_with_outline(draw, (author_x, author_y), author_text, self.font_author, text_color, outline_color)

        # Generate a unique ID for the image
        unique_id = str(uuid.uuid4())
        
        # Save the output image with a unique ID
        output_path = os.path.join(self.output_dir, f"{unique_id}.jpg")
        image.save(output_path)
        print(f"Generated image for {author}: {output_path}")

    def generate_images(self):
        """Generate images for all quotes."""
        os.makedirs(self.output_dir, exist_ok=True)

        for stoic in self.quotes_data['stoics']:
            author = stoic['name']
            quotes = stoic['quotes']
            
            for quote in quotes:
                self.generate_quote_image(quote, author)

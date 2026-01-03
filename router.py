import base64
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_event_details(image_path):
    
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

   
    base64_image = encode_image(image_path)

    
    prompt_text = (
        "Analyze this event poster and extract the following details in a list: "
        "1. Event Name and Theme\n"
        "2. Date and Time\n"
        "3. Venue/Location\n"
        "4. Key Artists/Speakers\n"
        "5. Ticket Information or Registration Links\n"
        "6. Any specific requirements (dress code, age limit, etc.)"
    )

    
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            },
        ]
    )

    response = model.invoke([message])
    return response.content


import openai
from langchain.document_loaders import PyPDFLoader
import ast
import base64
import os
import re
import requests



openai.api_key = "YOUR_API_KEY"

def split_pdf_to_text(pdf_path):

    # dir of the pdf
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    page_contents = [page.page_content for page in pages]

    print("pdf text array:", page_contents)

    return page_contents


def parse_string(st):
    
    # Extract the substring representing the list of dictionaries
    start_index = st.find('[')
    end_index = st.rfind(']') + 1
    substring = st[start_index:end_index]
    
    # Parse the substring using ast.literal_eval
    flashcards = ast.literal_eval(substring)

    print("Flashcards parsed:", flashcards)

    return flashcards


def create_flashcards(text_page):
    updated_text_page = text_page.replace('\n', '')

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.1,
        messages=[
          { 
            "role": "system", "content": "You are a helpful Geology Assitant that can create comprehensive flashcards from a provided text, and any figures depending on the context."
          },
          { 
            "role": "user", "content": "Create very comprehensive flashcards based on the following text: \n We will also introduce you to a geologist’s view of time. You will think about time differently as you begin to comprehend the immense span of geologic history. Earth and the other planets in our solar system formed about 4.5 billion years ago. More than 3 billion years ago, living cells developed on Earth’s surface, and life has been evolving ever since. Yet our human origins date back only a few million years—less than a tenth of a percent of Earth’s existence. The decades of individual lives or even the thousands of years of recorded human history are inadequate to study Earth’s long existence./H17039   The Scientiﬁ  c MethodThe term geology (from the Greek words for “Earth”  and “knowledge”) was coined by scientific philosophers more than 200 years ago to describe the study of rock formations and fossils. Through careful observations and reasoning, their successors developed the theories of biological evolu-tion, continental drift, and plate tectonics—major topics of this textbook. Today, geology  identifies the branch of Earth science that studies all aspects of the planet: its history, its composition and internal structure, and its surface features.The goal of geology—and of science in general—is to explain the physical universe. Scientists believe that physi-cal events have physical explanations, even if they may be beyond our present capacity to understand them. The scientific method,  on which all scientists rely, is the general procedure for discovering how the universe works through systematic observations and experiments. Using the scien-tific method to make new discoveries and to confirm old ones is the process of scientific research  (Figure 1.1 ).When scientists propose a hypothesis —a tentative expla-nation based on data collected through observations and experiments—they present it to the community of scien-tists for criticism and repeated testing. A hypothesis is sup-ported if it explains new data or predicts the outcome of new experiments. A hypothesis that is confirmed by other scientists gains credibility.Here are four interesting scientific hypotheses we will encounter in this textbook:/H17039 Earth is billions of years old./H17039 Coal is a rock formed from dead plants./H17039 Earthquakes are caused by the breaking of rocks along geologic faults./H17039 The burning of fossil fuels is causing global warming.The first hypothesis agrees with the ages of thousands of ancient rocks as measured by precise laboratory techniques, and the next two hypotheses have also been confirmed by many independent observations. The fourth hypothesis has been more controversial, though so many new data support it that most scientists now accept it as true (see Chapters 15 and 23).A coherent set of hypotheses that explains some aspect of nature constitutes a theory. Good theories are supported by substantial bodies of data and have survived repeated challenges. They usually obey physical laws, general principles about how the universe works that can be applied in almost every situation, such as Newton’s law of gravity.Some hypotheses and theories have been so exten-sively tested that all scientists accept them as true, at least to a good approximation. For instance, the theory that Earth is nearly spherical, which follows from Newton’s law of gravity, is supported by so much experience and direct evidence (ask any astronaut) that we take it to be a fact. The longer a theory holds up to all scientific challenges, the more confidently it is held. FIGURE 1. 1    /H17039     Scientiﬁ  c research is the process of discovery and conﬁ  rmation through observations of the real world. These geologists are researching soil samples near a lake in Minnesota. \n With this exact format: \n "
            "flashcards = [" \
                "{'question': 'When was the term Geology coined and what does it describe?', 'answer': 'The term geology was coined over 200 years ago to describe the study of rock formations and fossils.'}," \
                "{'question': 'The {{c1::scientific method}} is the general procedure for discovering how the {{c1::universe works}} through systematic {{c1::observations and experiments}}.', 'answer': 'The scientific method is the general procedure for discovering how the universe works through systematic observations and experiments.', 'image': 'Figure_1.1.jpg'}," \
                "{'question': 'What are some interesting scientific hypotheses encountered in geology?', 'answer': ['Earth is billions of years old.', 'Coal is a rock formed from dead plants.', 'Earthquakes are caused by the breaking of rocks along geologic faults.', 'The burning of fossil fuels is causing global warming. These hypotheses have been confirmed through observations and experiments, with the last one being widely accepted by most scientists.']}," \
                "{'question': 'What is a theory?', 'answer': 'A theory in science is a coherent set of hypotheses that explains some aspect of nature. Good theories are supported by substantial bodies of data and have survived repeated challenges, usually obeying physical laws.'}" \
                "]"
          },
          {
            "role": "assistant",
            "content": "flashcards = [" \
                "{'question': 'Geologists comprehend the immense span of {{c1::geologic history}}, considering that Earth and the other planets formed about {{c1::4.5 billion years ago}}, living cells developed on Earth more than {{c1::3 billion years ago}}, and human origins date back only {{c1::a few million years}}.', 'answer': 'Geologists comprehend the immense span of geologic history, considering that Earth and the other planets formed about 4.5 billion years ago, living cells developed on Earth more than 3 billion years ago, and human origins date back only a few million years.'}," \
                "{'question': 'The term {{c1::geology}} was coined over {{c1::200 years ago}} to describe the study of {{c1::rock formations and fossils}}.', 'answer': 'The term geology was coined over 200 years ago to describe the study of rock formations and fossils.'}," \
                "{'question': 'What is the scientific method?', 'answer': 'The scientific method is the general procedure for discovering how the universe works through systematic observations and experiments.', 'image': 'Figure_1.1.jpg'}," \
                "{'question': 'What are some interesting scientific hypotheses encountered in geology?', 'answer': ['Earth is billions of years old.', 'Coal is a rock formed from dead plants.', 'Earthquakes are caused by the breaking of rocks along geologic faults.', 'The burning of fossil fuels is causing global warming. These hypotheses have been confirmed through observations and experiments, with the last one being widely accepted by most scientists.']}," \
                "{'question': 'What is a theory?', 'answer': 'A theory in science is a coherent set of hypotheses that explains some aspect of nature. Good theories are supported by substantial bodies of data and have survived repeated challenges, usually obeying physical laws.'}" \
                "]"
          },
          {
            "role": "user", "content": "Create very comprehensive flashcards based on the following text: " + updated_text_page
          }
        ]
    )

    flashcards = completion.choices[0].message.content

    print("GPT Answer:", flashcards)

    """
    nb = "flashcards = [" \
            "{'question': 'Geologists comprehend the immense span of {{c1::geologic history}}, considering that Earth and the other planets formed about {{c1::4.5 billion years ago}}, living cells developed on Earth more than {{c1::3 billion years ago}}, and human origins date back only {{c1::a few million years}}.', 'answer': 'Geologists comprehend the immense span of geologic history, considering that Earth and the other planets formed about 4.5 billion years ago, living cells developed on Earth more than 3 billion years ago, and human origins date back only a few million years.'}," \
            "{'question': 'The term {{c1::geology}} was coined over {{c1::200 years ago}} to describe the study of {{c1::rock formations and fossils}}.', 'answer': 'The term geology was coined over 200 years ago to describe the study of rock formations and fossils.'}," \
            "{'question': 'The {{c1::scientific method}} is the general procedure for discovering how the {{c1::universe works}} through systematic {{c1::observations and experiments}}.', 'answer': 'The scientific method is the general procedure for discovering how the universe works through systematic observations and experiments.', 'image': 'Figure_1.1.jpg'}," \
            "{'question': 'What are some interesting scientific hypotheses encountered in geology?', 'answer': ['Earth is billions of years old.', 'Coal is a rock formed from dead plants.', 'Earthquakes are caused by the breaking of rocks along geologic faults.', 'The burning of fossil fuels is causing global warming. These hypotheses have been confirmed through observations and experiments, with the last one being widely accepted by most scientists.']}," \
            "{'question': 'A {{c1::theory}} in science is a coherent set of {{c1::hypotheses}} that explains some aspect of {{c1::nature}}. Good theories are supported by {{c1::substantial bodies of data}} and have survived {{c1::repeated challenges}}, usually obeying {{c1::physical laws}}.', 'answer': 'A theory in science is a coherent set of hypotheses that explains some aspect of nature. Good theories are supported by substantial bodies of data and have survived repeated challenges, usually obeying physical laws.'}" \
       "]"
    """

    # parse results
    parsed_flashcards = parse_string(flashcards)

    return parsed_flashcards


def add_flashcards_to_anki(flashcards):
    try:
        for flashcard in flashcards:
            # Extract question, answer, and optionally image

            print('THE INDIVIDUAL FLASHCARD', flashcard)
            print('THE TYPE OF QUESTION', type(flashcard['question']))
            print('THE TYPE OF ANSWER', type(flashcard['answer']))
            print('THE TYPE OF IMAGE', type(flashcard.get('image')))
            
            # Access the 'question' key from the flashcard dictionary
            question = flashcard['question']
            answer = flashcard['answer']
            image = flashcard.get('image')

            print('THE ANSWER BEFORE', answer)
            # Check if the answer is a list and format it accordingly
            if isinstance(answer, list):
                answer = '<br>'.join(answer)
            print('THE ANSWER AFTER', answer)

            # Detect flashcard type based on the question and answer format
            if isinstance(question, str) and isinstance(answer, str) and (re.search(r"{{c\d+::", question) or re.search(r"{{c\d+::", answer)):
                flashcard_type = 'cloze'
            else:
                flashcard_type = 'basic'
            
            # If there is an image, add it to Anki
            if image:
                image_path = os.path.join(os.getcwd(), 'chapter1', 'figures', image)
                print("IMAGE PATH:", image_path)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode('utf-8')
                        requests.post("http://localhost:8765", json={
                            "action": "storeMediaFile",
                            "params": {
                                "filename": image,
                                "data": img_data
                        }
                    })
                    # Append the image to the question
                    answer = f"{answer}<br><img src='{image}'>"
                else:
                    print(f"Image file does not exist at path: {image_path}")

            
            # Construct Anki note based on the flashcard type
            if flashcard_type == 'cloze':
                note_content = question  # Assuming the question contains the Cloze deletions
                model_name = "Cloze"
                fields = {"Text": note_content}
            else:  # Default to basic flashcard
                note_content = question
                model_name = "Basic"
                fields = {"Front": note_content, "Back": answer}
            
            deck_name = "YourDeckName"

            # Check if the deck already exists
            deck_list_response = requests.post("http://localhost:8765", json={
                "action": "deckNames",
                "version": 6
            })
            
            # Check if the request was successful
            if deck_list_response.status_code == 200:
                deck_list = deck_list_response.json().get('result', [])
                
                # If the deck does not exist, create it
                deck_list = deck_list_response.json().get('result', [])
                if isinstance(deck_list, list) and deck_name not in deck_list:
                    create_deck_response = requests.post("http://localhost:8765", json={
                        "action": "createDeck",
                        "version": 6,
                        "params": {
                            "deck": deck_name
                        }
                    })
                    
                    # Check if the deck was successfully created
                    if create_deck_response.status_code != 200 or create_deck_response.json().get('error') is not None:
                        print(f"Failed to create deck: {deck_name}")
            else:
                print(f"Failed to retrieve deck list. HTTP error: {deck_list_response.status_code}")    
            
            note = {
                "deckName": "YourDeckName",
                "modelName": model_name,
                "fields": fields,
                "options": {
                    "allowDuplicate": False
                },
                "tags": []
            }
            
            # Add note to Anki
            response = requests.post("http://localhost:8765", json={
                "action": "addNote",
                "params": {
                    "note": note
                }
            })

            if response.status_code == 200:
                # Parse the JSON response
                response_json = response.json()

                # Check for errors in the response JSON
                if isinstance(response_json, dict) and 'error' in response_json and response_json['error'] is not None:
                    print(f"Failed to add flashcard: {question}. AnkiConnect error: {response_json['error']}")
                else:
                    print(f"Successfully added flashcard: {question}")
            else:
                print(f"Failed to add flashcard: {question}. HTTP error: {response.status_code}")

        return True

    except Exception as e:
        print(f"Failed to add flashcard: {question}. Error: {e}")
        return False


def main(pdf_path):

    text_pages = split_pdf_to_text(pdf_path)

    counter = 0 
    for text_page in text_pages:
        counter += 1
        print(f'AN iteration within text_page {counter}')
        flashcards = create_flashcards(text_page)
        print(f"Type of flashcards: {type(flashcards)}, Value of flashcards: {flashcards}")
        response = add_flashcards_to_anki(flashcards)
        # check if the flashcards were created
        # otherwise break out of the loop
        print(type(response))
        print(response)
        if not response:
            return "Flashcards not added"

    return "Flashcards successfully added!"


print(main("./Chapter1/Chapter_1.pdf"))    

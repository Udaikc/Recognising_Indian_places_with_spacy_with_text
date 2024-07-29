import re
import spacy
from spacy.tokens import Span
from spacy.util import filter_spans
from spacy import displacy

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")


# Create your views here.
from django.shortcuts import render
from .forms import SentenceForm

from django.shortcuts import render
from .forms import SentenceForm  # Assuming you have SentenceForm defined in forms.py
import re
import spacy
from spacy.tokens import Span
from spacy.util import filter_spans

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns with flexibility for customization
location_pattern = r"\b\w*(pura|pur|kode|puram|giri|ool|luru|halli|nagar|nagara|ssan|Goa|Udupi|bad|kesh|sthan|bagh|mangala)\b"
city_pattern = r"\b(Surat|Patna|Bangalore|Mysore|Kolkata|Kochi)\b"

def input_form(request):
    if request.method == 'POST':
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data['sentence']
            # Process the sentence and extract entities
            entities = extract_entities(sentence)
            return render(request, 'myapp/display.html', {'sentence': sentence, 'entities': entities})
    else:
        form = SentenceForm()
    return render(request, 'myapp/input.html', {'form': form})

def extract_entities(text):
  """Extracts locations and cities from the given text.

  Args:
    text: The input text.

  Returns:
    A list of dictionaries, where each dictionary contains the entity text and its label (LOC or CITY).
  """

  doc = nlp(text)

  # List to store custom entities
  new_entities = []

  # Add location entities
  for match in re.finditer(location_pattern, text):
      start, end = match.span()
      span = doc.char_span(start, end, label="LOC", alignment_mode="strict")
      if span is not None:
          new_entities.append(span)

  # Add specific city entities
  for match in re.finditer(city_pattern, text):
      start, end = match.span()
      span = doc.char_span(start, end, label="CITY", alignment_mode="strict")
      if span is not None:
          new_entities.append(span)

  # Filter out overlapping spans
  new_entities = filter_spans(new_entities)

  # Convert entities to dictionaries for easier template handling
  entities = [{"text": ent.text, "label": ent.label_} for ent in new_entities]

  return entities




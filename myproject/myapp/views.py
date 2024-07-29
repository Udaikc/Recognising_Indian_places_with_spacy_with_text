import re
import spacy
from spacy.tokens import Span
from spacy.util import filter_spans
from spacy import displacy

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns with flexibility for customization
location_pattern = r"\b\w*(pura|pur|kode|puram|giri|ool|luru|halli|nagar|nagara|ssan|Goa|Udupi|bad|kesh|sthan)\b"
city_pattern = r"\b(Surat|Patna|Bangalore|Mysore|Kolkata|Kochi)\b"

# Create your views here.
from django.shortcuts import render
from .forms import SentenceForm

'''def input_form(request):
    if request.method == 'POST':
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data['sentence']
            return render(request, 'myapp/display.html', {'sentence': sentence})
    else:
        form = SentenceForm()
    return render(request, 'myapp/input.html', {'form': form})'''

def process_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        try:
            # Process text with SpaCy
            doc = nlp(text)

            # List to store custom entities
            new_entities = []

            # Add location and city entities based on patterns
            for match in re.finditer(location_pattern, text):
                start, end = match.span()
                span = doc.char_span(start, end, label="LOC", alignment_mode="strict")
                if span is not None:
                    new_entities.append(span)

            for match in re.finditer(city_pattern, text):
                start, end = match.span()
                span = doc.char_span(start, end, label="CITY", alignment_mode="strict")
                if span is not None:
                    new_entities.append(span)

            # Filter out overlapping spans
            new_entities = filter_spans(new_entities)

            # Set the new entities in the doc
            doc.set_ents(new_entities, default="unmodified")

            # Prepare context for template (escape HTML for security)
            context = {'doc': displacy.render(doc, style="ent", jupyter=False)}
            context['text'] = text  # Optional: Include original text for display

            return render(request, 'myapp/results.html', context)

        except Exception as e:  # Handle potential errors gracefully
            context = {'error_message': "An error occurred while processing text. Please try again."}
            return render(request, 'myapp/error.html', context)

    else:
        return render(request, 'myapp/input.html')


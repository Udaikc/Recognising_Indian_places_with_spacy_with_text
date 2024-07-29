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

def input_form(request):
    if request.method == 'POST':
        form = SentenceForm(request.POST)
        if form.is_valid():
            sentence = form.cleaned_data['sentence']
            return render(request, 'myapp/display.html', {'sentence': sentence})
    else:
        form = SentenceForm()
    return render(request, 'myapp/input.html', {'form': form})


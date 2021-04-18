#imports
import json
import re

from django import forms
from django.core.exceptions import ValidationError

class TranslateForm(forms.Form):
    #pull fantasy languages from json file and manage how they appear on the form - I commented out the references to fantasy language because they don't do anything on the form right now  
    f = open('translator_app/fantasy_languages.json')
    fantasy_languages = json.load(f)
    fantasy_languages = fantasy_languages['fantasy_languages']

    fantasy_language_options_list = []

    #Django's combo box requires a tuple containing the value as it is submitted and displayed respectively
    for language in fantasy_languages:
        fantasy_language_option = (language, fantasy_languages[language]["long_name"])
        fantasy_language_options_list.append(fantasy_language_option)
    
    #do the same for real languages
    f = open('translator_app/real_languages.json')
    real_languages = json.load(f)
    real_languages = real_languages['real_languages']

    real_language_options_list = []

    for language in real_languages:
        real_language_option = (language, real_languages[language]["long_name"])
        real_language_options_list.append(real_language_option)

    #adds language select dropdown
    fantasy_language_select = forms.ChoiceField(label=u"Select language:\n", label_suffix='', choices=fantasy_language_options_list, required=False)

    #get first key from fantasy languages to initialize input fields
    firstKey = list(fantasy_languages.keys())[0]

    #select real languages to combine to help shape fantasy language
    real_language_influences = forms.MultipleChoiceField(label=u"Influences:", initial=fantasy_languages[firstKey]['influences'], choices=real_language_options_list)

    #TODO - I want this to be something that the user can add into the DOM, rather than have to save in a text field all at once
    #TODO - I tried doing some validation on this using RegexValidator and a custom definition but both break the app. Leaving the planned regex below.

    # def validate_az_characters(value):
    #     if re.match("([a-zA-Z])(,[a-zA-Z])?", value):
    #         raise ValidationError('Must be comma-separated, non-numerical character')

    #RegexValidator(regex=character_validation_regex, message="Must be comma-seperated non-numerical character", code=None, inverse_match=None, flags=0)

    #add characters/patterns user wants represented more/less
    more_of = forms.CharField(label=u"More of:", max_length=6, initial=''.join(str(char) for char in (fantasy_languages[firstKey]['more_of'])), required=False, validators=[])
    less_of = forms.CharField(label=u"Less of:", max_length=6, initial=''.join(str(char) for char in (fantasy_languages[firstKey]['less_of'])), required=False)
    none_of = forms.CharField(label=u"None of:", max_length=6, initial=''.join(str(char) for char in (fantasy_languages[firstKey]['none_of'])), required=False)

    #adds text field
    enter_text = forms.CharField(label=u"\n Enter text:\n", label_suffix='', widget=forms.Textarea(attrs={"rows":4, "cols":50}))

class TranslationOutput(forms.Form):
    translation_output = forms.CharField(label=u"\n Translation:\n", label_suffix='', widget=forms.Textarea(attrs={'readonly': 'readonly',"rows":4, "cols":50}))
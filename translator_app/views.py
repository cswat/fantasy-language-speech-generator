#imports
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import json
import logging

#local imports
from translator_app.form import TranslateForm
from translator_app.form import TranslationOutput
from translator_app.translation import Translation

#display main page without path
def home(request):
    logging.info("User accessed homepage.")
    return HttpResponse("Alright!")

#display translation form
def translation_form(request):
    #process the form data
    if request.method == 'POST':
        #create a form instance and populate it with data from the request:
        form = TranslateForm(request.POST)
        #check whether it's valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required
            submission = form.cleaned_data
            logging.debug(submission)

            #put important data into variables
            text_in = submission['enter_text']
            real_language_influences_list = submission['real_language_influences']
            more_of_list = list(submission['more_of'])
            less_of_list = list(submission['less_of'])
            none_of_list = list(submission['none_of'])

            #create a new translation instance with the user's parameters
            translator = Translation(real_language_influences_list,more_of_list,less_of_list,none_of_list)
            #translate the input using the new translation instance and user's text
            translation = translator.translate(text_in)

            #populate output with results
            logging.info("User accessed translator.")
            output = TranslationOutput(initial={'translation_output' : translation})
            return render(request, 'translate.html', {'form': form, 'output': output})
        #TODO - if user submits POST request but form is not valid, how should output be set?

    # if a GET (or any other method) create blank form
    else:
        logging.info("User accessed blank translator.")
        form = TranslateForm()
        output = TranslationOutput()

    return render(request, 'translate.html', {'form': form, 'output': output})
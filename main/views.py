import math
import re

from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FileFieldForm


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "main/home.html"

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        count_files = 0
        list_dict = []
        marks = '''!()[]{};?@#$%:'"\,./^&*_'''
        for file in files:
            str_file = file.read().decode('utf-8')
            for x in marks:
                str_file = str_file.replace(x, "")
            list_word_file = str_file.lower().split(" ")
            new_list_word = list(filter(lambda x: len(x) >= 3, list_word_file))
            list_unique_words = list(set(new_list_word))
            dict_word = dict(file_name=file, all_words=new_list_word, unique_words=list_unique_words)

            list_dict.append(dict_word)
            count_files += 1

        for words in list_dict:
            word_50 = words['unique_words'][:50]
            all_words = words['all_words']
            count_all_words = len(all_words)
            list_dict_stats = []
            for word in word_50:
                count_file_w = 0
                count = all_words.count(word)
                tf = round(count / count_all_words, 3)
                for doc in list_dict:
                    if word in doc['unique_words']:
                        count_file_w += 1
                idf = round(math.log(count_files / count_file_w), 3)

                dict_stats = dict(word=word, tf=tf, idf=idf)
                list_dict_stats.append(dict_stats)

            words['stats'] = list_dict_stats
            words['stats'] = sorted(words['stats'], key=lambda x: x['idf'], reverse=True)

        context = self.get_context_data()
        context.update(dict(list_dict=list_dict))

        return render(self.request, self.template_name, context=context)

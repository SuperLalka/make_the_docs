# -*- coding: utf-8 -*-
import os
import re

from make_the_docs import settings


def transliterate(name):
    """Транслитерация значения name"""
    slovar = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
        'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
        'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e',
        'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
        'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
        'Ц': 'c', 'Ч': 'cz', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
        'Ю': 'u', 'Я': 'ja', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
        '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
        ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
        '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
        'Є': 'e'
    }
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name.lower()


def add_anchor(string):
    clear_string = re.sub("<span\s.+?>", "", re.sub("</span>", "", string))
    for i in re.findall(r'<h[23]>(.+?)</h[23]>', clear_string):
        clear_string = clear_string.replace(str(i), "<a id='%s'>%s</a>" % (transliterate(i), str(i)))
    return clear_string


def get_anchor_list(string):
    a1 = re.findall(r'<h[23]><a\s.+?>(.*?)</a></h[23]>', string)
    clear_a1 = [re.sub("<mark>", "", re.sub("</mark>", "", item)) for item in a1]
    a2 = [transliterate(i) for i in clear_a1]
    return dict(zip(a1, a2))


def search_formatting(results, key):
    for article in results:
        clear_body = re.sub("<span\s.+?>", "", re.sub("</span>", "", article.body))
        for item in re.findall(f'(?i){key}', clear_body):
            article.body = clear_body.replace(item, "<mark>" + item + "</mark>")
        clear_title = re.sub("<span\s.+?>", "", re.sub("</span>", "", article.title))
        for item in re.findall(f'(?i){key}', clear_title):
            article.title = clear_title.replace(item, "<mark>" + item + "</mark>")
    return results


def get_search_context(results, key):
    def get_dict_for_render(results_dict, found):
        for k, v in results_dict.items():
            if re.search(key, v, re.I):
                for item in re.findall(r'<p>.+?</p>', v):
                    if re.search(key, item, re.I):
                        if key not in found:
                            found[k] = item
            elif re.search(key, k, re.I):
                if k not in found:
                    found[k] = re.findall(r'<p>.+?</p>', v)[0]
            else:
                continue
        return found

    if not results:
        return None, 0

    count_num = 0
    for item in results:
        count_num += len(re.findall(key, item.body, re.I)) + len(re.findall(key, item.title, re.I))
        headlines = re.findall(r'<h[23]>(.+?)</h[23]>', item.body)
        paragraphs = re.split(r'<h[23]>.+?</h[23]>', item.body)
        item.anchor_list = get_anchor_list(add_anchor(item.body))
        found = {}

        if paragraphs and headlines:
            if item.body.index(paragraphs[0]) > item.body.index(headlines[0]):
                results_dict = dict(zip(headlines, paragraphs))
                item.found = get_dict_for_render(results_dict, found)

            else:
                preamble = paragraphs[0]
                results_dict = dict(zip(headlines, paragraphs[1:]))

                if key in preamble:
                    item.preamble = preamble

                item.found = get_dict_for_render(results_dict, found)

        else:
            if paragraphs:
                preamble = paragraphs[0]
            else:
                preamble = headlines[0]

            if re.search(key, preamble, re.I):
                item.preamble = preamble

    return results, count_num


def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path

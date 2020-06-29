# -*- coding: utf8 -*-

import re



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


def get_anchor_list(string):
    a1 = re.findall(r'headline">(.*?)<\/span><\/h2>', string)
    a2 = [transliterate(i) for i in a1]
    return dict(zip(a1, a2))


def add_anchor(string):
    for i in re.findall(r'headline">(.*?)<\/span><\/h2>', string):
        string = string.replace(str(i), str(i) + "<a id='%s'></a></span></h2>" % transliterate(i))
    return string


def search_formatting(results, key):
    for article in results:
        article.body = article.body.replace(key, "<mark>" + key + "</mark>")
        article.title = article.title.replace(key, "<mark>" + key + "</mark>")
    return results


def get_search_context(results, key):

    def get_dict_for_render(results_dict, found):
        for k, v in results_dict.items():
            if key in v:
                for item in re.findall(r'<p>.+?<\/p>', v):
                    if key in item:
                        if key not in found:
                            found[k] = item
            elif key in k:
                if k not in found:
                    found[k] = re.findall(r'<p>.+?<\/p>', v)[0]
            else:
                continue
        return found

    count_num = 0
    for item in results:
        count_num += item.body.count(key)
        headlines = re.findall(r'<h[23]>.+?<\/h[23]>', item.body)
        headlines_words = re.findall(r'headline">(.*?)<\/span><\/h[23]>', item.body)
        paragraphs = re.split(r'<h[23]>.+?<\/span><\/h[23]>', item.body)
        item.anchor_list = get_anchor_list(item.body)
        found = {}

        if item.body.index(paragraphs[0]) > item.body.index(headlines[0]):
            results_dict = dict(zip(headlines_words, paragraphs))
            item.found = get_dict_for_render(results_dict, found)

        else:
            preamble = paragraphs[0]
            results_dict = dict(zip(headlines_words, paragraphs[1:]))

            if key in preamble:
                item.preamble = preamble

            item.found = get_dict_for_render(results_dict, found)

    return results, count_num

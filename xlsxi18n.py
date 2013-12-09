#!/usr/bin/python
# -*- coding: utf-8 -*- 

import openpyxl
import os, sys, shutil
import json
from datetime import datetime

config = {}

def row_to_data(row):
    data = {
        'label': row[config['label']].value,
        'file': row[config['file']].value,
        'translations': {}
    }

    for key in config['translations'].keys():
        data['translations'][key] = row[config['translations'][key]].value

    return data

class File:

    def __init__(self, id):
        self.idd = id
        self.labels = []

    def add_label(self, label):
        self.labels.append(label)

    def format(self, language):
        file_format = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n\n'
        for label in self.labels:
            label_format = label.format(language)
            if label_format:
                file_format += "%s\n" % label.format(language)
        file_format += "\n\n</resources>"
        return file_format

class Label:

    def __init__(self, id):
        self.idd = id
        self.translations = {}

    def add_translation(self, language, translation):
        self.translations[language] = translation

    def format(self, language):
        if not self.translations[language]:
            return None
        if not self.translations[language].startswith('['):
            return '<string name="%s">%s</string>' % (self.idd, self.__ap(self.translations[language]))
        else:
            items_string = ""
            for item in self.translations[language].replace("[", "").replace("]", "").split(","):
                items_string += "\t<item>%s</item>\n" % self.__ap(item)
            array_string = '<string-array name="%s">\n%s</string-array>' % (self.idd, items_string)
            return array_string

    def __ap(self, item):
        return item.replace("\'", "\\\'").replace("\"", "\\\"")


def validate_data(data):
    if data['file'] and data['file'].endswith(".xml") and data['label']:
        return True
    return False

def create_label_from_data(data):
    label = Label(data['label'])
    for k in data['translations'].keys():
        label.add_translation(k, data['translations'][k])
    return label

def main():

    if len(sys.argv) != 2:
        print "Usage: xlsxi18n path_file.xlsx"
        exit(0)
    else:
        filename = sys.argv[1]

    config_file = "config.json"

    if not os.path.exists(config_file):
        print "Error! %s build file doesn't exist" % config_file
        exit(0)

    f = open(config_file, "r")
    json_file_content = f.read()
    print json_file_content
    global config 
    config = json.loads(json_file_content)
    default = config['default']

    files = {}

    print ""
    print "+++++++++++++++++++++++++++"
    print "+         XLSXI18N        +"
    print "+++++++++++++++++++++++++++"
    print ""

    print "Reading %s..." % filename
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook.get_sheet_by_name('Languages')
    for row in worksheet.rows:
        data = row_to_data(row)
        if validate_data(data):
            file_name = data['file']
            if not file_name in files:
                files[file_name] = File(file_name)
            label = create_label_from_data(data)
            files[file_name].add_label(label)

    try:
        if os.path.exists("res"):
            dest_folder = "backup_res_%s" % datetime.now().strftime('%Y%m%d_%H%M%S')
            print "Backing up 'res' folder into '%s'" % dest_folder
            shutil.copytree("res", dest_folder)
    except OSError:
        pass

    print "Writing files..."
    for k in data['translations'].keys():
        if default == k:
            folder = os.path.join("res", "values")
        else:
            folder = os.path.join("res", "values-%s" % k)
        if not os.path.exists(folder):
            os.makedirs(folder)
        for file_k in files.keys():
            f = open(os.path.join(folder, file_k), "w")
            f.write(files[file_k].format(k).encode('utf8'))
    print "End"

if __name__ == "__main__":
    main()
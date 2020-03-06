import re
from urllib.parse import urlencode
from urllib.request import urlopen
import json
import time



def get_attribute_http_request(content):
    try:
        params = urlencode(dict({'content':content}))
        req = urlopen('http://172.16.0.73:8080/BXHChatBotKeyAPI/KeyExtractor?' + params)
        raw = req.read().decode('UTF-8')
    except IOError:
        print('Error')
        return None
    else:
        data = json.loads(raw)
        if 'sen_key_pos' in data.keys():
            return data['sen_key_pos']['lst_keys'], data['sen_key_pos']['sen']
        else:
            return None, None
input_file = "E:\PythonSource\ChatbotIntentClassifier\data\\train_raw.txt"
output_file = "E:\PythonSource\ChatbotIntentClassifier\data\\train_nlu.md"

intent_sents = {}

f = open(input_file, encoding='utf-8')
fout = open(output_file, encoding='utf-8', mode='w+')
for line in f:
    split = line.split('\t')
    label, sent = split[0], split[1]
    if label == '1':
        label = 'tim_thong_tin_xe'
    elif label == '2':
        label = 'tim_goi_vay'
    else:
        label_split = label.split(',')
        if len(label_split) > 1:
            label = label_split[0].replace('@', '')
        label = label.replace('@', '')
    data, sent = get_attribute_http_request(sent)
    if data is None:
        continue
    sent_split = sent.split(' ')
    for key in data:
        pos = key['pos']
        label_key = key['label']
        entity = sent_split[pos]
        new_entity = '[{}]({})'.format(entity, label_key)
        sent = sent.replace(entity, new_entity)
    if label in intent_sents.keys():
        intent_sents[label].append(sent)
    else:
        intent_sents[label] = list()
        intent_sents[label].append(sent)
    sent = sent.replace('_', ' ')
    print(label, sent)
for label in intent_sents.keys():
    fout.write('## intent:'+ label + '\n')
    for sent in intent_sents[label]:
        fout.write('- ' + sent + '\n')

    fout.write('\n')

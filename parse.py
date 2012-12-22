# -*- coding: utf-8 -*-
"""
    Very basic script to parse a wiktionnary dump and extract each word type
"""
import codecs
import collections
import sys

from xml.sax import handler, make_parser


WORD_TYPE_ASSOCIATION = collections.OrderedDict([
    (u"{{-art-", "DT"),
    (u"{{-art-déf-", "DT"),
    (u"{{-art-indéf-", "DT"),
    (u"{{-art-part-", "DT"),
    (u"{{-adj-", "JJ"),
    (u"{{-loc-adj-", "JJ"),
    (u"{{-adv-", "RB"),
    (u"{{-loc-adv-", "RB"),
    (u"{{-adv-pron-", "RB"),
    (u"{{-nom-", "NN"),
    (u"{{-loc-nom-", "NN"),
    (u"{{-nom-pr-", "NN"),
    (u"{{-nom-fam-", "NN"),
    (u"{{-nom-sciences-", "NN"),
    (u"{{-prénom-", "NNP"),
    (u"{{-verb-", "VB"),
    (u"{-loc-verb-", "VB"),
    (u"{{-aux-", "VB"),
    (u"{{-flex-loc-verb-", "VB"),
    (u"{{-verb-pr-", "VB"),
    (u"{{-flex-loc-conj-", "VB"),
    (u"{{-flex-conj-", "VB"),
    (u"{{-flex-adj-", "JJ"),
    (u"{{-flex-adj-indéf-", "JJ"),
    (u"{{-flex-adv-", "RB"),
    (u"{{-flex-art-", "DT"),
    (u"{{-flex-art-déf-", "DT"),
    (u"{{-flex-art-indéf-", "DT"),
    (u"{{-flex-art-part-", "DT"),
    (u"{{-flex-interj-", ""),
    (u"{{-flex-loc-adj-", "JJ"),
    (u"{{-flex-loc-nom-", "NN"),
    (u"{{-flex-nom-", "NN"),
    (u"{{-flex-nom-fam-", "NN"),
    (u"{{-flex-nom-pr-", "NN"),
    (u"{{-flex-prénom-", "NNP"),
    (u"{{-flex-prép-", "IN"),
    (u"{{-flex-pronom-pers-", "PRP"),
    (u"{{-flex-pronom-pos-", "PRP$"),
    (u"{{-flex-verb-", "VB"),
    (u"{{-pronom-", "PR"),
    (u"{{-pronom-adj-", "JJPR"),
    (u"{{-pronom-dém-", "PR"),
    (u"{{-pronom-indéf-", "PR"),
    (u"{{-pronom-int-", "PR"),
    (u"{{-pronom-pers-", "PRP"),
    (u"{{-pronom-pos-", "PRP$"),
    (u"{{-adj-dém-", "JJ"),
    (u"{{-adj-excl-", "JJ"),
    (u"{{-adj-indéf-", "JJ"),
    (u"{{-adj-int-", "JJ"),
    (u"{{-adj-num-", "JJ"),
    (u"{{-adj-pos-", "JJ"),
    (u"{{-conj-", "VB"),
    (u"{{-loc-conj-", "VB"),
    (u"{{-prép-", "IN"),
    (u"{{-loc-prép-", "IN"),
])


class WkSaxDocumentHandler(handler.ContentHandler):

    def __init__(self, outputfilename):
        self.has_title = None
        self.word_buffer = {}
        self.output = outputfilename
        self.current_word = None
        self.tag_buffer = u""
        self.article_count = 0
        self.outputf = codecs.open(self.output, encoding='utf-8', mode="a+")


    def startElement(self, name, attrs):
        if name == "title":
            if name.startswith('MediaWiki:'):
                return
            self.has_title = False



    def endElement(self, name):
        if name == "title":
            if name.startswith('MediaWiki:'):
                return
            self.has_title = True
            self.current_word = self.tag_buffer.strip()

        if name == "text" and self.has_title:
            text_word = {}
            correct_region = False
            for line in self.tag_buffer.split():
                if '{{langue|fr}}' in line:
                    correct_region = True
                if not line.startswith('{{'):
                    continue

                for key in WORD_TYPE_ASSOCIATION:
                    if key in line.strip('\n'):
                        text_word[self.current_word] = WORD_TYPE_ASSOCIATION[key]
                        continue
            if correct_region:
                self.word_buffer.update(text_word)

        if name == "page":
            self.current_word = None
            self.article_count += 1

            if self.article_count % 10 == 0:
                self.dump()

        self.tag_buffer = u""

    def characters(self, chrs):
        self.tag_buffer += chrs

    def dump(self):
        if self.word_buffer:
            print self.article_count
            print self.word_buffer.keys()

            self.outputf.write(u"\n".join([u"{0}/{1}".format(k, v) for k, v in
                self.word_buffer.items()]))
            self.outputf.write("\n")
            self.word_buffer = {}

def main():
    filename = sys.argv[1]

    xml_handler = WkSaxDocumentHandler(sys.argv[2])
    parser = make_parser()
    parser.setContentHandler(xml_handler)
    parser.parse(file(filename, "r"))


if __name__ == '__main__':
    main()

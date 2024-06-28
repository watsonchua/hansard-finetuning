from __future__ import annotations

import logging
import re
from typing import Optional, List
from unittest import skip
from bs4 import BeautifulSoup
from dataclasses import dataclass

logger = logging.getLogger('extract-speech')

@dataclass
class HansardInfo:

    __slots__ = ['speaker', 'filename', 'title', 'subtitle', 'topic', 'text']
    speaker: str
    filename: Optional[str]
    title: Optional[str]
    subtitle: Optional[str]
    topic: Optional[str]
    text: str
        
# Checks
def check_proc_text_time(text: str) -> Optional[re.Match]:
    return re.search(r'proc(_| )text', text)

def check_in(text: str) -> Optional[re.Match]:
    return re.search(r'\(In ', text)

def check_page(text: str) -> Optional[re.Match]:
    return re.search("^Page:", text)

def run_all_checks(sent, i, section):
    if check_proc_text_time(sent):
        logger.warning("%s proc text appearing! %s\nIGNORING!", section, i)
        sent = ""
    if check_in(sent):
        logger.warning("%s IN FOUND %s\n text: %s", section, i, sent)
    if re.search(r"(\[|\])", sent):
        logger.warning("%s BRACKET %s\n text: %s\nIGNORING!", section, i, sent)
        sent = ""
    return sent

def remove_tag(text: str) -> str:
    text = re.sub(r'<.+?>', '', text)
#     text = re.sub(r'\s*\(.+?\)', '', text)
    text = re.sub(r'^\s*:\s*', '', text)
    text = re.sub(r'^\s*\):\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s*\d+[:\.]\d\d (am|pm)\s*$', '', text)
    text = re.sub(r'\[Laughter[\.|]\]', '{L}', text)
    text = re.sub(r'\[Applause[\.|]\]', '{Clap}', text)
    text = re.sub(r'\s*\[.*\]', ' ', text)
    return text

def rm_strong(text: str) -> str:
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'\ufeff*', '', text)
    text = re.sub(r'\xa0', ' ', text)
    # remove span too
    text = re.sub(r"<span[^<]*?>", "", text)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"</strong>\s*<strong[^<]*?>", "", text)
    text = re.sub(r"<strong[^<]*?>\s*</strong>", "", text)
    return text

def rm_em_italics(text: str) -> str:
    text = re.sub(r"<em[^<]*?>\s*", "", text)
    text = re.sub(r"</em>", "", text)
    text = re.sub(r"<i[^<]*?>\s*", "", text)
    text = re.sub(r"</i>", "", text)
    return text

def rm_em_lang(text: str) -> str:
    text = re.sub(r"<em[^<]*?>\(\s*In (Malay|English|Mandarin|Tamil|Hokkien)\)\s*:\s*</em>", ":", text)
    text = re.sub(r"\(<em[^<]*?>In (Malay|English|Mandarin|Tamil|Hokkien)</em>\)<em>\: </em>", ":", text)
    text = re.sub(r"\(\s*In (Malay|English|Mandarin|Tamil|Hokkien)\s*\)\s*:", ":", text)
    text = re.sub(r"\(\s*In (Malay|English|Mandarin|Tamil|Hokkien)\s*\)", "", text)
    text = re.sub(r"\(\s*<i[^<]*?>\s*In (Malay|English|Mandarin|Tamil|Hokkien)\s*</i>\s*\)\s*:",'', text)
    text = re.sub(r"\s*<em[^<]*?>\s*\(\s*In (Malay|English|Mandarin|Tamil|Hokkien)\)\s*</em>\s*", "", text)
    text = re.sub(r"\(\s*<em[^<]*?>\s*In (Malay|English|Mandarin|Tamil|Hokkien)\s*</em>\s*\)", "", text)
    text = re.sub(r"<em[^<]*?>\s*:\s*</em>", ":", text)
    text = re.sub(r"<em[^<]*?>\s*</em>", "", text)
    return text

def convert_lang(text: str) -> str:
    text = re.sub(r"\(\s*In (Malay|Mandarin|Tamil|Hokkien)\s*\)\s*:", "<strong>NONENGLISH</strong>:", text)
    text = re.sub(r"\(\s*In (Malay|Mandarin|Tamil|Hokkien)\s*\)", "<strong>NONENGLISH</strong>:", text)
    # Sometimes they put the change in language inside the square brack with the pdf... bringing them out
    text = re.sub(r"\[<strong>NONENGLISH</strong>:", r"<strong>NONENGLISH</strong>:\[", text)
    # Adding the para to prevent the situation of 
    # <strong>Mr Chen Show Mao (Aljunied)</strong>: <strong>NONENGLISH</strong>:
    # leading to two speakers
    text = re.sub(r"<strong>NONENGLISH</strong>:", r":</p><p><strong>NONENGLISH</strong>:", text)
    # iter = re.finditer(r":</p><p><strong>NONENGLISH</strong>:", text)
    # indices = [m.start(0) for m in iter]
    # for ind in indices:
    #     print(text[ind-50:ind+10])
    text = re.sub(r"\(\s*In English\s*\)\s*:", "<strong>ENGLISH</strong>:", text)
    text = re.sub(r"\(\s*In English\s*\)", "<strong>ENGLISH</strong>:", text)
    text = re.sub(r":\s*:", ":", text)
    return text

def preprocess_htmlFullContent(html) -> str:
    # Removing cols
    # html = re.sub(r'<p align="left">Column: \d+<(/|)p>|\*Cols\.\s\d\d\d\d-\d\d\d\d\.', "", html)
    # html = re.sub(r'<p align="left">Column: \d+<(/|)p>|\s*:\s*|<p>|</p>|\*Cols\.\s\d\d\d\d-\d\d\d\d\.', "", html)
    html = re.sub(r'<p align="left">Column:\s*\d+\s*<(/|)p>', " ", html)
    html = re.sub(r'<p align=left>Column:\s*\d+\s*<(/|)p>', " ", html)
    html = re.sub(r'Column No:\s*\d+\s*', " ", html)
    html = re.sub(r'\*Cols\.\s\d\d\d\d-\d\d\d\d\.', "", html)
    html = re.sub(r"</[Bb]>\s*<[Bb]>", " ", html)
    html = re.sub(r'<[Bb]>\s*</[Bb]>', " ", html)
    html = re.sub(r"<sup>(rd|th|st|nd)</sup>", r"\1", html)
    html = re.sub(r"<sup>(<strong>)?o(</strong>)</sup>", "°", html)
    html = re.sub(r"([msA-Z])<sup>([23])</sup>", r"\1\2", html)
    html = re.sub(r"<sup>.*?</sup>", r" ", html)
    # html = re.sub
    return html


def get_speaker_and_speech(sent, i, speaker, iter_content):
    pos_speaker_list = i.find_all('strong')
    if pos_speaker_list:
        if len(pos_speaker_list) == 1:
            w = pos_speaker_list[0]
            # Checking for : to indicate a actual speaker
            if re.search(r"\s*:\s*$", w.text) or re.search(r"^\s*:", w.next_sibling.__str__()):
                speaker = pos_speaker_list[0].text
                while w.next_sibling:
                    sent += w.next_sibling.__str__()
                    w = w.next_sibling 
            else:
                logger.debug("takesSectionVOList Strong tag found without colon: %s \n next line %s", i, w.next_sibling.__str__())
        else:
            found_speaker = False
            logger.warning("More than 1 speaker found %s", i)
            for w in pos_speaker_list:
                if re.search(r"\s*:\s*$", w.text) or re.search(r"^\s*:", w.next_sibling.__str__()):
                    speaker = pos_speaker_list[0].text
                    while w.next_sibling:
                        sent += w.next_sibling.__str__()
                        w = w.next_sibling 
                    found_speaker = True
                    logger.warning("Extracted speaker: %s \n text: %s", speaker, remove_tag(sent))
                    break 
            if (not found_speaker) and speaker:
                sent = i.text
                logger.warning("No speaker found using original %s: %s", speaker, remove_tag(sent))
    else:
        sent = i.text #i.__str__()
        # for child in i.children:
        #     if not (re.match("<em>", child.__str__()) or re.match(r"^\W+$", child.__str__())) or start:
        #         start = True
        #         sent += child.__str__()
    return sent, speaker, iter_content


def parse_takesSectionVOList(data: dict, hansard_info_list: List[HansardInfo], filename) -> List[HansardInfo]:
    """For 2020 hansard format, where the text is in field takesSectionVOList

    Args:
        data (dict): hansard json read as dictionary
        hansard_info_list (List(HansardInfo)): list of HansardInfo extracted to append to
        filename (str): Name of the hansard file
    Returns:
        hansard_info_list
    """
    for idx, article in enumerate(data['takesSectionVOList']):
        title = article['title']
        subtitle = article['subTitle']
        # print the before and after processing
        logger.debug("Filename: %s", filename)
        logger.debug("%s\nORIGINAL %s:\n%s\nREMOVED %s:\n%s", title, idx, article['content'], idx , convert_lang(rm_em_italics(rm_strong(preprocess_htmlFullContent(article['content'])))))
        content = BeautifulSoup(convert_lang(rm_em_italics(rm_strong(preprocess_htmlFullContent(article['content'])))), "html.parser")
        topic = ""
        speaker = ""
        cur_speaker = ""
        # getting h6 for the topic.. will have the page too but ignoring it.
        iter_content = content.find_all(['h6', 'p'])
        while iter_content:
            sent = ""
            i = iter_content.pop(0)
            # Expecting multipara for the case where someone asked a qn
            # E.g
            # <p>42 <strong>Ms He Ting Ru</strong> asked the Minister for Law whether a review of the Legal Profession Act to clarify the jurisdiction of the courts and routes of review/appeals available to a complainant, solicitor and the Law Society will be conducted. <p><strong>Mr K Shanmugam</strong>: My Ministry has noted the remarks of the Court of Appeal, and will study the issue and consult the relevant stakeholders. </p><p><br/></p></p>
            # For such a case will expect more than one speaker (strong)
            if i.find_all('p'): #Keeping only one para from the multipara
                html_text = i.__str__()
                html_text = re.sub('<p[ ].*?>', '<p>', html_text)
                i = BeautifulSoup(html_text.split('<p>')[1], "html.parser")
            if re.match("<h6>", i.__str__()):
                # Topics comes with <h6><em>, but time only have <h6>, [proc text] also
                # But to simplify the processing em and i tags have been removed.
                if (not re.match("\s*\d+(\.\d\d)?\s*(am|pm)", i.text)) and (not re.search("proc text", i.text)):
                    topic = i.text
                else: 
                    logger.debug("TIME detected %s SKIPPING", i.text)
            else:
                sent, speaker, iter_content = get_speaker_and_speech(sent, i, speaker, iter_content)
                if speaker not in  ["NONENGLISH", "ENGLISH"]:
                    cur_speaker = speaker

            # sent = rm_em_lang(sent)
            if check_page(sent):
                logger.warning("PAGE %s \n Text: %s\nSkipping it", i, remove_tag(sent))
                sent = ""
            sent = remove_tag(sent)
            sent = run_all_checks(sent, i, "takesSectionVOList")
            # sent = remove_tag(sent)
            if sent.strip() and cur_speaker:
                if speaker == "NONENGLISH":
                    hansard_info_list.append(HansardInfo(speaker=cur_speaker+"_NONENGLISH", filename=filename, title=title, subtitle=subtitle, topic=topic, text=sent))
                    logger.debug("title: %s\nsubtitle: %s\ntopic: %s\nspeaker: %s\ntext: %s", title, subtitle, topic, cur_speaker+"_NONENGLISH", sent)
                else:
                    hansard_info_list.append(HansardInfo(speaker=cur_speaker, filename=filename, title=title, subtitle=subtitle, topic=topic, text=sent))
                    logger.debug("title: %s\nsubtitle: %s\ntopic: %s\nspeaker: %s\ntext: %s", title, subtitle, topic, cur_speaker, sent)
    return hansard_info_list


def parse_hcSpeech(data: dict, hansard_info_list: List[HansardInfo], filename) -> List[HansardInfo]:
    html = data["htmlFullContent"].replace("\r\n", " ")
    html = preprocess_htmlFullContent(html)
    soup = BeautifulSoup(html, 'html.parser')
    is_english = True
    cur_speaker = ""
    for i in soup.find_all(class_="hcParagraph"):
        pos_speaker_list = i.find_all(class_='ph b')
        text = ""
        if pos_speaker_list:
            if len(pos_speaker_list) > 1:
                # looking at the logs all are one speaker with the title in ph b as well..
                logger.warning("hsSpeech More than one speaker! %s", i)
                if len(pos_speaker_list) == 2:
                    cur_speaker = " ".join([w.text for w in pos_speaker_list])
                    is_english = True
                    logger.debug("hsSpeech Speaker %s", cur_speaker)
                    text = i.text
                    text = re.sub(r".*:", "", text) 
                    # text = " ".join([part.__str__() for part in list(i.children)[5:]])
                    logger.warning("hsSpeech Extracted speaker: %s \n text: %s", cur_speaker, text)
            else:
                w = pos_speaker_list[0]
                if re.search(r"\s*:\s*$", w.text) or re.search(r":", i.text):
                    cur_speaker = pos_speaker_list[0].text
                    is_english = True
                    logger.debug("hsSpeech Speaker %s", cur_speaker)
                    text = " ".join([part.__str__() for part in list(i.children)[4:]])
                else:
                    logger.debug("hsSpeech Not a speaker %s", i)
        elif cur_speaker:
            text = i.text
        text = remove_tag(text)
        text = convert_lang(text)
        if re.search(r"<strong>NONENGLISH</strong>:", text):
            is_english = False
            text = re.sub(r":</p><p><strong>NONENGLISH</strong>:", "", text)
        elif re.search(r"<strong>ENGLISH</strong>:", text):
            is_english = True
            text = re.sub(r"<strong>ENGLISH</strong>:", "", text)
        text = remove_tag(text)
        text = run_all_checks(text, i, "hcSpeech")
        if text:
            if not is_english:
                hansard_info_list.append(HansardInfo(speaker=cur_speaker+"_NONENGLISH", filename=filename, title=None, subtitle=None, topic=None, text=text))
            else:
                hansard_info_list.append(HansardInfo(speaker=cur_speaker, filename=filename, title=None, subtitle=None, topic=None, text=text))
    return hansard_info_list

def parse_div_left(data: dict, hansard_info_list, filename):
    html = data["htmlFullContent"].replace("\r\n", " ")
    html = preprocess_htmlFullContent(html)
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all('div', align="left")
    speaker = ""
    while content:
        passage = content.pop(0)
        if passage.find_all('div', align="left"):
            html_text = passage.__str__()
            html_text = re.sub(r'<div[ ].*?align=[\'"]left[\'"]>', '<div align=left>', html_text)
            if len(html_text.split('<div align=left>'))>1:
                passage = BeautifulSoup(html_text.split('<div align=left>')[1], "html.parser")
            else:
                print(html_text)
                continue
        # print(passage)
        iter_content = passage.find_all('p')
        while iter_content:
            i = iter_content.pop(0)
            if i.find_all('p'):
                html_text = i.__str__()
                html_text = re.sub('<p[ ].*?>', '<p>', html_text)
                i = BeautifulSoup(html_text.split('<p>')[1], "html.parser")
            text = ""
            if i.find_all('b'):
                for w in i.find_all('b'):
                    if re.search(r"\s*:\s*$", w.text) or re.search(r"^\s*:", w.next_sibling.__str__()):
                        speaker = re.sub(r"^\s*|\s*:\s*$", "", w.text)
                        logger.debug(speaker)
                        logger.debug("********************")
                        text = ""
                        while w.next_sibling:
                            w = w.next_sibling
                            # text = BeautifulSoup(w.__str__(), "html.parser")
                            text += w.__str__() + " "
                        text = rm_em_lang(text)
                        logger.debug("PARA TOP: %s", remove_tag(text))
                        break
                    else:
                        speaker = ""
            else:
                if speaker:
                    text = i.text
                    text = rm_em_lang(text)
                    logger.debug("BOTTOM PARA: %s", remove_tag(text))
            if check_page(remove_tag(text)):
                logger.warning("PAGE %s \n Text: %s", i, remove_tag(text))
                text = ""
            text = remove_tag(text)
            text = run_all_checks(text, i, "PARSEDIVLEFT")
            if text.strip():
                hansard_info_list.append(HansardInfo(speaker=speaker, filename=filename, title=None, subtitle=None, topic=None, text=text.strip()))
                            
    # hansard_info_list = hansard_info_list[:-2]
    return hansard_info_list

# M³ SO² ½ ¾
def remove_punc(text):
    text = re.sub(r'[.|,|\?|\-|\$|:|%|"|!]', '', text)
    text = re.sub(r"'", '', text)
    return text

def remove_punc2(text):
    text = re.sub(r'[.|,|\?|\$|:|"|!]', '', text)
    return text

def convert_punc(text):
    text = re.sub(r'["]', '', text)
    text = re.sub(r'[-|/]', ' ', text)
    return text

def convert_unicode(text, del_brac=False, replace_sym=False):
    """Converts unicode symbol to ascii equivalent
    """
    text = re.sub(chr(8217), "'", text)
    text = re.sub("(“|‟|”)", '"', text)
    text = re.sub("(–|−|−|\xad|‐|—|─|‒|•|-|·|‑| ̶)", '-', text)
    text = re.sub("(‘|'|Ê¼|ʼ|`)", "'", text)
    text = re.sub("…", ". ", text)
    text = re.sub("(\\ufeff|\\u200b|»|¬)", "", text)
    text = re.sub("ﬁ", "fi", text)
    text = re.sub("€˜", "'", text)
    text = re.sub("(Ã©|é|è|ê)", "e", text)
    text = re.sub("(Ü)", "U", text)
    text = re.sub("(ü)", "u", text)
    text = re.sub("(Ã¡|à|Ã´|ä|á|Ã¨)", "a", text)
    text = re.sub("(ï)", "i", text)
    text = re.sub("(Íž|ÍŸ|€¦)", "", text)
    text = re.sub("(Ä«|Ã¯|ì)", "i", text)
    text = re.sub("(Ã±|ñ)", "n", text)
    text = re.sub("(Ã‰)", "E", text)
    text = re.sub("(ô|ō|a)", "o", text)
    text = re.sub("(ç|Ã§|أ§)", "c", text)
    text = re.sub("(Á|Ã)", "A", text)
    text = re.sub("(¦)", "", text)

    # remove col
    text = re.sub(r"\*Cols\.( \d{4}-\d{4};| \d{4}-\d{4})+( \d{4}-\d{4}\.|)", "", text)
    # remove bracket
    text = re.sub(r"\[.*\]", "", text)
    text = re.sub(r"\[.*", "", text)
    text = re.sub(r".*\]", "", text)
    # bracker
    text = re.sub(r'\(\s*In (Malay|English|Mandarin|Tamil|Hokkien)\s*\)\s*(:|)', "", text)
    #### REMOVING BRACKET
#     text = re.sub(r'\([^\(]*?\)\W*', "", text)
#     text = re.sub(r'\([^\(]*?\)\W*', "", text)
    if del_brac:
        text = re.sub(r'\([^\(]*?\)', '', text)
        text = re.sub(r'\([^\(]*?\)', '', text)
    #### Removing /
    text = re.sub(r'.*?\\:', "", text)
    text = re.sub(r'^\W*?:', "", text)
    
    if replace_sym:
        #### Changing slash to space
        text = re.sub(r'/', ' ', text)
        text = re.sub(r'&', ' and ', text)
        text = re.sub(r'@', " at ", text)
        text = re.sub(r"(?<=\w)\.(?=\w)", " dot ", text)
    
    ## random symbols
    text = re.sub(r'ج¶', '', text)
    
    return text

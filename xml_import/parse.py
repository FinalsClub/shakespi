import xml

import xml.etree.ElementTree as ET
tree = ET.parse('romeo_and_juliet_moby.xml')
root = tree.getroot()


def list_of_text(element, tag):
    """Find all children of element with the specified tag, 
    Return a list of the text of each element"""
    return [e.text for e in element.findall(tag)]


class ShakespeareParser:
    """namespace for static methods. Each method operates on an 
    certain type of element
    """

    @staticmethod
    def speech(speech):
        """
        <!ELEMENT SPEECH   (SPEAKER+, (LINE | STAGEDIR | SUBHEAD)+)>
        """
        if speech.tag != 'SPEECH': 
            raise Exception('Element is not a speech element', speech)
        d = {
            'speaker': speech.find('SPEAKER').text,
            'lines': list_of_text(speech, 'LINE')
        }
        return d

    @staticmethod
    def act(act):
        """
        <!ELEMENT ACT      (TITLE, SUBTITLE*, PROLOGUE?, SCENE+, EPILOGUE?)>

        An act contains: 
            TITLE
            zero or more SUBTITLE
            one optional PROLOGUE
            one or more SCENE
            one optional EPILOGUE
        """
        if act.tag != 'ACT':
            raise Exception('Element is not an ACT Element', act)

        # 'ACT I', 'ACT II', etc
        act_name = act.find('TITLE').text

        # most acts don't have subtitles
        #subtitles = list_of_text(act, 'SUBTITLE')

        scenes = []

        for e in act:
            if e.tag == 'SCENE':
                scenes.append(ShakespeareParser.scene(e))

        d = {
            'name': act_name,
            'scenes': scenes
        }

        return d

    @staticmethod
    def scene(scene):
        """ <!ELEMENT SCENE    (TITLE, SUBTITLE*, (SPEECH | STAGEDIR | SUBHEAD)+)>
        subhead and stagedir have .text only
        """
        if scene.tag != 'SCENE':
            raise Exception('Element is not a SCENE element')

        # ex "SCENE I.  Verona. A public place."
        scene_title = scene.find('TITLE').text

        events = []

        for e in scene:
            tag = e.tag
            if tag in ('STAGEDIR', 'SUBHEAD'):
                events.append({
                    'type':tag,
                    'content':e.text})
            elif tag == 'SPEECH':
                events.append(ShakespeareParser.speech(e))

        return events


a = root.find('ACT')
d = ShakespeareParser.act(a)














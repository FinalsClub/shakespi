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
    def parse_line(line, play):
        # TODO: set global line count state

        pass

    @staticmethod
    def parse_speech(speech, play_context):
        """
        <!ELEMENT SPEECH   (SPEAKER+, (LINE | STAGEDIR | SUBHEAD)+)>
        """
        if speech.tag != 'SPEECH': 
            raise Exception('Element is not a speech element', speech)

        # Rarely a speech will be two characters in unison
        speakers = list_of_text(speech, 'SPEAKER')
        play_context['speakers'] = ', '.join(speakers)
        play_context['speaker_list'] = speakers

        for e in speech:
            if e.tag == 'LINE':
                ShakespeareParser.parse_line(a, play_context)

    @staticmethod
    def parse_act(act, play_context):
        """
        <!ELEMENT ACT      (TITLE, SUBTITLE*, PROLOGUE?, SCENE+, EPILOGUE?)>

        An act contains: 
            TITLE
            zero or more SUBTITLE
            one optional PROLOGUE
            one or more SCENE
            one optional EPILOGUE
        """
        print 'parse_act:', play_context

        if act.tag != 'ACT':
            raise Exception('Element is not an ACT Element', act)

        # 'ACT I', 'ACT II', etc
        play_context['act_title']= act.find('TITLE').text

        # most acts don't have subtitles
        #subtitles = list_of_text(act, 'SUBTITLE')

        scenes = []

        prologue = act.find('PROLOGUE')
        if prologue:
            scenes.append(prologue)

        scenes = scenes + act.findall('SCENE')

        epilogue = act.find('EPILOGUE')
        if epilogue: 
            scenes.append(epilogue)

        for i, scene in enumerate(scenes):
            # If scene has a prologue index beginning at 0
            if prologue: 
                play_context['scene_index'] = i
            else:
                play_context['scene_index'] = i + 1
            parse_scene(scene, play_context)

    @staticmethod
    def parse_scene(scene, play_context):
        """
        Parse a SCENE, PROLOGUE, or EPILOGUE
        <!ELEMENT SCENE    (TITLE, SUBTITLE*, (SPEECH | STAGEDIR | SUBHEAD)+)>
        subhead and stagedir have .text only
        """
        if scene.tag not in ('SCENE', 'PROLOGUE', 'EPILOGUE'):
            raise Exception('Element is not a SCENE, PROLOGUE, or EPILOGUE element')

        # ex "SCENE I.  Verona. A public place."
        play_context['scene_title'] = scene.find('TITLE').text

        for e in scene:
            tag = e.tag
            if tag in ('STAGEDIR', 'SUBHEAD'):
                pass
            elif tag == 'SPEECH':
                ShakespeareParser.parse_speech(e, play_context)

        return events

    @staticmethod
    def parse_play(play_xml):

        tree = ET.parse(play_xml)
        root = tree.getroot()
        play_context = {
            play_title_long: root.find('TITLE').text,
            play_title: root.find('PLAYSUBT').text,
        }
        acts = root.findall('ACT')

        for i, act in enumerate(acts):
            play_context["act_index"] = i + 1
            ShakespeareParser.parse_act(act, play_context)

#a = root.find('ACT')
#d = ShakespeareParser.parse_act(a)














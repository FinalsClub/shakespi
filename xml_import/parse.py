import xml
import xml.etree.ElementTree as ET


def list_of_text(element, tag):
    """Find all children of element with the specified tag, 
    Return a list of the text of each element"""
    texts = []
    for e in element.findall(tag):
        if e.text:
            texts.append(e.text)
    return texts


class ShakespeareParser:
    """
    Instantiate me, then parse_play(xml_filename) to populate
    self.lines
    """
    def __init__(self):
        self.line_count = 0
        self.lines = []

    def parse_play(self, xml_filename):
        """
        <!ELEMENT PLAY (TITLE, FM, PERSONAE, SCNDESCR, PLAYSUBT, INDUCT?, PROLOGUE?, ACT+, EPILOGUE?)>
        """

        tree = ET.parse(xml_filename)
        root = tree.getroot()
        play_context = {
            'play_title_long': root.find('TITLE').text,
            'play_title': root.find('PLAYSUBT').text,
        }
        acts = root.findall('ACT')

        for i, act in enumerate(acts):
            play_context["act_index"] = i + 1
            self.parse_act(act, play_context)

    def parse_act(self, act, play_context):
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
            self.parse_scene(scene, play_context)

    def parse_scene(self, scene, play_context):
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
                self.parse_speech(e, play_context)

    def parse_speech(self, speech, play_context):
        """
        <!ELEMENT SPEECH   (SPEAKER+, (LINE | STAGEDIR | SUBHEAD)+)>
        """
        if speech.tag != 'SPEECH': 
            raise Exception('Element is not a speech element', speech)

        # Rarely a speech will be two characters in unison
        speakers = list_of_text(speech, 'SPEAKER')
        play_context['speaker_text'] = ', '.join(speakers)
        play_context['speaker_list'] = speakers

        for e in speech:
            if e.tag == 'LINE':
                self.parse_line(e, play_context)

    def parse_line(self, line, play_context):
        """
        <!ELEMENT LINE     (#PCDATA | STAGEDIR)*>
        """
        if line.tag != 'LINE':
            raise Exception('Element is not a LINE element', line)

        line_context = dict(play_context)
        line_context['line_text'] = line.text # BUG: doesn't handle case when stage dir preceeds text
        line_context['play_line_count'] = self.line_count
        self.line_count += 1
        self.lines.append(line_context)

    

if __name__ == '__main__':
    a = raw_input('Parse all .xml files in dir, overwriting .json files (y/n)?')
    if a.lower()== 'y':
        import os, json
        xml_filenames = [fn for fn in os.listdir('.') if fn.lower().endswith('.xml')]
        print xml_filenames
        for fn in xml_filenames:
            p = ShakespeareParser()
            p.parse_play(fn)
            json_filename = fn[:-4] + '.json'
            with open(json_filename, 'w') as f:
                json.dump(p.lines, f)
else:
    # for testing
    p = ShakespeareParser()
    p.parse_play('romeo_and_juliet_moby.xml')













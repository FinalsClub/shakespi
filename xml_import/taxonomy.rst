Taxonomy of MongoDB version of XML Shakespeare
==============================================

Questions
---------

 +  Do Prologue lines count towards line counts
 =  Line counts are generated on a Prologue, Scene or Epilogue basis
 =  And are variable based on the publisher's whims


What data are we generating?
----------------------------

Play provides:

  play_title_long: The long name for a Shakespeare play,
                    `The Tragedy of Romeo and Juliet`
  play_title:       The colloquial title of a play
                    `Romeo and Juliet`

Act provides:

  act_title: The title of an Act,
             `Act IV`
  act_index: 1-indexed act count, for presenting order
              1-indexed so it lines up with the act_title

Scene, Prologue or Epilogue provides:

  scene_title: the title of the scene
               `SCENE III.  Friar Laurence's cell.`
               `PROLOGUE`
               `EPILOGUE`

Speech provides:

  speaker_text:   The character speaking a line of text, `ROMEO`
                  or a comma delenated list of speakers: `Romeo, Juliet` (rare)

  speaker_list:   A list of speakers for a line of text
                  used to query for all lines by SPEAKER

Line provides:

  line_text:    The verse of the speaker

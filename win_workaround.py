from pynput import keyboard
import os

WINDOWS_SCANCODES = [
    None,    #0
    'LBUTTON',    #1
    'RBUTTON',    #2
    'CANCEL',    #3
    'MBUTTON',    #4
    'XBUTTON1',    #5
    'XBUTTON2',    #6
    None,    #7
    'BACKSPACE',    #8
    'TAB',    #9
    None,    #10
    None,    #11
    'CLEAR',    #12
    'ENTER',    #13
    None,    #14
    None,    #15
    'SHIFT',    #16
    'CTRL',    #17
    'ALT',    #18
    'PAUSE',    #19
    'CAPS_LOCK',    #20
    'KANA/HANGUL',    #21
    None,    #22
    'JUNJA',    #23
    'FINAL',    #24
    'HANJA/KANJI',    #25
    None,    #26
    'ESCAPE',    #27
    'CONVERT',    #28
    'NONCONVERT',    #29
    'ACCEPT',    #30
    'MODECHANGE',    #31
    'SPACE',    #32
    'PAGE_UP',    #33
    'PAGE_DOWN',    #34
    'END',    #35
    'HOME',    #36
    'LEFT',    #37
    'UP',    #38
    'RIGHT',    #39
    'DOWN',    #40
    'SELECT',    #41
    'PRINT',    #42
    'EXECUTE',    #43
    'PRINT_SCREEN',    #44
    'INS',    #45
    'DEL',    #46
    'HELP',    #47
    '0',    #48
    '1',    #49
    '2',    #50
    '3',    #51
    '4',    #52
    '5',    #53
    '6',    #54
    '7',    #55
    '8',    #56
    '9',    #57
    None,    #58
    None,    #59
    None,    #60
    None,    #61
    None,    #62
    None,    #63
    None,    #64
    'A',    #65
    'B',    #66
    'C',    #67
    'D',    #68
    'E',    #69
    'F',    #70
    'G',    #71
    'H',    #72
    'I',    #73
    'J',    #74
    'K',    #75
    'L',    #76
    'M',    #77
    'N',    #78
    'O',    #79
    'P',    #80
    'Q',    #81
    'R',    #82
    'S',    #83
    'T',    #84
    'U',    #85
    'V',    #86
    'W',    #87
    'X',    #88
    'Y',    #89
    'Z',    #90
    'LEFT_WIN',    #91
    'RIGHT_WIN',    #92
    'APPS',    #93
    None,    #94
    'SLEEP',    #95
    'NUMPAD_0',    #96
    'NUMPAD_1',    #97
    'NUMPAD_2',    #98
    'NUMPAD_3',    #99
    'NUMPAD_4',    #100
    'NUMPAD_5',    #101
    'NUMPAD_6',    #102
    'NUMPAD_7',    #103
    'NUMPAD_8',    #104
    'NUMPAD_9',    #105
    'MULTIPLY',    #106
    'ADD',    #107
    'SEPARATOR',    #108
    'SUBTRACT',    #109
    'DECIMAL',    #110
    'DIVIDE',    #111
    'F1',    #112
    'F2',    #113
    'F3',    #114
    'F4',    #115
    'F5',    #116
    'F6',    #117
    'F7',    #118
    'F8',    #119
    'F9',    #120
    'F10',    #121
    'F11',    #122
    'F12',    #123
    'F13',    #124
    'F14',    #125
    'F15',    #126
    'F16',    #127
    'F17',    #128
    'F18',    #129
    'F19',    #130
    'F20',    #131
    'F21',    #132
    'F22',    #133
    'F23',    #134
    'F24',    #135
    None,    #136
    None,    #137
    None,    #138
    None,    #139
    None,    #140
    None,    #141
    None,    #142
    None,    #143
    'NUM_LOCK',    #144
    'SCROLL_LOCK',    #145
    None,    #146
    None,    #147
    None,    #148
    None,    #149
    None,    #150
    None,    #151
    None,    #152
    None,    #153
    None,    #154
    None,    #155
    None,    #156
    None,    #157
    None,    #158
    None,    #159
    'L_SHIFT',    #160
    'R_SHIFT',    #161
    'L_CONTROL',    #162
    'R_CONTROL',    #163
    'L_MENU',    #164
    'R_MENU',    #165
    'BROWSER_BACK',    #166
    'BROWSER_FORWARD',    #167
    'BROWSER_REFRESH',    #168
    'BROWSER_STOP',    #169
    'BROWSER_SEARCH',    #170
    'BROWSER_STOP',    #171
    'BROWSER_HOME',    #172
    'VOLUME_MUTE',    #173
    'VOLUME_DOWN',    #174
    'VOLUME_UP',    #175
    'MEDIA_NEXT_TRACK',    #176
    'MEDIA_PREV_TRACK',    #177
    'MEDIA_STOP',    #178
    'MEDIA_PLAY_PAUSE',    #179
    'LAUNCH_MAIL',    #180
    'LAUNCH_MEDIA_SELECT',    #181
    'LAUNCH_APP1',    #182
    'LAUNCH_APP2',    #183
    None,    #184
    None,    #185
    ';',    #186
    '+',    #187
    ',',    #188
    '-',    #189
    '.',    #190
    '/',    #191
    '~',    #192
    None,    #193
    None,    #194
    None,    #195
    None,    #196
    None,    #197
    None,    #198
    None,    #199
    None,    #200
    None,    #201
    None,    #202
    None,    #203
    None,    #204
    None,    #205
    None,    #206
    None,    #207
    None,    #208
    None,    #209
    None,    #210
    None,    #211
    None,    #212
    None,    #213
    None,    #214
    None,    #215
    None,    #216
    None,    #217
    None,    #218
    '[',    #219
    '\\',    #220
    ']',    #221
    '\'',    #222
    None,    #223
    None,    #224
    None,    #225
    None,    #226
    None,    #227
    None,    #228
    'PROCESS',    #229
    None,    #230
    'PACKET',    #231
    None,    #232
    None,    #233
    None,    #234
    None,    #235
    None,    #236
    None,    #237
    None,    #238
    None,    #239
    None,    #240
    None,    #241
    None,    #242
    None,    #243
    None,    #244
    None,    #245
    'ATTN',    #246
    'CR_SEL',    #247
    'EX_SEL',    #248
    'ERASE_EOF',    #249
    'PLAY',    #250
    'ZOOM',    #251
    None,    #252
    'PA1',    #253
    'CLEAR']    #254

def parse_key(key):
        if os.name == 'nt' and type(key) == keyboard.KeyCode:
            return keyboard.KeyCode(vk=key.vk, char=WINDOWS_SCANCODES[key.vk])
        else:
            return key
DEBUG_MODE = False

CONDITIONS = [(('EASY', 'NEUTRAL'), ('DIFFICULT', 'NEUTRAL')), (('DIFFICULT', 'NEUTRAL'), ('EASY', 'NEUTRAL'))]

RULE_PROPS = {'EASY': {'rule': 'diamonds on left, all others on right', 'demo_cards': [54, 60], 'cards': [48, 47, 10, 58, 14, 18, 57, 32], 'demo_answers': [0, 1], 'answers': [1, 0, 0, 1, 1, 0, 1, 1]},
            'DIFFICULT': {'rule': 'green-one, red/purple on left, green two/three on right', 'demo_cards': [61, 34], 'cards': [33, 32, 42, 17, 68, 29, 26, 45], 'demo_answers': [0, 1], 'answers': [0, 1, 0, 0, 0, 1, 0, 0]}}

FEEDBACK = {
    'NEUTRAL': {'CORRECT': ['neutral1', 'neutral2'], 'INCORRECT': ['neutral1', 'neutral2']}
}

NEUTRAL = ['neutral1', 'neutral2']

VIDEO_LIST = ['neutral1', 'neutral2']
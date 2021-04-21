def evaluate_card(rule, card):
    for c in rule:
        res = True
        for prop_num in range(4):
            if not CARD_PROPERTIES[card][prop_num] in c[prop_num]:
                res = False
        if res:
            return res
    return False


DEBUG_MODE = False

CARD_PROPERTIES = []
for color in ['red', 'green', 'purple']:
    for shading in ['open', 'striped', 'solid']:
        for shape in ['diamond', 'oval', 'squiggle']:
            for number in ['one', 'two', 'three']:
                CARD_PROPERTIES.append((color, shading, shape, number))

CONDITIONS = [(('EASY', 'NONVERBAL'), ('DIFFICULT', 'NONVERBAL')), (('EASY', 'NEUTRAL'), ('DIFFICULT', 'NEUTRAL')), (('DIFFICULT', 'NONVERBAL'), ('EASY', 'NONVERBAL')), (('DIFFICULT', 'NEUTRAL'), ('EASY', 'NEUTRAL')), 
(('EASY', 'NEUTRAL'), ('DIFFICULT', 'NONVERBAL')), (('EASY', 'NONVERBAL'), ('DIFFICULT', 'NEUTRAL')), (('DIFFICULT', 'NEUTRAL'), ('EASY', 'NONVERBAL')), (('DIFFICULT', 'NONVERBAL'), ('EASY', 'NEUTRAL')),
]

easy_rule = [
            [
                [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['oval'], ['one', 'two', 'three']]
            ],
            [
                [['red', 'green', 'purple'], ['open', 'striped', 'solid'], ['diamond', 'squiggle'], ['one', 'two', 'three']]
            ]
        ]

difficult_rule = [
            [
                [['green', 'purple'], ['open', 'striped', 'solid'], ['oval', 'diamond', 'squiggle'], ['one', 'two', 'three']],
                [['red'], ['open', 'striped', 'solid'], ['oval', 'diamond', 'squiggle'], ['one']]
            ],
            [
                [['red'], ['open', 'striped', 'solid'], ['oval', 'diamond', 'squiggle'], ['two', 'three']]
            ]
        ]

RULE_PROPS = {'EASY': {'rule': easy_rule, 'demo_cards': [10, 75, 33, 4], 'cards': [56, 36, 31, 16, 0, 76, 41, 71, 3, 61]},
            'DIFFICULT': {'rule': difficult_rule, 'demo_cards': [38, 76, 1, 9], 'cards': [56, 22, 31, 17, 0, 76, 41, 71, 3, 23]}}

for rule_name, props in RULE_PROPS.items():
    demo_answer = []
    for card in props['demo_cards']:
        bin_res = [0] * len(props['rule'])
        for cur_bin_num, cur_bin_rule in enumerate(props['rule']):
            bin_res[cur_bin_num] = evaluate_card(cur_bin_rule, card)
        demo_answer.append(bin_res)
    RULE_PROPS[rule_name]['demo_answers'] = demo_answer
    
    answer = []
    for card in props['cards']:
        bin_res = [0] * len(props['rule'])
        for cur_bin_num, cur_bin_rule in enumerate(props['rule']):
            bin_res[cur_bin_num] = evaluate_card(cur_bin_rule, card)
        answer.append(bin_res)
    RULE_PROPS[rule_name]['answers'] = answer

FEEDBACK = {
    'NEUTRAL': {'CORRECT': ['neutral1', 'neutral2'], 'INCORRECT': ['neutral1', 'neutral2']},
    'NONVERBAL': {'CORRECT': ['happy1', 'happy2'], 'INCORRECT': ['sad1', 'sad2']}
}

NEUTRAL = ['neutral1', 'neutral2']

VIDEO_LIST = ['neutral1', 'neutral2', 'happy1', 'happy2', 'sad1', 'sad2']
TAXONOMY = {
    "speech_act": {
        "template": "This sentence functions as {}.",
        "labels": {
            "a direct command": {"alias": "command", "quadrant": "Directive-External"},
            "a request for help or support": {"alias": "request", "quadrant": "Directive-External"},
            "a suggestion or recommendation": {"alias": "suggestion", "quadrant": "Directive-Internal"},
            "an affirmation or agreement": {"alias": "affirmation", "quadrant": "Directive-Internal"},
            "a question or inquiry": {"alias": "question", "quadrant": "Interpretive-External"},
            "an urgent demand": {"alias": "demand", "quadrant": "Directive-External"},
            "a rhetorical question": {"alias": "rhetorical", "quadrant": "Interpretive-External"}
        }
    },
    "emotion": {
        "template": "The speaker expresses {}.",
        "labels": {
            "joy or happiness": {"alias": "joy", "quadrant": "Interpretive-Internal"},
            "fear or anxiety": {"alias": "fear", "quadrant": "Interpretive-Internal"},
            "anger or frustration": {"alias": "anger", "quadrant": "Interpretive-Internal"},
            "sadness or disappointment": {"alias": "sadness", "quadrant": "Interpretive-Internal"},
            "surprise or shock": {"alias": "surprise", "quadrant": "Interpretive-External"},
            "disgust or aversion": {"alias": "disgust", "quadrant": "Interpretive-Internal"},
            "relief or release": {"alias": "relief", "quadrant": "Interpretive-Internal"},
            "anticipation or tension": {"alias": "anticipation", "quadrant": "Interpretive-External"},
            "gratitude or appreciation": {"alias": "gratitude", "quadrant": "Directive-Internal"}
        }
    },
    "sentiment": {
        "template": "The sentiment expressed is {}.",
        "labels": {
            "positive or affirming": {"alias": "positive", "quadrant": "Directive-Internal"},
            "negative or critical": {"alias": "negative", "quadrant": "Directive-Internal"},
            "neutral or balanced": {"alias": "neutral", "quadrant": "Interpretive-Internal"},
            "factual or impartial": {"alias": "factual", "quadrant": "Interpretive-Internal"}
        }
    },
    "cognitive_state": {
        "template": "The speaker's mental state is {}.",
        "labels": {
            "focused and attentive": {"alias": "focused", "quadrant": "Directive-Internal"},
            "distracted or unfocused": {"alias": "distracted", "quadrant": "Interpretive-External"},
            "calm and composed": {"alias": "calm", "quadrant": "Interpretive-Internal"},
            "overwhelmed or overloaded": {"alias": "overloaded", "quadrant": "Interpretive-Internal"},
            "reflective or introspective": {"alias": "reflective", "quadrant": "Interpretive-Internal"},
            "confused or uncertain": {"alias": "confused", "quadrant": "Interpretive-External"}
        }
    },
    "tonality": {
        "template": "The overall tone of voice is {}.",
        "labels": {
            "assertive and in control": {"alias": "dominant", "quadrant": "Directive-External"},
            "yielding or submissive": {"alias": "submissive", "quadrant": "Interpretive-Internal"},
            "playfully resistant": {"alias": "bratty", "quadrant": "Interpretive-External"},
            "obedient and compliant": {"alias": "obedient", "quadrant": "Directive-Internal"},
            "teasing or provocative": {"alias": "tease", "quadrant": "Interpretive-External"},
            "withholding or denying": {"alias": "denial", "quadrant": "Interpretive-Internal"},
            "pleasurable or soothing": {"alias": "pleasure", "quadrant": "Interpretive-Internal"},
            "harsh or painful": {"alias": "pain", "quadrant": "Interpretive-External"},
            "caring and reassuring": {"alias": "reassuring", "quadrant": "Directive-Internal"}
        }
    }
}
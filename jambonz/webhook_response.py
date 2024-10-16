import json

class WebhookResponse:
    def __init__(self):
        self.verbs = []

    def say(self, text, **kwargs):
        verb = {"verb": "say", "text": text}
        verb.update(kwargs)
        self.verbs.append(verb)
        return self

    def pause(self, length=1):
        self.verbs.append({"verb": "pause", "length": length})
        return self

    def hangup(self):
        self.verbs.append({"verb": "hangup"})
        return self

    def play(self, url, **kwargs):
        verb = {"verb": "play", "url": url}
        verb.update(kwargs)
        self.verbs.append(verb)
        return self

    def gather(self, action_hook, input_types, **kwargs):
        verb = {
            "verb": "gather",
            "actionHook": action_hook,
            "input": input_types
        }
        verb.update(kwargs)
        self.verbs.append(verb)
        return self

    def dial(self, target, **kwargs):
        verb = {"verb": "dial", "target": target}
        verb.update(kwargs)
        self.verbs.append(verb)
        return self

    def redirect(self, action_hook):
        self.verbs.append({"verb": "redirect", "actionHook": action_hook})
        return self

    def leave(self):
        self.verbs.append({"verb": "leave"})
        return self

    def sip_request(self, method, **kwargs):
        verb = {"verb": "sip:request", "method": method}
        verb.update(kwargs)
        self.verbs.append(verb)
        return self

    def to_json(self):
        """Returns the response as JSON, ready to be returned in a HTTP response."""
        return json.dumps(self.verbs)

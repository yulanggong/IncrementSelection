import sublime_plugin

class IncrementSelectionCommand(sublime_plugin.TextCommand):
    digits = '0123456789'
    letters = 'abcdefghijklmnopqrstuvwxyz'
    special = '#'

    def run(self, edit):
        selections = self.view.sel()
        first_selection = self.view.substr(selections[0]).replace(' ', '').split(',')
        start = first_selection[0]
        step = 1

        if len(first_selection) == 1:
            if start != '' and len(selections) > 1:
                second = self.view.substr(selections[1]).replace(' ', '').split(',')[0]
                if start != second:
                    if start[0] in self.digits:
                        step = int(second) - int(start)
                    elif start[0].lower() in self.letters:
                        step = self.letter_decode(second) - self.letter_decode(start)
            if step == 0:
                step = 1
        else:
            step = int(first_selection[1])

        if start == '':
            start = 1
            def gen(counter):
                return str(start + counter)

        elif start[0] in self.digits:
            if start[0] == '0':
                length = len(start)
                start = int(start)
                def gen(counter):
                    result = str(start + counter)
                    while len(result) < length:
                        result = '0' + result
                    return result
            else:
                start = int(start)
                def gen(counter):
                    return str(start + counter)

        elif start[0] in self.letters:
            start = self.letter_decode(start)
            def gen(counter):
                return self.letter_encode(start + counter)

        elif start[0] in self.letters.upper():
            start = self.letter_decode(start)
            def gen(counter):
                return self.letter_encode(start + counter).upper()

        elif start[0] in self.special:
            if start[0] == '#':
                def gen(counter):
                    return str(self.view.rowcol(selection.begin())[0] + 1)

        else:
            return

        counter = 0

        for selection in self.view.sel():
            self.view.insert(edit, selection.begin(), gen(counter))
            counter += step

        for selection in self.view.sel():
            self.view.erase(edit, selection)

    def letter_encode(self, number):
        result = ''

        while number > 0:
            number -= 1
            result = self.letters[number % 26] + result
            number //= 26

        return result

    def letter_decode(self, str):
        result = 0

        for i in str.lower():
            result *= 26
            result += self.letters.index(i) + 1

        return result

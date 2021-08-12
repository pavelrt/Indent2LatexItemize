import sublime
import sublime_plugin


class IndentItemizeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		def count_tabs(s):
			i = 0
			t = 0
			while s[i] == '\t' or s[i] == '•':
				if s[i] == '\t':
					t = t + 1
				i = i + 1
			return (s[i:], t)		
		currentPosition = self.view.sel()[0].begin()
		clipboard = sublime.get_clipboard()
		result = []
		level = 0
		for line in clipboard.splitlines():
			(line_no_tabs, number_of_tabs) = count_tabs(line)
			if level == number_of_tabs:
				if level == 0:
					result.append(line)
				else:
					result.append('\t' * level + '\\item ' + line_no_tabs)
			if level < number_of_tabs:
				level = number_of_tabs
				result.append('\t' * (level - 1) + '\\begin{itemize}')
				result.append('\t' * level + '\\item ' + line_no_tabs)
			elif level > number_of_tabs:
				while level > number_of_tabs:
					result.append('\t' * number_of_tabs + '\\end{itemize}')
					level = level - 1
				result.append('\t' * number_of_tabs + '\\item ' + line_no_tabs)
		while level > 0:
			level = level - 1
			result.append('\t' * level + '\\end{itemize}')

		result_text = '\n'.join(result)


		self.view.insert(edit, currentPosition, result_text)


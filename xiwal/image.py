import re
import subprocess


def extract_colors(path, colors):
	cmd = [
		'convert', path,
		'-resize', '25%',
		'-alpha', 'deactivate',
		'-colors', str(colors),
		'-unique-colors',
		'txt:-'
	]
	output = subprocess.check_output(cmd)
	for line in output.splitlines()[1:]:
		line = line.decode('ascii')
		match = re.search(r'#[0-9A-F]{6}', line)
		yield match.group()

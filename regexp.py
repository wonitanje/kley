import re

regexp = re.compile(r"\s+")

def compile(input: str):
  return regexp.sub('_', input.strip()).lower().replace('«', '').replace('»', '').replace('?', '').replace('"', '').replace('_г)', 'г)').replace('_гр)', 'гр)').replace(' (', '(').replace('г)', '').replace('гр)', '').replace('(', '')


def strip_format(input: str):
  if '.' not in input:
    return None
  idx = input.rindex('.')
  return input[:idx].lower()


def format(input: str):
  if '.' not in input:
    return None
  idx = input.rindex('.')
  return input[idx:].lower()
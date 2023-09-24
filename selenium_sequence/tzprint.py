import textwrap


def tzprint(string, indent=0):
  prefix = "" * indent
  preferredWidth = 100
  wrapper = textwrap.TextWrapper(
    initial_indent=prefix, 
    width=preferredWidth,
    subsequent_indent=' '*indent)
  # message = "LEFTLEFTLEFTLEFTLEFTLEFTLEFT RIGHTRIGHTRIGHT " * 3
  print(wrapper.fill(string))
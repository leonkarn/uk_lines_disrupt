def lines_parser(description):
  lines_list = ["central", "bakerloo", "circle", "district", "hammersmith-city", "jubilee", "metropolitan",
                  "northern",
                  "piccadilly", "victoria", "waterloo and city"]
  newlines = []
  for line in lines_list:
    if line in description.lower():
      newlines.append(line)

  return newlines
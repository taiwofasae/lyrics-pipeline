import os
import csv

def csv_reader(filepath):
  output = []
  with open(filepath,"r") as file:
    reader = csv.reader(file)
    for line in reader:
      output.append(line)

  return output

def read_csv_max_split(filepath):
  output = []
  with open(filepath,"r") as file:
    for line in file:
      output.append([x.lstrip('\"').rstrip('\"') for x in line.rstrip().split('","',4)])

  return output

def read_csv_max_split_folder(folder, func):
  for f in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, f)):
      output = read_csv_max_split(os.path.join(folder, f))
      func(output)


def read_first_N_lines(filepath, cols=4, N=5):
  output = []
  with open(filepath,"r") as file:
    for i in range(N):
      line = next(file)
      output.append(line.rstrip())

  return output
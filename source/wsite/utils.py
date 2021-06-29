

# will split string into first, middle and last
def namesplit(name):
  result = ['', '', '']
  sp_lst = name.split()
  if len(sp_lst) > 0:
    result[0] = sp_lst[0]
  if len(sp_lst) > 1:
    result[2] = sp_lst[-1]
  if len(sp_lst) > 2:
    result[1] = name.split(' ', 1)[1]
    result[1] = result[1].rsplit(' ', 1)[0]
  return result
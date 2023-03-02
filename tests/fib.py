def main(args):
    if 'n' in args:
        n = int(args['n'])
    else:
        n = 20
    num= fib(n)
    print(num)
    return {"body": num}

def fib(n):
  if n < 2:
    return n
  
  return fib(n - 1) + fib(n - 2)
def main(args):
    if 'name' in args:
        name = args['name']
    else:
        name = "stranger"
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"body": greeting}
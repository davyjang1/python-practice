def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                print("%s is running." % func.__name__)
            return func(*args)

        return wrapper
    return decorator

@use_logging(level = "warn")
def foo(name = "foo"):
    def fool1():
        def fool2():
            print("I am %s" % name)

        fool2()
    fool1()


foo()


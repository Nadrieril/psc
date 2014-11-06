# code récupéré sur internet qui permet de forcer le type des arguments
# http://kedeligdata.blogspot.fr/2009/03/type-checking-in-python.html


def decorator_with_args(decorator):
    def new(*args, **kwargs):
        def new2(fn):
            return decorator(fn, *args, **kwargs)
        return new2
    return new


@decorator_with_args
def typecheck(fn, *decorator_args):
    def new(*args):
        if len(decorator_args) != len(args):
            raise Exception('Wrong number of arguments given to\
                             decorator.')
        for x in range(0, len(args)):
            if type(args[x]) != decorator_args[x]:
                raise TypeError('Argument %i is of wrong type.\
                                %s expected, %s received.'
                                (x+1, str(decorator_args[x]),
                                 str(type(args[x]))))
        return fn(*args)
    return new


@typecheck(int, int)
def add(x, y):
    return x+y

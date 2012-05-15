'''
Copied from http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
'''
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QApplication
#TODO: Merge with QApplication-less Singleton decorator
class Singleton(QObject):
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from and the
    type of the singleton instance cannot be checked with `isinstance`. 

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return getattr(QApplication.instance(),self._decorated.__name__)
        except AttributeError:
#            print 'instantiating',self._decorated,'as',self._decorated.__name__
            
            setattr(QApplication.instance(),self._decorated.__name__, self._decorated())
            return getattr(QApplication.instance(),self._decorated.__name__)
            
    def __call__(self):
        """
        Call method that raises an exception in order to prevent creation
        of multiple instances of the singleton. The `Instance` method should
        be used instead.

        """
        raise TypeError(
            'Singletons must be accessed through the `Instance` method.')

if __name__ == '__main__':
    @Singleton
    class Foo:
        def __init__(self):
            print 'Foo created'
    
    f = Foo() # Error, this isn't how you get the instance of a singleton
    f = Foo.Instance() # Good. Being explicit is in line with the Python Zen
    g = Foo.Instance() # Returns already created instance
    print f is g # True

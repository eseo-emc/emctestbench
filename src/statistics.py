
import os
import fnmatch

def Walk(root='.', recurse=True, pattern='*'):
    """
        Generator for walking a directory tree.
        Starts at specified root folder, returning files
        that match our pattern. Optionally will also
        recurse through sub-folders.
    """
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path, name)
        if not recurse:
            break

def LOC(root='', recurse=True):
    """
        Counts lines of code in two ways:
            maximal size (source LOC) with blank lines and comments
            minimal size (logical LOC) stripping same

        Sums all Python files in the specified folder.
        By default recurses through subfolders.
    """
    count_mini, count_maxi = 0, 0
    for fspec in Walk(root, recurse, '*.py'):
        skip = False
        for line in open(fspec).readlines():
            count_maxi += 1
            
            line = line.strip()
            if line:
                if line.startswith('#'):
                    continue
                if line.startswith('"""'):
                    skip = not skip
                    continue
                if not skip:
                    count_mini += 1

    return count_mini, count_maxi

nonBlank,allLines = LOC('.')
print 'Non-blank lines of code:',nonBlank
## http://stackoverflow.com/questions/5764437/python-code-statistics
#
#import collections
#import os
#import ast
#
#def analyze(packagedir):
#    stats = collections.defaultdict(int)
#    for (dirpath, dirnames, filenames) in os.walk(packagedir):
#        for filename in filenames:
#            if not filename.endswith('.py'):
#                continue
#
#            filename = os.path.join(dirpath, filename)
#
#            syntax_tree = ast.parse(open(filename).read(), filename)
#            for node in ast.walk(syntax_tree):
#                stats[type(node)] += 1
#
#
#    return stats
#
#print(analyze('.')[ast.FunctionDef])
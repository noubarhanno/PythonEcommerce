# from .base import *
#
# from .production import *
#
#
# try:
#     from .local import *
# except:
#     pass

try:
    from .local_justin import *
except:
    pass


# we did the import above because wenever we import the settings from base file all the content will be overidden by local and then all the content will be again overidden
# by local_justin and last one will be overidden again by production


# the import above will let you work in local and production each one has it's own settings if you want

# and this is the standard that you should work with all the time

# whenever you did any change in the local or production make sure to update your base based on the current environment you're working with

# we put the try and except block just to see whenever we did mistake inside local it will not import the file and it will pass it

# the order above is important - the production should be high priority
# in the production we should have only one import which is the prouction

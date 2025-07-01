class DotDictLibrary:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
            

# class DotDictLibrary:
#     def __init__(self, dictionary):
#         for key, value in dictionary.items():
#             if isinstance(value, dict):
#                 value = DotDictLibrary(value)
#             setattr(self, key, value)

#     def __getitem__(self, key):
#         return getattr(self, key)
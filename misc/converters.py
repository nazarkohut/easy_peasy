def list_of_ordered_dict_to_list(list_of_ordered_dict: list, field: any) -> list:
    """
    Takes List[OrderDict] and field as a key of these dicts and converts them to list of values
    :parameter list_of_ordered_dict: [OrderedDict([('tag', 'easy')]), OrderedDict([('tag', 'equation')])]
    :parameter field: 'tag'
    :returns: lst: ['easy', 'equation']
    """
    lst = list()
    for dictionary in list_of_ordered_dict:
        lst.append(dictionary[field])
    return lst


def custom_response_with_lists(data: dict, first_level: tuple, second_level: tuple) -> dict:
    """
    Function for reformatting dictionary, it is useful when you have a lot of lists of OrderedDict inside your
    dictionary, and you want to convert them to list of values
    :param data: data you want to reformat: {'strings': [OrderedDict([('string', 'smile')])],
    'numbers': [OrderedDict([('number', 1)]), OrderedDict([('number', 2)])]}
    :param first_level: keys to get list of ordered dictionaries: ('strings', 'numbers')
    :param second_level: keys to get values from list of ordered dictionaries: ('string', 'number')
    :return: data: {'strings': ['smile'], 'numbers': [1, 2]}
    """
    if len(first_level) != len(second_level):
        raise ValueError("Length of first level must be equal to length of the second level!")
    for f, s in zip(first_level, second_level):
        data[f] = list_of_ordered_dict_to_list(data[f], s)
    return data

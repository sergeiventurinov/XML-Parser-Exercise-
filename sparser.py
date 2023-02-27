

class Objecto:

    def __init__(self, name, ident):
        self.id = ident
        self.name = name
        self.txt = ''
        self.attributes = []
        self.content = []
        self.isclosed = False  # For construction purposes only. While is opened objects «fall» inside its hierarchy.

    def __str__(self):
        return self.name


def appender(obj, lista):
    if len(lista) != 0:  # If list is not empty
        if lista[-1].isclosed is False:  # If last element in list is opened
            if len(lista[-1].content) != 0:
                lista[-1].content = appender(obj, lista[-1].content)
            else:
                lista[-1].content.append(obj)
                # print(obj.name, 'appended to list')
        else:
            lista.append(obj)
            # print(obj.name, 'appended to list')
    else:
        lista.append(obj)
        # print(obj.name, 'appended to list')
    return lista


def closer(tag, lista):  # Closes Tag in a List
    lista.reverse()
    if len(lista) != 0:  # If list is not empty
        for n, objeto in enumerate(lista):
            # print('Checking element -', n)
            if lista[n].isclosed is False:  # If last element in list is opened
                if len(lista[n].content) != 0:
                    # print('(still going in)')
                    lista[n].content = closer(tag, lista[n].content)
                if tag == lista[n].name:  # tal vez iterar inversamente buscando esto
                    print('closed tag:', tag)
                    lista[n].isclosed = True
    else:
        print('Empty List')
    lista.reverse()
    return lista


def identifier(lista, ident):  # Checks Name for a determined ID
    id_wanted = ident
    name_wanted = None
    # print('trying to find ID', ident, 'in list')
    lista.reverse()
    if len(lista) != 0:  # If list is not empty
        for n, objeto in enumerate(lista):
            # print('Checking ID -', lista[n].id)
            if lista[n].id != id_wanted:  # If last element in list is opened
                if len(lista[n].content) != 0:
                    # print('(still going in)')
                    name_wanted = identifier(lista[n].content, ident)
            else:
                name_wanted = lista[n].name
                # print(name_wanted, '!')
                return name_wanted
    else:
        print('Tried to search ID in empty list')
    return name_wanted


def attacher(lista, ident, att_type, att_content):
    kind = att_type  # Type of object to be attached (tag text content or attribute)
    value = att_content  # Value of element to be attached
    id_obj = ident  # To which element it belongs

    # Clean value's String from empty spaces and avoid empty strings

    if value == ' ' or value == '' or value == '/':
        print(value, 'is a non-valid value. skipped')
        return lista

    while len(value) > 1:
        if value[0] == ' ':
            if len(value) > 1:
                value = value[1:]
            else:
                print(value, 'is a non-valid value. skipped')
                return lista
        if value[-1] == ' ':
            if len(value) > 1:
                value = value[:-1]
            else:
                print(value, 'is a non-valid value. skipped')
                return lista
        if value[0] != ' ' and value[-1] != ' ':
            break

    # Start iterating from the last elements added

    lista.reverse()

    if len(lista) != 0:  # If list is not empty
        for n, objeto in enumerate(lista):
            if lista[n].id == id_obj:
                if kind == 'att':
                    print('attached succesfully')
                    lista[n].attributes.append(value)
                if kind == 'txt':
                    print('attached succesfully')
                    lista[n].txt = value
            elif lista[n].isclosed is False:  # If last element in list is opened
                if len(lista[n].content) != 0:
                    # print('(still going in)')
                    lista[n].content = attacher(lista[n].content, id_obj, kind, value)
                else:  # Last element added
                    # print(lista[n].id, 'matches', id_obj, '?')
                    if lista[n].id == id_obj:  # If Object matches the identity we are looking for
                        if kind == 'att':
                            print('Attached Attribute', value)
                            lista[n].attributes.append(value)
                        if kind == 'txt':
                            print('Attached Text Content', value)
                            lista[n].txt = value

    else:
        print('Empty List')

    lista.reverse()
    return lista


def sparse(file):

    print('SERGIOs PARSE PARSING LOG')
    print('=========================')
    print('Parsing file:', file)

    capture_tag = False
    capture_att = False
    capture_txt = False
    tag_name = ''
    close_it = False
    content = ''
    attribute = ''
    obj_id = 0
    parse = []  # List of content

    try:
        with open(file) as f:
            for line in f.readlines():
                # print(line)
                # attribute_list = []
                for i, character in enumerate(line):

                    # TAGs
                    if capture_tag is True:
                        tag_name += character
                    if character == '<':
                        capture_tag = True
                        capture_txt = False
                    if character == '>':
                        tag_name = tag_name[:-1]
                        capture_tag = False
                    if capture_tag is True and character == ' ':  # space initiates capturing attributes
                        tag_name = tag_name[:-1]
                        capture_tag = False
                        capture_att = True
                    if capture_tag is False and tag_name != '':
                        if close_it is False:
                            parse = appender(Objecto(tag_name, obj_id), parse)
                            print('opened tag:', tag_name, '( ID', obj_id, ')')
                            obj_id += 1
                            tag_name = ''
                        else:
                            parse = closer(tag_name[1:], parse)
                            close_it = False
                            tag_name = ''
                    if capture_tag is True and character == '/':
                        if line[i + 1] != '>':
                            close_it = True
                        else:
                            parse = closer(tag_name, parse)
                            close_it = False
                            tag_name = ''

                    # TEXT CONTENT
                    if 0 < i < len(line) - 1:
                        if line[i - 1] == '>' or line[i + 1] == '<':
                            if line[i] != '<':
                                capture_txt = True
                    if capture_txt is True:
                        content += character
                    if capture_txt is False:
                        if content != '' and content != ' ':
                            print('attaching txt (', content, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id-1), 'txt', content)
                            content = ''

                    # ATTRIBUTES
                    if capture_att is True:
                        if line[i + 1] == ' ':
                            attribute += character
                            print('attaching (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id-1), 'att', attribute)
                            attribute = ''
                        elif line[i + 1] == '/':
                            attribute += character
                            print('attaching (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id - 1), 'att', attribute)
                            attribute = ''
                            self_closing_tab = identifier(parse, obj_id-1)
                            parse = closer(self_closing_tab, parse)
                            print('closed self-closing tag:', self_closing_tab)
                            capture_att = False
                            capture_tag = False

                        elif line[i + 1] == '>':
                            attribute += character
                            print('attaching att (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id-1), 'att', attribute)
                            attribute = ''
                            capture_att = False
                        else:
                            attribute += character
        return parse
    except FileNotFoundError:
        print('File Not Found')
        return []


parsed_xml = sparse('test.xml')  # el objeto que resulte
print('')
print('END OF CODE')
# StillNotOver


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


def sparse(file):  # Creates standard python objecto for each element, that is a generic object with all XML possible attributes.
    print('SERGIOs PARSE PARSING LOG')
    print('=========================')
    print('\n1. Parsing file:', file)

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
                    if character == '>' and capture_tag is True:
                        tag_name = tag_name[:-1]
                        tag_name = tag_name.title()
                        capture_tag = False
                    if capture_tag is True and character == ' ':  # space initiates capturing attributes
                        tag_name = tag_name[:-1]
                        tag_name = tag_name.title()
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
                            parse = attacher(parse, (obj_id - 1), 'txt', content)
                            content = ''

                    # ATTRIBUTES
                    if capture_att is True:
                        if line[i + 1] == ' ':
                            attribute += character
                            print('attaching (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id - 1), 'att', attribute)
                            attribute = ''
                        elif line[i + 1] == '/':
                            attribute += character
                            print('attaching (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id - 1), 'att', attribute)
                            attribute = ''
                            self_closing_tab = identifier(parse, obj_id - 1)
                            parse = closer(self_closing_tab, parse)
                            print('closed self-closing tag:', self_closing_tab)
                            capture_att = False
                            capture_tag = False

                        elif line[i + 1] == '>':
                            attribute += character
                            print('attaching att (', attribute, ') to ID', obj_id - 1)
                            parse = attacher(parse, (obj_id - 1), 'att', attribute)
                            attribute = ''
                            capture_att = False
                        else:
                            attribute += character
        return parse
    except FileNotFoundError:
        print('File Not Found')
        return []


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


def attacher(lista, ident, att_type, att_content):
    kind = att_type  # Type of object to be attached (tag text content or attribute)
    value = att_content  # Value of element to be attached
    id_obj = ident  # To which element it belongs

    # Clean value's String from empty spaces and avoid empty strings

    if value == ' ' or value == '' or value == '/' or value == '\t':
        print('«', value, '» is a non-valid value. skipped')
        return lista

    while len(value) > 1:
        if value[0] == ' ':
            if len(value) > 1:
                value = value[1:]
            else:
                print('«', value, '» is a non-valid value. skipped')
                return lista
        if value[-1] == ' ':
            if len(value) > 1:
                value = value[:-1]
            else:
                print('«', value, '» is a non-valid value. skipped')
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
                lista.reverse()
                return name_wanted
    else:
        print('Tried to search ID in empty list')
    lista.reverse()
    return name_wanted


def tree_writer(lista):  # Makes a python code with declaration of classes of objects named after the parsed ones, and their instances.
    print('\n2. creating python code from XML...')

    def code_writer(lista2, parseTree):  # Imports Elements parsed and codeline of parse's list.
        instances_declarations = parseTree
        class_list = []
        class_declaration = []

        for elemento in lista2:
            # Regarding Class declaration
            class_declaration.append('class {}:\n'.format(elemento.name))
            class_declaration.append('\tdef __init__(self, *args, txt=""')  # This must be completed after all atts found.
            class_declaration.append('\t\tself.contains = []\n\t\tfor arg in args:\n\t\t\tself.contains.append(arg)\n')
            # Regarding Instance declaration
            instance_declaration = '{}('.format(elemento.name, elemento.id, elemento.name)  # Begin creating the code line containing element's declaration.

            if elemento.content:
                print('going into «', elemento.name, '» hierarchy')
                class_list.extend(code_writer(elemento.content, instances_declarations)[0])
                instance_declaration = code_writer(elemento.content, instance_declaration)[1]  # Code Pending, contains = (list)
                print('gone out of «', elemento.name, '» hierarchy')

            if elemento.txt != '':
                # Regarding Class declaration
                class_declaration.append('\t\tself.txt = txt\n')
                # Regarding Instance declaration
                instance_declaration += ('txt="' + elemento.txt + '"')
            for attribute in elemento.attributes:
                # Regarding Class declaration
                class_attribute = (attribute.split('='))[0]
                class_declaration[1] += ', {}=None'.format(class_attribute)
                class_declaration.append('\t\tself.{} = {}\n'.format(class_attribute, class_attribute))
                # Regarding Instance declaration
                if instance_declaration[-1] == '(':  # If First attribute.
                    instance_declaration += attribute.split('=')[0] + '=' + attribute.split('=')[1]
                else:
                    instance_declaration += ', ' + attribute.split('=')[0] + '=' + attribute.split('=')[1]

            # Closes this instance's declaration
            class_declaration[1] += '):\n'
            instance_declaration += ')'
            print('declaration added: ', instance_declaration)
            if len(instances_declarations) == 0:   # If First element
                instances_declarations += instance_declaration
            else:
                if instances_declarations[-1] == '(':
                    instances_declarations = instances_declarations + instance_declaration
                else:
                    instances_declarations = instances_declarations + ', ' + instance_declaration
            # print(instances_declarations)
            class_declaration.append('\n\n')
            class_list.append(class_declaration)
            class_declaration = []
            instance_declaration = []

        return class_list, instances_declarations

    def class_synth(lista3):  # This function compares two elements' attributes and returns one merging both.
        print('\n3.looking for element duplicates')
        for i, clase in enumerate(lista3):
            for i_match, clase_match in enumerate(lista3):
                if clase[0] == clase_match[0] and i != i_match:
                    print('duplicate found for ID', i, 'in ID', i_match)
                    print('merging...')
                    for i2 in range(len(clase_match)):
                        if clase_match[i2] not in clase:
                            if i2 != 1:
                                print(clase_match[i2], 'attribute not in first element')
                                clase.insert(i2 + 1, clase_match[i2])
                            else:
                                print('Modifying Class Arguments')
                                # Code Pending

                    del lista3[i_match]
        return lista3

    # Frist create Class & their instance's declarations
    instances_declarations_codeline = ''
    class_declarations_codelines, instances_declarations_codeline = code_writer(lista, instances_declarations_codeline)
    instances_declarations_codeline = 'sparserTree = [' + instances_declarations_codeline + ']'  # Close Tree's list

    # Now merge class repetitions and their differences.
    class_synth(class_declarations_codelines)

    tree_code_file = open("temporary_code.py", "w")
    for declaration in class_declarations_codelines:
        for line in declaration:
            tree_code_file.write(line)
    tree_code_file.write(instances_declarations_codeline)
    tree_code_file.close()


parsed_xml = sparse('test.xml')
tree_writer(parsed_xml)  # darle a tree writer tambien un nombre de archivo.
print('')
print('END OF CODE')

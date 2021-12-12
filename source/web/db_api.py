# def make_format(value):
#     return f'value is {value}'

# def make_format_2(value):
#     return 'value is {}'.format(value) 

# a = make_format(1)
# b = make_format_2(2)


from typing import Pattern


def make_db_command(mode, *args, **kwargs):
    
    # mode: insert_p insert_c vote search_style search_style_file  
    def insert_Database(pattern, file_id):
        InsertData = '''
            INSERT INTO pattern (pattern,file_id)
            VALUES({},{})
        '''.format(pattern,file_id)
        return InsertData
    
    def insert_Compare(compare):
        InsertCompare = '''
            INSERT INTO compare (fake)
            VALUES({})
        '''.format(compare)
        return InsertCompare

    def voteRealCounter(compare_id):
        counter = '''
            UPDATE compare
            SET real_counter = real_counter + 1
            WHERE id = ({})
        '''.format(compare_id)
        return counter

    def voteFakeCounter(compare_id):
        counter = '''
            UPDATE compare
            SET fake_counter = fake_counter + 1
            WHERE id = ({})
        '''.format(compare_id)
        return counter

    def search_style(composer):
        cmd = '''
            SELECT * 
            FROM pattern JOIN Music ON pattern.file_id = Music.id
            WHERE Music.style = {}
        '''
        return cmd.format(composer)

    def search_style_file(composer):
        cmd2 = '''
            SELECT *
            FROM Compare JOIN Pattern ON Compare.pattern = Pattern.id JOIN Music ON Pattern.pattern = Music.id 
            WHERE Music.style = {}
        '''#語句修正
        return cmd2.format(composer)
    
    if mode == 'insert_p':
        sql = insert_Database(kwargs['pattern'],kwargs['file_id'])
    elif mode == 'insert_c':
        sql = insert_Compare(kwargs['compare'])
    elif mode == 'voteR':
        sql = voteRealCounter(kwargs['compare_id'])
    elif mode == 'voteF':
        sql = voteFakeCounter(kwargs['compare_id'])
    elif mode == 'search_style':
        sql = search_style(kwargs['composer'])
    elif mode == 'search_style_file':
        sql = search_style_file(kwargs['composer'])
    
    return sql

    # if mode == 'pattern':
    #     style = kwargs['style']
    #     return search_style(style)

    #if 'style' in kwargs:
    #    return search_style()

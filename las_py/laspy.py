import re
from types import SimpleNamespace


class Laspy:
    def __init__(self, file):
        self.__file = self.__initialize(file)
        self.__secret = LasContent(self.__file)
        self.other = self.__secret.other_sect
        self.data = self.__get_data()
        self.data_stripped = self.__get_cleaned_data()
        self.header = self.__header()
        self.header_and_descr = self.__hd_and_descr()
        self.well = read_param(self.__secret.well_sect)
        self.curve = read_param(self.__secret.curve_sect)
        self.param = read_param(self.__secret.param_sect)
        self.row_count = len(self.__get_data())
        self.column_count = len(self.__get_data()[0])
        self.version, self.wrap, *self.other_infos = self.__get_version()

    def __str__(self):
        if(len(self.header) > 0):
            return 'Valid'
        else:
            return 'Invalid'

    def __repr__(self):
        if(len(self.header) > 0):
            return {'Valid': True}
        else:
            return {'Valid': False}

    def __initialize(self, f):
        with open(f, 'r') as f:
            result = f.read()
        f.closed
        return result

    def __header(self):
        text = self.__secret.curve_sect.split('\n')
        return [re.split(r'\s+|[.]', u.strip())[0] for u in text]

    def __hd_and_descr(self):
        def get_descr(substr):
            if re.match(r'\d', substr) == None:
                return substr
            else:
                return re.split(r'\d', substr)[1].strip()
        text = self.__secret.curve_sect.split('\n')
        hd = [re.split(r'\s+|[.]', u.strip())[0] for u in text]
        descr = [u.split(':')[1].strip() for u in text]
        new_descr = [get_descr(x) for x in descr]
        res = {s_hd: s_des for (s_hd, s_des) in zip(hd, new_descr)}
        return res

    def __get_data(self):
        text = self.__secret.data_sect.strip()
        text_list = re.split(r'\s+', text)
        chunked = [_convert_to_value(x) for x in text_list]
        return list(Laspy.__chunks(chunked, len(self.__header())))

    def __get_cleaned_data(self):
        data = self.__get_data()
        null_value = read_param(self.__secret.well_sect).NULL.value
        filtered = filter(lambda x: null_value not in x, data)
        return list(filtered)


    @staticmethod
    def __chunks(l, n):
        pass
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def column(self, str):
        obj = {}
        try:
            for index, val in enumerate(self.header):
                obj[val] = [x[index] for x in self.data]
            return obj[str]
        except KeyError:
            return 'Column with title {} doesn\'t exist'.format(str)

    def column_stripped(self, str):
        obj = {}
        try:
            for index, val in enumerate(self.header):
                obj[val] = [x[index] for x in self.data_stripped]
            return obj[str]
        except KeyError:
            return 'Column with title {} doesn\'t exist'.format(str)

    def __get_version(self):
        text = self.__secret.version_sect.strip().split('\n')

        def split_it(te):
            return re.split(r'\s+', te, maxsplit=1)[1].split(':')[0].strip()
        return [split_it(x) for x in text]

    def __get_other(self):
        return self.__secret.other_sect

    def to_csv(self, file_name):
        header = ','.join(self.__header()) + '\n'
        data = [','.join([str(y) for y in x])+'\n' for x in self.__get_data()]
        with open(file_name+'.csv', mode='a', encoding='utf-8') as f:
            f.write(header + ''.join(data))
        f.close()
        return '{}.csv has been created Successfully!'.format(file_name)

    def to_csv_stripped(self, file_name):
        header = ','.join(self.__header()) + '\n'
        data = [','.join([str(y) for y in x]) +
                '\n' for x in self.__get_cleaned_data()]
        with open(file_name+'.csv', mode='a', encoding='utf-8') as f:
            f.write(header + ''.join(data))
        f.close()
        return '{}.csv has been created Successfully!'.format(file_name)


class LasContent:
    def __init__(self, str):
        self.__str = str
        self.well_sect = self.__get_part('W')
        self.curve_sect = self.__get_part('C')
        self.data_sect = self.__get_data_sect()
        self.param_sect = self.__get_part('P')
        self.other_sect = self.__get_part('O')
        self.version_sect = self.__get_part('V')

    def __get_data_sect(self):
        return re.split(self.__pattern('A'), self.__str)[1]

    def __get_part(self, letter):
        try:
            text = re.split(self.__pattern(letter), self.__str)[1]
            return LasContent.__remove_comment(text.split('~')[0])
        except IndexError:
            return False


    @staticmethod
    def __remove_comment(str):
        pass
        arr = str.strip().split('\n')
        mapped_array = list(filter(lambda val: not val.startswith('#'), arr))
        return '\n'.join(mapped_array)

    def __pattern(self, letter):
        return re.compile(f'~{letter!s}(?:\\w*\\s*)*\n', flags=re.IGNORECASE)


class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


def _convert_to_value(s):
    try:
        value = int(s)
    except ValueError:
        try:
            value = float(s)
        except ValueError:
            value = s
    return value


def read_param(str_blob):
    val = str_blob.splitlines()
    con = {}
    for i in range(len(val)):
        items = from_line(val[i])
        item_key = list(items.keys())[0]
        item_values = list(items.values())[0]
        con[item_key] = item_values
    return NestedNamespace(con)


def from_line(res):
    obj = {}
    first, descr = res.rsplit(':', 1)
    descr = descr.strip()
    name, mid = first.split('.', 1)
    name = name.strip()

    if mid.startswith(' '):
        units = ''
        data = mid
    else:
        units_data = mid.split(None, 1)
        if len(units_data) == 1:
            units = units_data[0]
            data = ''
        else:
            units, data = units_data

    obj[name] = {'units': units, 'value': _convert_to_value(
        data.strip()), 'descr': descr.strip()}
    return obj


class List(list):
    def flatten(self):
        lst = List()

        def _flatten(cur_list):
            is_list = lambda i : isinstance(i, [List, list])
            lsts = [l for l in items if is_list is True]
            not_lsts = [l for l in items if is_list is False]
            
            lst.extend(not_lsts)

            for l in lsts:
                _flatten(l)
        
        items = self.__items__
        _flatten(items)

        return lst

ListTypes = (list, List)

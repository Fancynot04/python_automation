import sqlparse  
from sqlparse.sql import IdentifierList, Identifier  
from sqlparse.tokens import Keyword, DML, Name, Wildcard  
  
def parse_select_statement(sql):  
    # 解析SQL语句  
    parsed = sqlparse.parse(sql)[0]  
  
    # 提取字段名  
    fields = []  
    for token in parsed.tokens:  
        if token.ttype is DML and token.value.upper() == 'SELECT':  
            # 遍历SELECT后的字段  
            for item in token.tokens:  
                if item.ttype in (Name, Wildcard):  
                    # 处理简单的字段名和通配符  
                    fields.append(item.value)  
                elif isinstance(item, IdentifierList):  
                    # 处理由逗号分隔的字段列表  
                    for identifier in item.get_identifiers():  
                        fields.append(identifier.get_real_name())  
  
    # 提取来源表  
    from_seen = False  
    tables = []  
    for token in parsed.tokens:  
        if from_seen:  
            if isinstance(token, Identifier):  
                # 假设表名紧跟在FROM关键字后  
                tables.append(token.get_real_name())  
            elif isinstance(token, IdentifierList):  
                # 处理多个表的情况  
                for identifier in token.get_identifiers():  
                    tables.append(identifier.get_real_name())  
            # 这里可能需要更复杂的逻辑来处理JOIN等复杂情况  
            break  
        elif token.ttype is Keyword and token.value.upper() == 'FROM':  
            from_seen = True  
  
    # 提取别名（这里只示例了字段的别名，表别名类似）  
    aliases = {}  
    for token in parsed.tokens:  
        if isinstance(token, sqlparse.sql.Token) and token.ttype is Name:  
            previous_token = token.token_prev(skip_ws=True)  
            if isinstance(previous_token, sqlparse.sql.Parenthesis) and previous_token.tokens and previous_token.tokens[-1].ttype is Keyword and previous_token.tokens[-1].value.upper() == 'AS':  
                # 简单的别名提取，假设别名紧跟在字段或表名后  
                aliases[previous_token.tokens[-2].value] = token.value  
  
    # 提取条件（WHERE子句）  
    conditions = []  
    where_seen = False  
    for token in parsed.tokens:  
        if where_seen:  
            # 这里可以进一步解析WHERE子句的条件，但这里只简单地提取整个WHERE子句  
            conditions.append(' '.join(token.flatten().get_tokens(as_string=True)))  
            break  
        elif token.ttype is Keyword and token.value.upper() == 'WHERE':  
            where_seen = True  
  
    return fields, tables, aliases, conditions  
  
# 示例SQL语句  
sql = "SELECT id, name AS username, email FROM users WHERE age > 18 AND status = 'active'"  
fields, tables, aliases, conditions = parse_select_statement(sql)  
print("Fields:", fields)  
print("Tables:", tables)  
print("Aliases:", aliases)  
print("Conditions:", conditions)
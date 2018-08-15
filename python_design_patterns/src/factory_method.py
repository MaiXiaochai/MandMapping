# --coding: utf-8 -*-

import xml.etree.ElementTree as tree
import json

"""
这里用抽象工厂方法，解决对XML和json文件的解析。
注意编程中的代码组织方式和思想。
"""

class JsonConnector:
    """解析json文件"""
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    @property
    def parsed_data(self):
        return self.data

    
class XmlConnector:
    """解析XML文件"""
    def __init__(self, filepath):
        self.tree = tree.parse(filepath)
        
    @property
    def parsed_data(self):
        return self.tree
    

def connection_factory(filepath):
    """一个工厂方法，基于输入文件的扩展名返回一个JsonConnector或XmlConnector的实例"""
    if filepath.endwith('json'):
        connector = JsonConnector
    
    elif filepath.endwith('xml'):
        connector = XmlConnector

    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector
    

def connect_to(filepath):
    """该函数对connection_factory()进行包装，添加了异常处理。"""
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    
    # 根据effective python中的建议，这里最好不要返回None，
    # 最好返回一个二元元组，第一个元素表示是否成功得到connector，第二元素表示connector，
    # 若True，第二个是connector实例，若False，第二个元素为空
    return factory


def main():
    """演示如何使用工厂方法"""
    sqlite_factory = connect_to('data/person.sq3')
    

if __name__ == '__main__':
    pass
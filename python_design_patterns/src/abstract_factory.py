# -*-coding: utf-8 -*-

"""
简单分级游戏，演示抽象工厂的使用
游戏一: 青蛙遇到障碍物虫子，吃掉它。
"""

class Frog:
    """
    Frog 英 /frɒg/ 青蛙
    encounter 英 /ɪn'kaʊntə; en-/ 遭遇，邂逅，遇到
    """
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
    
    def interact_with(self, obstacle):
        print('{} the Frog encounters {} and {}!'.format(self, obstacle, obstacle.action()))
    

class Bug:
    def __str__(self):
        return 'a bug'
    
    def action(self):
        return 'eat it'
    

class FrogWorld:
    """
    该类是一个抽象工厂。
    主要职责是创建游戏的主人公和障碍物，
    区分创建方法并使其（创建方法的）名字通用（比如，make_character()和make_obstacle()），
    这让我们可以动态地改变当前激活的工厂（也因此改变了当前激活的游戏），而无需进行任何代码更改。
    """
    def __init__(self, name):
        self.player_name = name
        print(self)
    
    def __str__(self):
        return '\n\n\t------ Frog World ------'
    
    def make_character(self):
        return Frog(self.player_name)
    
    def make_obstacle(self):
        return Bug()

    
"""
游戏二: WizardWorld
男巫遇到兽人，杀死它。
"""
    

class Wizard:
    def __init__(self, name):
        self.name = name
        print(self)
    
    def __str__(self):
        return self.name

    def intercat_with(self, obstacle):
        print('{} the Wizard encounters {} and {}!'.format(self, obstacle, obstacle.action()))


class Ork:
    def __str__(self):
        return 'an evil ork'
    
    def action(self):
        return 'kills it'


class WizardWorld:
    def __init__(self, name):
        self.player_name = name
        print(self)
        
    def __str__(self):
        return '\n\n\t ------ Wizard World ------'
    
    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()


class GameEvn:
    """
    游戏主入口，接受factory作为输入，用其创建游戏的世界。
    方法play()则会启动hero和obstacle之间的交互。
    """
    
    def __init__(self, factory):
        self.hero = factory.make_charcater()
        self.obstacle = factory.make_obstacle()
    
    def play(self):
        self.hero.interact_with(self.obstacle)

        
def validate_age(name):
    """
    validate 英 /'vælɪdeɪt/ 验证
    提示用户输入一个有效的年龄,若年龄无效，返回一个元组，第一个元素为False；
    若年龄没问题，第一个元素为True，第二个元素为用户年龄。
    """
    
    try:
        age = input('Welcome {}. How old are you?'.format(name))
        age = int(age)
    except ValueError as err:
        print('Age {} is invalid, please try again ...'.format(age))
        return (False, age)
    return (True, age)


def main():
    """
    询问用户的姓名和年龄，并根据年龄确定该玩哪个游戏。
    """
    name = input("Hello, What's your name? ")
    valid_input = False
    while not valid_input:
        valid_input, age = validate_age(name)
    game = FrogWorld if age < 18 else WizardWorld
    env = GameEvn(game(name))
    env.play()


if __name__ == '__main__':
    main()
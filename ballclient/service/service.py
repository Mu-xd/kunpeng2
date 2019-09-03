# encoding:utf8
'''
业务方法模块，需要选手实现
选手也可以另外创造模块，在本模块定义的方法中填入调用逻辑。这由选手决定
所有方法的参数均已经被解析成json，直接使用即可
所有方法的返回值为dict对象。客户端会在dict前面增加字符个数。
1、防守时按照方向和距离远离进攻方
2、防守时候能左右走就不上下走
3、远离传送阵的出口
'''
import copy
import json

import ballclient.service.constants as constants
import random
#防守模式
def Defense1(map, player):
    x = int(player['x'])
    y = int(player['y'])
    d_x = []
    d_y = []
    r_x = 0
    r_y = 0
    d = []
    res = ""
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    #读取地图分析位置
    for i in range(height):
        for j in range(width):
            if map[i][j][0] == '-':
                d_y.append(i)
                d_x.append(j)
    # 如果视野内没有敌人 看看附近有没有分数
    if len(d_x) == 0:
        return Defense1_Attack(map, player, [])
    d = []
    #计算与敌人的距离
    for i in range(len(d_x)):
        d.append(pow((pow((d_x[i] - x), 2)) + pow(d_y[i] - y, 2), 0.5))
    #按照权重去寻找方向
    for i in range(len(d)):
        if d[i] == 1:
            r_x += (d_x[i] - x) * 0.9
            r_y += (d_y[i] - y) * 0.9
        elif 2 > d[i] > 1:
            r_x += (d_x[i] - x) * 0.09
            r_y += (d_y[i] - y) * 0.09
        elif d[i] == 2:
            r_x += (d_x[i] - x) * 0.009
            r_y += (d_y[i] - y) * 0.009
        elif 3 > d[i] > 2:
            r_x += (d_x[i] - x) * 0.0009
            r_y += (d_y[i] - y) * 0.0009
        elif d[i] == 3:
            r_x += (d_x[i] - x) * 0.00009
            r_y += (d_y[i] - y) * 0.00009
        elif 4 > d[i] > 3:
            r_x += (d_x[i] - x) * 0.00001
            r_y += (d_y[i] - y) * 0.00001
    # 离得很远#或者两个方向的相同抵消了
    if r_x == 0 and r_y == 0:
        # 认为在左右两侧
        if x > 0 and map[y][x - 1][0] != '-':
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                return 'up'
            else:
                return 'down'
        elif x < (width - 1) and map[y][x + 1][0] != '-':
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V' :
                return 'up'
            else:
                return 'down'
        # 认为在上下两侧
        elif y > 0 and map[y - 1][x][0] != '-':
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-'and map[y][x - 1] != '>':
                return 'left'
            else:
                return 'right'
        elif y < height -1 and map[y + 1][x][0] != '-':
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                return 'left'
            else:
                return 'right'
        return Defense1_Attack(map, player)
    # 这个敌人在下面
    elif r_x == 0 and r_y > 0:
        if y > 1 and map[y - 2][x][0] != '-':
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'down'
        else:#在下面稍远的位置或者上面稍远的位置有一个对其影响了
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0  and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'up'
    # 这个敌人在上面
    elif r_x == 0 and r_y < 0:
        # 下面两个都不是敌人
        if y < height - 2 and map[y + 2][x][0] != '-':
            if y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'up'
        else:
            if width - 1 > x and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            else:
                res = 'down'
    elif r_x > 0 and r_y == 0:#这个敌人在右面
        if x > 1 and map[y][x - 2][0] != '-':
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = 'left'
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'right'
        else:
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'left'
    elif r_x < 0 and r_y == 0:#这个敌人在左面
        if x < width - 2 and map[y][x + 2][0] != '-':
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = 'right'
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'left'
        else:
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = 'up'
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                res = "down"
            else:
                res = 'right'
    else:
        O = r_y / r_x
        if (O > 1 or O < -1) and r_y > 0:        #方向向下
            if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                res = "up"
            else:
                if O > 0:
                    if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    else:
                        res = 'down'
                else:
                    if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    else:
                        res = 'down'
        elif (O > 1 or O < -1) and r_y < 0:      #方向向上
            if y < height - 1 and map[y + 1][x] != 'x'and map[y + 1][x][0] != '-'and map[y + 1][x] != '^':
                res = "down"
            else:
                if O < 0:
                    if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    else:
                        res = 'up'
                else:
                    if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                        res = 'right'
                    elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                        res = 'left'
                    else:
                        res = 'up'
        elif -1 < O < 1 and r_x > 0:            #方向向右
            if x > 0 and x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':
                res = "left"
            else:
                if O > 0:
                    if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    elif y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    else:
                        res = 'right'
                else:
                    if y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    else:
                        res = 'right'
        elif -1 < O < 1 and r_x < 0:            #方向向左
            if x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = "right"
            else:
                if O > 0:
                    if y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    else:
                        res = 'left'
                else:
                    if y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':
                        res = 'up'
                    elif y < height -1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':
                        res = 'down'
                    else:
                        res = 'left'
        elif O == -1 and r_x > 0:               #判断两个方向走都可以的情况 右下
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':#左侧没有石头并且油路
                res = "left"
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':  # 上侧没有石头并且有路
                res = "up"
            elif x < width - 1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':
                res = "right"
            else:
                res = "down"
        elif O == 1 and r_x < 0 :               #判断两个方向走都可以的情况 左上
            if x < width -1 and map[y][x + 1] != 'x' and map[y][x + 1][0] != '-' and map[y][x + 1] != '<':#右侧没有石头并且油路
                res = "right"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x]!= '^':    #下侧没有石头并且有路
                res = "down"
            elif x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':  # 左侧没有石头并且油路
                res = "left"
            else:
                res = "up"
        elif O == -1 and r_x < 0:               #判断两个方向走都可以的情况 左下
            if x < width -1 and map[y][x +1] != 'x' and map[y][x +1][0] != '-' and map[y][x +1] != '<':#右侧没有石头并且油路
                res = "right"
            elif y > 0 and map[y - 1][x] != 'x' and map[y - 1][x][0] != '-' and map[y - 1][x] != 'V':    #上侧没有石头并且有路
                res = "up"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x]!= '^':    #下侧没有石头并且有路
                res = "down"
            else:
                res = "left"
        elif O == 1 and r_x < 0:               #判断两个方向走都可以的情况 右上
            if x > 0 and map[y][x - 1] != 'x' and map[y][x - 1][0] != '-' and map[y][x - 1] != '>':#左侧没有石头并且油路
                res = "left"
            elif y < height - 1 and map[y + 1][x] != 'x' and map[y + 1][x][0] != '-' and map[y + 1][x] != '^':  # 下侧没有石头并且有路
                res = "down"
            else:
                res = "up"
    return res
def Defense1_Attack(map, player,zj = []):
    x = int(player['x'])
    y = int(player['y'])
    d_x = []
    d_y = []
    r_x = 0
    r_y = 0
    s = []
    d = []
    res = ""
    direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
    for i in range(height):  # 读取基础地图
        for j in range(width):
            try:
                if map[i][j][0] == '-' or map[i][j][0] == 'p':#有敌人和分
                    s.append(int(map[i][j][1:]))
                    d_y.append(i)
                    d_x.append(j)
            except ValueError:
                continue
    if(len(d_x) == 0): #敌人和分数都没有
        if x < 2:
            if map[y][x + 1] != 'x' and map[y][x + 1] != '<' and (str(x + 1) + '_' + str(y)) not in zj:
                return "right"
        if x > width - 3:
            if map[y][x -1] != 'x' and map[y][x -1] != '>'and (str(x - 1) + '_' + str(y)) not in zj:
                return "left"
        if y < 2:
            if map[y + 1][x] != 'x' and map[y + 1][x] != '^' and (str(x) + '_' + str(y + 1)) not in zj:
                return "down"
        if y > height - 3:
            if map[y - 1][x] != 'x' and map[y - 1][x] != 'V' and (str(x) + '_' + str(y - 1)) not in zj:
                return 'up'
        return direction[random.randint(1, 4)] #随机走
    else:   #地图上有敌人或分数
        d = []
        # 计算与敌人的距离
        for i in range(len(d_x)):
            d.append(pow((pow((d_x[i] - x), 2)) + pow(d_y[i] - y, 2), 0.5))
        # 这里配置权重
        for i in range(len(d)):
            if d[i] == 1:
                r_x += (d_x[i] - x) * 0.9 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.9 * pow(10, s[i])
            elif 2 > d[i] > 1:
                r_x += (d_x[i] - x) * 0.09 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.09 * pow(10, s[i])
            elif d[i] == 2:
                r_x += (d_x[i] - x) * 0.009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.009 * pow(10, s[i])
            elif 3 > d[i] > 2:
                r_x += (d_x[i] - x) * 0.0009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.0009 * pow(10, s[i])
            elif d[i] == 3:
                r_x += (d_x[i] - x) * 0.00009 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.00009 * pow(10, s[i])
            elif 4 > d[i] > 3:
                r_x += (d_x[i] - x) * 0.00001 * pow(10, s[i])
                r_y += (d_y[i] - y) * 0.00001 * pow(10, s[i])
        # 离得很远#或者两个方向的相同抵消了
        if r_x == 0 and r_y == 0:
            try:
                if x > 0:
                    a1 = int(map[y][x - 1][1:])
            except ValueError:
                a1 = 0
            try:
                if x < width - 1:
                    a2 = int(map[y][x + 1][1:])
            except ValueError:
                a2 = 0
            try:
                if y > 0:
                    a3 = int(map[y - 1][x][1:])
            except ValueError:
                a3 = 0
            try:
                if y< height - 1:
                    a4 = int(map[y + 1][x][1:])
            except ValueError:
                a4 = 0
            # 认为在左右两侧
            if x > 0 and (0 < a1) and (str(x - 1) + '_' + str(y)) not in zj:
                return 'left'
            elif x < (width - 1) and (a2 > 0) and (str(x + 1) + '_' + str(y)) not in zj:
                return 'right'
            # 认为在上下两侧
            elif y > 0 and (a3 > 0) and (str(x) + '_' + str(y - 1)) not in zj:
                return 'up'
            # 认为在上下两侧
            elif y < height - 1 and (a4 > 0) and (str(x) + '_' + str(y + 1)) not in zj:
                return 'down'
            # 分/敌人离得很远
            else:
                if x < 2:
                    if map[y][x + 1] != 'x' and map[y][x + 1] != '<' and (str(x + 1) + '_' + str(y)) not in zj:
                        return "right"
                if x > width - 2:
                    if map[y][x - 1] != 'x' and map[y][x - 1] != '>' and (str(x - 1) + '_' + str(y)) not in zj:
                        return "left"
                if y < 2:
                    if map[y + 1][x] != 'x' and map[y + 1][x] != '^' and (str(x) + '_' + str(y + 1)) not in zj:
                        return "down"
                if y > height - 2:
                    if map[y - 1][x] != 'x' and map[y - 1][x] != 'V' and (str(x) + '_' + str(y - 1)) not in zj:
                        return 'up'
            return direction[random.randint(1, 4)]  # 随机走
        # 这个分数在下面
        elif r_x == 0 and r_y > 0:
            if y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y - 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                res = "down"
            elif x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            else:
                res = 'up'
        # 这个分在上面
        elif r_x == 0 and r_y < 0:
            if y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            elif x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            else:
                res = 'left'
        # 这个分在右面
        elif r_x > 0 and r_y == 0:
            if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                res = 'right'
            elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            else:
                res = 'down'
        # 这个敌人在左面
        elif r_x < 0 and r_y == 0:
            if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                res = 'left'
            elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                res = 'up'
            else:
                res = 'down'
        else:
            O = r_y / r_x
            # 方向向下
            if (O > 1 or O < -1) and r_y > 0:
                if y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                    res = "down"
                else:
                    if O < 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                        res = 'left'
                    else:
                        res = 'right'
            # 方向向上
            elif (O > 1 or O < -1) and r_y < 0:
                if y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                    res = "up"
                else:
                    if O > 0 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                        res = 'right'
                    else:
                        res = 'left'
            # 方向向右
            elif -1 < O < 1 and r_x > 0:
                if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:
                    res = "right"
                else:
                    if O > 0 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:
                        res = 'down'
                    else:
                        res = 'up'
            # 方向向左
            elif -1 < O < 1 and r_x < 0:
                if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:
                    res = "left"
                else:
                    if O > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:
                        res = 'up'
                    else:
                        res = 'down'
            # 判断两个方向走都可以的情况 右上
            elif O == -1 and r_x > 0:
                if x < width -1 and (map[y][x +1] != 'x' and map[y][x +1] != '+' and map[y][x +1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:#右侧没有石头并且油路
                    res = "right"
                elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:    #上侧没有石头并且有路
                    res = "up"
                else:
                    res = "left"
            # 判断两个方向走都可以的情况 左上
            elif O == 1 and r_x < 0 :
                if x > 0 and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '>') and (str(x - 1) + '_' + str(y)) not in zj:#左侧没有石头并且油路
                    res = "left"
                elif y > 0 and (map[y - 1][x] != 'x' and map[y - 1][x] != '+' and map[y - 1][x] != 'V') and (str(x) + '_' + str(y - 1)) not in zj:  # 上侧没有石头并且有路
                    res = "up"
                else:
                    res = "down"
            # 判断两个方向走都可以的情况 左下
            elif O == -1 and r_x < 0:
                if x > 0  and (map[y][x - 1] != 'x' and map[y][x - 1] != '+' and map[y][x - 1] != '<') and (str(x - 1) + '_' + str(y)) not in zj:#zuo侧没有石头并且油路
                    res = "left"
                elif y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:  # 下侧没有石头并且有路
                    res = "down"
                else:
                    res = "right"
            # 判断两个方向走都可以的情况 右xia
            elif O == 1 and r_x > 0:
                if x < width - 1 and (map[y][x + 1] != 'x' and map[y][x + 1] != '+' and map[y][x + 1] != '<') and (str(x + 1) + '_' + str(y)) not in zj:#右侧没有石头并且油路
                    res = "right"
                elif y < height - 1 and (map[y + 1][x] != 'x' and map[y + 1][x] != '+' and map[y + 1][x] != '^') and (str(x) + '_' + str(y + 1)) not in zj:    #下侧没有石头并且有路
                    res = "down"
                else:
                    res = "up"
    return res
#计算最短路径
def Dijkstra_all_minpath(start, end,matrix):
    length = len(matrix)  # 该图的节点数
    path_array = []
    temp_array = []
    path_array.extend(matrix[start])  # 深复制
    temp_array.extend(matrix[start])  # 深复制
    temp_array[start] = 100000  # 临时数组会把处理过的节点的值变成inf，表示不是最小权值的节点了
    already_traversal = [start]  # start已处理
    path_parent = [start] * length  # 用于画路径，记录此路径中该节点的父节点
    num = 1
    while (1 == 1):
        num += 1
        i = temp_array.index(min(temp_array))  # 找最小权值的节点的坐标
        temp_array[i] = 100000
        path = []  # 用于画路径
        path.append(str(i))
        k = i
        while (path_parent[k] != start):  # 找该节点的父节点添加到path，直到父节点是start
            path.append(str(path_parent[k]))
            k = path_parent[k]
        path.append(str(start))
        if i in end:
            path.reverse()  # path反序产生路径
            return path[1], i
        if num == 80:
            path.reverse()  # path反序产生路径
            return path[1],0
        already_traversal.append(i)  # 该索引已经处理了
        for j in range(length):  # 这个不用多说了吧
            if j not in already_traversal:
                if (path_array[i] + matrix[i][j]) < path_array[j]:
                    path_array[j] = temp_array[j] = path_array[i] + matrix[i][j]
                    path_parent[j] = i  # 说明父节点是i
#进攻模式
def Attack(map, players,round_id):
    '''
    #1、如果当前地图上的敌人身上的分数大于某一数值，实现视图中所有机器人向分数目前视野中分数最高的人的方向移动
    #2、如果当前地图上的敌人身上的分数小于某一数值，吃掉地图中的分和附近的敌人
    #   如果当前视野没有分数，去找历史视野中分数
    #   有分数就安排最近的去吃分数
    #3、自己人和敌人的位置不能重合，每个回合按照自己的人的顺序进行安排部署，后面的服从前面的
    #
    '''
    #输出返回的结果
    res = {}
    #算法部分
    #查找地图找出 当前分数最高的人或者分数的位置
    garde = garde_x = garde_y = 0
    for i in range(height):
        for j in range(width):
            # 是敌人或者分数
            if map[i][j][0] == '-' or map[i][j][0] == 'p':
                if garde < int(map[i][j][1:]):#更新最高分和最高分的位置
                    garde = int(map[i][j][1:]) + (0 if(map[i][j][0] != '-') else 10)
                    garde_y = i
                    garde_x = j
    # 把相邻矩阵拿出来复制一遍
    Dijkstra_map_l = copy.deepcopy(Dijkstra_map)
    #找到了带有分的敌人 值得吃的
    if garde >= 20:
        #对每一个角色进行遍历 看看是不是自己的角色 如果是自己的角色就对其安排任务
        for player in players:
            if player['team'] == constants.team_id:
                y = int(player["y"])
                x = int(player["x"])
                #计算下一个要走的路
                [res_xy, n] = Dijkstra_all_minpath(y * height + x, [garde_y * height + garde_x], Dijkstra_map_l)
                #需要走很远的路 就自己走自己的
                if n == 0:
                    res[player['id']] = Defense1_Attack(map, player)
                    continue
                res_xy = int(res_xy)
                # 计算下一步的位置
                res_y = int(res_xy / height)
                res_x = int(res_xy % height)
                #计算走的方式
                res[player['id']] = ""
                if res_y == y and res_x == x - 1:
                    res[player['id']] = "left"
                    d_rl[player['id']] = "left"
                    if res_x - 2 >= 0 and garde_y == res_y and garde_x == res_x and map[res_y][res_x - 1] != 'x':
                        garde_x -= 2
                elif res_y == y and res_x == x + 1:
                    res[player['id']] = "right"
                    d_rl[player['id']] = "right"
                    if res_x + 2 < width and garde_y == res_y and garde_x == res_x and map[res_y][res_x + 1] != 'x':
                        garde_x += 2
                elif res_y == y - 1 and res_x == x:
                    res[player['id']] = "up"
                    d_rl[player['id']] = "up"
                    if res_y - 2 >= 0 and garde_y == res_y and garde_x == res_x and map[res_y - 1][res_x] != 'x':
                        garde_y -= 2
                elif res_y == y + 1 and res_x == x:
                    res[player['id']] = "down"
                    d_rl[player['id']] = "down"
                    if res_y + 2 < height and garde_y == res_y and garde_x == res_x and map[res_y + 2][res_x] != 'x':
                        garde_y += 2
                else:
                    pass
                #更新数组 把走过的点变成石头 让其他队友不再走这里 避免重合
                if res_x - 1 >= 0 and Dijkstra_map_l[res_xy - 1][res_xy] == 50:
                    Dijkstra_map_l[res_xy - 1][res_xy] = 300
                if res_x + 1 < width and Dijkstra_map_l[res_xy + 1][res_xy] == 50:
                    Dijkstra_map_l[res_xy + 1][res_xy] = 300
                if res_y - 1 >= 0 and Dijkstra_map_l[res_xy - 20][res_xy] == 50:
                    Dijkstra_map_l[res_xy - 20][res_xy] = 300
                if res_y + 1 < height  and Dijkstra_map_l[res_xy + 20][res_xy] == 50:
                    Dijkstra_map_l[res_xy + 20][res_xy] = 300
    #只找到了分数 和不值得吃的敌人
    else:
        num = 0
        gardes = []
        # 遍历地图 看看地图上那些地方有分数
        for i in range(height):  # 读取地图
            for j in range(width):
                if map[i][j][0] == 'p':
                    num += 1
                    gardes.append(i * height + j)
        # 对每一个角色进行遍历 看看是不是自己的角色 如果是自己的角色就对其安排任务
        for player in players:
            if player['team'] == constants.team_id:
                # 当前视野上没有分数
                if num == 0:
                    # 上一次是追击敌人 敌人突然消失或者被吃掉
                    res[player['id']] = ""
                    if player['id'] in d_rl.keys():
                        res[player['id']] = d_rl[player['id']]
                        del d_rl[player['id']]
                    #上一次是吃分 或者其他情况 去查历史 图形
                    else:
                        res[player['id']] = Defense1_Attack(map, player)
                #对每一个角色让他去找地图上离他最近的分数 已经被定位目标的分数不再成为别人的目标
                else:
                    y = int(player["y"])
                    x = int(player["x"])
                    # 计算下一个要走的路
                    [res_xy, n] = Dijkstra_all_minpath(y * height + x, gardes, Dijkstra_map_l)
                    if n == 0:
                        res[player['id']] = ""
                        res[player['id']] = Attack_myself(player, Dijkstra_map_l)
                        continue
                    res_xy = int(res_xy)
                    # 计算下一步的位置
                    res_y = int(res_xy / height)
                    res_x = int(res_xy % height)
                    # 计算走的方式
                    res[player['id']] = ""
                    if res_y == y and res_x == x - 1:
                        res[player['id']] = "left"
                    elif res_y == y and res_x == x + 1:
                        res[player['id']] = "right"
                    elif res_y == y - 1 and res_x == x:
                        res[player['id']] = "up"
                    elif res_y == y + 1 and res_x == x:
                        res[player['id']] = "down"
                    else:
                        pass
                    # 去掉这个目标点
                    if n!= 0:
                        gardes.remove(n)
                        num -= 1
                    #更新数组 把走过的点变成石头 让其他队友不再走这里 避免重合
                    if res_x - 1 >= 0 and Dijkstra_map_l[res_xy - 1][res_xy] == 50:
                        Dijkstra_map_l[res_xy - 1][res_xy] = 300
                    if res_x + 1 < width and Dijkstra_map_l[res_xy + 1][res_xy] == 50:
                        Dijkstra_map_l[res_xy + 1][res_xy] = 300
                    if res_y - 1 >= 0 and Dijkstra_map_l[res_xy - 20][res_xy] == 50:
                        Dijkstra_map_l[res_xy - 20][res_xy] = 300
                    if res_y + 1 < height  and Dijkstra_map_l[res_xy + 20][res_xy] == 50:
                        Dijkstra_map_l[res_xy + 20][res_xy] = 300
    return res
#吃糖
def sweets(map,player,Dijkstra_map_l):
    num = 0
    gardes = []
    # 遍历地图 看看地图上那些地方有分数
    for i in range(height):  # 读取地图
        for j in range(width):
            if map[i][j][0] == 'p':
                num += 1
                gardes.append(i * height + j)
    y = int(player["y"])
    x = int(player["x"])
    # 计算下一个要走的路
    [res_xy, n] = Dijkstra_all_minpath(y * height + x, gardes, Dijkstra_map_l)
    #没有糖
    if n == 0:
        return Attack_myself(player,Dijkstra_map_l)
    res_xy = int(res_xy)
    # 计算下一步的位置
    res_y = int(res_xy / height)
    res_x = int(res_xy % height)
    # 计算走的方式
    if res_y == y and res_x == x - 1:
        return "left"
    elif res_y == y and res_x == x + 1:
        return "right"
    elif res_y == y - 1 and res_x == x:
        return "up"
    elif res_y == y + 1 and res_x == x:
        return "down"
#开拓地图
def Attack_myself(player,Dijkstra_map_l):
        heistor = []
        for i in range(height * width):
            if heistor_eye[i] == 0:
                heistor.append(i)
        y = int(player["y"])
        x = int(player["x"])
        # 计算下一个要走的路
        [res_xy, n] = Dijkstra_all_minpath(y * height + x, heistor, Dijkstra_map_l)
        res_xy = int(res_xy)
        # 计算下一步的位置
        res_y = int(res_xy / height)
        res_x = int(res_xy % height)
        # 计算走的方式
        if res_y == y and res_x == x - 1:
            return "left"
        elif res_y == y and res_x == x + 1:
            return "right"
        elif res_y == y - 1 and res_x == x:
            return "up"
        elif res_y == y + 1 and res_x == x:
            return "down"

#防守模式
def Defense(map, players,round_id):
    '''
    #现根据敌人的位置 将敌人可能走的地方的权重全都变掉 使自己不能去
    #如果视野里有分再去吃分
    #如果没有分的话就去没去过的地方
    '''
    #把相邻矩阵拿出来复制一遍
    Dijkstra_map_l = copy.deepcopy(Dijkstra_map)
    # 对每一个角色进行遍历 看看是不是自己的角色 如果不是自己的角色就变更权重矩阵
    for player in players:
        if player['team'] != constants.team_id:
            a = int(player['y']) * height + int(player['x'])#计算敌人再权重矩阵中的位置
            if int(player['x']) - 1 >= 0and map_s[int(player['y'])][int(player['x']) - 1] == 'o' \
                    and map[int(player['y'])][int(player['x']) + 1] != '+':
                for i in range(height * width):
                    Dijkstra_map_l[i][a - 1] = 100000
            if int(player['x']) + 1 < width and map_s[int(player['y'])][int(player['x']) + 1] == 'o' \
                    and map[int(player['y'])][int(player['x']) + 1] != '+':
                for i in range(height * width):
                    Dijkstra_map_l[i][a + 1] = 100000
            if int(player['y']) - 1 >= 0 and  map_s[int(player['y']) - 1][int(player['x'])] == 'o' \
                    and map[int(player['y']) - 1][int(player['x'])] != '+':
                for i in range(height * width):
                    Dijkstra_map_l[i][a - 20] = 100000
            if int(player['y']) + 1 < height and  map_s[int(player['y']) + 1][int(player['x'])] == 'o' \
                    and map[int(player['y']) + 1][int(player['x'])] != '+':
                for i in range(height * width):
                    Dijkstra_map_l[i][a + 20] = 100000
    #res = {}
    # # 遍历地图 看看地图上那些地方有分数
    # num = 0
    # gardes = []
    # for i in range(height):  # 读取地图
    #     for j in range(width):
    #         if map[i][j][0] == 'p':
    #             num += 1
    #             gardes.append(i * height + j)
    # 对每一个角色进行遍历 看看是不是自己的角色 如果是自己的角色就安排任务
    res = {}
    for player in players:
        if player['team'] == constants.team_id:
            res[player['id']] = sweets(map,player,Dijkstra_map_l)
            # #视野中有分数 派一个人去吃它
            # if num != 0:
            #     y = int(player["y"])
            #     x = int(player["x"])
            #     # 计算下一个要走的路
            #     [res_xy, n] = Dijkstra_all_minpath(y * height + x, gardes, Dijkstra_map_l)
            #     if int(res_xy) == 0 and n == 0:
            #         res[player['id']] = Attack_myself(player, Dijkstra_map_l)
            #         continue
            #     res_xy = int(res_xy)
            #     # 计算下一步的位置
            #     res_y = int(res_xy / height)
            #     res_x = int(res_xy % height)
            #     # 计算走的方式
            #     if res_y == y and res_x == x - 1:
            #         res[player['id']] = "left"
            #     elif res_y == y and res_x == x + 1:
            #         res[player['id']] = "right"
            #     elif res_y == y - 1 and res_x == x:
            #         res[player['id']] = "up"
            #     elif res_y == y + 1 and res_x == x:
            #         res[player['id']] = "down"
            #     else:
            #         pass
            #     # 去掉这个目标点
            #     gardes.remove(n)
            #     num -= 1
            # #视野中没有分数 去刷新历史地图
            # else:
            #     res[player['id']] = Attack_myself(player, Dijkstra_map_l)

    return res
def leg_start(msg):
    '''
    :param msg:
    :return: None
    '''
    print("round start")
    try:
        global width
        global height
        global vision
        global map_s
        global map_f
        global my_id
        global R_B
        global Dijkstra_map
        global d_rl
        global heistor_eye
    finally:
        a = 1 + 1
    d_rl = {}
    # 地图范围
    height = int(msg['msg_data']['map']['height'])
    width = int(msg['msg_data']['map']['width'])
    #视野范围
    vision = int(msg['msg_data']['map']['vision'])
    #地图构建
    map_s = [['o' for i in range(width)]for i in range(height)]         #可以走的地方
    for itm in msg['msg_data']['map']['meteor']:
        map_s[int(itm['y'])][int(itm['x'])] = 'x'                       #陨石
    for itm in msg['msg_data']['map']['tunnel']:
        if itm['direction'] == 'down':
            map_s[int(itm['y'])][int(itm['x'])] = 'V'                   #快速通道
        elif itm['direction'] == 'up':
            map_s[int(itm['y'])][int(itm['x'])] = '^'                   #快速通道
        elif itm['direction'] == 'left':
            map_s[int(itm['y'])][int(itm['x'])] = '<'                   #快速通道
        elif itm['direction'] == 'right':
            map_s[int(itm['y'])][int(itm['x'])] = '>'                   #快速通道
    for itm in msg['msg_data']['map']['wormhole']:
            map_s[int(itm['y'])][int(itm['x'])] = itm['name']          #传送门\
    #历史步数
    heistor_eye = { i:0 for i in range(width * height)}
    # 计算一个权重矩阵 用于计算最短路径
    Dijkstra_map = [[100000 for i in range(height * width)] for i in range(height * width)]
    for i in range(height * width):
        for j in range(height * width):
            # 将j和i 转换为 坐标值
            i_y = int(i / height)
            i_x = i % height
            j_y = int(j / height)
            j_x = j % height
            #要到达的点不是石头
            if map_s[j_y][j_x] != 'x':
                if i == j:#自己到自己
                    Dijkstra_map[i][j] = 0
                elif i_y + 1 < height and i + 20 == j:
                    Dijkstra_map[i][j] = 50
                elif i_y - 1 >= 0 and i - 20 == j:
                    Dijkstra_map[i][j] = 50
                elif i_x - 1 >= 0 and i - 1 == j:
                    Dijkstra_map[i][j] = 50
                elif i_x + 1 < width and i + 1 == j:
                    Dijkstra_map[i][j] = 50
                else:
                    Dijkstra_map[i][j] = 100000
            else:
                Dijkstra_map[i][j] = 100000
    #传送门的权值
    for itm_A in msg['msg_data']['map']['wormhole']:
        for itm_a in msg['msg_data']['map']['wormhole']:
            if ord(itm_A['name']) == (ord(itm_a['name']) + 32)or itm_A['name'] == ord(itm_A['name']) == (ord(itm_a['name']) - 32):
                Dijkstra_map[int(itm_a['y']) * height + int(itm_a['x'])][int(itm_A['y']) * height + int(itm_A['x'])] = 50
                Dijkstra_map[int(itm_A['y']) * height + int(itm_A['x'])][int(itm_a['y']) * height + int(itm_a['x'])] = 50
    #快速通道的权值
    for itm in msg['msg_data']['map']['tunnel']:
        if itm['direction'] == 'down':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']) + 1) * height + int(itm['x'])] = 10
            Dijkstra_map[(int(itm['y']) + 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y'])) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) + 1] = 100000
            Dijkstra_map[(int(itm['y'])) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) - 1] = 100000
        elif itm['direction'] == 'up':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']) - 1) * height + int(itm['x'])] = 10
            Dijkstra_map[(int(itm['y']) - 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y'])) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) + 1] = 100000
            Dijkstra_map[(int(itm['y'])) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) - 1] = 100000
        elif itm['direction'] == 'left':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) - 1] = 10
            Dijkstra_map[int(itm['y']) * height + int(itm['x']) - 1][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y']) - 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y']) + 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
        elif itm['direction'] == 'right':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x']) + 1] = 10
            Dijkstra_map[int(itm['y']) * height + int(itm['x']) + 1][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y']) - 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
            Dijkstra_map[(int(itm['y']) + 1) * height + int(itm['x'])][(int(itm['y'])) * height + int(itm['x'])] = 100000
    map_f = copy.deepcopy(map_s)
    try:
        my_id = []
        for my in msg['msg_data']['teams']:
            if my['id'] == constants.team_id:
                R_B = my['force']
                for i in range(4):
                    my_id.append(int(my['players'][i]))
    except KeyError:
        a = 1+1
    for i in range(height):
        for j in range(width):
            print(map_s[i][j],end=" ")
        print("")

    print ("msg_name:%s" % msg['msg_name'])
    print ("map_width:%s" % msg['msg_data']['map']['width'])
    print ("map_height:%s" % msg['msg_data']['map']['height'])
    print ("vision:%s" % msg['msg_data']['map']['vision'])
    print ("meteor:%s" % msg['msg_data']['map']['meteor'])
    # print ("cloud:%s" % msg['msg_data']['map']['cloud'])
    print ("tunnel:%s" % msg['msg_data']['map']['tunnel'])
    print ("wormhole:%s" % msg['msg_data']['map']['wormhole'])
    print ("teams:%s" % msg['msg_data']['teams'])

def leg_end(msg):
    '''
    :param msg:
    {
        "msg_name" : "leg_end",
        "msg_data" : {
            "teams" : [
            {
                "id" : 1001,				#队ID
                "point" : 770             #本leg的各队所得点数
            },
            {
            "id" : 1002,
            "point" : 450
             }
            ]
        }
    }
    :return:
    '''
    print ("round over")
    teams = msg["msg_data"]['teams']
    for team in teams:
        print ("teams:%s" % team['id'])
        print ("point:%s" % team['point'])
        print ("\n\n")
    f = open("./out.txt", "a")
    print ("round over",file=f)

def game_over(msg):
    print ("game over!")
    f = open("out.txt", "a")
    print ("game over!", file = f)

def round(msg):
    import random
    '''
    :param msg: dict
    :return:
    return type: dict
    '''
    print("round")
    resove = {}
    try:
        #移动方向定义
        direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
        # #在原始地图上标注分数位置
        try:                                                                    #获取能量位置
            for itm in msg['msg_data']['power']:
                map_f[int(itm['y'])][int(itm['x'])] = 'p' + str(itm['point'])
        except KeyError:
           a = 1 + 1
        # 创建本回合的视野地图
        round_map = copy.deepcopy(map_s)               #创建地图模型
        try:                                                                    #获取能量位置
            for itm in msg['msg_data']['power']:
                round_map[int(itm['y'])][int(itm['x'])] = 'p' + str(itm['point'])
        except KeyError:
            a = 1 + 1
        try:                                                                    #获取对手和自己的位置
            for itm in msg['msg_data']['players']:
                if itm['team'] == constants.team_id:
                    round_map[int(itm['y'])][int(itm['x'])] = '+'
                else:
                    round_map[int(itm['y'])][int(itm['x'])] = "-" + str(itm['score'])
        except KeyError:
            a = 1+1
        #获取回合信息
        #获取回合号
        round_id = msg['msg_data']['round_id']
        # 获取本回合场上玩家信息
        try:
            players = msg['msg_data']['players']
        except KeyError:
            players = []
        # 获取本回合的进攻防守模式 beat防守 think进攻
        mode = msg['msg_data']['mode']
        # 记录足迹
        for i in range(height * width):
            if heistor_eye[i] != 0:
                heistor_eye[i] -= 1
        for player in players:
            if player['team'] == constants.team_id:
                for i in range(-vision,vision):
                    for j in range(-vision,vision):
                        heistor_eye[(int(player['y']) + j) * height + int(player['x']) + i] = 30
        # 进攻模式
        if str(mode) == str(R_B):
            resove = Attack(round_map, players, round_id)
        #防守模式
        else:
            resove = Defense(round_map, players, round_id)
    except Exception as e:
        print("fffffffffffffffffffffffffff" + str(round_id))
        direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
        for player in players:
            if player['team'] == constants.team_id:
                resove[player['id']] = direction[random.randint(1, 4)]
    #返回信息模型
    action = []
    for player in players:
        if player['team'] == constants.team_id:
            action.append({"team": player['team'], "player_id": player['id'],
                           "move": [resove[player['id']]]})
    result = {
        "msg_name": "action",
        "msg_data": {
            "round_id": round_id
        }
    }
    result['msg_data']['actions'] = action
    ## 输出 和 日志
    f = open("./out.txt", "a")
    print("youshi:{}:{}".format(msg['msg_data']['mode'], round_id))
    print("a = " + str(round_id), file=f)
    print('msg = ' + str(msg), file=f)
    print('print(ser.round(msg))', file=f)
    print(result, file=f)
    for i in range(height):
        for j in range(width):
            print(round_map[i][j], end=" ", file=f)
        print("", end="\n", file=f)

    return result

# pushd %CD%
# cd /d bin
# client.exe %1 %2 %3
# popd

# EXIT
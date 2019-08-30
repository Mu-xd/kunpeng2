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
        return "down"#Attack(map, player, [])
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
        return 'right'#Attack(map, player)
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
    while (1 == 1):
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
    res = []
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
    if garde >= 10:
        #对每一个角色进行遍历 看看是不是自己的角色 如果是自己的角色就对其安排任务
        for player in players:
            if player['team'] == constants.team_id:
                y = int(player["y"])
                x = int(player["x"])
                # if Dijkstra_map_l[y*height + x][y*height + x + 1] == 100000 and\
                #     Dijkstra_map_l[y*height + x][y*height + x + 1] == 100000 and\
                #     Dijkstra_map_l[y*height + x - 1][y*height + x] == 100000 and\
                #     Dijkstra_map_l[y*height + x + 1][y*height + x] == 100000:
                #     res.append("")
                #     d_rl[player['id']] = ""
                #     continue

                #计算下一个要走的路
                [res_xy, n] = Dijkstra_all_minpath(y * height + x, [garde_y * height + garde_x], Dijkstra_map_l)
                res_xy = int(res_xy)
                # 计算下一步的位置
                res_y = int(res_xy / height)
                res_x = int(res_xy % height)
                #计算走的方式
                if res_y == y and res_x == x - 1:
                    res.append("left")
                    d_rl[player['id']] = "left"
                elif res_y == y and res_x == x + 1:
                    res.append("right")
                    d_rl[player['id']] = "right"
                elif res_y == y - 1 and res_x == x:
                    res.append("up")
                    d_rl[player['id']] = "up"
                elif res_y == y + 1 and res_x == x:
                    res.append("down")
                    d_rl[player['id']] = "down"
                else:
                    pass
                #更新数组 把走过的点变成石头 让其他队友不再走这里
                # if res_xy - 1 >= 0 and Dijkstra_map_l[res_xy - 1][res_xy] == 50:
                #     Dijkstra_map_l[res_xy - 1][res_xy] = 51
                # if res_xy + 1 < 400 and Dijkstra_map_l[res_xy + 1][res_xy] == 50:
                #     Dijkstra_map_l[res_xy + 1][res_xy] = 51
                # if res_xy + height < 400 and Dijkstra_map_l[res_xy + height][res_xy] == 50:
                #     Dijkstra_map_l[res_xy + height][res_xy] = 51
                # if res_xy - height >= 0 and Dijkstra_map_l[res_xy - height][res_xy] == 50:
                #     Dijkstra_map_l[res_xy - height][res_xy] = 51
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
                    if player['id'] in d_rl.keys():
                        res.append(d_rl[player['id']])
                        del d_rl[player['id']]
                    # 上一次是吃分 或者其他情况 去查历史 图形
                    else:
                        gardes1 = []
                        nums = 0
                        #查历史地图
                        for i in range(height):
                            for j in range(width):
                                #这个点是分数并且不和现在的记录重合
                                if map_f[i][j][0] == 'p':
                                    nums += 1
                                    gardes1.append(i * height + j)
                        y = int(player["y"])
                        x = int(player["x"])
                        #如果这个自己所在的点历史上是分数 就把这个点除去 防止一直在一个点呆着
                        if (y * height + x) in gardes1:
                            gardes1.remove(y * height + x)
                            nums -= 1
                        #如果历史上没有分数点了 按顺序遍历地图 让所有的点都依次出现在视野中
                        if nums == 0:
                            res.append("left")#随便走的
                        #历史上有分数点
                        else:
                            # 计算下一个要走的路
                            [res_xy, n] = Dijkstra_all_minpath(y * height + x, gardes1, Dijkstra_map_l)
                            res_xy = int(res_xy)
                            # 计算下一步的位置
                            res_y = int(res_xy / height)
                            res_x = int(res_xy % height)
                            # 计算走的方式
                            if res_y == y and res_x == x - 1:
                                res.append("left")
                            elif res_y == y and res_x == x + 1:
                                res.append("right")
                            elif res_y == y - 1 and res_x == x:
                                res.append("up")
                            elif res_y == y + 1 and res_x == x:
                                res.append("down")
                            else:
                                pass
                            #如果我在的这个点在历史上是分数点 就清除它
                            if map_f[int(res_xy/height)][res_xy % height][0] == "p":
                                map_f[int(res_xy / height)][res_xy % height] = 'o'
                #对每一个角色让他去找地图上离他最近的分数 已经被定位目标的分数不再成为别人的目标
                else:
                    y = int(player["y"])
                    x = int(player["x"])
                    # 计算下一个要走的路
                    [res_xy, n] = Dijkstra_all_minpath(y * height + x, gardes, Dijkstra_map_l)
                    res_xy = int(res_xy)
                    # 计算下一步的位置
                    res_y = int(res_xy / height)
                    res_x = int(res_xy % height)
                    # 计算走的方式
                    if res_y == y and res_x == x - 1:
                        res.append("left")
                    elif res_y == y and res_x == x + 1:
                        res.append("right")
                    elif res_y == y - 1 and res_x == x:
                        res.append("up")
                    elif res_y == y + 1 and res_x == x:
                        res.append("down")
                    else:
                        pass
                    # 去掉这个目标点
                    gardes.remove(n)
                    num -= 1
                    #更新数组 把走过的点变成石头 让其他队友不再走这里 避免重合
                    # if res_xy - 1 >= 0 and Dijkstra_map_l[res_xy - 1][res_xy] == 50:
                    #     Dijkstra_map_l[res_xy - 1][res_xy] = 51
                    # if res_xy + 1 < 400 and Dijkstra_map_l[res_xy + 1][res_xy] == 50:
                    #     Dijkstra_map_l[res_xy + 1][res_xy] = 51
                    # if res_xy + height < 400 and Dijkstra_map_l[res_xy + height][res_xy] == 50:
                    #     Dijkstra_map_l[res_xy + height][res_xy] = 51
                    # if res_xy - height >= 0 and Dijkstra_map_l[res_xy - height][res_xy] == 50:
                    #     Dijkstra_map_l[res_xy - height][res_xy] = 51
    return res
#防守模式
def Defense(map, players,round_id):
    res = []
    for player in players:
        res.append(Defense1(map, player))
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
    finally:
        a = 1 + 1
    d_rl = {}
    height = int(msg['msg_data']['map']['height'])
    width = int(msg['msg_data']['map']['width'])
    vision = int(msg['msg_data']['map']['vision'])
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
            map_s[int(itm['y'])][int(itm['x'])] = itm['name']          #传送门
    Dijkstra_map = [[100000 for i in range(height * width)] for i in range(height * width)]
    # 计算一个权重矩阵 用于计算最短路径
    for i in range(height * width):
        for j in range(height * width):
            # 将j和i 转换为 坐标值
            i_y = int(i / height)
            i_x = i % height
            j_y = int(j / height)
            j_x = j % height
            if i == j:
                Dijkstra_map[i][j] = 0
            # 在i的附近
            elif (j_x == i_x and (i_y == j_y - 1 or j_y + 1 == i_y)) or (
                    j_y == i_y and (i_x == j_x - 1 or j_x + 1 == i_x)):
                # 附近可以走的路
                if map_s[j_y][j_x][0] == 'o':
                    Dijkstra_map[i][j] = 50
                else:
                    Dijkstra_map[i][j] = 100000
            else:
                Dijkstra_map[i][j] = 100000
    #传送门的权值
    for itm_A in msg['msg_data']['map']['wormhole']:
        for itm_a in msg['msg_data']['map']['wormhole']:
            if ord(itm_A['name']) == (ord(itm_a['name']) + 32)or itm_A['name'] == ord(itm_A['name']) == (ord(itm_a['name']) - 32):
                Dijkstra_map[int(itm_a['y']) * height + int(itm_a['x'])][int(itm_A['y']) * height + int(itm_A['x'])] = 10
    #快速通道的权值
    for itm in msg['msg_data']['map']['tunnel']:
        if itm['direction'] == 'down':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']) + 1)* height + int(itm['x'])] = 10
        elif itm['direction'] == 'up':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']) - 1)* height + int(itm['x'])] = 10
        elif itm['direction'] == 'left':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']))* height + int(itm['x']) - 1] = 10
        elif itm['direction'] == 'right':
            Dijkstra_map[int(itm['y']) * height + int(itm['x'])][(int(itm['y']))* height + int(itm['x']) + 1] = 10
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
    f = open("./out.txt", "a")
    for i in range(height):
        for j in range(width):
            print(map_s[i][j],end=" ",file=f)
        print("",file=f)
    print ("round start",file=f)
    print (str(msg),file=f)

    print ("msg_name:%s" % msg['msg_name'],file=f)
    print ("map_width:%s" % msg['msg_data']['map']['width'],file=f)
    print ("map_height:%s" % msg['msg_data']['map']['height'],file=f)
    print ("vision:%s" % msg['msg_data']['map']['vision'],file=f)
    print ("meteor:%s" % msg['msg_data']['map']['meteor'],file=f)
    # print ("cloud:%s" % msg['msg_data']['map']['cloud'],file=f)
    print ("tunnel:%s" % msg['msg_data']['map']['tunnel'],file=f)
    print ("wormhole:%s" % msg['msg_data']['map']['wormhole'],file=f)
    print ("teams:%s" % msg['msg_data']['teams'],file=f)

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
    # for i in range(height):                                                  #读取基础地图
    #     for j in range(width):
    #         round_map[i][j] = map_s[i][j]
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
    #确定自己的动作
    action = []
    # 记录足迹
    zj = []
    # 进攻模式
    if str(mode) == str(R_B):
        resove = Attack(round_map, players, round_id)
    #防守模式
    else:
        resove = Defense(round_map, players, round_id)
    i = 0
    #返回信息模型
    for player in players:
        if player['team'] == constants.team_id:
            action.append({"team": player['team'], "player_id": player['id'],
                           "move": [resove[i]]})
            i += 1
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
    #print(result, file=f)
    print(msg, file=f)
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
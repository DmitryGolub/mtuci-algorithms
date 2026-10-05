import random
import time

from avl import avl_insert, balance_factor, imbalance_case, rebalance
from bst import Node, build_bst, delete, height, inorder, insert, postorder, preorder, search
from range_queries import (
    FenwickTree,
    SegmentTree,
    StatsSegmentTree,
    build_prefix,
    range_sum_naive,
    range_sum_prefix,
)
from sensor_system import MeasurementAnalyzer, Sensor, SensorRegistry

random.seed(42)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def subsection(title):
    print()
    print(f"--- {title}")


def fmt_time(seconds):
    if seconds < 1e-6:
        return f"{seconds * 1e9:8.1f} нс"
    if seconds < 1e-3:
        return f"{seconds * 1e6:8.1f} мкс"
    if seconds < 1:
        return f"{seconds * 1e3:8.2f} мс"
    return f"{seconds:8.3f} с"


def fmt_int(value):
    return f"{value:,}".replace(",", " ")


def show_tree(root, label=lambda node: str(node.key)):
    def walk(node, indent, tag):
        if node is None:
            return
        print(f"  {indent}{tag}{label(node)}")
        walk(node.left, indent + "    ", "L: ")
        walk(node.right, indent + "    ", "R: ")

    if root is None:
        print("  (пустое дерево)")
    walk(root, "", "")


def avl_label(node):
    return f"{node.key}  [h={node.height}, bf={balance_factor(node):+d}]"


def task_1():
    section("Задание 1: Создание бинарного дерева")

    root = Node(8)
    root.left = Node(4)
    root.right = Node(12)
    root.left.left = Node(2)
    root.left.right = Node(6)
    root.right.left = Node(10)
    root.right.right = Node(14)

    show_tree(root)
    subsection("Значения узлов")
    print(f"  корень:              {root.key}")
    print(f"  левый потомок:       {root.left.key}")
    print(f"  правый потомок:      {root.right.key}")
    print(f"  лист root.left.left: {root.left.left.key}"
          f"   (left={root.left.left.left}, right={root.left.left.right})")
    return root


def task_2(manual_root):
    section("Задание 2: Вставка в бинарное дерево поиска")

    keys = [8, 4, 12, 2, 6, 10, 14]
    root = None
    for key in keys:
        root = insert(root, key)
    print(f"  Последовательность вставки: {keys}")
    show_tree(root)
    same = preorder(root) == preorder(manual_root)
    print(f"  Структура совпадает с деревом из задания 1: {same}")
    return root


def task_3(root):
    section("Задание 3: Поиск элемента")

    cases = (
        (4, "близко к корню"),
        (10, "нижний уровень"),
        (7, "отсутствует"),
    )
    for key, description in cases:
        node, visited = search(root, key)
        found = node.key if node else None
        print(f"  search(root, {key:>2}) -> {str(found):>4}   посещено узлов: {visited}   ({description})")


def task_4(root):
    section("Задание 4: Обходы дерева")

    print(f"  preorder:  {preorder(root)}")
    print(f"  inorder:   {inorder(root)}")
    print(f"  postorder: {postorder(root)}")
    print(f"  inorder отсортирован: {inorder(root) == sorted(inorder(root))}")


def task_5():
    section("Задание 5: Удаление из BST")

    root = build_bst([8, 4, 12, 2, 6, 10, 14])
    subsection("Исходное дерево")
    show_tree(root)

    steps = (
        (2, "лист"),
        (4, "узел с одним потомком (6) после удаления листа 2"),
        (8, "узел с двумя потомками (корень)"),
    )
    for key, description in steps:
        root = delete(root, key)
        subsection(f"delete({key}) — {description}")
        show_tree(root)
        print(f"  inorder: {inorder(root)}")


def task_6():
    section("Задание 6: Влияние порядка вставки на высоту дерева")

    sequences = (
        ("Первое BST", [8, 4, 12, 2, 6, 10, 14]),
        ("Второе BST", [2, 4, 6, 8, 10, 12, 14]),
    )
    for title, keys in sequences:
        root = build_bst(keys)
        last = keys[-1]
        _, visited = search(root, last)
        subsection(f"{title}: {keys}")
        show_tree(root)
        print(f"  height = {height(root)}")
        print(f"  поиск последнего добавленного ({last}): посещено узлов {visited}")


def task_7():
    section("Задание 7: Повороты AVL-дерева")

    rotations = {
        "LL": "rotate_right(корень)",
        "RR": "rotate_left(корень)",
        "LR": "rotate_left(левый потомок), затем rotate_right(корень)",
        "RL": "rotate_right(правый потомок), затем rotate_left(корень)",
    }
    for keys in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
        subsection(f"Последовательность {keys}")

        unbalanced = None
        for key in keys:
            unbalanced = avl_insert(unbalanced, key, balance=False)
        print("  До балансировки:")
        show_tree(unbalanced, avl_label)

        case = imbalance_case(unbalanced)
        print(f"  Случай {case}: {rotations[case]}")

        balanced = rebalance(unbalanced)
        print("  После балансировки:")
        show_tree(balanced, avl_label)

        auto = None
        for key in keys:
            auto = avl_insert(auto, key)
        print(f"  avl_insert с балансировкой даёт то же дерево: {preorder(auto) == preorder(balanced)}")


def task_8():
    section("Задание 8: Наивный запрос суммы диапазона")

    n = 100_000
    data = [random.randint(1, 1000) for _ in range(n)]
    ranges = []
    for _ in range(1000):
        left = random.randint(0, n - 1)
        right = random.randint(left, n - 1)
        ranges.append((left, right))

    print(f"  Размер массива: {fmt_int(n)}, запросов: {len(ranges)}")
    print(f"  Средняя длина диапазона: {fmt_int(round(sum(r - l + 1 for l, r in ranges) / len(ranges)))}")
    for left, right in ranges[:3]:
        print(f"  range_sum_naive(data, {left:>5}, {right:>5}) = {fmt_int(range_sum_naive(data, left, right))}")

    start = time.perf_counter()
    naive_results = [range_sum_naive(data, left, right) for left, right in ranges]
    naive_time = time.perf_counter() - start

    print(f"  Суммарное время {len(ranges)} запросов: {fmt_time(naive_time)}")
    print(f"  Среднее время одного запроса:   {fmt_time(naive_time / len(ranges))}")
    return data, ranges, naive_results, naive_time


def task_9(data, ranges, naive_results, naive_time):
    section("Задание 9: Префиксные суммы")

    start = time.perf_counter()
    prefix = build_prefix(data)
    build_time = time.perf_counter() - start

    start = time.perf_counter()
    prefix_results = [range_sum_prefix(prefix, left, right) for left, right in ranges]
    query_time = time.perf_counter() - start

    print(f"  prefix[:6] = {prefix[:6]}")
    print(f"  Результаты совпадают с наивным способом: {prefix_results == naive_results}")

    subsection("Сравнение времени")
    print(f"  построение prefix:                   {fmt_time(build_time)}")
    print(f"  {len(ranges)} запросов через prefix:          {fmt_time(query_time)}")
    print(f"  {len(ranges)} запросов наивно:                {fmt_time(naive_time)}")
    print(f"  ускорение запросов:                  в {fmt_int(round(naive_time / query_time))} раз")
    print(f"  ускорение с учётом построения:       в {fmt_int(round(naive_time / (build_time + query_time)))} раз")

    subsection("Изменение элемента после построения prefix")
    changed = list(data)
    index = 50_000
    changed[index] += 500
    left, right = 49_000, 51_000
    stale = range_sum_prefix(prefix, left, right)
    actual = range_sum_naive(changed, left, right)
    print(f"  data[{index}]: {data[index]} -> {changed[index]}")
    print(f"  сумма [{left}, {right}] по старому prefix: {fmt_int(stale)}")
    print(f"  фактическая сумма:                  {fmt_int(actual)}")
    fresh = build_prefix(changed)
    broken = sum(1 for a, b in zip(prefix, fresh) if a != b)
    print(f"  некорректных значений prefix: {fmt_int(broken)} из {fmt_int(len(prefix))} (все prefix[i] при i > {index})")
    print(f"  после перестроения prefix: {fmt_int(range_sum_prefix(fresh, left, right))}")


def task_10():
    section("Задание 10: Дерево Фенвика")

    data = [5, 3, 7, 9, 6, 4, 1, 2, 8, 10]
    fenwick = FenwickTree(data)
    print(f"  data = {data}")
    print(f"  tree = {fenwick.tree}")

    subsection("Блоки, за которые отвечают ячейки tree (индексация с 1)")
    for i in range(1, fenwick.n + 1):
        low = i & -i
        print(f"  tree[{i:>2}]  i = {i:04b}  i & -i = {low:>2}  отвечает за data[{i - low}..{i - 1}]"
              f"  сумма = {fenwick.tree[i]}")

    subsection("Сравнение с sum()")
    queries = [(0, 9), (2, 5), (3, 3), (0, 4), (6, 9), (1, 8)]
    for left, right in queries:
        expected = sum(data[left:right + 1])
        actual = fenwick.range_sum(left, right)
        print(f"  range_sum({left}, {right}) = {actual:>3}   sum() = {expected:>3}   {actual == expected}")

    subsection("update(3, +5)")
    fenwick.update(3, 5)
    data[3] += 5
    print(f"  data = {data}")
    for left, right in queries[:3]:
        expected = sum(data[left:right + 1])
        actual = fenwick.range_sum(left, right)
        print(f"  range_sum({left}, {right}) = {actual:>3}   sum() = {expected:>3}   {actual == expected}")


def task_11():
    section("Задание 11: Дерево отрезков для суммы")

    data = [5, 3, 7, 9, 6, 4, 1, 2, 8, 10]
    tree = SegmentTree(data)
    print(f"  data = {data}")
    print(f"  корень tree[1] = {tree.tree[1]} (сумма всего массива)")
    print(f"  tree[2] = {tree.tree[2]} (data[0..4]), tree[3] = {tree.tree[3]} (data[5..9])")

    queries = [(0, 9), (2, 5), (3, 3), (0, 4), (6, 9), (1, 8)]
    subsection("Сравнение с sum()")
    for left, right in queries:
        expected = sum(data[left:right + 1])
        actual = tree.query(left, right)
        print(f"  query({left}, {right}) = {actual:>3}   sum() = {expected:>3}   {actual == expected}")

    subsection("update(4, 20)")
    tree.update(4, 20)
    data[4] = 20
    print(f"  data = {data}")
    for left, right in queries:
        expected = sum(data[left:right + 1])
        actual = tree.query(left, right)
        print(f"  query({left}, {right}) = {actual:>3}   sum() = {expected:>3}   {actual == expected}")


def task_12():
    section("Задание 12: Сумма, минимум и максимум")

    data = [5, 3, 7, 9, 6, 4, 1, 2, 8, 10]
    tree = StatsSegmentTree(data)
    print(f"  data = {data}")
    print(f"  корень tree[1] = {tree.tree[1]} (сумма, минимум, максимум)")

    queries = [(4, 4), (0, 1), (2, 6), (5, 9), (1, 8), (0, 9)]

    def check():
        for left, right in queries:
            part = data[left:right + 1]
            expected = (sum(part), min(part), max(part))
            actual = tree.query(left, right)
            print(f"  query({left}, {right})  длина {right - left + 1:>2}: {str(actual):<12}"
                  f" ожидалось {str(expected):<12} {actual == expected}")

    subsection("Запросы (sum, min, max)")
    check()

    subsection("update(6, 15)")
    tree.update(6, 15)
    data[6] = 15
    print(f"  data = {data}")
    check()


def task_13():
    section("Задание 13: Самостоятельная работа: анализ измерений датчиков")

    sensors = [
        (512, "Температура цеха №1"),
        (128, "Давление магистрали"),
        (777, "Влажность склада"),
        (64, "Температура котла"),
        (300, "Расход воды"),
        (650, "Вибрация насоса"),
        (900, "Освещённость"),
        (33, "Уровень CO2"),
        (205, "Напряжение сети"),
        (1024, "Температура улицы"),
    ]
    selected = 512
    measurements = [215 + random.randint(-30, 30) for _ in range(1440)]

    registry = SensorRegistry()
    for sensor_id, name in sensors:
        registry.add(Sensor(sensor_id, name, measurements if sensor_id == selected else None))

    print(f"  Датчиков в реестре: {registry.count}, высота BST: {registry.height()}")

    subsection("Поиск датчика по идентификатору (BST)")
    for sensor_id in (512, 650, 33, 400):
        sensor, visited = registry.find(sensor_id)
        result = f"{sensor.name}" if sensor else "не найден"
        print(f"  id={sensor_id:<5} -> {result:<22} посещено узлов: {visited}")

    subsection("Идентификаторы в отсортированном порядке (inorder)")
    for sensor_id in registry.sorted_ids():
        print(f"  {sensor_id:>5}  {registry.find(sensor_id)[0].name}")

    sensor = registry.find(selected)[0]
    analyzer = MeasurementAnalyzer(sensor.measurements)
    print()
    print(f"  Выбран датчик {selected} «{sensor.name}»: {len(sensor.measurements)} измерений"
          f" (раз в минуту за сутки, десятые доли °C)")

    ranges = [(0, 59), (600, 719), (650, 650), (0, 1439)]

    def report():
        for left, right in ranges:
            part = analyzer.values[left:right + 1]
            s_prefix = analyzer.sum_prefix(left, right)
            s_fenwick = analyzer.sum_fenwick(left, right)
            s_segment, low, high = analyzer.stats(left, right)
            ok = s_prefix == s_fenwick == s_segment == sum(part) and low == min(part) and high == max(part)
            print(f"  [{left:>4}, {right:>4}]  prefix={s_prefix:>7}  fenwick={s_fenwick:>7}"
                  f"  segment={s_segment:>7}  min={low:>3}  max={high:>3}  {ok}")

    subsection("Диапазонные запросы до обновления")
    report()

    index, value = 650, 400
    subsection(f"Обновление: измерение [{index}] {analyzer.values[index]} -> {value}")
    analyzer.update(index, value)
    report()

    subsection("Сравнение структур")
    rows = (
        ("Структура", "Операции", "Запрос", "Обновление", "Построение"),
        ("BST (реестр)", "поиск, вставка, обход", "O(h)", "O(h)", "O(n·h)"),
        ("Префиксные суммы", "сумма", "O(1)", "O(n)", "O(n)"),
        ("Дерево Фенвика", "сумма", "O(log n)", "O(log n)", "O(n log n)"),
        ("Дерево отрезков", "сумма, min, max", "O(log n)", "O(log n)", "O(n)"),
    )
    for row in rows:
        print(f"  {row[0]:<17} {row[1]:<22} {row[2]:<9} {row[3]:<11} {row[4]}")


def main():
    print("Лабораторная работа №2: Деревья и быстрые запросы к данным")
    manual_root = task_1()
    root = task_2(manual_root)
    task_3(root)
    task_4(root)
    task_5()
    task_6()
    task_7()
    data, ranges, naive_results, naive_time = task_8()
    task_9(data, ranges, naive_results, naive_time)
    task_10()
    task_11()
    task_12()
    task_13()
    print()


if __name__ == "__main__":
    main()

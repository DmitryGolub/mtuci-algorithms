import heapq
import itertools
import random
import timeit
from collections import defaultdict

from binary_heap import MinHeap, left, parent, right
from hash_table import HashTable

random.seed(42)


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def subsection(title):
    print()
    print(f"--- {title}")


def bench(func, repeats=5, number=1):
    return min(timeit.repeat(func, repeat=repeats, number=number)) / number


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


def linear_search(numbers, target):
    for index, value in enumerate(numbers):
        if value == target:
            return index
    return -1


def task_2():
    section("Задание 2: Доступ по индексу и линейный поиск")

    n = 100_000
    numbers = random.sample(range(n * 10), n)
    print(f"Список из {fmt_int(len(numbers))} целых чисел")

    subsection("Доступ по индексу")
    for name, idx in (("начало", 0), ("середина", n // 2), ("конец", n - 1)):
        print(f"  numbers[{idx:>6}] = {numbers[idx]:>8}   ({name})")

    subsection("Линейный поиск")
    targets = {
        "начало": numbers[0],
        "середина": numbers[n // 2],
        "конец": numbers[n - 1],
        "отсутствует": -1,
    }
    for name, target in targets.items():
        print(f"  linear_search(numbers, {target:>8}) = {linear_search(numbers, target):>6}   ({name})")

    subsection("Замер времени")
    idx_mid = n // 2
    t_index = bench(lambda: numbers[idx_mid], repeats=5, number=1_000_000)
    print(f"  доступ по индексу numbers[{idx_mid}]:      {fmt_time(t_index)}")
    for name, target in targets.items():
        t = bench(lambda: linear_search(numbers, target), repeats=5, number=5)
        print(f"  линейный поиск ({name:<11}): {fmt_time(t)}   (в {fmt_int(round(t / t_index)):>8} раз дольше)")


def find_by_id_list(records, target_id):
    for record_id, value in records:
        if record_id == target_id:
            return value
    return None


def task_3():
    section("Задание 3: Доступ по ключу")

    n = 10_000
    ids = random.sample(range(1, n * 10), n)
    records = [(record_id, f"value_{record_id}") for record_id in ids]
    lookup = {record_id: value for record_id, value in records}
    print(f"Создано {fmt_int(len(records))} записей (id, value); словарь из {fmt_int(len(lookup))} ключей")

    subsection("Поиск одинаковых id в списке и словаре")
    for target_id in (ids[0], ids[n // 2], ids[-1], -1):
        from_list = find_by_id_list(records, target_id)
        from_dict = lookup.get(target_id)
        print(f"  id={target_id:>6}: список -> {from_list!s:<12} словарь -> {from_dict!s:<12}")

    subsection("Большое количество запросов")
    queries = random.choices(ids, k=2_000)

    def many_list():
        for q in queries:
            find_by_id_list(records, q)

    def many_dict():
        for q in queries:
            lookup.get(q)

    t_list = bench(many_list, repeats=3)
    t_dict = bench(many_dict, repeats=3)
    print(f"  {len(queries)} запросов, список:  {fmt_time(t_list)}   ({fmt_time(t_list / len(queries))} на запрос)")
    print(f"  {len(queries)} запросов, словарь: {fmt_time(t_dict)}   ({fmt_time(t_dict / len(queries))} на запрос)")
    print(f"  словарь быстрее в {fmt_int(round(t_list / t_dict))} раз")


def bucket_index(key, table_size):
    return hash(key) % table_size


def task_4():
    section("Задание 4: Исследование функции hash()")

    subsection("Хеши целых чисел и строк")
    for key in (0, 1, 7, 42, 1_000_000, -1, "a", "student_205", "Иванов"):
        print(f"  hash({key!r:<14}) = {hash(key)}")

    subsection("Повторное вычисление для одинаковых ключей в одном запуске")
    for key in (205, "student_205", "Иванов"):
        h1, h2, h3 = hash(key), hash(key), hash(key)
        print(f"  hash({key!r}) три раза: {h1}, {h2}, {h3} -> одинаковы: {h1 == h2 == h3}")

    subsection("bucket_index(key, 10) для 30 ключей")
    table_size = 10
    keys = list(range(1, 16)) + [
        "apple", "banana", "cherry", "date", "fig",
        "grape", "kiwi", "lemon", "mango", "melon",
        "id_101", "id_205", "id_317", "Иванов", "Петров",
    ]
    buckets = defaultdict(list)
    for key in keys:
        idx = bucket_index(key, table_size)
        buckets[idx].append(key)
        print(f"  bucket_index({key!r:<10}, {table_size}) = {idx}")

    subsection("Ключи, попавшие в одинаковую корзину")
    for idx in range(table_size):
        group = buckets.get(idx, [])
        marker = "  <- коллизия" if len(group) > 1 else ""
        print(f"  корзина {idx}: {group}{marker}")


def task_5():
    section("Задание 5: Простая хеш-таблица методом цепочек")

    table = HashTable(size=10)

    subsection("set / get / обновление")
    table.set("Иванов", 101)
    table.set("Петров", 205)
    table.set("Сидорова", 317)
    print(f"  get('Петров')   = {table.get('Петров')}")
    print(f"  get('Нет')      = {table.get('Нет')}")
    table.set("Петров", 999)
    print(f"  после set('Петров', 999): get('Петров') = {table.get('Петров')}, count = {table.count}")

    subsection("remove")
    print(f"  remove('Иванов') = {table.remove('Иванов')}, get('Иванов') = {table.get('Иванов')}, count = {table.count}")
    print(f"  remove('Иванов') повторно = {table.remove('Иванов')}")

    subsection("Несколько ключей в одной корзине")
    collide = HashTable(size=10)
    for key in (7, 17, 27, 37):
        collide.set(key, f"v{key}")
    for i, bucket in enumerate(collide.buckets):
        if bucket:
            print(f"  корзина {i}: {bucket}")
    print(f"  get(27) = {collide.get(27)}, get(37) = {collide.get(37)}")


def task_6():
    section("Задание 6: Коэффициент заполнения и коллизии")

    total_keys = 1_000
    step = 200
    keys = [f"user_{num}" for num in random.sample(range(10_000_000), total_keys)]

    for size in (10, 100, 1000):
        table = HashTable(size=size)
        subsection(f"Таблица из {size} корзин")
        print(f"  {'n':>6} {'alpha':>8} {'коллизии':>10} {'макс. цепочка':>14}")
        for start in range(0, total_keys, step):
            for key in keys[start:start + step]:
                table.set(key, True)
            print(f"  {table.count:>6} {table.load_factor:>8.2f} {table.collision_count():>10} {table.max_chain_length():>14}")


def task_7():
    section("Задание 7: Представление бинарной кучи")

    heap = MinHeap()
    heap.data = [2, 5, 7, 9, 11, 10, 15]
    data = heap.data
    print(f"  data = {data}, свойство кучи выполняется: {heap.is_valid()}")
    print()
    print(f"  {'i':>3} {'значение':>9} {'родитель':>10} {'левый':>8} {'правый':>8}")
    for i, value in enumerate(data):
        p = data[parent(i)] if i > 0 else "—"
        l = data[left(i)] if left(i) < len(data) else "—"
        r = data[right(i)] if right(i) < len(data) else "—"
        print(f"  {i:>3} {value:>9} {p!s:>10} {l!s:>8} {r!s:>8}")


def task_8():
    section("Задание 8: Реализация sift up и вставки")

    heap = MinHeap()
    for value in (10, 4, 7, 1, 9, 3):
        heap.push(value)
        print(f"  push({value:>2}) -> data = {heap.data!s:<24} "
              f"корень = {heap.data[0]} (min = {min(heap.data)}), min-heap: {heap.is_valid()}")


def task_9():
    section("Задание 9: Реализация sift down и извлечения корня")

    heap = MinHeap()
    for value in (10, 4, 7, 1, 9, 3):
        heap.push(value)
    print(f"  исходная куча: {heap.data}")
    order = []
    while heap.data:
        value = heap.pop()
        order.append(value)
        print(f"  pop() = {value:>2} -> data = {heap.data!s:<20} min-heap: {heap.is_valid()}")
    print(f"  порядок извлечения: {order}")
    print(f"  отсортирован по возрастанию: {order == sorted(order)}")


def task_10():
    section("Задание 10: Приоритетная очередь")

    subsection("Задачи с различными приоритетами")
    tasks = []
    todo = [
        (3, "Обновить документацию"),
        (1, "Исправить критическую ошибку"),
        (5, "Рефакторинг модуля отчётов"),
        (2, "Проверить лабораторную"),
        (8, "Обновить зависимости"),
        (4, "Написать тесты"),
        (7, "Провести код-ревью"),
        (6, "Настроить CI"),
    ]
    for priority, description in todo:
        heapq.heappush(tasks, (priority, description))
    print("  порядок обработки:")
    while tasks:
        priority, description = heapq.heappop(tasks)
        print(f"    приоритет {priority}: {description}")

    subsection("Одинаковые приоритеты без счётчика")
    tasks = []
    same = [(1, "Задача Я"), (1, "Задача Б"), (1, "Задача А"), (1, "Задача В")]
    for item in same:
        heapq.heappush(tasks, item)
    print(f"  порядок добавления:  {[d for _, d in same]}")
    print(f"  порядок извлечения:  {[heapq.heappop(tasks)[1] for _ in range(len(same))]}")

    subsection("Одинаковые приоритеты со счётчиком поступления")
    tasks = []
    counter = itertools.count()
    for priority, description in same:
        heapq.heappush(tasks, (priority, next(counter), description))
    print(f"  порядок добавления:  {[d for _, d in same]}")
    print(f"  порядок извлечения:  {[heapq.heappop(tasks)[2] for _ in range(len(same))]}")


def top_k_sorted(data, k):
    return sorted(data, reverse=True)[:k]


def task_11():
    section("Задание 11: Top-K с полной сортировкой")

    n = 100_000
    data = [random.randint(0, 10**9) for _ in range(n)]
    print(f"  n = {fmt_int(n)}")
    for k in (10, 100, 1000):
        t = bench(lambda: top_k_sorted(data, k), repeats=5)
        print(f"  K = {k:>5}: {fmt_time(t)}   первые 3: {top_k_sorted(data, k)[:3]}")


def top_k_heap(data, k):
    heap = []
    for value in data:
        if len(heap) < k:
            heapq.heappush(heap, value)
        elif value > heap[0]:
            heapq.heapreplace(heap, value)
    return sorted(heap, reverse=True)


def task_12():
    section("Задание 12: Top-K с помощью кучи")

    subsection("Проверка совпадения результатов")
    data = [random.randint(0, 10**9) for _ in range(100_000)]
    for k in (10, 100, 1000):
        print(f"  K = {k:>4}: top_k_heap == top_k_sorted: {top_k_heap(data, k) == top_k_sorted(data, k)}")

    subsection("Сравнение времени")
    print(f"  {'n':>10} {'K':>7} {'сортировка':>13} {'куча':>14} {'куча/сорт.':>11}")
    for n in (10_000, 100_000, 1_000_000):
        data = [random.randint(0, 10**9) for _ in range(n)]
        for k in (10, 100, 1_000, 10_000):
            t_sort = bench(lambda: top_k_sorted(data, k), repeats=3)
            t_heap = bench(lambda: top_k_heap(data, k), repeats=3)
            print(f"  {fmt_int(n):>10} {fmt_int(k):>7} {fmt_time(t_sort):>13} {fmt_time(t_heap):>14} {t_heap / t_sort:>10.2f}x")


class CompetitionSystem:
    def __init__(self):
        self.participants = {}
        self.review_queue = []
        self._seq = itertools.count()

    @staticmethod
    def _log(structure, message):
        print(f"  [{structure:<24}] {message}")

    def add_or_update(self, participant_id, name, score):
        action = "обновлён" if participant_id in self.participants else "добавлен"
        self.participants[participant_id] = {"name": name, "score": score}
        self._log("dict (хеш-таблица)", f"{action} участник id={participant_id}: {name}, результат {score}")

    def get(self, participant_id):
        record = self.participants.get(participant_id)
        self._log("dict (хеш-таблица)", f"поиск id={participant_id} -> {record}")
        return record

    def enqueue_review(self, participant_id, priority):
        heapq.heappush(self.review_queue, (priority, next(self._seq), participant_id))
        self._log("heapq (бинарная куча)", f"в очередь проверки: id={participant_id}, приоритет {priority}")

    def next_review(self):
        if not self.review_queue:
            self._log("heapq (бинарная куча)", "очередь проверки пуста")
            return None
        priority, _, participant_id = heapq.heappop(self.review_queue)
        name = self.participants[participant_id]["name"]
        self._log("heapq (бинарная куча)", f"на проверку: id={participant_id} ({name}), приоритет {priority}")
        return participant_id

    def top_k(self, k):
        heap = []
        for participant_id, record in self.participants.items():
            item = (record["score"], participant_id)
            if len(heap) < k:
                heapq.heappush(heap, item)
            elif item > heap[0]:
                heapq.heapreplace(heap, item)
        result = []
        while heap:
            score, participant_id = heapq.heappop(heap)
            result.append((participant_id, self.participants[participant_id]["name"], score))
        result.reverse()
        self._log(f"min-heap размера K={k}", f"Top-{k} из {len(self.participants)} участников")
        return result

    @staticmethod
    def explain():
        print("  Поиск по id      — dict: словарь реализован как хеш-таблица, поэтому получение,")
        print("                     добавление и обновление записи по ключу в среднем O(1).")
        print("  Очередь проверки — heapq (min-heap): следующим всегда извлекается элемент с")
        print("                     наименьшим приоритетом за O(log n), вставка тоже O(log n);")
        print("                     счётчик seq сохраняет порядок поступления при равных приоритетах.")
        print("  Top-K            — min-heap размера K: один проход по участникам, O(n log K)")
        print("                     вместо O(n log n) полной сортировки; в памяти только K записей.")


def task_13():
    section("Задание 13: Система обработки результатов соревнования")

    system = CompetitionSystem()

    subsection("Добавление и обновление участников")
    roster = [
        (101, "Иванов", 78), (205, "Петров", 92), (317, "Сидорова", 85),
        (418, "Кузнецов", 67), (522, "Смирнова", 92), (633, "Попов", 54),
        (741, "Васильева", 88), (859, "Новиков", 73), (960, "Морозова", 95),
        (1071, "Фёдоров", 61),
    ]
    for participant_id, name, score in roster:
        system.add_or_update(participant_id, name, score)
    system.add_or_update(418, "Кузнецов", 81)

    subsection("Поиск по id")
    system.get(205)
    system.get(999)

    subsection("Очередь результатов на проверку (меньший приоритет = срочнее)")
    system.enqueue_review(101, 3)
    system.enqueue_review(960, 1)
    system.enqueue_review(418, 2)
    system.enqueue_review(522, 1)
    system.enqueue_review(633, 5)
    while system.next_review() is not None:
        pass

    subsection("Top-K участников по результату")
    for k in (3, 5):
        for place, (participant_id, name, score) in enumerate(system.top_k(k), start=1):
            print(f"      {place}. id={participant_id:<5} {name:<10} {score}")

    subsection("Обоснование выбора структур данных")
    CompetitionSystem.explain()


def main():
    print("Лабораторная работа №1: Быстрый доступ к данным")
    for task in (task_2, task_3, task_4, task_5, task_6, task_7,
                 task_8, task_9, task_10, task_11, task_12, task_13):
        task()
    print()


if __name__ == "__main__":
    main()

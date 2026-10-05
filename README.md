# Структуры и алгоритмы обработки данных — лабораторные работы

МТУСИ, курс «Структуры и алгоритмы обработки данных».

- Студент: Голуб Дмитрий Сергеевич
- Группа: БПИ2401
- Преподаватель: Борзов Максим Вадимович

| № | Тема | Папка |
|---|------|-------|
| 1 | Быстрый доступ к данным: индекс и ключ, хеш-таблица с цепочками, бинарная куча, приоритетная очередь, Top-K | [`lab1/`](lab1/) |
| 2 | Деревья и быстрые запросы к данным: BST, обходы, AVL-повороты, префиксные суммы, дерево Фенвика, дерево отрезков | [`lab2/`](lab2/) |

## Запуск

```bash
cd lab2                        # или lab1
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
python main.py
```

Сторонние библиотеки не требуются. Программа выводит результаты всех заданий в консоль.

В папке каждой лабораторной:
- `main.py` и модули — код заданий;
- `Отчет.docx` — отчёт с теорией, ходом работы и выводами;
- `Контрольные_вопросы.md` — ответы на контрольные вопросы.

## Лабораторная работа №2

| Файл | Содержимое | Задания |
|------|------------|---------|
| `bst.py` | `Node`, `insert`, `build_bst`, `search` (с подсчётом посещённых узлов), `preorder` / `inorder` / `postorder`, `delete`, `height` | 1–6 |
| `avl.py` | `AVLNode`, `node_height`, `balance_factor`, `rotate_right`, `rotate_left`, `imbalance_case`, `rebalance`, `avl_insert` | 7 |
| `range_queries.py` | `range_sum_naive`, `build_prefix`, `range_sum_prefix`, `FenwickTree`, `SegmentTree`, `StatsSegmentTree` | 8–12 |
| `sensor_system.py` | `Sensor`, `SensorRegistry` (реестр датчиков на BST), `MeasurementAnalyzer` (сумма, min, max, обновление) | 13 |
| `main.py` | демонстрация всех заданий, точка входа | 1–13 |

Индексы диапазонов во всех функциях — с нуля, границы `left` и `right` включаются. Модули можно использовать отдельно:

```python
from bst import build_bst, search, inorder
from range_queries import FenwickTree, StatsSegmentTree

root = build_bst([8, 4, 12, 2, 6, 10, 14])
node, visited = search(root, 10)       # узел и число посещённых узлов
print(inorder(root))                   # [2, 4, 6, 8, 10, 12, 14]

fenwick = FenwickTree([5, 3, 7, 9])
fenwick.update(1, 10)                  # data[1] += 10
print(fenwick.range_sum(0, 2))         # 25

tree = StatsSegmentTree([5, 3, 7, 9])
tree.update(2, 1)                      # data[2] = 1
print(tree.query(1, 3))                # (сумма, минимум, максимум) = (13, 1, 9)
```

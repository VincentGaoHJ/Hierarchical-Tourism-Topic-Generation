from graphviz import Digraph
import os


def load_nodes(node_file, min_level=1, max_level=3, prefix_list=['*']):
    nodes = {'*': []}
    with open(node_file, 'r') as f:
        for line in f:
            items = line.strip().split('\t')
            node_id = items[0]

            if node_id == "*/top":
                node_content = items[1].split(',')[:8]
                nodes["*"] = node_content
                continue

            if len(items) > 1:
                node_content = items[1].split(',')[:8]
            else:
                node_content = []
            nodes[node_id] = node_content

    prune_nodes = {}
    for node_id, node_content in nodes.items():
        # prune nodes
        # if not has_one_prefix(node_id, prefix_list):
        # continue
        level = len(node_id.split('/')) - 1
        if not min_level <= level <= max_level:
            continue
        # if max_level - min_level > 1 and level == min_level:
        #     node_content = []
        prune_nodes[node_id] = node_content
    return prune_nodes


def has_one_prefix(node_id, prefix_list):
    for prefix in prefix_list:
        if is_exact_prefix(node_id, prefix):
            return True
    return False


def is_exact_prefix(s, prefix):
    if not s.startswith(prefix):
        return False
    tmp = s.replace(prefix, '', 1).lstrip('/')
    if '/' in tmp:
        return False
    return True


def gen_edges(nodes):
    node_ids = list(nodes.keys())
    node_ids.sort(key=lambda x: len(x))
    edges = []
    for i in range(len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            if is_parent(node_ids[i], node_ids[j]):
                edges.append([node_ids[i], node_ids[j]])
    return edges


def is_parent(node_a, node_b):
    if not node_b.startswith(node_a):
        return False

    items_a = node_a.split('/')
    items_b = node_b.split('/')

    # 差集为1
    ret_list = [item for item in items_b if item not in items_a]
    if len(ret_list) != 1:
        return False

    if len(items_b) - len(items_a) == 1:
        return True
    else:
        return False


def gen_node_label(node_id, node_content):
    node_name = node_id.split('/')[-1]

    keywords = '\\n'.join(node_content)

    if node_id == "*":
        return '{%s|%s}' % ("北京", keywords)

    if len(node_content) == 0:
        return node_name
    else:
        return '{%s|%s}' % (node_name, keywords)


def draw(nodes, edges, output_file):
    d = Digraph(node_attr={'shape': 'record', "fontname": "PMingLiu-CN"})
    for node_id, node_content in nodes.items():
        d.node(node_id, gen_node_label(node_id, node_content))
    for e in edges:
        d.edge(e[0], e[1])
    d.render(filename=output_file)


def main(node_file, output_file, min_level, max_level, prefix='*'):
    nodes = load_nodes(node_file, min_level, max_level, prefix)
    edges = gen_edges(nodes)
    draw(nodes, edges, output_file)


def visualize(dir):
    # prefix_list = ['*', '*/information_retrieval', '*/information_retrieval/web_search']

    result_file = os.path.join(dir, 'result.txt')
    main(result_file, dir + "\\" + dir[-14:-6] + '-our-overall-3', min_level=0, max_level=2)
    main(result_file, dir + "\\" + dir[-14:-6] + '-our-overall-4', min_level=0, max_level=3)
    main(result_file, dir + "\\" + dir[-14:-6] + '-our-overall-5', min_level=0, max_level=4)


if __name__ == '__main__':
    dir = "2019-06-30-18-12-29【全部数据集】"
    visualize(dir)

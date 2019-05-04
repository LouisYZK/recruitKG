import json

"""
Use knows.json to store the [en, relation, en2] into Neo4j.
"""

from py2neo import Graph, Node, Relationship, NodeMatcher

seen_en = set()

def store_in_neo4j():
    graph = Graph('bolt://localhost:7687', user='neo4j', password='woyaozou555')
    # graph = Graph('http://localhost:7474', user='neo4j', password='yangzhikai668'
    # select = NodeSelector(graph)
    select = NodeMatcher(graph)
    with open('knows.json', 'r') as fp:
        knows = json.load(fp)

    entities = []
    triple = []
    for en, rel_en in knows.items():
        # rel_en: {'rel':[en],...}
        if en not in seen_en:
            entities.append(en)
            seen_en.add(en)
        for rel, en2 in rel_en.items():
            if en2[0] not in seen_en:
                entities.append(en2[0])
                seen_en.add(en2[0])
            triple.append((en, rel, en2[0]))

 	# 添加所有实体为结点
    for en in entities:
        node = Node('Entity',name=en)
        graph.create(node)

	# 遍历三元组，添加节点的属性，结点间关系等
	# for en, kw in triple.items():
	# 	node_1 = select.select('Entity').where(name = en).first()
	# 	for item in kw:
	# 		if item[1] in triple.keys():
	# 			node_2 = select.select('Entity').where(name = item[1]).first()
	# 			relate = Relationship(node_1,item[0],node_2)
	# 			graph.create(relate)
	# 		else:
	# 			node_1[item[0]] = item[1]
	# 			graph.push(node_1)
    for tri in triple:
        en1, rel, en2 = tri
        node_1 = select.match('Entity', name=en1).first()
        node_2 = select.match('Entity', name=en2).first()
        relate = Relationship(node_1, rel, node_2)
        graph.create(relate)
        print(tri, 'has pushed in graph')

store_in_neo4j()
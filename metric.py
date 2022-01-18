import bashlex, bashparse, bashunroll, bashtemplate, copy


def calculate_command_weight():
    return 1

def calculate_pipeline_weight():
    return 1

def calculate_compound_weight():
    return 1

def calculate_substitution_weight():
    return 1

def calculate_for_weight(score):
    return score

def calculate_if_weight(score):
    return score + 1

def calculate_function_weight(score):
    return score - 1

def calculate_parts_weight(score):
    return score

def calculate_list_weight(score):
    return score

def calculate_command_attr_weight(score):
    return score

def calculate_output_attr_weight(score):
    return score




def calculate_single_node_complexity(node):
    """ Definitely need a templating metric for functions, for loops, etc. 
    Should everything be tempalted and just use that rather than the raw line count? """
    score = 0
    if type(node) is not bashlex.ast.node: return 0
    if node.kind == 'command': score += calculate_command_weight()
    if node.kind == 'pipeline': score += calculate_pipeline_weight()
    if node.kind == 'compound': score += calculate_compound_weight()
    if node.kind == 'commandsubstitution': score += 1
    if node.kind == 'for':
        for_score = 0
        for part in node.parts[4:]:
            for_score += calculate_single_node_complexity(part)
        score += calculate_for_weight(for_score)
    if node.kind == 'if':
        if_score = 0
        for part in node.parts[3:]: if_score += calculate_single_node_complexity(part)
        score += calculate_if_weight(if_score)
    if node.kind == 'function':
        command_section = bashparse.return_nodes_of_type(node, 'compound')  # function has actual commands in their compound node
        function_score = 0
        for part in command_section: function_score += calculate_function_weight(calculate_single_node_complexity(part))
    if hasattr(node, 'parts'):
        parts_score = 0
        for part in node.parts: parts_score += calculate_single_node_complexity(part)
        score += calculate_parts_weight(parts_score)
    if hasattr(node, 'list'):
        list_score = 0
        for part in node.list: list_score += calculate_single_node_complexity(part)
        score = calculate_list_weight(list_score)
    if hasattr(node, 'command'):
        command_attr_score = 0 
        command_attr_score += calculate_single_node_complexity(node.command)
        score += calculate_command_attr_weight(command_attr_score)
    if hasattr(node, 'output'): 
        output_attr_score = 0
        output_attr_score += calculate_single_node_complexity(node.output)
        score += calculate_output_attr_weight(output_attr_score)

    return score


def calculate_raw_file_score(nodes):
    raw_score = 0
    for i in range(0, len(nodes)):
        raw_score += calculate_single_node_complexity(nodes[i])
    return raw_score


def calculate_weighted_file_score(nodes):
    raw_score = calculate_raw_file_score(nodes)    
     
    weighted_score = raw_score / len(nodes)

    return weighted_score




def calcaulte_single_node_complexity_hashing(node, commands = []):
    score = 0
    if type(node) is not bashlex.ast.node: return 0
    if node.kind == 'command': 
        generalized_node = bashtemplate.generalize.basic_generalization(copy.deepcopy(node))
        if generalized_node not in commands:
            score += 1
            commands += [ generalized_node ]
    if node.kind == 'pipeline': score += 1
    if node.kind == 'compound': score += 1
    if node.kind == 'commandsubstitution': score += 1
    if node.kind == 'for':
        for part in node.parts[4:]:
            score += calcaulte_single_node_complexity_hashing(part, commands)
    if node.kind == 'if':
        score += 1
        for part in node.parts[3:]: score += calcaulte_single_node_complexity_hashing(part, commands)
    if node.kind == 'function':
        command_section = bashparse.return_nodes_of_type(node, 'compound')  # function has actual commands in their compound node
        for part in command_section: score += calcaulte_single_node_complexity_hashing(part, commands) - 1
    if hasattr(node, 'parts'):
        for part in node.parts: score += calcaulte_single_node_complexity_hashing(part, commands)
    if hasattr(node, 'list'):
        for part in node.list: score += calcaulte_single_node_complexity_hashing(part, commands)
    if hasattr(node, 'command'): score += calcaulte_single_node_complexity_hashing(node.command, commands)
    if hasattr(node, 'output'): score += calcaulte_single_node_complexity_hashing(node.output, commands)

    return score


def calculate_raw_hashing_score(nodes):
    raw_score = 0
    for node in nodes:
        raw_score += calcaulte_single_node_complexity_hashing(node)
    return raw_score


def calculate_weighted_hasing_score(nodes):
    raw_score = calculate_raw_hashing_score(nodes)    
     
    weighted_score = raw_score / len(nodes)

    return weighted_score


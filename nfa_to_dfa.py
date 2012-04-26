EP = "epsilon"

def all_path(state, nfa):
	"""for any state, return a map for all the input to next state"""
	ret = {}
	for k, value in nfa.items():
		if k[0] == state:
			ret[k[1]] = '-'.join(sorted(value)) if isinstance(value, list) else value
			
	return ret
	
	
def all_states(combined_state, nfa):
	"""computing all the next states of current state by collaps multiple destination states"""
	from collections import OrderedDict
	combine = lambda k1, k2: '-'.join(OrderedDict.fromkeys(k1.split('-') + k2.split('-')).keys())
	
	ret = {}
	
	for state in combined_state.split('-'):
		mapping = { (state, k): v for k, v in all_path(state, nfa).items() }
		for k, v in mapping.items(): #k[0] => state, k[1] => input symbol
			new_key = (combined_state, k[1])
			ret[new_key] = combine(ret[new_key], v) if new_key in ret else v
		
	return {k: '-'.join(sorted(v.split('-'))) for k, v in ret.items()}

def not_visited(states, visited):
	ret = []
	for v in states.values():
		if not v in visited:
			ret.append(v)
	
	return ret

def new_accepted(dfa, accepted):
	return set([k for k, _ in dfa if len(set(accepted) & set(k.split('-'))) > 0])

def closure(state, nfa):
	"""return the closure of a given state as a set"""
	is_epilson_tr = lambda key: key[0] == state and key[1] == EP

	ret = set([state])
	for key in nfa:
		if is_epilson_tr(key):
			next_state = nfa[key]
			if isinstance(next_state, list):
				for s in next_state:
					ret.update(closure(s, nfa))
			else:
				ret.update(closure(next_state, nfa))
	return ret

def non_epsilon_states(state, states, nfa):
	ret = {}
	for s in states:
		for key, value in nfa.items():
			ss, symbol = key[0], key[1]
			if s == ss and symbol != EP:
				new_key = (state, symbol)
				if new_key in ret:
					ret[new_key].append(value)
				else:
					ret[new_key] = value if isinstance(value, list) else [value]

	return ret


def remove_epsilon(nfa, accepted):
	"""remove the epislon transition and update the final states"""
	ret = {}
	accepted_set = set(accepted)
	for key in nfa:
		state, symbol = key[0], key[1]
		if symbol == EP:			
			states = closure(state, nfa)
			if len(states & accepted_set) > 0:
				accepted.append(state)
			ret.update(non_epsilon_states(state, states, nfa))
		else:
			ret[key] = nfa[key]
	return ret
			
def nfa_to_dfa(start, nfa, accepted):
	"""return dfa as a dictionary and accepted final states as a set"""
	nfa = remove_epsilon(nfa, accepted) #remove all the epislon transition
	
	from collections import deque
	queue = deque([start])
	dfa, visited = {}, []

	while len(queue) > 0:
		elem = queue.popleft()
		visited.append(elem)
		next_states = all_states(elem, nfa)
		dfa.update(next_states)
		queue.extend(not_visited(next_states, visited))
	
	return dfa, new_accepted(dfa, accepted)

def test1():
	"""checker board states"""
	nfa = {('1', 'r'): ['2', '4'],
		   ('1', 'b'): '5',
		   ('2', 'r'): ['4', '6'],
		   ('2', 'b'): ['1', '3', '5'],
		   ('3', 'r'): ['2', '6'],
		   ('3', 'b'): '5',
		   ('4', 'r'): ['2', '8'],
		   ('4', 'b'): ['1', '5', '7'],
		   ('5', 'r'): ['2', '4', '6', '8'],
		   ('5', 'b'): ['1', '3', '7', '9'],
		   ('6', 'r'): ['2', '8'],
		   ('6', 'b'): ['3', '5', '9'],
		   ('7', 'r'): ['4', '8'],
		   ('7', 'b'): '5',
		   ('8', 'r'): ['4', '6'],
		   ('8', 'b'): ['5', '7', '9'],
		   ('9', 'r'): ['6', '8'],
		   ('9', 'b'): '5'}

	start = '1'
	accepted = ['9']
			
	dfa, accepted = nfa_to_dfa(start, nfa, accepted)
	print("new dfa is:")
	print(dfa)
	print("final states are:")
	print(accepted)


def test2():
	nfa = {('A', '0') : ['B', 'G'],
		   ('A', 'epsilon'): 'C',
		   ('A', '1') : 'D',
		   ('B', 'epsilon'): 'C', 
		   ('C', '1') : 'B',
		   ('C', '0') : 'F',
		   ('D', '1') : 'A',
		   ('D', 'epsilon') : 'F',
		   ('G', '1') : 'F'}

	start = 'A'
	accepted = ['F']
	
	dfa, accepted = nfa_to_dfa(start, nfa, accepted)
	print("new dfa is:")
	print(dfa)
	print("final states are:")
	print(accepted)
	
test1()
test2()


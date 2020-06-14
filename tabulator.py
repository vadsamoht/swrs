def tabulator(in_array, padding=1):
	# assumes all elements within the top-level array have the same number of elements, and all elements are string or printable as such
	charsizes = []
	for i in in_array[0]:
		charsizes.append(len(str(i)))
	print(charsizes)

	for i in range(len(in_array)):
		#print(in_array[i])
		for j in range(len(in_array[i])):
			#print (i, j)
			if len(str(in_array[i][j])) > charsizes[j]:
				charsizes[j] = len(str(in_array[i][j]))
				
	print(charsizes)


test_array = [('Nick Kerton', 126), ('Doug Clark', 118), ('Jan-Erik Spangberg', 118), ('Abel Martos-Lopez', 117), ('Matt Leto', 117), ('Wes Pipkin', 117), ('BMac_Attack_64', 117), ('VivaGorditas007', 116), ('Nathan Stinson', 115), ('Zefram42', 115), ('Nighthawk711', 115), ('Evan K. N. Jankowski', 115), ('Nairb10', 114), ('Vadsamoht', 112), ('Logan_West', 107)]
tabulator(test_array)
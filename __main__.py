from random import randint
from pandas import read_csv


if __name__ == "__main__":
	# read csv column "Name" into a list
	df = read_csv("sample_list.csv")
	names = df["Name"].tolist()
		
	# make a copy of the family names list to avoid modifying the original list
	givers = [n for n in names]
	recipients = [n for n in names]
	pairs = []

	# randomly pick a recipient for each family member
	for i, giver in enumerate(givers):
		# possible receipients are all family members except the giver
		possible_recipients = [r for r in recipients if r != giver]
		
		# randomly select a recipient from the possible recipients
		recipient_i = randint(0, len(possible_recipients) - 1)
		
		# EDGE CASE
		#   if only 2 recipients left,
		#   if the current giver is the next to last giver and is assigned someone else,
		#   then the giver would be stuck giving to themselves
		#   --> have to flip the next index
		if (len(possible_recipients) == 2 and i == len(givers)-2 and (possible_recipients[recipient_i] != givers[i+1])):
			recipient_i = 1 - recipient_i
		
		# assign the recipient to the giver and remove the recipient from the list of available recipients
		print(f"{giver} --> {possible_recipients[recipient_i]}")
		pairs.append([giver, possible_recipients[recipient_i]])
		recipients.remove(possible_recipients[recipient_i])

	# validate that no one was assigned to themselves
	for p in pairs:
		if (p[0] == p[1]):
			print("Error: A family member was assigned to themselves.")
			raise RuntimeError("A family member was assigned to themselves.")

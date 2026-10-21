from random import randint
from pandas import read_csv, DataFrame
from datetime import datetime


if __name__ == "__main__":
	# read csv column "Name" into a list
	print(f"Reading in data...")
	df = read_csv("gift_exchange_2025.csv")
	last_year_givers = df["Giver"].tolist()
	last_year_recipients = df["Recipient"].tolist()

	# make a copy of the family names list to avoid modifying the original list
	print(f"Copying data to system memory...")
	givers = [n for n in last_year_givers]
	recipients = [n for n in givers]
	pairs = []

	# randomly pick a recipient for each family member
	print(f"Assigning the Giver/Recipient pairs...")
	for i, giver in enumerate(givers):
		# possible receipients are all family members EXCEPT:
		# the giver themselves
		# the last year's recipient
		last_year_recipient = last_year_recipients[i]
		possible_recipients = [r for r in recipients if r != giver and r != last_year_recipient]
		
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
	print(f"Validating the Giver/Recipient pairs...")
	for p in pairs:
		if (p[0] == p[1]):
			print("Error: A family member was assigned to themselves.")
			raise RuntimeError("A family member was assigned to themselves.")
	
	# write the pairs to a new csv file
	output_dataframe_data = {
		"Giver": [p[0] for p in pairs],
		"Recipient": [p[1] for p in pairs]
	}
	output_dataframe = DataFrame(output_dataframe_data)
	output_filename = f"gift_exchange_{datetime.now().year}.csv"
	print(f"Writing to file...")
	output_dataframe.to_csv(output_filename, index=False)
	print(f"Done. Output written to {output_filename}.")
